from typing import Union

from .base import ReaderFile, ReadFileException
from .file_readers_s3 import (
    CsvCloudFile,
    ExcelCloudFile,
)
from .file_readers_gcp import (
    CsvGCPFile,
    ExcelGCPFile,
)
from .file_readers_local import (
    CsvLocalFile,
    ExcelLocalFile,
)
from .object_factory import ObjectFactory


from .logger import get_logger


class HelperReader(ReaderFile):
    """
    Helper class to read files from local or cloud provider.

    :param s3_client: The S3 client to us of botocore.client.S3.
    :type s3_client: boto3.session.Session.client
    :param bucket_name: The name of the S3 bucket.
    :type bucket_name: str
    :param path_filename: The path to the file to read.
    :type path_filename: str
    :param filename: The name of the file to read.
    :type filename: str
    :param extfile: The extension of the file to read.
    :type extfile: str
    :param contract: The contract to use to read the file.
    :type contract: TypedDataFrame

    """

    def __init__(
        self,
    ) -> None:
        self.logger = get_logger(__name__)

        self._file_factory: ObjectFactory = ObjectFactory()

        HelperReader._init_services(self._file_factory, self.logger)

    @staticmethod
    def _init_services(file_factory, logger):
        """
        Registers the file builders for different file types with the file factory.
        Args:
        - file_factory: An instance of the FileFactory class.
        """
        logger.info("Initializing file readers...")

        file_factory.register_builder("CsvLocal", CsvLocalFile)
        file_factory.register_builder("ExcelLocal", ExcelLocalFile)
        file_factory.register_builder("CsvCloud", CsvCloudFile)
        file_factory.register_builder("ExcelCloud", ExcelCloudFile)
        file_factory.register_builder("CsvGCP", CsvGCPFile)
        file_factory.register_builder("ExcelGCP", ExcelGCPFile)
        file_factory.register_builder("CsvGCP", CsvLocalFile)
        file_factory.register_builder("ExcelGCP", ExcelLocalFile)

    def choice_handler(
        self, provider
    ) -> Union[
        CsvCloudFile,
        ExcelCloudFile,
        CsvGCPFile,
        ExcelGCPFile,
        CsvLocalFile,
        ExcelLocalFile,
    ]:
        """
        This function determines the type of file and returns the appropriate reader object.

        :raise Exception: If the filename containe invalid extension.
        :return: he appropriate reader object based on the file type..
        :rtype: Union[CsvCloudFile, ExcelCloudFile, DatCloudFile]

        """
        if self.filename.endswith(".xlsx") and provider == "aws":
            self.logger.info("Using ExcelCloud reader...")
            return self._file_factory.create("ExcelCloud", contract_cls=self._contract)
        elif self.filename.endswith(".csv") and provider == "aws":
            self.logger.info("Using CsvCloud reader...")
        elif self.filename.endswith(".csv") and provider == "gcp":
            self.logger.info("Using CsvGCP reader...")
            return self._file_factory.create("CsvGCP", contract_cls=self._contract)
        elif self.filename.endswith(".xlsx") and provider == "gcp":
            self.logger.info("Using ExcelGCP reader...")
            return self._file_factory.create("ExcelGCP", contract_cls=self._contract)
        elif self.filename.endswith(".csv") and provider == "local":
            self.logger.info("Using CsvLocal reader...")
            return self._file_factory.create("CsvLocal", contract_cls=self._contract)
        elif self.filename.endswith(".xlsx") and provider == "local":
            self.logger.info("Using ExcelLocal reader...")
            return self._file_factory.create("ExcelLocal", contract_cls=self._contract)
        else:
            raise ReadFileException("File not supported and provider not supported yet")
