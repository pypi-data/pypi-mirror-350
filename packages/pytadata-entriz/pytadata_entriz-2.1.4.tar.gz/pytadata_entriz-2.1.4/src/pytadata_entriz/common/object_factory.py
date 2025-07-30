from typing import Union

from .file_readers_s3 import (  # Assuming you've kept the readers in a file named file_readers.py
    CsvCloudFile,
    ExcelCloudFile,
)

from .file_readers_gcp import (  # Assuming you've kept the readers in a file named file_readers.py
    CsvGCPFile,
    ExcelGCPFile,
)


class ObjectFactory:
    """
    A factory class for creating objects based on a key.

    Attributes:
        _builders (dict): A dictionary containing the registered builders.
    """

    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        """
        Registers a builder function for a given key.
        Args:
            key (str): The key to associate with the builder function.
            builder (function): The builder function to register.
        """
        self._builders[key] = builder

    def create(
        self, key, **kwargs
    ) -> Union[CsvCloudFile, ExcelCloudFile, CsvGCPFile, ExcelGCPFile]:
        """
        Creates an object using the registered builder function for the given key.
        Args:
            key (str): The key associated with the builder function to use.
            **kwargs: Additional keyword arguments to pass to the builder function.
        Returns:
            The object created by the builder function.
        Raises:
            ValueError: If no builder function is registered for the given key.
        """
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
