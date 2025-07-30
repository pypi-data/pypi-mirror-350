"""Cache manager for schema and data points."""

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, List, Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from bitfount import config

Base = declarative_base()

_SCHEMA_DATASETS_CACHE_TABLE: str = "datasets"
_MAIN_SCHEMA_CACHE_TABLE: str = "main_schema_cache"
_CACHED_FILE_PATHS = "file_paths"
# As the logs from cache interaction may be large, a specific flag is provided to
# control whether debug logging is enabled within this module specifically.
#
# Note that setting this flag will also cause the SQL to be output in the logs.
_logger = logging.getLogger(__name__)
if not config.settings.logging.data_cache_debug:
    _logger.setLevel(logging.INFO)


# Define ORM models
class DatasetsTable(Base):
    """ORM for storing dataset names."""

    __tablename__: str = _SCHEMA_DATASETS_CACHE_TABLE

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_name: Mapped[str] = mapped_column(String, unique=True)

    def __init__(self, dataset_name: str) -> None:
        self.dataset_name = dataset_name


class MainSchemaCacheTable(Base):
    """ORM for linking datasets to their partial schemas."""

    __tablename__: str = _MAIN_SCHEMA_CACHE_TABLE

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("datasets.id", ondelete="CASCADE")
    )
    partial_schema: Mapped[str] = mapped_column(Text)
    cache_updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    def __init__(self, dataset_id: int, partial_schema: str) -> None:
        self.dataset_id = dataset_id
        self.partial_schema = partial_schema


class FilePathsTable(Base):
    """ORM for storing file paths associated with datasets."""

    __tablename__: str = _CACHED_FILE_PATHS

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("datasets.id", ondelete="CASCADE")
    )
    file_path: Mapped[str] = mapped_column(Text, unique=True)

    def __init__(self, dataset_id: int, file_path: str) -> None:
        self.dataset_id = dataset_id
        self.file_path = file_path


