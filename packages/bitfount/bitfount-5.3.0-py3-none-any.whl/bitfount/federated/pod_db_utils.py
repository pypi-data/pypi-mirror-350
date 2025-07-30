"""Utilities for the Pod results database."""

from __future__ import annotations

from collections.abc import Sequence
from sqlite3 import Connection

import pandas as pd

from bitfount.data.datasources.base_source import FileSystemIterableSource
from bitfount.federated import _get_federated_logger
from bitfount.federated.types import SerializedProtocol

logger = _get_federated_logger(__name__)


def map_task_to_hash_add_to_db(
    serialized_protocol: SerializedProtocol, task_hash: str, project_db_con: Connection
) -> None:
    """Maps the task hash to the protocol and algorithm used.

    Adds the task to the task database if it is not already present.

    Args:
        serialized_protocol: The serialized protocol used for the task.
        task_hash: The hash of the task.
        project_db_con: The connection to the database.
    """
    algorithm_ = serialized_protocol["algorithm"]
    if not isinstance(algorithm_, Sequence):
        algorithm_ = [algorithm_]
    for algorithm in algorithm_:
        if "model" in algorithm:
            algorithm["model"].pop("schema", None)
            if algorithm["model"]["class_name"] == "BitfountModelReference":
                algorithm["model"].pop("hub", None)

    cur = project_db_con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS "task_definitions" ('index' INTEGER  PRIMARY KEY AUTOINCREMENT  NOT NULL, 'taskhash' TEXT,'protocol' TEXT,'algorithm' TEXT)"""  # noqa: E501
    )
    data = pd.read_sql("SELECT * FROM 'task_definitions' ", project_db_con)
    if task_hash not in list(data["taskhash"]):
        logger.info("Adding task to task database")
        cur.execute(
            """INSERT INTO "task_definitions" ('taskhash',  'protocol', 'algorithm' ) VALUES (?,?,?);""",  # noqa: E501
            (
                task_hash,
                serialized_protocol["class_name"],
                str(algorithm_),
            ),
        )
    else:
        logger.debug("Task already in task database")
    project_db_con.commit()


def save_processed_datapoint_to_project_db(
    project_db_con: Connection,
    datasource: FileSystemIterableSource,
    task_hash: str,
) -> None:
    """Saves the result of a task run to the database.

    Args:
        project_db_con: The connection to the project database.
        datasource: The datasource used for the task.
        task_hash: The hash of the task, a unique identifier for when results have
            come from the same task definition, regardless of whether they are from
            the same run.
    """
    logger.info("Saving results to database")

    # Process and merge each dataframe to store it into the database
    for i, data_that_results_apply_to in enumerate(
        datasource.yield_data(datasource.selected_file_names, use_cache=True), start=1
    ):
        try:
            _save_processed_datapoint_references_to_project_db(
                data_that_results_apply_to=data_that_results_apply_to,
                datasource=datasource,
                task_hash=task_hash,
                project_db_con=project_db_con,
            )
        except Exception as e:
            logger.error(f"Error saving batch {i} to database")
            logger.exception(e)

    logger.info("Results saved to database")


def _save_processed_datapoint_references_to_project_db(
    data_that_results_apply_to: pd.DataFrame,
    datasource: FileSystemIterableSource,
    task_hash: str,
    project_db_con: Connection,
) -> None:
    """Saves the references to the processed data to the project database.

    Args:
        data_that_results_apply_to: The data that the results apply to.
        datasource: The datasource used for the task.
        task_hash: The hash of the task, a unique identifier for when results have
            come from the same task definition, regardless of whether they are from
            the same run.
        project_db_con: The connection to the project database.
    """
    columns = datasource.get_project_db_sqlite_columns()
    data_that_results_apply_to = data_that_results_apply_to[columns]
    data_that_results_apply_to.to_sql(
        f"{task_hash}-v2", con=project_db_con, if_exists="append", index=False
    )
