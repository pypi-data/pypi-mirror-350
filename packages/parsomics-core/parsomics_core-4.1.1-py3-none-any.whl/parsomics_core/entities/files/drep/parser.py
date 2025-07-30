import logging
from pathlib import Path

import polars as pl
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from parsomics_core.entities.files.drep.entry.models import DrepEntry
from parsomics_core.entities.files.drep.directory.models import DrepDirectory


class DrepDirectoryParser(BaseModel):
    directory: DrepDirectory

    def to_dataframe(self) -> pl.DataFrame:
        winners_file_path = Path(self.directory.path) / Path("Wdb.csv")
        winners_df = pl.read_csv(winners_file_path)
        winners_df = winners_df.with_columns(pl.lit(True).alias("is_winner"))
        winners_df = winners_df.drop("score")

        clusters_file_path = Path(self.directory.path) / Path("Cdb.csv")
        clusters_df = pl.read_csv(clusters_file_path)
        clusters_df = clusters_df.rename({"secondary_cluster": "genome_cluster_name"})
        clusters_df = clusters_df.drop(
            [
                "threshold",
                "cluster_method",
                "comparison_algorithm",
                "primary_cluster",
            ]
        )

        df = clusters_df.join(winners_df, on="genome", how="outer")

        # Extract genome name from "genome" column
        df = df.with_columns(
            pl.col("genome").map_elements(lambda s: Path(s).stem, return_dtype=pl.Utf8)
        )
        df = df.rename({"genome": "genome_name"})

        df = df.with_columns(df["is_winner"].fill_null(False).alias("is_winner"))
        df = df.drop(
            [
                "genome_right",
            ]
        )

        return df

    def _add_directory_key_to_df(self, df):
        return df.with_columns(pl.lit(self.directory.key).alias("directory_key"))

    def parse(self, engine):
        df = self.to_dataframe()
        df = self._add_directory_key_to_df(df)

        mappings = df.to_dicts()

        with Session(engine) as session:
            try:
                session.bulk_insert_mappings(DrepEntry, mappings)
                session.commit()
                logging.info(
                    f"Added dRep entries from {self.directory.path} to the database."
                )
            except IntegrityError as e:
                logging.warning(
                    f"Failed to add dRep entries from {self.directory.path} "
                    f"to the database. Exception caught: {e}"
                )