def _set_sqlite_foreign_key_pragma(dbapi_connection: Any, _: Any) -> None:
    """Ensure foreign keys are enabled on SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class SQLiteSchemaCacheManager:
    """A schema caching implementation that uses an SQLite database."""

    def __init__(self, sqlite_path: Path) -> None:
        self._sqlite_path = sqlite_path
        self._engine = create_engine(
            f"sqlite:///{sqlite_path}", echo=False, future=True
        )
        listen(self._engine, "connect", _set_sqlite_foreign_key_pragma)
        self._Session = sessionmaker(bind=self._engine)
        Base.metadata.create_all(self._engine)

    def add_dataset(self, dataset_name: str) -> int:
        """Add a dataset to the Datasets table if it doesn't already exist."""
        with self._Session() as session:
            dataset = (
                session.query(DatasetsTable)
                .filter(DatasetsTable.dataset_name == dataset_name)
                .first()
            )
            if not dataset:
                dataset = DatasetsTable(dataset_name=dataset_name)
                session.add(dataset)
                session.commit()
                session.refresh(dataset)
            return dataset.id

    def cache_file_paths_with_partial_schema(
        self,
        dataset_name: str,
        file_paths: List[str],
        partial_schema: dict[str, Any],
    ) -> None:
        """Cache file paths and the latest partial schema for a specific dataset.

        - Adds file paths to the file paths table.
        - Updates the 'number_of_records' field in the partial_schema
            based on new files added.
        - Saves the updated schema to the cache.

        Args:
            dataset_name: The name of the dataset.
            file_paths: A list of file paths to cache.
            partial_schema: The partial schema dictionary to update and cache.
        """
        dataset_id = self.add_dataset(dataset_name)
        with self._Session() as session:
            # Load existing schema from cache
            schema_record = (
                session.query(MainSchemaCacheTable)
                .filter(MainSchemaCacheTable.dataset_id == dataset_id)
                .first()
            )
            existing_schema = (
                json.loads(schema_record.partial_schema) if schema_record else {}
            )

            # Retrieve the current number_of_records from the cached schema
            existing_count = existing_schema.get("number_of_records", 0)

            # Track new files added
            new_files_added = 0

            # Cache new file paths
            for file_path in file_paths:
                file_record = (
                    session.query(FilePathsTable)
                    .filter(
                        FilePathsTable.dataset_id == dataset_id,
                        FilePathsTable.file_path == file_path,
                    )
                    .first()
                )
                if not file_record:
                    session.add(
                        FilePathsTable(file_path=file_path, dataset_id=dataset_id)
                    )
                    new_files_added += 1

            # Update the 'number_of_records' field in the partial_schema
            partial_schema["number_of_records"] = existing_count + new_files_added

            # Save the updated schema back to the cache
            schema_json = json.dumps(partial_schema)
            if schema_record:
                schema_record.partial_schema = schema_json
            else:
                session.add(
                    MainSchemaCacheTable(
                        dataset_id=dataset_id,
                        partial_schema=schema_json,
                    )
                )

            session.commit()

    def get_partial_schema(self, dataset_name: str) -> Optional[dict[str, Any]]:
        """Retrieve the partial schema for a dataset."""
        with self._Session() as session:
            dataset = (
                session.query(DatasetsTable)
                .filter(DatasetsTable.dataset_name == dataset_name)
                .first()
            )
            if not dataset:
                return None

            schema_record = (
                session.query(MainSchemaCacheTable)
                .filter(MainSchemaCacheTable.dataset_id == dataset.id)
                .first()
            )
            return json.loads(schema_record.partial_schema) if schema_record else None

    def get_file_paths(self, dataset_name: str) -> List[str]:
        """Retrieve all file paths associated with a dataset."""
        with self._Session() as session:
            dataset = (
                session.query(DatasetsTable)
                .filter(DatasetsTable.dataset_name == dataset_name)
                .first()
            )
            if not dataset:
                return []

            file_paths = session.query(FilePathsTable).filter(
                FilePathsTable.dataset_id == dataset.id
            )
            return [file_record.file_path for file_record in file_paths]

    def get_partial_schema_and_file_paths(
        self, dataset_name: str
    ) -> tuple[Optional[dict[str, Any]], List[str]]:
        """Retrieve the partial schema and filepaths for a dataset."""
        return self.get_partial_schema(dataset_name), self.get_file_paths(dataset_name)

    def update_partial_schema_field(
        self, dataset_name: str, field_path: List[str], value: Any
    ) -> None:
        """Update a specific field in the partial schema for a given dataset.

        Args:
            dataset_name: The name of the dataset.
            field_path: A list of keys representing the nested field path to update.
                        E.g., ["metadata", "schema_type"].
            value: The new value to set for the field.
        """
        dataset_id = self.add_dataset(dataset_name)
        with self._Session() as session:
            schema_record = (
                session.query(MainSchemaCacheTable)
                .filter(MainSchemaCacheTable.dataset_id == dataset_id)
                .first()
            )
            if not schema_record:
                _logger.warning(
                    f"No partial schema found for dataset '{dataset_name}'."
                )
                return

            # Load and update the partial schema
            partial_schema = json.loads(schema_record.partial_schema)

            # Traverse the nested dictionary to update the value
            # and log warning if not
            current = partial_schema
            for key in field_path[:-1]:
                if key not in current:
                    _logger.warning(
                        f"Field '{key}' not found in partial schema, cannot be updated."
                    )
                    return
                current = current[key]
            if field_path[-1] not in current:
                _logger.warning(
                    f"Field '{field_path[-1]}' not found in partial schema, "
                    "cannot be updated."
                )
                return
            current[field_path[-1]] = value

            # Save the updated schema back to the database
            schema_record.partial_schema = json.dumps(partial_schema)
            session.commit()

    def clear_dataset(self, dataset_name: str) -> None:
        """Clear all cached data for a dataset."""
        with self._Session() as session:
            dataset = (
                session.query(DatasetsTable)
                .filter(DatasetsTable.dataset_name == dataset_name)
                .first()
            )
            if dataset:
                session.query(MainSchemaCacheTable).filter(
                    MainSchemaCacheTable.dataset_id == dataset.id
                ).delete()
                session.query(FilePathsTable).filter(
                    FilePathsTable.dataset_id == dataset.id
                ).delete()
                session.query(DatasetsTable).filter(
                    DatasetsTable.id == dataset.id
                ).delete()
                session.commit()
