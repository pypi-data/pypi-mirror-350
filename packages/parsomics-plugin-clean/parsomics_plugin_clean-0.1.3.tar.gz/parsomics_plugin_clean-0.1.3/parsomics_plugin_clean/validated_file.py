from pathlib import Path
from typing import ClassVar

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome


class CleanValidatedFile(ValidatedFileWithGenome):
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        "_maxsep.csv",
        "_pvalue.csv",
    ]

    @property
    def genome_name(self) -> str:
        path_obj = Path(self.path)
        return path_obj.name.replace("_maxsep.csv", "").replace("_pvalue.csv", "")
