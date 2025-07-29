from __future__ import annotations

from evoml_preprocessor.preprocess.transformers.scalers._base import Scaler
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame


class IdentityScaler(Scaler):
    def __str__(self):
        return "IdentityScaler()"

    def fit(self, X: DataFrame[dtype.Float64]) -> None: ...

    def transform(self, X: DataFrame[dtype.Float64]) -> DataFrame[dtype.Float64]:
        return X
