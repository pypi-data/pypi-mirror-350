"""
GCP implementation (pandas-gbq ≥0.20 → google-cloud-bigquery).
"""

from __future__ import annotations
import pandas as pd
from ..common.helper import HelperReader
from pandas_gbq import to_gbq, generate_bq_schema
from typedframe import TypedDataFrame

from .._typing import JsonMapping, Kwargs, WriteMode

_BQ_WRITE_MODES: dict[WriteMode, str] = {
    "append": "append",
    "overwrite": "truncate",
    "replace": "replace",
}


# def read(uri: str, **storage_opts) -> pd.DataFrame:
#     ds_ = ds.dataset(uri, format="parquet", filesystem="gcsfs", **storage_opts)
#     return ds_.to_table().to_pandas()
def read(
    dest: str,
    columns: list[str] | None = None,
    **extra: Kwargs,
) -> pd.DataFrame:
    """
    Load a DataFrame from an GCS dataset (Parquet/CSV/…) using ds.
    Example dest → "gs://bucket/prefix/"
    """

    data_df_cleaned = _define_context(filepath=dest, **extra)

    return data_df_cleaned


def write(
    df: pd.DataFrame,
    *,
    dest: str,
    mode: WriteMode,
    partition_cols: list[str] | None,
    dtype: JsonMapping | None,
    **extra: Kwargs,
) -> None:
    """Write DataFrame to BigQuery table."""
    to_gbq(
        dataframe=df,
        destination_table=dest,  # project.dataset.table
        if_exists=_BQ_WRITE_MODES[mode],
        table_schema=_merge_schema(df, dtype) if dtype else None,
        **extra,
    )


def define_schema(
    df: pd.DataFrame,
    *,
    camel_case: bool = False,
) -> JsonMapping:
    raw = generate_bq_schema(df)
    if camel_case:
        for f in raw:
            f["name"] = _camel(f["name"])
    # convert list[dict] → {name:type}
    return {f["name"]: f["type"] for f in raw}


# ──────────────────────────────────────────────────────────
def _merge_schema(df: pd.DataFrame, overrides: JsonMapping | None) -> list[dict]:
    base = generate_bq_schema(df)
    if not overrides:
        return base
    for field in base:
        if field["name"] in overrides:
            field["type"] = overrides[field["name"]]
    return base


def _camel(s: str) -> str:
    head, *tail = s.split("_")
    return "".join([head.lower(), *[t.capitalize() for t in tail]])


def _define_context(
    filepath: str | None = None,
    contract_definition: TypedDataFrame | None = None,
    pre_transformations: list[any] | None = None,
    post_transformations: list[any] | None = None,
) -> str:
    """
    Return a string representation of the current configuration.
    """

    helper_reader1 = HelperReader()
    helper_reader1.bucket_name = ""
    helper_reader1.path_filename = filepath
    helper_reader1.filename = filepath.split("/")[-1]
    helper_reader1.extfile = filepath.split(".")[-1]
    helper_reader1.filter_file = filepath.split(".")[-1]
    helper_reader1.contract = contract_definition

    # s3_path_to_read1 = helper_reader1.build_input_to_read()

    reader_file1 = helper_reader1.choice_handler("gcp")

    [reader_file1.add_post_hook(hook_custom for hook_custom in pre_transformations)]

    [reader_file1.add_post_hook(hook_custom for hook_custom in post_transformations)]

    return reader_file1
