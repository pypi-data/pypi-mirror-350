from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.preprocessing import PowerTransformer

from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class PowerEncoder(Encoder[dtype.Float64, dtype.Float64]):
    """
    Encoder for performing power transformation.
    Inherits the Encoder class.

    Example:
        encoder = PowerEncoder()
        transformed_data = encoder.transform(data)
    """

    def __init__(self) -> None:
        self._encoder: Optional[PowerTransformer] = None

    @property
    def encoder(self) -> PowerTransformer:
        if self._encoder is None:
            raise AttributeError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Float64], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = PowerTransformer(method="yeo-johnson", standardize=True, copy=True)
        # @data: no copy
        X_np = X.to_numpy().reshape(-1, 1)
        self.encoder.fit(X_np)

    def transform(self, X: Series[dtype.Float64]) -> DataFrame[dtype.Float64]:
        # @data: only copy here is the `transform` operation, set by the `PowerTransformer`
        # constructor
        X_np = X.to_numpy().reshape(-1, 1)
        transformed = self.encoder.transform(X_np)
        return pd.DataFrame(transformed, columns=[X.name], index=X.index)  # type: ignore
