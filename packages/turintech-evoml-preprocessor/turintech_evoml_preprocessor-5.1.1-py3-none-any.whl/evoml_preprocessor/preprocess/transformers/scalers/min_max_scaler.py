from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.preprocessing import MinMaxScaler as _MinMaxScaler

from evoml_preprocessor.preprocess.transformers.scalers._base import Scaler
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame


class MinMaxScaler(Scaler):
    def __init__(self):
        self._scaler: Optional[_MinMaxScaler] = None

    def __str__(self):
        return "MinMaxScaler()"

    @property
    def scaler(self) -> _MinMaxScaler:
        if self._scaler is None:
            raise AttributeError("Fit must be called to set the scaler.")
        return self._scaler

    def fit(self, X: DataFrame[dtype.Float64]) -> None:
        self._scaler = _MinMaxScaler()
        self.scaler.fit(X.to_numpy())

    def transform(self, X: DataFrame[dtype.Float64]) -> DataFrame[dtype.Float64]:
        # @typing: wrapped method doesn't know about our DataFrame typing
        return pd.DataFrame(self.scaler.transform(X.to_numpy()), columns=X.columns, index=X.index)  # type: ignore
