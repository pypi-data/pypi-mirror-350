import logging

import polars as pl
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from parsomics_core.entities.files.gff.entry.models import GFFEntry
from parsomics_core.entities.files.gff.file.models import GFFFile
from parsomics_core.entities.omics.fragment.fragment_type import FragmentType
from parsomics_core.entities.workflow.source.models import Source, SourceCreate
from parsomics_core.entities.workflow.source.transactions import SourceTransactions


class GFFParser(BaseModel):
    file: GFFFile
    tool_key: int

    def _extract_range(self) -> tuple[int, int]:
        begin: int = 0
        end: int = 1

        with open(self.file.path, "r") as file:
            for line in file:
                if line.startswith("##FASTA"):
                    break

                elif line.startswith("##"):
                    begin += 1

                end += 1

        return begin, end

    def to_dataframe(self) -> pl.DataFrame:
        schema: dict[str, pl.PolarsDataType] = {
            "contig_name": pl.String,
            "source_name": pl.String,
            "fragment_type": pl.String,
            "coord_start": pl.Int32,
            "coord_stop": pl.Int32,
            "score": pl.Float64,
            "strand": pl.String,
            "phase": pl.String,
            "attributes_raw": pl.String,
        }

        begin, end = self._extract_range()
        skip_rows = begin
        n_rows = end - begin - 1

        df = pl.read_csv(
            self.file.path,
            separator="\t",
            schema=schema,
            infer_schema_length=0,
            skip_rows=skip_rows,
            comment_prefix="#",
            n_rows=n_rows,
            has_header=False,
            null_values=["."],
        )

        df = df.with_columns(pl.col("fragment_type").str.to_uppercase())

        return df

    def _parse_attributes(self, mapping) -> None:
        attributes_raw = mapping["attributes_raw"]
        attributes = attributes_raw.strip().split(";")
        attributes = list(map(lambda s: s.split("="), attributes))
        attributes_dict = {item[0]: item[1] for item in attributes}
        mapping["attributes"] = attributes_dict

    def _add_source_key_to_df(self, engine, df) -> pl.DataFrame:
        with Session(engine) as session:
            # First, add all sources that are already in the database (and,
            # thus, already have a primary key) to the dictionary that relates
            # source name to primary key
            sources_in_db = session.exec(select(Source)).all()
            source_name_to_key = {source.name: source.key for source in sources_in_db}

        # Then, iterate over the sources in the DataFrame and add them
        # to the database if they are not present in the source_name_to_key
        # dictionary. Add them to the dictionary once they have been added
        # to the database and have a primary key
        source_names_in_df = df.select(pl.col("source_name")).unique().to_series()

        # This dict converts clean name to version ("Prodigal" -> "002006")
        source_name_to_version = {
            source.split(":")[0]: (
                source.split(":")[1] if len(source.split(":")) >= 2 else None
            )
            for source in source_names_in_df
        }

        for source_name in source_name_to_version:
            if source_name not in source_name_to_key:
                source_create_model = SourceCreate(
                    name=source_name,
                    tool_key=self.tool_key,
                    version=source_name_to_version[source_name],
                )
                with Session(engine) as session:
                    source_key = (
                        SourceTransactions()
                        .create(
                            session,
                            source_create_model,
                        )
                        .key
                    )
                source_name_to_key[source_name] = source_key

        # Clean source names in DataFrame
        source_raw_name_to_name = {
            source: source.split(":")[0] for source in source_names_in_df
        }
        df = df.with_columns(
            source_name=pl.col("source_name").replace(
                source_raw_name_to_name,
                default=None,
            )
        )

        # Finally, use source_name_to_key to add source_key to the DataFrame
        df = df.with_columns(
            source_key=pl.col("source_name").replace(
                source_name_to_key,
                default=None,
            )
        )

        df = df.drop("source_name")

        return df

    def _add_file_key_to_df(self, df):
        return df.with_columns(pl.lit(self.file.key).alias("file_key"))

    def _add_transcription_info(self, mapping) -> None:
        gene_name: str | None = None
        identifier: str | None = None

        if "attributes" not in mapping:
            raise Exception(f'Mapping {mapping} does not contain "attributes"')
        else:
            attributes = mapping["attributes"]

            if "ID" in attributes:
                identifier = attributes["ID"]

                # NOTE: check for the existence of "Parent" key in attributes,
                #       for compatibility with the GFF of funannotate
                #       (https://github.com/nextgenusfs/funannotate)
                #
                if "Parent" in attributes:
                    gene_name = "".join(identifier.split("-")[:-1])
                else:
                    gene_name = identifier

            if "locus_tag" in attributes:
                gene_name = attributes["locus_tag"]

        mapping["gene_name"] = gene_name
        mapping["identifier"] = identifier

    def parse(self, engine) -> None:
        df = self.to_dataframe()
        df = self._add_source_key_to_df(engine, df)
        df = self._add_file_key_to_df(df)

        mappings = df.to_dicts()

        # NOTE: polars does not support custom types nor dicts, so some
        #       conversions can only be done once the DataFrame has been
        #       converted into a python native dict

        for mapping in mappings:
            # Cast fragment_type to FragmentType
            mapping["fragment_type"] = FragmentType(mapping["fragment_type"])

            # Parse the attributes_raw field
            self._parse_attributes(mapping)
            self._add_transcription_info(mapping)
            mapping.pop("attributes_raw")

        with Session(engine) as session:
            try:
                session.bulk_insert_mappings(GFFEntry, mappings)
                session.commit()
                logging.info(
                    f"Added GFF entries from {self.file.path} to the database."
                )
            except IntegrityError as e:
                logging.warning(
                    f"Failed to add GFF entries from {self.file.path} to the "
                    f"database. Exception caught: {e}"
                )
