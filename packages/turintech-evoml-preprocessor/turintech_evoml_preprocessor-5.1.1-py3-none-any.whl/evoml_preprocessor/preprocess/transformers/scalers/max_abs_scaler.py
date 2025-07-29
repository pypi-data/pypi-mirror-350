from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.preprocessing import MaxAbsScaler as _MaxAbsScaler

from evoml_preprocessor.preprocess.transformers.scalers._base import Scaler
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame


class MaxAbsScaler(Scaler):
    def __init__(self):
        self._scaler: Optional[_MaxAbsScaler] = None

    def __str__(self):
        return "MaxAbsScaler()"

    @property
    def scaler(self) -> _MaxAbsScaler:
        if self._scaler is None:
            raise AttributeError("Fit must be called to set the scaler.")
        return self._scaler

    def fit(self, X: DataFrame[dtype.Float64]) -> None:
        self._scaler = _MaxAbsScaler()
        self.scaler.fit(X.to_numpy())

    def transform(self, X: DataFrame[dtype.Float64]) -> DataFrame[dtype.Float64]:
        # @typing: wrapped method doesn't know about our DataFrame typing
        return pd.DataFrame(self.scaler.transform(X.to_numpy()), columns=X.columns, index=X.index)  # type: ignore
