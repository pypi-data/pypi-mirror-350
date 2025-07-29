from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

import evoml_preprocessor.types.dtype as dtype
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class SquareEncoder(Encoder[dtype.Float64, dtype.Float64]):
    """
    Encoder for performing square encoding.
    Inherits the TransformerMixin class.

    Example:
        encoder = SquareEncoder()
        transformed_data = encoder.transform(data)
    """

    def fit(self, X: Series[dtype.Float64], y: Optional[SeriesTarget] = None) -> None: ...

    def transform(self, X: Series[dtype.Float64]) -> DataFrame[dtype.Float64]:
        # @data: `np.square` saves to new array
        transformed: Series[dtype.Float64] = pd.Series(np.square(X), name=X.name, index=X.index)  # type: ignore
        return transformed.to_frame()
