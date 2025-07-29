from __future__ import annotations

import logging
from typing import TypeVar, Any

from evoml_preprocessor.preprocess.models import ImputeStrategy
from evoml_preprocessor.preprocess.transformers.imputers._base import Imputer
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import Series

logger = logging.getLogger("preprocessor")

NumericT = TypeVar("NumericT", bound=dtype.Numeric)


class TimeseriesImputer(Imputer):
    """
    Imputer class for handling missing values in timeseries data.
    """

    def __init__(self, impute_strategy: ImputeStrategy, value: Any):
        """
        Initialize the TimeseriesImputer.

        Args:
            impute_strategy (ImputeStrategy): The impute strategy for handling
            missing values.
            value (Any): The value used to impute missing values remaining after the strategy has been applied.
        """
        super().__init__()
        self.impute_strategy = impute_strategy
        self.lag = 5
        self.value = value

    def fit(self, X: Series[NumericT]) -> None: ...

    def transform(self, X: Series[NumericT]) -> Series[NumericT]:
        """
        Transform the data by imputing missing values.

        @NOTE: there are a lot of type ignores in this method, where we haven't
        added type hints for various pandas functions with our own type stubs,
        particularly ones that just create a copy like Series[A] -> Series[A]

        Args:
            X (pd.Series):
                Input data to be imputed.

        Returns:
            X' (pd.Series):
                Imputed version of the input data.
        """

        if self.impute_strategy == ImputeStrategy.FORWARD_FILL:
            return X.ffill().fillna(value=self.value)  # type: ignore

        if self.impute_strategy == ImputeStrategy.BACKWARD_FILL:
            return X.bfill().fillna(value=self.value)  # type: ignore

        if self.impute_strategy == ImputeStrategy.POLYNOMIAL_INTERPOLATE:
            X_ = X.interpolate(method="polynomial", order=2).fillna(value=self.value)
            assert X_ is not None
            return X_  # type: ignore

        if self.impute_strategy == ImputeStrategy.LINEAR_INTERPOLATE:
            X_ = X.interpolate(method="linear", limit_direction="both").fillna(value=self.value)
            assert X_ is not None
            return X_  # type: ignore

        if self.impute_strategy == ImputeStrategy.SPLINE_INTERPOLATE:
            X_ = X.interpolate(method="spline", order=2).fillna(value=self.value)
            assert X_ is not None
            return X_  # type: ignore

        if self.impute_strategy == ImputeStrategy.MOVING_AVERAGE:
            return X.rolling(self.lag, center=True, min_periods=1).mean().fillna(value=self.value)  # type: ignore

        logger.error(f"Timeseries impute strategy {self.impute_strategy} was not performed on {X.name}")

        return X
