from __future__ import annotations

from typing import TypeVar

from evoml_preprocessor.preprocess.transformers.imputers._base import Imputer
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import Series

FeatureT = TypeVar("FeatureT", bound=dtype.Any)


class IdentityImputer(Imputer[FeatureT, FeatureT]):
    def __int__(self):
        super().__init__()

    def fit(self, X: Series[FeatureT]) -> None: ...

    def transform(self, X: Series[FeatureT]) -> Series[FeatureT]:
        return X
