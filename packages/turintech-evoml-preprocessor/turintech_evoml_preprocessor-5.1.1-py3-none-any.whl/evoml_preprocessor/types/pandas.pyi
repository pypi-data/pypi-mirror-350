# mypy: ignore-errors
"""Custom stubs for pandas.

@NOTE: mypy complains a lot about valid overrides, but since we're effectively restricting
what is okay and what is not okay for pandas, we ignore all of them.
"""

from __future__ import annotations

import typing

import numpy as np
import numpy.typing as npt
import pandas as pd
from numpy.random import RandomState
from pandas._libs import lib
from pandas._typing import AxisIndex, IgnoreRaise, Level
from pandas.core import indexing
from typing_extensions import Self

import evoml_preprocessor.types.dtype as dtype

# this is expected dtype of raw data entering preprocessor
DtypeT = typing.TypeVar("DtypeT", bound=dtype.Any)

IndexT = typing.TypeVar("IndexT", bound=typing.Hashable)
ColT = typing.TypeVar("ColT", bound=typing.Hashable)

class _LocIndexerSeries(indexing._LocIndexer, typing.Generic[IndexT, DtypeT]):
    # Type of the object returned by 'series.loc' in order to properly type the
    # syntax series.loc[...]

    # Type checking when setting values
    # e.g. series.loc[0.8] = 1  -> only valid for IndexedSeries[float, int]
    def __setitem__(self, key: IndexT, value: DtypeT) -> None: ...

    # @TODO: overload for series.loc[[0, 6]] = 0
    # @TODO: overload for series.loc[:5] = 0

    # Type checking when getting values
    # e.g. series.loc[0.8] = 1  -> only valid for IndexedSeries[float, int]
    def __getitem__(self, key: IndexT) -> DtypeT: ...

    # @TODO: overload for series.loc[[0, 6]]
    # @TODO: overload for series.loc[:5]

class _LocIndexerFrame(indexing._LocIndexer, typing.Generic[IndexT, ColT, DtypeT]):
    # Same as above, type of the object returned by 'df.loc' & 'df.iloc'
    # @mypy: complains about incompatible return types, but this is consistent
    # with pandas logic

    @typing.overload
    def __getitem__(self, key: IndexT) -> IndexedSeries[ColT, DtypeT]: ...  # type: ignore
    @typing.overload
    def __getitem__(self, key: typing.Sequence[IndexT]) -> IndexedDataFrame[ColT, DtypeT]: ...  # type: ignore
    @typing.overload
    def __getitem__(self, key: typing.Tuple[IndexT, ColT]) -> DtypeT: ...  # type: ignore
    @typing.overload
    def __getitem__(self, key: typing.Tuple[typing.Sequence[IndexT], ColT]) -> IndexedSeries[IndexT, DtypeT]: ...  # type: ignore
    @typing.overload
    def __getitem__(self, key: typing.Tuple[IndexT, typing.Sequence[ColT]]) -> IndexedSeries[ColT, DtypeT]: ...  # type: ignore
    @typing.overload
    def __getitem__(
        self, key: typing.Tuple[typing.Sequence[IndexT], typing.Sequence[ColT]]
    ) -> IndexedDataFrame[IndexT, DtypeT]: ...
    @typing.overload
    def __getitem__(self, key: typing.Tuple[slice, ColT]) -> IndexedSeries[IndexT, DtypeT]: ...

