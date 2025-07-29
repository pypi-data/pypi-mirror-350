from __future__ import annotations

from typing import List, Optional, TypeVar

from evoml_preprocessor.preprocess.models import GenericOption
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget

AnyT = TypeVar("AnyT", bound=dtype.Any)
NumericT = TypeVar("NumericT", bound=dtype.Numeric)


class IdentityEncoder:
    """The identity encoder only ensures the correct typing of the output

    Since the expectation of the output is numeric, the identity encoder
    is not equipped to handle non-numeric input
    """

    columns: List[str]

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__()
        self.name = str(name)
        self.columns = [self.name]
        self.slug = GenericOption.NONE

    def fit(self, X: Series[AnyT], y: Optional[SeriesTarget] = None) -> None: ...

    def transform(self, X: Series[AnyT]) -> DataFrame[AnyT]:
        # @TODO: this should be handled better, see parent note
        #   1. What does it mean to perform this operation on a non-numeric series?
        #   2. Should we consider non-numeric models as targets in this framework?
        return X.to_frame()

    def fit_transform(self, X: Series[AnyT], y: Optional[SeriesTarget] = None) -> DataFrame[AnyT]:
        self.fit(X, y)
        return self.transform(X)
