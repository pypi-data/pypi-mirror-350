import logging
from typing import Sequence

from parsomics_core.entities.files.protein_annotation.file.models import (
    ProteinAnnotationFile,
    ProteinAnnotationFileDemand,
)
from parsomics_core.entities.files.protein_annotation.file.transactions import (
    ProteinAnnotationFileTransactions,
)
from parsomics_core.processors._helpers import retrieve_genome_key
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from .file_factory import CleanFileFactory
from .parser import CleanParser
from .validated_file import CleanValidatedFile


class CleanOutputProcessor(BaseModel):
    output_directory: str
    dereplicated_genomes: Sequence[str]
    assembly_key: int
    run_key: int
    tool_key: int

    def process_clean_files(self, engine: Engine):
        clean_file_factory: CleanFileFactory = CleanFileFactory(
            self.output_directory,
            self.dereplicated_genomes,
        )

        clean_files: list[CleanValidatedFile] = clean_file_factory.assemble()
        for f in clean_files:
            genome_key = retrieve_genome_key(engine, f, self.assembly_key)
            run_key = self.run_key

            protein_annotation_file_demand_model = ProteinAnnotationFileDemand(
                path=f.path,
                run_key=run_key,
                genome_key=genome_key,
            )

            with Session(engine) as session:
                protein_annotation_file: ProteinAnnotationFile = (
                    ProteinAnnotationFile.model_validate(
                        ProteinAnnotationFileTransactions().demand(
                            session,
                            protein_annotation_file_demand_model,
                        )
                    )
                )

            clean_parser = CleanParser(
                file=protein_annotation_file,
                assembly_key=self.assembly_key,
                tool_key=self.tool_key,
            )
            clean_parser.parse(engine)

        logging.info(
            f"Finished adding all CLEAN files on {self.output_directory} to the database."
        )
