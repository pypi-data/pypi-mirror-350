import gc
import pandas as pd
import awswrangler as wr
from .base import AbstractFile, ReadFileException


CHUNKSIZE = 10000


class CsvGCPFile(AbstractFile):
    def _read_impl(
        self, s3_path, skiprows=None, usecols=None, **kwargs
    ) -> pd.DataFrame:
        print(f"skiprows {skiprows}, usecols {usecols}, kwargs {kwargs}")
        df = wr.s3.read_csv(s3_path, skiprows=skiprows, usecols=usecols, **kwargs)
        df.columns = list(self.contract_cls.schema.keys())
        return self.contract_cls.convert(df).df

    def _read_impl_without_validation_schema(
        self, s3_path, skiprows=None, usecols=None, reader_behavior="all", **kwargs
    ) -> pd.DataFrame:
        print(
            f"skiprows {skiprows}, usecols {usecols}, kwargs {kwargs}, reader_behavior {reader_behavior}"
        )
        if reader_behavior == "all":
            df = wr.s3.read_csv(s3_path, skiprows=skiprows, usecols=usecols, **kwargs)
        elif reader_behavior == "one":
            df = self._read_core_process(
                s3_path, skiprows=skiprows, usecols=usecols, **kwargs
            )
        return df

    def _read_core_process(
        self, s3_path, sheet_name=0, skiprows=None, usecols=None, **kwargs
    ) -> pd.DataFrame:
        try:
            if (
                isinstance(s3_path, list) and sheet_name == 0
            ):  # read several xlsx file and sheet 0 by each file
                out = []
                for ind, path in enumerate(s3_path):
                    filename_absolute = path.split("/")[-1]
                    filename_relative = filename_absolute.split(".")[0]
                    # data = wr.s3.read_csv(
                    #     path,
                    #     skiprows=skiprows,
                    #     usecols=usecols,
                    #     **kwargs,
                    # )
                    for chunk in wr.s3.read_csv(
                        path,
                        skiprows=skiprows,
                        usecols=usecols,
                        chunksize=CHUNKSIZE,
                        **kwargs,
                    ):
                        chunk["filename"] = filename_relative
                        out.append(chunk)
                        # columns = list(chunk.columns)
                        # map each column except the first like float64
                        # for col in columns[1:]:
                        #     chunk[col] = chunk[col].str.replace(',', '.').astype("float64")
                        print(f"{ind} dataframe - {chunk.shape}")
                        # print(f" Info Memory Usage: {chunk.info(memory_usage='deep')}")
                        print(
                            f"Memory Usage: {chunk.memory_usage(deep=True).sum() / 1024**2} MB"
                        )
                        del chunk
                        gc.collect()
                    # out.append(data)
                    # data["filename"] = filename_relative
                    # print(f"{ind} dataframe - {data.shape}")
                output = pd.concat(out, axis=0, ignore_index=True)
                print(
                    f"Memory Usage: {output.memory_usage(deep=True).sum() / 1024**2} MB"
                )
                del out
                gc.collect()
                return output
            elif isinstance(
                s3_path, str
            ):  # read single xlsx file and several sheets if sheet_name is equal to None
                return wr.s3.read_csv(
                    s3_path,
                    skiprows=skiprows,
                    usecols=usecols,
                    **kwargs,
                )
            else:
                raise NotImplementedError("Invalid type of S3_PATH")
        except Exception as e:
            raise ReadFileException(f"Error reading file {s3_path} - {e}")


class ExcelGCPFile(AbstractFile):
    def _read_impl(
        self, s3_path, sheet_name=0, skiprows=None, usecols=None, **kwargs
    ) -> pd.DataFrame:
        df: pd.DataFrame = self._read_core_process(
            s3_path, sheet_name=sheet_name, skiprows=skiprows, usecols=usecols, **kwargs
        )
        print(df.columns)
        df.columns = list(self.contract_cls.schema.keys())
        print(f"total rows and columns dataframe - {df.shape}")
        return self.contract_cls.convert(df).df

    def _read_impl_without_validation_schema(
        self, s3_path, sheet_name=0, skiprows=None, usecols=None, **kwargs
    ) -> pd.DataFrame:
        df = self._read_core_process(
            s3_path, sheet_name=sheet_name, skiprows=skiprows, usecols=usecols, **kwargs
        )
        print(f"total rows and columns dataframe - {df.shape}")
        return df

    def _read_core_process(
        self, s3_path, sheet_name=0, skiprows=None, usecols=None, **kwargs
    ) -> pd.DataFrame:
        try:
            if (
                isinstance(s3_path, list) and sheet_name == 0
            ):  # read several xlsx file and sheet 0 by each file
                out = []
                for ind, path in enumerate(s3_path):
                    data = wr.s3.read_excel(
                        path,
                        sheet_name=sheet_name,
                        skiprows=skiprows,
                        usecols=usecols,
                        **kwargs,
                    )
                    out.append(data)
                    print(f"{ind} dataframe - {data.shape}")
                return pd.concat(out, axis=0, ignore_index=True)
            elif (
                isinstance(s3_path, list) and sheet_name is None
            ):  # read several xlsx file and all sheet by each file
                raise NotImplementedError()
            elif (
                isinstance(s3_path, str) and sheet_name == 0
            ):  # read single xlsx file and several sheets if sheet_name is equal to None
                print(f"sheet_name {sheet_name}")
                return wr.s3.read_excel(
                    s3_path,
                    sheet_name=sheet_name,
                    skiprows=skiprows,
                    usecols=usecols,
                    **kwargs,
                )
            elif (
                isinstance(s3_path, str) and sheet_name is None
            ):  # read single xlsx file and several sheets if sheet_name is equal to None
                print(f"sheet_name {sheet_name}")
                dict_dtaframes = wr.s3.read_excel(
                    s3_path,
                    sheet_name=sheet_name,
                    skiprows=skiprows,
                    usecols=usecols,
                    **kwargs,
                )
                df_concated = pd.concat(
                    [
                        frame.assign(sheetname=name)
                        for name, frame in dict_dtaframes.items()
                    ],
                    axis=0,
                    ignore_index=True,
                )
                return df_concated.assign(sheetname=df_concated.pop("sheetname"))

            else:
                raise NotImplementedError("Invalid type of S3_PATH")
        except Exception as e:
            raise ReadFileException(f"Error reading file {s3_path} - {e}")

    def _get_sheets_names(self, s3_path):
        raise NotImplementedError
