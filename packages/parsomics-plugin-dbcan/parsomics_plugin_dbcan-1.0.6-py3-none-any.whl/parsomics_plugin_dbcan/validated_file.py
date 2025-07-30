from pathlib import Path
from typing import ClassVar

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome


class DbcanTsvValidatedFile(ValidatedFileWithGenome):
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        ".OUT.overview.txt",
        ".overview.txt",
        "_rundbcanoverview.txt",
    ]

    @property
    def genome_name(self) -> str:
        file_name = Path(self.path).name

        for termination in DbcanTsvValidatedFile._VALID_FILE_TERMINATIONS:
            file_name = file_name.removesuffix(termination)

        genome_name = file_name
        if genome_name is None:
            raise Exception("Failed at extracting genome name from dbcan tsv file")

        return genome_name
