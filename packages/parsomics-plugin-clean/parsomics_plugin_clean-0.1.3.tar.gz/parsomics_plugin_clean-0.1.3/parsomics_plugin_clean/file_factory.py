from typing import Sequence

from parsomics_core.factories import FileFactory

from .validated_file import CleanValidatedFile


class CleanFileFactory(FileFactory):
    def __init__(self, path: str, dereplicated_genomes: Sequence[str]):
        return super().__init__(
            validation_class=CleanValidatedFile,
            path=path,
            dereplicated_genomes=dereplicated_genomes,
        )
