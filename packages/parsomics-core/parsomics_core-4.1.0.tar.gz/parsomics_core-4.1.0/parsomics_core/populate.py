"""
This module does not populate Metadata, Project, and Assembly. These are not
populated one-by-one, as the configuration file is parsed by the Runner, from
the runner module.
"""

import datetime as dt
import logging
import os
from pathlib import Path
from typing import Any, Callable, Sequence

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, or_
from timeit_decorator import timeit

from parsomics_core.entities.files.drep.directory.models import DrepDirectory
from parsomics_core.entities.files.drep.entry.models import DrepEntry, DrepEntryPublic
from parsomics_core.entities.files.fasta.entry.models import FASTAEntry
from parsomics_core.entities.files.fasta.file.models import FASTAFile
from parsomics_core.entities.files.fasta.sequence_type import SequenceType
from parsomics_core.entities.files.gff.entry.models import GFFEntry

# Workflow
from parsomics_core.entities.files.gff.file.models import GFFFile
from parsomics_core.entities.omics.contig.models import Contig
from parsomics_core.entities.omics.fragment.fragment_type import FragmentType
from parsomics_core.entities.omics.fragment.models import Fragment
from parsomics_core.entities.omics.fragment_protein_link.models import (
    FragmentProteinLink,
)
from parsomics_core.entities.omics.gene.models import Gene
from parsomics_core.entities.omics.genome.models import Genome
from parsomics_core.entities.omics.genome_cluster.models import (
    GenomeClusterDemand,
    GenomeClusterPublic,
)
from parsomics_core.entities.omics.genome_cluster.transactions import (
    GenomeClusterTransactions,
)
from parsomics_core.entities.omics.protein.models import Protein
from parsomics_core.entities.omics.repeated_region.models import RepeatedRegion
from parsomics_core.entities.omics.sample.models import SampleDemand, SamplePublic
from parsomics_core.entities.omics.sample.transactions import SampleTransactions

# Files
from parsomics_core.entities.workflow.assembly.models import Assembly
from parsomics_core.entities.workflow.progress import ProgressStatus
from parsomics_core.entities.workflow.run.models import Run, RunDemand
from parsomics_core.entities.workflow.run.transactions import RunTransactions
from parsomics_core.entities.workflow.tool.models import ToolDemand
from parsomics_core.entities.workflow.tool.transactions import ToolTransactions
from parsomics_core.globals.database import engine

# Processors
from parsomics_core.plugin_utils.plugin_initializer import PluginInitializer
from parsomics_core.processors.drep_processor import DrepOutputProcessor
from parsomics_core.processors.gtdbtk_processor import GTDBTkOutputProcessor
from parsomics_core.processors.prokka_processor import ProkkaOutputProcessor

# Globals


def _batch_insert(session, model, mappings):
    try:
        session.bulk_insert_mappings(model, mappings)
        session.commit()
    except IntegrityError as e:
        logging.warning(
            f"Ignored duplicated and/or invalid entry for {model}. Exception caught: {e}"
        )
        session.rollback()


@timeit()
def populate_clusters_samples_and_genomes(session, assembly_key):
    statement = (
        select(DrepEntry)
        .join(DrepDirectory)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
    )
    drep_entries = session.exec(statement).all()

    mappings = []
    for drep_entry in drep_entries:
        drep_entry_public = DrepEntryPublic.model_validate(drep_entry)

        genome_name = drep_entry_public.genome_name
        sample_name = genome_name.split(".bin")[0]
        genome_cluster_name = drep_entry_public.genome_cluster_name
        drep_directory_key = drep_entry_public.directory_key
        drep_entry_key = drep_entry_public.key

        # demand sample
        sample_demand_model: SampleDemand = SampleDemand(
            name=sample_name,
            drep_directory_key=drep_directory_key,
        )
        sample: SamplePublic = SampleTransactions().demand(
            session,
            sample_demand_model,
        )
        sample_key: int = sample.key

        # demand genome cluster
        genome_cluster_create_model: GenomeClusterDemand = GenomeClusterDemand(
            name=genome_cluster_name,
            drep_directory_key=drep_directory_key,
        )
        genome_cluster: GenomeClusterPublic = GenomeClusterTransactions().demand(
            session,
            genome_cluster_create_model,
        )
        genome_cluster_key = genome_cluster.key

        mappings.append(
            {
                "drep_entry_key": drep_entry_key,
                "genome_cluster_key": genome_cluster_key,
                "sample_key": sample_key,
            }
        )
    _batch_insert(session, Genome, mappings)


