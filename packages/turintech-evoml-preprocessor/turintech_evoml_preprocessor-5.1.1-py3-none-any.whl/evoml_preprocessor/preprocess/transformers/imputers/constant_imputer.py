from __future__ import annotations

from typing import TypeVar

from evoml_preprocessor.preprocess.models import ImputeValue
from evoml_preprocessor.preprocess.transformers.imputers._base import Imputer
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import Series

FeatureT = TypeVar("FeatureT", bound=dtype.Any)


class ConstantImputer(Imputer[FeatureT, FeatureT]):
    def __init__(self, value: ImputeValue):
        super().__init__()
        self.value = value

    def fit(self, X: Series[FeatureT]) -> None:
        pass

    def transform(self, X: Series[FeatureT]) -> Series[FeatureT]:
        # ensure column type and fill type is consistent
        if X.dtype == object and type(self.value) not in [str, dict]:
            self.value = str(self.value)

        return X.where(~X.isnull(), other=self.value)
