from __future__ import annotations

from typing import Optional

import numpy as np

from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class LogEncoder(Encoder[dtype.Float64, dtype.Float64]):
    def fit(self, X: Series[dtype.Float64], y: Optional[SeriesTarget] = None) -> None: ...

    def transform(self, X: Series[dtype.Float64]) -> DataFrame[dtype.Float64]:
        # @NOTE: here, a copy is made if the dtype is not compatible.
        # If the dtype is float64, say, no copy is made.
        transformed: Series[dtype.Float64] = X.astype(float, copy=False)  # force output type of X
        positive_index = transformed >= 0.0
        negative_index = transformed < 0.0
        transformed[positive_index] = np.log(transformed[positive_index] + 1)
        transformed[negative_index] = -1
        return transformed.to_frame()