@timeit()
def populate_contigs(session, assembly_key):
    statement = (
        select(FASTAEntry)
        .join(FASTAFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(FASTAFile.sequence_type == SequenceType.CONTIG)
    )
    fasta_contig_entries = session.exec(statement).all()

    mappings = []
    for fasta_contig_entry in fasta_contig_entries:
        mappings.append(
            {
                "fasta_entry_key": fasta_contig_entry.key,
                "genome_key": fasta_contig_entry.file.genome.key,
            }
        )
    _batch_insert(session, Contig, mappings)


@timeit()
def populate_genes(session, assembly_key):
    statement = (
        select(GFFEntry)
        .join(GFFFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(GFFEntry.fragment_type == FragmentType.GENE)
    )
    gff_gene_entries = session.exec(statement).all()

    # NOTE: some tools output no fragments typed as FragmentType.GENE. Instead,
    #       they use all other fragment types for all gene-like fragments. For
    #       that reason, in case a search for FragmentType.GENE yields nothing,
    #       search for all other fragment types.
    if not gff_gene_entries:
        statement = (
            select(GFFEntry)
            .join(GFFFile)
            .join(Run)
            .join(Assembly)
            .where(Assembly.key == assembly_key)
            .where(
                or_(
                    GFFEntry.fragment_type == FragmentType.CDS,
                    GFFEntry.fragment_type == FragmentType.TRNA,
                    GFFEntry.fragment_type == FragmentType.RRNA,
                    GFFEntry.fragment_type == FragmentType.TMRNA,
                    GFFEntry.fragment_type == FragmentType.MISC_RNA,
                )
            )
        )
        gff_gene_entries = session.exec(statement).all()

    gene_name_to_contig_key: dict[str, int] = {}
    contig_name_to_contig_key: dict[str, int] = {}
    for gff_gene_entry in gff_gene_entries:
        contig_name = gff_gene_entry.contig_name
        gene_name = gff_gene_entry.gene_name

        if contig_name not in contig_name_to_contig_key:
            statement = (
                select(Contig)
                .join(FASTAEntry)
                .join(FASTAFile)
                .join(Run)
                .join(Assembly)
                .where(Assembly.key == assembly_key)
                .where(
                    FASTAEntry.sequence_name == contig_name,
                )
            )
            contigs = session.exec(statement).all()

            if len(contigs) > 1:
                logging.warning(
                    f"Expected only one Contig to match name {contig_name}, "
                    f"but matched: {contigs}"
                )
            if not contigs:
                logging.warning(f"No Contigs were matched to name {contig_name}")
            else:
                contig_name_to_contig_key[contig_name] = contigs[0].key

        if contig_name in contig_name_to_contig_key:
            gene_name_to_contig_key[gene_name] = contig_name_to_contig_key[contig_name]

    statement = (
        select(FASTAEntry)
        .join(FASTAFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(FASTAFile.sequence_type == SequenceType.GENE)
    )
    fasta_gene_entries = session.exec(statement).all()

    mappings = []
    for fasta_gene_entry in fasta_gene_entries:
        gene_name = fasta_gene_entry.sequence_name
        contig_key = gene_name_to_contig_key[gene_name]

        mappings.append(
            {
                "fasta_entry_key": fasta_gene_entry.key,
                "contig_key": contig_key,
            }
        )
    _batch_insert(session, Gene, mappings)


@timeit()
def populate_repeated_region(session, assembly_key):
    statement = (
        select(GFFEntry)
        .join(GFFFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(GFFEntry.fragment_type == FragmentType.REPEAT_REGION)
    )
    gff_entries = session.exec(statement).all()

    mappings = []
    contig_name_to_contig_key: dict[str, int] = {}
    for gff_entry in gff_entries:
        contig_name = gff_entry.contig_name

        if contig_name not in contig_name_to_contig_key:
            statement = (
                select(Contig)
                .join(FASTAEntry)
                .join(FASTAFile)
                .join(Run)
                .join(Assembly)
                .where(Assembly.key == assembly_key)
                .where(
                    FASTAEntry.sequence_name == contig_name,
                )
            )
            contigs = session.exec(statement).all()

            if len(contigs) > 1:
                logging.warning(
                    f"Expected only one Contig to match name {contig_name}, "
                    f"of the GFFEntry {gff_entry}, but matched: {contigs}"
                )

            if not contigs:
                logging.warning(
                    f"No Genes were matched to name {contig_name}, of the "
                    f"GFFEntry {gff_entry}"
                )
            else:
                contig_key = contigs[0].key
                contig_name_to_contig_key[contig_name] = contig_key

        if contig_name in contig_name_to_contig_key:
            contig_key = contig_name_to_contig_key[contig_name]
            mappings.append(
                {
                    "gff_entry_key": gff_entry.key,
                    "contig_key": contig_key,
                }
            )
    _batch_insert(session, RepeatedRegion, mappings)


@timeit()
def populate_fragments(session, assembly_key):
    statement = (
        select(GFFEntry)
        .join(GFFFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(GFFEntry.fragment_type != FragmentType.REPEAT_REGION)
    )
    gff_entries = session.exec(statement).all()

    mappings = []
    gene_name_to_gene_key: dict[str, int] = {}
    for gff_entry in gff_entries:
        gene_name = gff_entry.gene_name

        if gene_name not in gene_name_to_gene_key:
            statement = (
                select(Gene)
                .join(FASTAEntry)
                .join(FASTAFile)
                .join(Run)
                .join(Assembly)
                .where(Assembly.key == assembly_key)
                .where(
                    FASTAEntry.sequence_name == gene_name,
                )
            )
            genes = session.exec(statement).all()

            if len(genes) > 1:
                logging.warning(
                    f"Expected only one Gene to match name {gene_name}, "
                    f"of the GFFEntry {gff_entry}, but matched: {genes}"
                )

            if not genes:
                logging.warning(
                    f"No Genes were matched to name {gene_name}, of the "
                    f"GFFEntry {gff_entry}"
                )
            else:
                gene_key = genes[0].key
                gene_name_to_gene_key[gene_name] = gene_key

        if gene_name in gene_name_to_gene_key:
            gene_key = gene_name_to_gene_key[gene_name]
            mappings.append(
                {
                    "gff_entry_key": gff_entry.key,
                    "gene_key": gene_key,
                }
            )
    _batch_insert(session, Fragment, mappings)


@timeit()
def populate_proteins(session, assembly_key):
    statement = (
        select(FASTAEntry)
        .join(FASTAFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(FASTAFile.sequence_type == SequenceType.PROTEIN)
    )
    fasta_protein_entries = session.exec(statement).all()
    mappings = [
        {"fasta_entry_key": fasta_protein_entry.key}
        for fasta_protein_entry in fasta_protein_entries
    ]
    _batch_insert(session, Protein, mappings)


@timeit()
def populate_fragment_protein_links(session, assembly_key):
    statement = (
        select(Fragment)
        .join(GFFEntry)
        .join(GFFFile)
        .join(Run)
        .join(Assembly)
        .where(Assembly.key == assembly_key)
        .where(GFFEntry.fragment_type == FragmentType.CDS)
    )
    cdss = session.exec(statement).all()

    mappings = []
    gene_name_to_protein_key: dict[str, int] = {}
    for cds in cdss:
        gene_name = cds.gff_entry.gene_name

        if gene_name not in gene_name_to_protein_key:
            statement = (
                select(Protein)
                .join(FASTAEntry)
                .join(FASTAFile)
                .join(Run)
                .join(Assembly)
                .where(Assembly.key == assembly_key)
                #
                # NOTE: in prokaryotes, there's a 1:1 relationship between genes
                #       and proteins. For that reason, prokka names each protein
                #       with the same name as the gene that encodes them.
                #
                .where(FASTAEntry.sequence_name == gene_name)
            )
            proteins = session.exec(statement).all()

            if len(proteins) > 1:
                logging.warning(
                    f"Expected only one Protein to match name {gene_name}, "
                    f"but matched: {proteins}"
                )

            if not proteins:
                logging.warning(f"No Proteins were matched to name {gene_name} ")
            else:
                protein_key = proteins[0].key
                gene_name_to_protein_key[gene_name] = protein_key

        if gene_name in gene_name_to_protein_key:
            protein_key = gene_name_to_protein_key[gene_name]
            mappings.append(
                {
                    "fragment_key": cds.key,
                    "protein_key": protein_key,
                }
            )

    _batch_insert(session, FragmentProteinLink, mappings)


def _get_tool_key(tool_name) -> int:
    tool_demand_model = ToolDemand(name=tool_name)
    with Session(engine) as session:
        tool_key = ToolTransactions().demand(session, tool_demand_model).key
    return tool_key


def _get_run_key(run_info: dict, assembly_key: int, tool_key: int) -> int:
    # Parse the variables in the run configuration
    output_directory = run_info["output_directory"]

    version: str | None = None
    if "version" in run_info:
        version = run_info["version"]

    date: dt.date | None = None
    if "date" in run_info:
        date = dt.datetime.strptime(run_info["date"], "%d/%m/%Y").date()

    # Create the Run
    run_demand_model = RunDemand(
        output_directory=output_directory,
        version=version,
        date=date,
        tool_key=tool_key,
        assembly_key=assembly_key,
    )
    with Session(engine) as session:
        run = RunTransactions().demand(session, run_demand_model)
        run.status = ProgressStatus.IN_PROGRESS
        session.commit()
        run_key = run.key

    return run_key


def process_files(
    run_info: dict,
    assembly_key: int,
    dereplicated_genomes: Sequence[str],
    tool_name: str,
    process_files_func: Callable[[str, int, int, int, Sequence[str]], None],
) -> None:
    # Tool
    tool_key = _get_tool_key(tool_name)

    # Run
    if "output_directory" not in run_info:
        raise Exception(
            f'Mandatory "output_directory" field not in {tool_name} '
            f"configuration: {run_info}"
        )
    run_key = _get_run_key(run_info, assembly_key, tool_key)

    # Files and Entries
    output_directory = run_info["output_directory"]
    process_files_func(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    )

    # Update progress status for Run
    with Session(engine) as session:
        run = session.get(Run, run_key)
        if not run:
            raise Exception(f"Unexpectedly unable to get Run with key {run_key}")
        run.status = ProgressStatus.DONE
        session.commit()


def _find_drep_results_directory(drep_output_directory: str) -> str | None:
    for dirpath, _, filenames in os.walk(drep_output_directory):
        if {"Wdb.csv", "Cdb.csv"}.issubset(filenames):
            return dirpath
    return None


def _get_dereplicated_genomes(drep_run_info) -> Sequence[str]:
    output_directory = drep_run_info["output_directory"]
    results_directory = _find_drep_results_directory(output_directory)

    if not results_directory:
        raise Exception(
            f"""Invalid dRep directory. Wdb.csv and Cdb.csv files not found
            in {output_directory} nor any of its subdirectories"""
        )

    dereplicated_genomes: Sequence[str]
    with Session(engine) as session:
        statement = (
            select(DrepEntry.genome_name)
            .join(DrepDirectory)
            .where(DrepDirectory.path == results_directory)
        )
        results = session.exec(statement)
        dereplicated_genomes = results.all()

    if not dereplicated_genomes:
        raise Exception(f"No dereplicated genomes were found in {output_directory}")

    return dereplicated_genomes


@timeit()
def populate_drep(run_info: dict, assembly_key: int) -> None:
    def process_drep_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):
        results_directory = _find_drep_results_directory(output_directory)

        if not results_directory:
            raise Exception(
                f"""Invalid dRep directory. Wdb.csv and Cdb.csv files not found
                in {output_directory} nor any of its subdirectories"""
            )

        drep_output_processor = DrepOutputProcessor(
            output_directory=results_directory,
            run_key=run_key,
        )
        drep_output_processor.process_drep_directory(engine)

    process_files(run_info, assembly_key, [], "drep", process_drep_files)


@timeit()
def populate_gtdbtk(
    run_info: dict, assembly_key: int, dereplicated_genomes: Sequence[str]
) -> None:
    def process_gtdbtk_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):
        gtdbtk_output_processor = GTDBTkOutputProcessor(
            output_directory=output_directory,
            assembly_key=assembly_key,
            run_key=run_key,
            tool_key=tool_key,
            dereplicated_genomes=dereplicated_genomes,
        )
        gtdbtk_output_processor.process_gtdbtk_files(engine)

    process_files(
        run_info, assembly_key, dereplicated_genomes, "gtdbtk", process_gtdbtk_files
    )


@timeit()
def populate_prokka(
    run_info: dict, assembly_key: int, dereplicated_genomes: Sequence[str]
) -> None:
    def process_prokka_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):
        prokka_output_processor = ProkkaOutputProcessor(
            output_directory=output_directory,
            assembly_key=assembly_key,
            run_key=run_key,
            tool_key=tool_key,
            dereplicated_genomes=dereplicated_genomes,
        )
        prokka_output_processor.process_fasta_files(engine)
        prokka_output_processor.process_gff_files(engine)

    process_files(
        run_info, assembly_key, dereplicated_genomes, "prokka", process_prokka_files
    )


@timeit()
def populate_plugins(
    assembly_key: int,
    assembly_config: dict[str, Any],
    dereplicated_genomes: Sequence[str],
    plugin_initializers: list[PluginInitializer],
):
    for plugin_initializer in plugin_initializers:
        if plugin_initializer.subject in assembly_config:
            plugin_run_info = assembly_config[plugin_initializer.subject]
            populate_plugin = plugin_initializer.populate_func
            populate_plugin(plugin_run_info, assembly_key, dereplicated_genomes)


@timeit()
def populate_all(assembly_config, assembly_name, assembly_key, plugin_initializers):
    # Populate dRep
    if "drep" not in assembly_config:
        raise Exception(f"No dRep runs found in config for assembly {assembly_name}")

    drep_run_info = assembly_config["drep"]
    populate_drep(drep_run_info, assembly_key)
    dereplicated_genomes = _get_dereplicated_genomes(drep_run_info)

    # Populate Genomes, Samples, and Genome Clusters. This must be done at this
    # stage, so Genomes can be referenced in the foreign key of the next files
    # (FASTA, GFF, etc)
    with Session(engine) as session:
        populate_clusters_samples_and_genomes(session, assembly_key)

    # Populate GTDB-Tk
    if "gtdbtk" in assembly_config:
        gtdbtk_run_info = assembly_config["gtdbtk"]
        populate_gtdbtk(gtdbtk_run_info, assembly_key, dereplicated_genomes)

    # Populate prokka
    if "prokka" in assembly_config:
        prokka_run_info = assembly_config["prokka"]
        populate_prokka(prokka_run_info, assembly_key, dereplicated_genomes)

    # Populate remaining built-in tables
    with Session(engine) as session:
        populate_contigs(session, assembly_key)
        populate_genes(session, assembly_key)
        populate_repeated_region(session, assembly_key)
        populate_fragments(session, assembly_key)
        populate_proteins(session, assembly_key)
        populate_fragment_protein_links(session, assembly_key)

    # Populate plugins
    populate_plugins(
        assembly_key, assembly_config, dereplicated_genomes, plugin_initializers
    )
