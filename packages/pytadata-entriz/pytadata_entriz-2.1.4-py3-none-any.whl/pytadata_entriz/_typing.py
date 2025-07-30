from typing import Literal, Mapping, MutableMapping, Any
import pandas as pd

Provider = Literal["aws", "gcp", "auto"]
WriteMode = Literal["append", "overwrite", "replace"]

JsonMapping = MutableMapping[str, Any]
Kwargs = Mapping[str, Any]

DataFrame = pd.DataFrame  # alias only for Protocol declaration
