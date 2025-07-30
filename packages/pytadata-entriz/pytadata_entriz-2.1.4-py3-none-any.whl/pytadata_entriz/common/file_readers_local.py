import pandas as pd
from .base import AbstractFile
from typedframe import TypedDataFrame

from .logger import get_logger

logger = get_logger(__name__)


class CsvLocalFile(AbstractFile):
    def _read_impl(self, path, skiprows=None, usecols=None, **kwargs) -> pd.DataFrame:
        logger.info(
            f"Reading CSV file from {path} with skiprows={skiprows} and usecols={usecols}"
        )

        df = pd.read_csv(path, skiprows=skiprows, usecols=usecols, **kwargs)

        logger.info(f"CSV file read successfully, shape: {df.shape}")

        logger.debug(
            f"Validating CSV file against contract schema: {self.contract_cls.schema}"
        )

        # df.columns = list(self.contract_cls.schema.keys())

        return self.contract_cls.convert(df).df

    def _read_impl_without_validation_schema(
        self, path, skiprows=None, usecols=None, **kwargs
    ) -> pd.DataFrame:
        logger.info("No validation schema provided, reading CSV without validation.")

        logger.info(
            f"Reading CSV file from {path} with skiprows={skiprows} and usecols={usecols}"
        )

        df = pd.read_csv(path, skiprows=skiprows, usecols=usecols, **kwargs)

        logger.info(f"CSV file read successfully, shape: {df.shape}")

        return df


class ExcelLocalFile(AbstractFile):
    def _read_impl(
        self, path, sheet_name=0, skiprows=None, usecols=None
    ) -> TypedDataFrame:
        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            skiprows=skiprows,
            usecols=usecols,
            engine="openpyxl",
        )
        return self.contract_cls.convert(df)

    def _read_impl_without_validation_schema(
        self, path, sheet_name=0, skiprows=None, usecols=None
    ) -> TypedDataFrame:
        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            skiprows=skiprows,
            usecols=usecols,
            engine="openpyxl",
        )
        return df
