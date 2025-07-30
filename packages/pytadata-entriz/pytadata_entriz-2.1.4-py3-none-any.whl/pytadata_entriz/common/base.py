from typing import Type
import time
import os
import sys
import botocore
import pandas as pd
from typedframe import TypedDataFrame


from .logger import get_logger

logger = get_logger(__name__)


class AbstractFile:
    def __init__(self, contract_cls: Type[TypedDataFrame]):
        self.contract_cls = contract_cls
        self.pre_hooks = []
        self.post_hooks = []

    def add_pre_hook(self, func):
        self.pre_hooks.append(func)

    def add_post_hook(self, func):
        self.post_hooks.append(func)

    def read(self, path_or_key, validation=True, **kwargs) -> pd.DataFrame:
        # Call all pre-processing hooks

        logger.info(
            "Starting read method with validation {} and config {}".format(
                validation, kwargs
            )
        )

        logger.info("Hooks pre-processing called {}".format(self.pre_hooks))

        for hook in self.pre_hooks:
            hook()

        logger.info("Wrapper read method called {}".format(path_or_key))

        data = (
            self._read_impl(path_or_key, **kwargs)
            if validation
            else self._read_impl_without_validation_schema(path_or_key, **kwargs)
        )

        logger.info("Hooks post-processing called {}".format(self.post_hooks))

        # Call all post-processing hooks
        for hook in self.post_hooks:
            modified_data = hook(data, self.contract_cls)
            if modified_data is not None:  # Check if a new DataFrame is returned
                data = modified_data

        return data

    def _read_impl(self, path_or_key, **kwargs):
        raise NotImplementedError

    def _read_impl_without_validation_schema(self, path_or_key, **kwargs):
        raise NotImplementedError


class ReadFileException(Exception):
    pass


class ReaderFile:
    def read_bulk_data(self) -> list:
        """
        Read bulk data from file.
        """
        pass

    def read_single_data(self) -> dict:
        """
        Read single data from file.
        """
        pass

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, value: str):
        self._filename = value

    @property
    def path_filename(self) -> str:
        return self._path_filename

    @path_filename.setter
    def path_filename(self, value: str):
        self._path_filename = value

    @property
    def config_reader(self) -> dict:
        return self._config_reader

    @config_reader.setter
    def config_reader(self, value: dict):
        self._config_reader = value

    @property
    def extfile(self) -> str:
        return self._extfile

    @extfile.setter
    def extfile(self, value: str):
        self._extfile = value

    @property
    def contract(self) -> TypedDataFrame:
        return self._contract

    @contract.setter
    def contract(self, value: TypedDataFrame):
        self._contract = value

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, value: str):
        self._bucket_name = value

    @property
    def filter_file(self) -> str:
        return self._filter_file

    @filter_file.setter
    def filter_file(self, value: str):
        self._filter_file = value


class HelperSysPaths:
    @staticmethod
    def __detect_system():
        if sys.platform == "win32":
            return "\\\\"
        else:
            return "/"

    @staticmethod
    def build_path_filename(filename_path: str, filename: StopIteration = None) -> str:
        sep_path = HelperSysPaths().__detect_system()

        filename_path = filename_path.replace("/", sep_path)

        con_path = f"{filename_path}{sep_path}{filename}"

        return con_path if filename else filename_path

    @staticmethod
    def get_file_extension(path: str) -> str:
        """
        Returns the file extension of the given path.
        """
        return os.path.splitext(path)[-1].lower()

    @staticmethod
    def is_local_file(path: str) -> bool:
        """
        Checks if the given local path corresponds to a file.
        """
        return os.path.isfile(path)

    @staticmethod
    def is_local_directory(path: str) -> bool:
        """
        Checks if the given local path corresponds to a directory.
        """
        return os.path.isdir(path)

    @staticmethod
    def is_s3_object(s3, bucket: str, key: str) -> bool:
        """
        Checks if the given S3 path corresponds to an object.
        """
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return True
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 403:
                raise Exception(f"Access denied for bucket: {bucket} and key: {key}")
            elif error_code == 404:
                return False
            else:
                raise Exception(
                    f"Error unknow: {str(e)} in bucket: {bucket} and key: {key}"
                )

    @staticmethod
    def is_s3_prefix(s3, bucket: str, prefix: str) -> bool:
        """
        Checks if the given S3 prefix corresponds to any objects (like a directory containing files).
        """
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
        return "Contents" in response or "CommonPrefixes" in response

    @staticmethod
    def to_list_files(
        s3, bucket_name: str, folder_path: str, filter_file: str = None
    ) -> list:
        output = []
        time.sleep(60)
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

        for obj in response.get("Contents", []):
            output.append(obj["Key"])

        if filter_file:
            output = list(
                filter(
                    lambda x: x.endswith(filter_file.lower())
                    or x.endswith(filter_file.upper()),
                    output,
                )
            )

        return output
