from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget

FeatureT = TypeVar("FeatureT", bound=dtype.Any)
NumericT = TypeVar("NumericT", bound=dtype.Numeric)


class Encoder(ABC, Generic[FeatureT, NumericT]):
    """Base class for encoders

    @TODO: strictly, different encoders expect different types of inputs.
    We should consider separating the categorical and numeric encoders.
    """

    @abstractmethod
    def fit(self, X: Series[FeatureT], y: Optional[SeriesTarget] = None) -> None:
        """Fit the encoder to the data.

        Args:
            X (Series):
                Input data to be encoded.
            y (Series, optional):
                Target labels.
        """
        ...

    @abstractmethod
    def transform(self, X: Series[FeatureT]) -> DataFrame[NumericT]:
        """Transform the data.

        Args:
            X (Series):
                Input data to be encoded.

        Returns:
            Series:
                Encoded version of the input data.
        """
        ...

    def fit_transform(self, X: Series[FeatureT], y: Optional[SeriesTarget] = None) -> DataFrame[NumericT]:
        """Fit the encoder to the data and transform the data.

        Args:
            X (Series):
                Input data to be encoded.
            y (Series, optional):
                Target labels. Default is None.

        Returns:
            Series:
                Encoded version of the input data.
        """
        self.fit(X, y)
        return self.transform(X)
