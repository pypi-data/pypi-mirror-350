from __future__ import annotations

from abc import ABC, abstractmethod

from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame


class Scaler(ABC):
    """
    Abstract base class for scalers.

    Subclasses of Scaler must implement the fit_transform, fit, and transform methods.
    """

    @abstractmethod
    def fit(self, X: DataFrame[dtype.Float64]) -> None:
        """
        Fit the scaler to the data.

        Args:
            X (DataFrame): The input data to fit the scaler.

        Returns:
            None
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, X: DataFrame[dtype.Float64]) -> DataFrame[dtype.Float64]:
        """
        Transform the data using the fitted scaler.

        Args:
            X (DataFrame): The input data to transform.

        Returns:
            DataFrame: The transformed data.
        """
        raise NotImplementedError

    def fit_transform(self, X: DataFrame[dtype.Float64]) -> DataFrame[dtype.Float64]:
        """
        Fit the scaler to the data and transform the data.

        Args:
            X (DataFrame): The input data to fit and transform.

        Returns:
            DataFrame: The transformed data.
        """
        self.fit(X)
        return self.transform(X)
