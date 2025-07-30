from typing import Sequence

from parsomics_core.globals.database import engine
from parsomics_core.populate import process_files
from timeit_decorator import timeit

from parsomics_plugin_dbcan.processor import DbcanOutputProcessor


@timeit()
def populate_dbcan(
    run_info: dict, assembly_key: int, dereplicated_genomes: Sequence[str]
) -> None:
    def process_dbcan_files(
        output_directory, assembly_key, run_key, tool_key, dereplicated_genomes
    ):
        dbcan_output_processor = DbcanOutputProcessor(
            output_directory=output_directory,
            assembly_key=assembly_key,
            run_key=run_key,
            tool_key=tool_key,
            dereplicated_genomes=dereplicated_genomes,
        )
        dbcan_output_processor.process_dbcan_tsv_files(engine)

    process_files(
        run_info, assembly_key, dereplicated_genomes, "dbcan", process_dbcan_files
    )
