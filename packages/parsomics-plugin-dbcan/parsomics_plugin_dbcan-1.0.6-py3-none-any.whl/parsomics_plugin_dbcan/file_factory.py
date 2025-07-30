from typing import Sequence

from parsomics_core.entities.files.file_factory import FileFactory
from parsomics_plugin_dbcan.validated_file import DbcanTsvValidatedFile


class DbcanTsvFileFactory(FileFactory):
    def __init__(self, path: str, dereplicated_genomes: Sequence[str]):
        return super().__init__(
            validation_class=DbcanTsvValidatedFile,
            path=path,
            dereplicated_genomes=dereplicated_genomes,
        )
