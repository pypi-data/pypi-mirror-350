from dataclasses import dataclass
from typing import List, Optional, Union

from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import (
    CategoricalEncoder,
    GenericOption,
    ImputeStrategy,
    NumericEncoder,
    ScalerEncoder,
)


@dataclass
class EncoderSpace:
    col_info: ColumnInfo
    encoders: Union[List[NumericEncoder], List[CategoricalEncoder]]
    scalers: Optional[List[Union[ScalerEncoder, GenericOption]]]
    impute_strategy: ImputeStrategy
    impute_value: Optional[ImputeValue] = None
