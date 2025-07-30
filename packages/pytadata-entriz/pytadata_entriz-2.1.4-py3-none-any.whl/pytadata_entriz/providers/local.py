"""
AWS implementation (awswrangler ≥3.7).
"""

from __future__ import annotations
import pandas as pd
import awswrangler as wr
import os
import pyarrow as pa
import pyarrow.parquet as pq

from ..common.helper import HelperReader
from typedframe import TypedDataFrame


from .._typing import JsonMapping, Kwargs, WriteMode

from ..common.logger import get_logger

logger = get_logger(__name__)

_S3_WRITE_MODES: dict[WriteMode, str] = {
    "append": "append",
    "overwrite": "overwrite_partitions",
    "replace": "overwrite",
}


def read(
    dest: str,
    columns: list[str] | None = None,
    validation: bool = False,
    **extra: Kwargs,
) -> pd.DataFrame:
    """
    Load a DataFrame from an S3 dataset (Parquet/CSV/…) using awswrangler.
    Example dest → "s3://bucket/prefix/"
    """

    logger.info(f"Reading data from {dest} and {extra}...")

    logger.info(f"Reading data from local {dest}...")

    reader_manager = _define_context(
        filepath=dest,
        contract_definition=extra.get("contract_definition"),
        pre_transformations=extra.get("pre_transformations", []),
        post_transformations=extra.get("post_transformations", []),
    )
    data_cleaned_df = reader_manager.read(
        dest,
        validation=validation,
    )

    return data_cleaned_df


def write(
    df: pd.DataFrame,
    *,
    dest: str,
    mode: WriteMode,
    partition_cols: list[str] | None,
    dtype: JsonMapping | None,
    **extra: Kwargs,
) -> None:
    """Write DataFrame to S3 (Parquet) using awswrangler."""

    logger.info(f"Writing data to {dest}...")

    # Validate if exists folder with os

    dest_folder = "/".join(dest.split("/")[:-1])  # Remove the file name from the path

    if not os.path.exists(dest_folder):
        logger.info(f"Creating directory {dest_folder}...")
        os.makedirs(dest_folder, exist_ok=True)
    else:
        logger.info(f"Directory {dest} already exists.")

    table = pa.Table.from_pandas(df)
    pq.write_table(table, dest, compression="snappy")

    logger.info(f"Data written to {dest} successfully.")


def define_schema(
    df: pd.DataFrame,
    *,
    camel_case: bool = False,
) -> JsonMapping:
    sch = wr.catalog.extract_athena_types(df)
    if camel_case:
        sch = {_camel(k): v for k, v in sch.items()}
    return sch


# ──────────────────────────────────────────────────────────
def _camel(s: str) -> str:
    head, *tail = s.split("_")
    return "".join([head.lower(), *[t.capitalize() for t in tail]])


def _define_context(
    filepath: str | None = None,
    contract_definition: TypedDataFrame | None = None,
    pre_transformations: list[any] | None = [],
    post_transformations: list[any] | None = [],
) -> str:
    """
    Return a string representation of the current configuration.
    """
    logger.info(f"Defining context with filepath: {filepath}, ")
    if not filepath:
        raise ValueError("Filepath must be provided.")

    helper_reader1 = HelperReader()
    helper_reader1.bucket_name = ""
    helper_reader1.path_filename = filepath
    helper_reader1.filename = filepath.split("/")[-1]
    helper_reader1.extfile = filepath.split(".")[-1]
    helper_reader1.filter_file = filepath.split(".")[-1]
    helper_reader1.contract = contract_definition

    # s3_path_to_read1 = helper_reader1.build_input_to_read()

    reader_file1 = helper_reader1.choice_handler("local")

    logger.info(f"Reader file component : {reader_file1.__class__}")

    logger.info(f"Reader file component : {reader_file1.__dict__}")

    logger.info("Hooks to be added:")
    logger.info(f"Pre-transformations: {pre_transformations}")
    logger.info(f"Post-transformations: {post_transformations}")

    if not pre_transformations:
        logger.info("No pre-transformations to add.")
    else:
        logger.info(f"Adding pre-transformations: {pre_transformations}")
        [reader_file1.add_pre_hook(hook_custom) for hook_custom in pre_transformations]
    if not post_transformations:
        logger.info("No post-transformations to add.")
    else:
        logger.info(f"Adding post-transformations: {post_transformations}")
        [
            reader_file1.add_post_hook(hook_custom)
            for hook_custom in post_transformations
        ]

    return reader_file1
