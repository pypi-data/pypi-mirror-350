"""
pytadata_entriz ― Uniform DataFrame writer for AWS or GCP back-ends.
"""

from importlib.metadata import version as _v
from .data_entry import DataEntry

__all__ = ["DataEntry", "__version__"]
__version__: str = _v(__name__)
