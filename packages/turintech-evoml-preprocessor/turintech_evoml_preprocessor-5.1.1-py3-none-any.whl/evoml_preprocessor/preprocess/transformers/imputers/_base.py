from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import Series

FeatureT = TypeVar("FeatureT", bound=dtype.Any)
CleanT = TypeVar("CleanT", bound=dtype.Any)


class Imputer(ABC, Generic[FeatureT, CleanT]):
    def __init__(self):
        self.value = None
        self.imputer = None

    @abstractmethod
    def fit(self, X: Series[FeatureT]) -> None:
        """
        Fit the imputer on the data.

        Args:
            X (pd.Series):
                Input data to be imputed.

        Returns:
            None
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, X: Series[FeatureT]) -> Series[CleanT]:
        """
        Fit the imputer on the data and transform the data.

        Args:
            X (pd.Series):
                Input data to be imputed.

        Returns:
            X' (pd.Series):
                Imputed version of the input data.
        """
        raise NotImplementedError

    def fit_transform(self, X: Series[FeatureT]) -> Series[CleanT]:
        """
        Fit the imputer on the data and transform the data.

        Args:
            X (pd.Series):
                Input data to be imputed.

        Returns:
            X' (pd.Series):
                Imputed version of the input data.
        """
        self.fit(X)
        return self.transform(X)