# @typing: we're overwriting the valid dtypes for a series here, since it's difficult to provide
# a set that works nicely with both pandas and numpy. See `dtype.py`
class Series(pd.Series[DtypeT]):

    # See the _LocIndexerSeries class for the type of the 'loc' attribute
    @property
    def loc(self) -> _LocIndexerSeries[typing.Hashable, DtypeT]: ...  # type: ignore

    # The '.iloc' attribute is properly typed by the pandas stubs as far as I
    # know, we can extend the typing if needed

    @property
    def dtype(self) -> DtypeT: ...  # type: ignore

    # Return our internal wrapper around DataFrame typing
    def to_frame(self, name: typing.Hashable = lib.no_default) -> DataFrame[DtypeT]: ...

    # Return our internal wrapper around Series typing
    def astype(self, dtype: DtypeT, copy: bool = ..., errors: IgnoreRaise = ...) -> Series[DtypeT]: ...  # type: ignore

    # Return our internal wrapper for `where`
    def where(  # type: ignore
        self,
        cond: (
            Series[DtypeT]
            | Series[dtype.Bool]
            | np.ndarray
            | typing.Callable[[Series[DtypeT]], Series[dtype.Bool]]
            | typing.Callable[[DtypeT], bool]
        ),
        other=...,
        *,
        inplace: bool = ...,
        axis: AxisIndex | None = ...,
        level: Level | None = ...,
        try_cast: bool = ...,
    ) -> Series[DtypeT]: ...
    # overrides parent by recasting output type
    def isnull(self) -> Series[dtype.Bool]: ...  # type: ignore
    def sample(  # type: ignore
        self,
        n: int | None = ...,
        frac: float | None = ...,
        replace: bool = ...,
        weights: str | typing.List | np.ndarray | None = ...,
        random_state: RandomState | None = ...,
        axis: AxisIndex | None = ...,
        ignore_index: bool = ...,
    ) -> Series[DtypeT]: ...

    # Preserve typing from pandas to numpy (no typecasting)
    # @TODO: add more `to_numpy` casts as needed.
    # @mypy: ignore overload errors, we decide what types we want to support here.
    @typing.overload  # type: ignore
    def to_numpy(
        self: Series[dtype.Float64], dtype: None = ..., copy: bool = ..., na_value: object = ..., **kwargs: typing.Any
    ) -> npt.NDArray[np.float64]: ...
    @typing.overload
    def to_numpy(
        self: Series[dtype.Int64], dtype: None = ..., copy: bool = ..., na_value: object = ..., **kwargs: typing.Any
    ) -> npt.NDArray[np.int64]: ...
    @typing.overload
    def to_numpy(
        self: Series[dtype.String], dtype: None = ..., copy: bool = ..., na_value: object = ..., **kwargs: typing.Any
    ) -> npt.NDArray[np.str_]: ...

    # Pandas to numpy with typecasting
    # @TODO: add more `to_numpy` casts as needed.
    # @pyright: ignore inheritance errors, we decide what types we want to support here.
    @typing.overload
    def to_numpy(  # type: ignore
        self, dtype: np.float64, copy: bool = ..., na_value: object = ..., **kwargs: typing.Any
    ) -> npt.NDArray[np.float64]: ...

    # -------------------------------------------------- operations -------------------------------------------------- #
    # Additions & substractions are implemented for right-hand only (__radd__,
    # ...) but we need to type the generic operation for it to show up when
    # using the symbol syntax (eg. 'a + b')

    # Addition '+'
    # Special case for int/float that are compatible
    @typing.overload
    def __add__(
        self: Series[dtype.Float64] | Series[dtype.Int64], other: Series[dtype.Int64] | Series[dtype.Float64]
    ) -> Series[dtype.Float64]: ...
    @typing.overload
    def __add__(self, other: DtypeT | Series[DtypeT]) -> Self: ...
    @typing.overload  # Type ignore on the last occurence as it's not in the class
    def __add__(self, other: Series[typing.Any]) -> Series[typing.Any]: ...  # type: ignore

    # Subtraction '-'
    @typing.overload  # Special case for int/float that are compatible
    def __sub__(
        self: Series[dtype.Float64] | Series[dtype.Int64], other: Series[dtype.Int64] | Series[dtype.Float64]
    ) -> Series[dtype.Float64]: ...
    @typing.overload
    def __sub__(self, other: DtypeT | Series[DtypeT]) -> Self: ...
    @typing.overload
    def __sub__(self, other: Series[typing.Any]) -> Series[typing.Any]: ...  # type: ignore

    # @pyright: ignore typing errors in favour for internal `DtypeT` definition
    # LT comparison '<'
    def __lt__(self, other: DtypeT | Series[DtypeT]) -> Series[dtype.Bool]: ...  # type: ignore
    # GT comparison '>'
    def __gt__(self, other: DtypeT | Series[DtypeT]) -> Series[dtype.Bool]: ...  # type: ignore
    # LE comparison '<='
    def __le__(self, other: DtypeT | Series[DtypeT]) -> Series[dtype.Bool]: ...  # type: ignore
    # LE comparison '>='
    def __ge__(self, other: DtypeT | Series[DtypeT]) -> Series[dtype.Bool]: ...  # type: ignore

    # invert operator '~'
    def __invert__(self: Series[DtypeT]) -> Series[DtypeT]: ...

class IndexedSeries(Series[DtypeT], typing.Generic[IndexT, DtypeT]):
    # Does the same as series but injects the type of the index whenever possible

    index: pd.Index[IndexT]  # type: ignore

    def to_frame(self, name: typing.Hashable = lib.no_default) -> IndexedDataFrame[IndexT, DtypeT]: ...
    @property
    def loc(self) -> _LocIndexerSeries[IndexT, DtypeT]: ...  # type: ignore
    def items(self) -> typing.Iterable[typing.Tuple[IndexT, DtypeT]]:
        return super().items()  # type: ignore

class DataFrame(pd.DataFrame, typing.Generic[DtypeT]):

    # For loc and iloc, we assume that column names are always string. Pandas
    # allows non-string, but we never want that.
    @property
    def loc(self) -> _LocIndexerFrame[typing.Hashable, str, DtypeT]: ...  # type: ignore
    @property
    def iloc(self) -> _LocIndexerFrame[int, int, DtypeT]: ...  # type: ignore

    # Re-type the direct access 'df[...]'
    @typing.overload
    def __getitem__(self, key: typing.List[str]) -> IndexedDataFrame[typing.Hashable, DtypeT]: ...
    @typing.overload
    def __getitem__(self, key: str) -> IndexedSeries[typing.Hashable, DtypeT]: ...  # type: ignore

class IndexedDataFrame(DataFrame[DtypeT], typing.Generic[IndexT, DtypeT]):
    index: pd.Index[IndexT]  # type: ignore

    @property
    def loc(self) -> _LocIndexerFrame[IndexT, str, DtypeT]: ...  # type: ignore

    # The property 'iloc' is properly typed in our internal 'DataFrame' (it's
    # independant of index type)

    # Re-type the direct access 'df[...]'
    @typing.overload
    def __getitem__(self, key: typing.List[str]) -> IndexedDataFrame[IndexT, DtypeT]: ...
    @typing.overload
    def __getitem__(self, key: str) -> IndexedSeries[IndexT, DtypeT]: ...  # type: ignore

    # Possible extensions
    # - add, sub, ...

AnySeries = (
    Series[dtype.Float64]
    | Series[dtype.Int64]
    | Series[dtype.Int8]
    | Series[dtype.Bool]
    | Series[dtype.String]
    | Series[dtype.DateTime64]
)
AnyDataFrame = (
    DataFrame[dtype.Float64]
    | DataFrame[dtype.Int64]
    | DataFrame[dtype.Int8]
    | DataFrame[dtype.Bool]
    | DataFrame[dtype.String]
    | DataFrame[dtype.DateTime64]
)
SeriesTarget = Series[dtype.Float64] | Series[dtype.Int64]
