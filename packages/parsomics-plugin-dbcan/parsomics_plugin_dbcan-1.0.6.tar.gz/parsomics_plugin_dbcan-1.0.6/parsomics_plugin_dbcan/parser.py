import re
import logging

import polars as pl
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from parsomics_plugin_dbcan.annotation_type import DbcanAnnotationType
from parsomics_core.entities.files.protein_annotation.entry.models import (
    ProteinAnnotationEntry,
)
from parsomics_core.entities.files.protein_annotation.file.models import (
    ProteinAnnotationFile,
)
from parsomics_core.plugin_utils import search_protein_by_name
from parsomics_core.entities.workflow.source.models import Source, SourceCreate
from parsomics_core.entities.workflow.source.transactions import SourceTransactions


class DbcanTsvParser(BaseModel):
    file: ProteinAnnotationFile
    assembly_key: int
    tool_key: int

    def to_dataframe(self) -> pl.DataFrame:
        df = pl.read_csv(
            self.file.path,
            separator="\t",
            null_values=["-"],
        )

        if "Signalp" in df.columns:
            df = df.drop("Signalp")
        if "#ofTools" in df.columns:
            df = df.drop("#ofTools")

        df = df.rename({"Gene ID": "protein_name"})

        df = df.melt(
            id_vars="protein_name",
            variable_name="source_name",
            value_name="description",
        )

        # Remove rows that have an empty description (represented with "-")
        df = df.filter(pl.col("description").is_not_null())

        df = df.with_columns(
            annotation_type=pl.when(source_name="EC#")
            .then(pl.lit("EC_NUMBER"))
            .otherwise(pl.lit("DOMAIN"))
        )

        # NOTE: The EC# (Enzyme Comission number) column may be predicted by
        #       eCAMI or dbCAN_sub depending on the version of run_dbCAN.

        ecnum_source_name = "eCAMI" if "eCAMI" in df.columns else "dbCAN_sub"
        df = df.with_columns(
            pl.col("source_name").str.replace("EC#", ecnum_source_name)
        )

        return df

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
        for source_name in source_names_in_df:
            if source_name not in source_name_to_key:
                source_create_model = SourceCreate(
                    name=source_name,
                    tool_key=self.tool_key,
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

        # Finally, use source_name_to_key to add source_key to the DataFrame
        df = df.with_columns(
            source_key=pl.col("source_name").replace(
                source_name_to_key,
                default=None,
            )
        )

        # Drop source_name since we can get the Source object with source_key
        df = df.drop("source_name")

        return df

    def _add_file_key_to_df(self, df):
        return df.with_columns(pl.lit(self.file.key).alias("file_key"))

    def _add_coords_to_mappings(self, mappings):
        for mapping in mappings:
            description = mapping["description"]
            match = re.search(r"(\w+)\((\d+)-(\d+)\)", description)
            if match:
                mapping["description"] = match.group(1)
                mapping["coord_start"] = int(match.group(2))
                mapping["coord_stop"] = int(match.group(3))

    def _add_annotation_type_to_mappings(self, mappings):
        for mapping in mappings:
            mapping["annotation_type"] = DbcanAnnotationType(mapping["annotation_type"])

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

    def parse(self, engine):
        df = self.to_dataframe()
        df = self._add_source_key_to_df(engine, df)
        df = self._add_file_key_to_df(df)

        mappings = df.to_dicts()
        self._add_coords_to_mappings(mappings)
        self._add_annotation_type_to_mappings(mappings)
        self._add_protein_key_to_mappings(mappings)
        self._add_empty_details(mappings)

        for mapping in mappings:
            mapping["annotation_type"] = DbcanAnnotationType(mapping["annotation_type"])

        with Session(engine) as session:
            try:
                session.bulk_insert_mappings(ProteinAnnotationEntry, mappings)
                session.commit()
                logging.info(
                    f"Added dbCAN entries from {self.file.path} to the database."
                )
            except IntegrityError as e:
                logging.warning(
                    f"Failed to add dbCAN entries from {self.file.path} to "
                    f"the database. Exception caught: {e}"
                )
