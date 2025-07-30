import logging
from enum import Enum

import polars as pl
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from parsomics_core.entities.files.drep.directory.models import DrepDirectory
from parsomics_core.entities.files.drep.entry.models import DrepEntry
from parsomics_core.entities.files.gtdbtk.entry.models import GTDBTkEntry
from parsomics_core.entities.files.gtdbtk.file.models import GTDBTkFile
from parsomics_core.entities.omics.genome.models import Genome, GenomePublic
from parsomics_core.entities.workflow.assembly.models import Assembly
from parsomics_core.entities.workflow.run.models import Run


class GTDBTkClassificationMethod(str, Enum):
    ANI = "ANI"
    TOPOLOGY = "TOPOLOGY"
    TOPOLOGY_ANI = "TOPOLOGY_ANI"
    TOPOLOGY_RED = "TOPOLOGY_RED"
    ANISCREEN = "ANISCREEN"


class GTDBTkParser(BaseModel):
    file: GTDBTkFile
    assembly_key: int
    tool_key: int

    def to_dataframe(self) -> pl.DataFrame:
        schema: dict[str, pl.PolarsDataType] = {
            "genome_name": pl.String,
            "classification_raw": pl.String,
            #
            # NOTE: columns preceeded by "fastani_" have been renamed in GTDB-Tk
            #       to be preeced by "closest_genome_" instead, since commit bacae42
            #
            "closest_genome_reference": pl.String,
            "closest_genome_reference_radius": pl.Float64,
            "closest_genome_taxonomy": pl.String,
            "closest_genome_ani": pl.Float64,
            "closest_genome_af": pl.Float64,
            "closest_placement_reference": pl.String,
            "closest_placement_radius": pl.Float64,
            "closest_placement_taxonomy": pl.String,
            "closest_placement_ani": pl.Float64,
            "closest_placement_af": pl.Float64,
            "pplacer_taxonomy": pl.String,
            "classification_method": pl.String,
            "note": pl.String,
            "other_related_references": pl.String,
            "msa_percent": pl.Float64,
            "translation_table": pl.Int32,
            "red_value": pl.Float64,
            "warnings": pl.String,
        }

        df = pl.read_csv(
            self.file.path,
            separator="\t",
            schema=schema,
            null_values=["N/A"],
        )

        df = df.with_columns(
            classification_raw_split=pl.col("classification_raw")
            .str.replace_all(r"[dpcofgs]__", "")
            .str.split(";")
        )

        # fmt: off
        df = df.with_columns(
            domain=pl.col("classification_raw_split").list.get(0),
            phylum=pl.col("classification_raw_split").list.get(1),
            klass=pl.col("classification_raw_split").list.get(2),
            order=pl.col("classification_raw_split").list.get(3),
            family=pl.col("classification_raw_split").list.get(4),
            genus=pl.col("classification_raw_split").list.get(5),
            species=pl.col("classification_raw_split").list.get(6),
        )
        # fmt: on

        df = df.drop("classification_raw_split")
        df = df.drop("classification_raw")

        classification_method_cleaner = {
            "ANI": GTDBTkClassificationMethod.ANI,
            "ANI/Placement": GTDBTkClassificationMethod.TOPOLOGY_ANI,
            "taxonomic classification fully defined by topology": GTDBTkClassificationMethod.TOPOLOGY,
            "taxonomic novelty determined using RED": GTDBTkClassificationMethod.TOPOLOGY_RED,
            "ani_screen": GTDBTkClassificationMethod.ANISCREEN,
            "taxonomic classification defined by topology and ANI": GTDBTkClassificationMethod.TOPOLOGY_ANI,
        }

        df = df.with_columns(
            classification_method=pl.col("classification_method").replace(
                classification_method_cleaner,
                default=None,
            )
        )

        df = df.with_columns(
            taxonomic_novelty=pl.col("classification_method").eq(
                GTDBTkClassificationMethod.TOPOLOGY_RED
            )
        )

        df = self._keep_relevant_column(
            df,
            "closest_genome_ani",
            "closest_placement_ani",
            property_name="ani",
        )
        df = self._keep_relevant_column(
            df,
            "closest_genome_af",
            "closest_placement_af",
            property_name="af",
        )
        df = self._keep_relevant_column(
            df,
            "closest_genome_reference",
            "closest_placement_reference",
            property_name="reference",
        )
        df = self._keep_relevant_column(
            df,
            "closest_genome_reference_radius",
            "closest_placement_radius",
            property_name="radius",
        )

        # Drop redundant and unimportant columns
        df = df.drop(
            [
                "pplacer_taxonomy",
                "closest_genome_taxonomy",
                "closest_placement_taxonomy",
                "other_related_references",
                "msa_percent",
                "translation_table",
            ]
        )

        # Remove file extension suffixes from genome names
        df = df.with_columns(
            pl.col("genome_name")
            .str.replace(r"\.fa$", "", literal=False)
            .str.replace(r"\.fna$", "", literal=False)
            .alias("genome_name")
        )

        return df

    def _genome_name_to_genome_key(self, genome_name, engine):
        assembly_key = self.assembly_key

        with Session(engine) as session:
            statement = (
                select(Genome)
                .join(DrepEntry)
                .join(DrepDirectory)
                .join(Run)
                .join(Assembly)
                .where(DrepEntry.genome_name == genome_name)
                .where(Assembly.key == assembly_key)
            )
            results = session.exec(statement)
            genomes = results.all()

            if len(genomes) > 1:
                logging.warning(
                    f"Expected only one Genome in the same Assembly (key "
                    f"= {assembly_key}) to match name {genome_name}, but "
                    f"matched: {genomes}"
                )

            if not genomes:
                raise Exception(
                    f"No Genomes were matched to name {genome_name}, in "
                    f"the same Assembly (key {assembly_key})"
                )

            genome_key: int = GenomePublic.model_validate(genomes[0]).key
            return genome_key

    def _keep_relevant_column(
        self,
        df,
        closest_genome_column_name,
        closest_placement_column_name,
        property_name,
    ):
        df = df.with_columns(
            pl.when(
                pl.col("classification_method") == GTDBTkClassificationMethod.ANISCREEN
            )
            .then(pl.col(closest_genome_column_name))
            .otherwise(closest_placement_column_name)
            .alias(property_name)
        )
        df = df.drop([closest_genome_column_name, closest_placement_column_name])
        return df

    def _add_file_key_to_df(self, df):
        return df.with_columns(pl.lit(self.file.key).alias("file_key"))

    def _add_genome_key_to_df(self, df, engine):
        # Add reference to Genome
        df = df.with_columns(
            [
                (
                    pl.col("genome_name")
                    .map_elements(
                        lambda x: self._genome_name_to_genome_key(x, engine),
                        return_dtype=pl.Int32,
                    )
                    .alias("genome_key")
                )
            ]
        )
        df = df.drop("genome_name")
        return df

    def parse(self, engine) -> None:
        df = self.to_dataframe()
        df = self._add_file_key_to_df(df)
        df = self._add_genome_key_to_df(df, engine)

        mappings = df.to_dicts()

        with Session(engine) as session:
            try:
                session.bulk_insert_mappings(GTDBTkEntry, mappings)
                session.commit()
                logging.info(
                    f"Added GTDB-Tk entries from {self.file.path} to the database."
                )
            except IntegrityError as e:
                logging.warning(
                    f"Failed to add GTDB-Tk entries from {self.file.path} to "
                    f"the database. Exception caught: {e}"
                )
