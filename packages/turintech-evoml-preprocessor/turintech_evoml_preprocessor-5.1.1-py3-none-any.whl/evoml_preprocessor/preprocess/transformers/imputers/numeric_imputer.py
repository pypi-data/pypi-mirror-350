from __future__ import annotations

from typing import Callable, Dict, Optional, TypeVar

import pandas as pd

from evoml_preprocessor.preprocess.models import ImputeStrategy
from evoml_preprocessor.preprocess.transformers.imputers._base import Imputer
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import Series

MAX_ROWS_CONSIDERED = 1000


NumericT = TypeVar("NumericT", bound=dtype.Numeric)


class NumericImputer(Imputer[NumericT, NumericT]):
    """Imputer class for handling missing numeric values."""

    # @mypy mean/median not implemented for our pandas typing stubs
    strategy_func_map: Dict[ImputeStrategy, Callable[[Series[NumericT]], NumericT]] = {
        ImputeStrategy.MEAN: pd.DataFrame.mean,  # type: ignore
        ImputeStrategy.MEDIAN: pd.DataFrame.median,  # type: ignore
        ImputeStrategy.MOST_FREQUENT: lambda df: df.mode().iloc[0],
    }  # type: ignore

    def __init__(self, strategy: ImputeStrategy, fill_value: NumericT):
        """
        Initialize the NumericImputer.

        Args:
            strategy (ImputeStrategy): The impute strategy for handling missing values.
            fill_value: The value to fill missing values with.
        """
        super().__init__()
        self.strategy = strategy
        self.value = fill_value
        self.dtype: Optional[NumericT] = None

    def get_value(self, X: Series[NumericT]) -> NumericT:
        sample = X.sample(min(MAX_ROWS_CONSIDERED, len(X)))
        return self.strategy_func_map[self.strategy](sample) if self.strategy in self.strategy_func_map else self.value

    def fit(self, X: Series[NumericT]) -> None:
        self.dtype = X.dtype
        self.value = self.get_value(X)

    def transform(self, X: Series[NumericT]) -> Series[NumericT]:
        # this is a bit of a hacky fix to ensure that the typing for transform is consistent
        # with the typing for fit_transform

        # @pyright: no fillna implemented for our series implementation
        result: Series[NumericT] = X.fillna(self.value)  # type: ignore

        assert self.dtype is not None, "`dtype` should not be None, has `fit` been called?"
        if X.dtype != self.dtype:
            result = result.astype(self.dtype)

        if pd.isna(self.value):  # type: ignore
            raise ValueError("Impute value is NaN after fitting. Please check your data.")

        return result
