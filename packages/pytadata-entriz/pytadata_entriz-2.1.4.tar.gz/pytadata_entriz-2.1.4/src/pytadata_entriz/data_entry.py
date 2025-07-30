"""
Public façade: one class that routes to the proper provider module.
"""

from __future__ import annotations
import pandas as pd
from typing import Any

from ._typing import (
    Provider,
    WriteMode,
    JsonMapping,
    Kwargs,
)
from ._detect import load_module
from .providers import Backend
from .common.logger import get_logger
from .common.validator import SchemaDataValidator


class DataEntry:
    """
    Write a **pandas.DataFrame** to the configured destination (S3, BigQuery).

    Parameters
    ----------
    provider :
        "aws", "gcp" or "auto" (default).  When "auto", the first installed
        backend wins (awswrangler before pandas-gbq).
    default_dest :
        • AWS → an *S3 URI* “s3://bucket/prefix/”
        • GCP → “project.dataset.table”
    config :
        Mapping of provider-specific options that will be splashed into every
        ``write()`` call.  (e.g. ``{"region": "us-east-1"}`` for AWS or
        ``{"location": "EU"}`` for BigQuery.)
    """

    # ────────────────────────────────────────────────────────────────
    def __init__(
        self,
        *,
        provider: Provider = "local",
        default_dest: str | None = None,
        config: Kwargs | None = None,
    ) -> None:
        mod = load_module(provider)
        self._backend: Backend = mod  # type: ignore[assignment]
        self._default_dest = default_dest
        self._config: Kwargs = dict(config or {})
        self.logger = get_logger(__name__)

    # ────────────────────────────────────────────────────────────────
    def read(
        self,
        dest: str | None = None,
        validation: bool = True,
        columns: list[str] | None = None,
        **extra: Kwargs,
    ) -> pd.DataFrame:
        """
        Load a DataFrame from the destination previously written.

        Parameters
        ----------
        dest :
            Overrides ``default_dest``.
        columns :
            Subset of columns to pull back (provider-specific push-down).
        **extra :
            Passed to the backend's read() (credentials, filters, etc.)
        """
        if dest is None and self._default_dest is None:
            self.logger.error("Destination must be supplied (dest= or default_dest).")
            raise ValueError("Destination must be supplied (dest= or default_dest).")

        self.logger.info(f"Reading data from {dest or self._default_dest}...")

        return self._backend.read(
            dest or self._default_dest,  # type: ignore[arg-type]
            columns=columns,
            validation=validation,
            **self._config,
            **extra,
        )

    # ────────────────────────────────────────────────────────────────

    def write(
        self,
        df: pd.DataFrame,
        *,
        dest: str | None = None,
        mode: WriteMode = "append",
        partition_cols: list[str] | None = None,
        dtype: JsonMapping | None = None,
        **extra: Kwargs,
    ) -> None:
        """
        Persist *df* to the chosen destination.

        Parameters
        ----------
        dest :
            Overrides the constructor’s ``default_dest``.
        mode :
            "append" | "overwrite" | "replace"
        partition_cols :
            Partition keys (S3 prefix or BQ partition columns).
        dtype :
            Explicit column types mapping; skips auto inference.
        **extra :
            Passed as-is to the underlying provider writer.
        """
        if dest is None and self._default_dest is None:
            raise ValueError("Destination must be supplied (dest= or default_dest).")
        self._backend.write(
            df,
            dest=dest or self._default_dest,  # type: ignore[arg-type]
            mode=mode,
            partition_cols=partition_cols,
            dtype=dtype,
            **self._config,  # from constructor
            **extra,  # per-call
        )

    # ────────────────────────────────────────────────────────────────
    def define_schema(
        self,
        df: pd.DataFrame,
        *,
        camel_case: bool = False,
    ) -> JsonMapping:
        """
        Return {column: bigquery_or_glue_type} mapping.
        """
        return self._backend.define_schema(df, camel_case=camel_case)

    def validate(
        self,
        df: pd.DataFrame,
        schema_csv_path: str = "./local/schema.csv",
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Validate the DataFrame against the contract schema.





        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame to validate.
        validation : bool, optional
            Whether to perform validation (default is True).
        **kwargs : Any
            Additional keyword arguments for validation.

        Returns
        -------
        pd.DataFrame
            The validated DataFrame.
        """
        validator = SchemaDataValidator(
            schema_csv_path=schema_csv_path,
            input_data_df=df,
            logger=self.logger,
        )

        result_df = validator.run_validation_and_report()

        return result_df
