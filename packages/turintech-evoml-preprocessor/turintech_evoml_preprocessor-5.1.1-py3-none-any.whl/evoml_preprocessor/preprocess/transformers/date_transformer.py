# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, Dict, List, Optional, Union

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType
from evoml_utils.convertors.detected_types import to_datetime_column

# Module
from evoml_preprocessor.preprocess.models import Block, GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.models.report import TransformationBlock
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class DateTransformer(Transformer):
    """
    Transforms a :class:`pd.DataFrame` single column containing string
    formatted dates, into several columns containing numbers.

    List of the columns created by this method, depending on available
    information::

       ┌─────────────────┬───┬───┬───┬───┬───┬───┬─────────┬──────┐
       │ Column          │ Y │ M │ D │ H │ m │ S │ Range   │ Fill │
       ├─────────────────┼───┼───┼───┼───┼───┼───┼─────────┼──────┤
       │ unix_timestamp  │   │   │   │   │   │   │ [0,+∞)  │  0   │
       │ day_of_week     │ ✗ │ ✗ │ ✗ │   │   │   │ [1,7]   │  0   │
       │ day_of_year     │ ✗ │ ✗ │ ✗ │   │   │   │ [1,366] │  0   │
       │ week_of_year    │ ✗ │ ✗ │ ✗ │   │   │   │ [1,53]  │  0   │
       │ is_weekend      │ ✗ │ ✗ │ ✗ │   │   │   │ {T,F}   │  F   │
       │ quarter         │   │ ✗ │   │   │   │   │ [0,3]   │ -1   │
       │ relative_year   │ ✗ │   │   │   │   │   │ [0,_]   │ -1   │
       │ month           │   │ ✗ │   │   │   │   │ [1,12]  │  0   │
       │ day             │   │   │ ✗ │   │   │   │ [1,31]  │  0   │
       │ hour            │   │   │   │ ✗ │   │   │ [0,23]  │ -1   │
       │ minute          │   │   │   │   │ ✗ │   │ [0,59]  │ -1   │
       │ second          │   │   │   │   │   │ ✗ │ [0,59]  │ -1   │
       ├─────────────────┼───┴───┴───┴───┴───┴───┼─────────┼──────┤
       │ public holidays │    not implemented    │ {T,F}   │  F   │
       └─────────────────┴───────────────────────┴─────────┴──────┘

    The filling value (value if the row is NaN) is false for booleans, and
    the minimal value minus one for numbers.
    """

    date_options: Optional[List[DateOptions]]
    fields: Dict[str, Union[str, bool]]

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
    ) -> None:
        super().__init__(column_info, encoder, scaler, impute_strategy, impute_value, derived_columns)

        if self.metadata is None:
            raise ValueError("Conversion metadata must be provided for the DateTransformer.")

        if "to_datetime_kwargs" in self.metadata:
            self.to_datetime_kwargs = self.metadata.get("to_datetime_kwargs", {})
            format = self.to_datetime_kwargs.get("format")
            if format is None:
                self.fields = {
                    "year": True,
                    "month": True,
                    "day": True,
                    "hour": False,
                    "minute": False,
                    "second": False,
                }
            else:
                self.fields = {
                    "year": "%y" or "%Y" in format,
                    "month": "%m" in format,
                    "day": "%d" in format,
                    "hour": "%H" in format,
                    "minute": "%M" in format,
                    "second": "%S" in format,
                }
        elif "dateTimeOrder" in self.metadata:  # legacy datetime format e.g. "ymdHMS"
            datetime_order = self.metadata["dateTimeOrder"]
            self.to_datetime_kwargs = {"datetime_order": datetime_order}
            self.fields = {
                field: letter in datetime_order
                for field, letter in {
                    "year": "y",
                    "month": "m",
                    "day": "d",
                    "hour": "H",
                    "minute": "M",
                    "second": "S",
                }.items()
            }
            if datetime_order == "":
                self.fields.update({"year": True, "month": True, "day": True})
        else:
            raise ValueError(f"Could not find datetime format in {self.metadata}")

        self.min_year: Optional[int] = None  # set in fit to be used by transform
        self.min_timestamp: Optional[float] = None  # set in fit to be used by transform
        self.selected_columns: Optional[List[str]] = None

        # impute
        self.impute_setting = DetectedType.datetime

        # scaler
        self.scaler = None

    def _init_operations(self, data: pd.Series[Any]) -> None:
        if self.encoder_slug == GenericOption.NONE:
            self.scaler_slug = GenericOption.NONE
        else:
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data

        dates = to_datetime_column(data, **self.to_datetime_kwargs)

        if not pd.api.types.is_datetime64_any_dtype(dates):
            raise ValueError(f"Date column {dates.name} type mismatch (check utils conversion)")

        return dates

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series] = None) -> NumericArray:
        if isinstance(data, pd.DataFrame):
            raise NotImplementedError("This encoder has not yet been implemented for DataFrame input.")

        if self.encoder_slug == GenericOption.NONE:
            return data.to_frame()

        data_df = self.split_date_column(data)
        return data_df

    def split_date_column(self, dates: pd.Series[Any]) -> pd.DataFrame:
        """Split the date column into multiple columns based on the datetime order.

        Args:
            dates (pd.Series): The series containing the dates to split.

        Returns:
            pd.DataFrame: A DataFrame containing the split date columns.
        """

        if not pd.api.types.is_datetime64_any_dtype(dates):
            raise TypeError("The input must be of datetime64 type.")

        if self.min_timestamp is None or self.min_year is None:
            self.min_timestamp = dates.min().timestamp()
            self.min_year = dates.dt.year.min()

        self.date_options = self.date_options or [DateOptions.UNIX_TIMESTAMP]

        transformed = {
            f"{self.name}_{option.value.replace('-', '_')}": self.compute_transformed_column(dates, option)
            for option in self.date_options
        }

        result = pd.DataFrame(transformed, index=dates.index)

        # Drop unary value columns
        if self.selected_columns is None:
            result = result.loc[:, result.nunique() > 1]
            self.selected_columns = list(result.columns)
        else:
            result = result[self.selected_columns]

        self.columns = result.columns.tolist()
        return result

    def compute_transformed_column(self, dates: pd.Series[Any], option: DateOptions) -> pd.Series[Any]:
        """Compute the transformed column based on the specified option.

        Args:
            dates (pd.Series): The series containing the dates.
            option (DateOptions): The specific date option to compute.

        Returns:
            pd.Series: The computed transformed column.
        """
        if option == DateOptions.UNIX_TIMESTAMP:
            if self.min_timestamp is None:
                raise ValueError("Min timestamp should be set.")
            return (dates.astype(np.int64) // 10**9) - self.min_timestamp
        elif option == DateOptions.DAY_OF_WEEK:
            return dates.dt.dayofweek
        elif option == DateOptions.DAY_OF_YEAR:
            return dates.dt.dayofyear
        elif option == DateOptions.WEEK_OF_YEAR:
            return dates.dt.isocalendar().week.astype(np.float64)
        elif option == DateOptions.IS_WEEKEND:
            return dates.dt.dayofweek > 5
        elif option == DateOptions.QUARTER:
            return (dates.dt.month - 1) // 3
        elif option == DateOptions.RELATIVE_YEAR:
            if self.min_year is None:
                raise ValueError("Min year should be set.")
            return dates.dt.year - self.min_year
        elif option == DateOptions.MONTH:
            return dates.dt.month
        elif option == DateOptions.DAY:
            return dates.dt.day
        elif option == DateOptions.HOUR and self.fields.get("hour"):
            return dates.dt.hour
        elif option == DateOptions.MINUTE and self.fields.get("minute"):
            return dates.dt.minute
        elif option == DateOptions.SECOND and self.fields.get("second"):
            return dates.dt.second

        return pd.Series()

    def _report(self) -> None:
        self.transformation_block.append(
            TransformationBlock(
                block_name=Block.DATE,
                encoder_name=None,
                scaler_name=self.scaler_slug,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )
