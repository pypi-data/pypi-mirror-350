"""
Concrete thin shims around cloud libraries.
Each module must expose

    def write(...)
    def define_schema(...)

with identical signatures.
"""

from importlib import import_module
from types import ModuleType
from typing import Protocol
import pandas as pd
from .._typing import JsonMapping, Kwargs, WriteMode


class Backend(Protocol):
    # write & define_schema will be implemented by each provider
    def write(
        self,
        df: pd.DataFrame,
        *,
        dest: str,
        mode: WriteMode,
        partition_cols: list[str] | None,
        dtype: JsonMapping | None,
        **extra: Kwargs,
    ) -> None: ...

    def define_schema(
        self,
        df: pd.DataFrame,
        *,
        camel_case: bool = False,
    ) -> JsonMapping: ...


def import_backend(name: str) -> ModuleType:
    return import_module(f".{name}", package=__name__)
