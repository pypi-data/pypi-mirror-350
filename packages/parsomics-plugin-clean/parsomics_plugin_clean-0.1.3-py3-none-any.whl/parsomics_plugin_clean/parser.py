import csv
import logging

import polars as pl
from parsomics_core.entities import ProteinAnnotationEntry, ProteinAnnotationFile
from parsomics_core.entities.workflow.source import (
    Source,
    SourceCreate,
    SourceTransactions,
)
from parsomics_core.plugin_utils import search_protein_by_name
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

ANNOTATION_TYPE = "EC_NUMBER"


class CleanParser(BaseModel):
    file: ProteinAnnotationFile
    assembly_key: int
    tool_key: int

    def to_dataframe(self) -> pl.DataFrame:
        rows = []
        with open(self.file.path, mode="r") as infile:
            reader = csv.reader(infile)
            for row in reader:
                id_val = row[0]
                for data in row[1:]:
                    rows.append([id_val, data])

        with open(self.file.path, mode="w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)

        df = pl.read_csv(
            self.file.path,
            has_header=False,
            infer_schema=False,
        )

        df = df.with_columns(
            df[:, 0]
            .str.strip_chars('"')
            .str.split(" ")
            .list.first()
            .alias(df.columns[0])
        )

        df = df.with_columns(df[:, 1].str.strip_chars("EC:"))

        rows = []

        for row in df.iter_rows():
            id_val, data = row
            entries = data.split(",")
            for entry in entries:
                ec_number, score = entry.split("/")
                rows.append(
                    (
                        id_val,
                        ec_number,
                        score,
                        ANNOTATION_TYPE,
                    )
                )

        schema: dict[str, pl.PolarsDataType] = {
            "protein_name": pl.String,
            "accession": pl.String,
            "score": pl.Float64,
            "annotation_type": pl.String,
        }

        df = pl.DataFrame(rows, schema=schema, orient="row")

        return df

    def _add_file_key_to_df(self, df):
        return df.with_columns(pl.lit(self.file.key).alias("file_key"))

    def _add_protein_key_to_mappings(self, mappings):
        protein_name_to_key = {}
        for mapping in mappings:
            protein_name = mapping["protein_name"]
            if protein_name not in protein_name_to_key:
                protein_key = search_protein_by_name(protein_name, self.assembly_key)
                protein_name_to_key[protein_name] = protein_key

            protein_key = protein_name_to_key[protein_name]
            mapping["protein_key"] = protein_key
            mapping.pop("protein_name")

    def _add_empty_details(self, mappings):
        # NOTE: Although the details field in ProteinAnnotation has a default
        # value of {} as per "Field(default={}, sa_column=Column(JSONB))", this
        # default value is not inserted when using bulk_insert_mappings, since
        # bulk_insert_mappings skips object construction
        #
        for mapping in mappings:
            mapping["details"] = {}

    def parse(self, engine) -> None:
        df = self.to_dataframe()
        df = self._add_file_key_to_df(df)

        mappings = df.to_dicts()
        self._add_protein_key_to_mappings(mappings)
        self._add_empty_details(mappings)

        for mapping in mappings:
            mapping["annotation_type"] = ANNOTATION_TYPE

        with Session(engine) as session:
            try:
                session.bulk_insert_mappings(ProteinAnnotationEntry, mappings)
                session.commit()
                logging.info(
                    f"Added CLEAN entries from {self.file.path} to the database."
                )
            except IntegrityError as e:
                logging.warning(
                    f"Failed to add CLEAN entries from {self.file.path} to "
                    f"the database. Exception caught: {e}"
                )
