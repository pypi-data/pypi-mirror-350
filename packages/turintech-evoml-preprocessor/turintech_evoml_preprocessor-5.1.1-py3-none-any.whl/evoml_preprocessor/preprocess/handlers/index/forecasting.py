"""Implements the processing of index columns for forecasting task"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional, Union, Dict, Any

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType, MlTask
from evoml_utils.convertors.detected_types import to_datetime_column, to_int_column
from evoml_utils.convertors import type_to_convert_function
from pandas.api.types import is_datetime64_any_dtype as is_datetime

# Module
from evoml_preprocessor.preprocess.handlers.index._base import IndexHandler
from evoml_preprocessor.preprocess.models import ColumnInfo
from evoml_preprocessor.preprocess.transformers.type_aliases import Converter

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class ForecastingIndexHandler(IndexHandler):
    """This class provides methods to fit and transform index columns for time
    series.
    """

    DEFAULT_NAME = "DefaultIndex"

    def __init__(self, ml_task: MlTask):
        super().__init__(ml_task)
        # Values used for transform that will be set in fit_transform
        self._converter: Optional[Converter] = None  # function used to convert index to the desired type
        self.index_name: Optional[str] = None
        self.start = 0  # Will be used if no index
        self.metadata: Optional[Dict[str, Union[str, Dict[str, Union[str, bool]]]]] = None
        self.to_datetime_kwargs: Optional[Dict[str, Union[str, bool]]] = None

    def fit_transform(
        self,
        index_col: Optional[pd.Series],
        index_info: Optional[ColumnInfo],
        index_size: Optional[int] = None,
    ) -> pd.Series:
        """Fits and transforms the index column. If index_info and index_col
        are given, the method returns the index_col, converted to the detected
        type if needed, and updates converter, converter_metadata, which will
        be used by transform method. Otherwise, it returns a default index
        column with range(0, index_size) and updates start such that
        transform method will continue from the current point.

        Args:
            index_info:
                Column info for index.
            index_col:
                Index column. If None, a default index column will be created.
            index_size:
                Size of index column. If index_col is given, this is ignored.
        Returns:
             pd.Series:
                The converted index_col if it is given or a new default index column.
        """

        logger.info(" Index Column Transformation ".center(60, "-"))

        if not (index_col is not None and index_info) and not index_size:
            logger.error("No index column and no index size were given.")
            raise ValueError("This method requires either (index_col & index_info) or index_size")

        if index_col is None:  # ⇒ index_size != None
            assert index_size is not None
            # Without index col, we use the index_size to generate an index
            index_col = pd.Series(
                range(self.start, index_size + self.start),
                name=self.DEFAULT_NAME,
            )
            self.start += index_size  # update start for transform
            self.fitted = True
            self.index_name = str(index_col.name)
            logger.info(f"→ created {self.DEFAULT_NAME} column")
            # @pyright: there is a mismatch between the Converter and TypeConverter types defined in utils and preprocessor
            self._converter = type_to_convert_function(DetectedType.integer)  # type: ignore
            return index_col

        # We can report if there's an existing index
        if index_info is None:
            raise ValueError("Index info must be provided if the index column is provided.")
        # We can report if there's an existing index
        self.index_name = index_info.name
        self.feature_builder.column_name = index_info.name
        self.feature_builder.column_index = index_info.columnIndex
        self.feature_builder.detected_type = index_info.detectedType
        self.metadata = index_info.metadata

        index_type = index_info.detectedType
        if index_type == DetectedType.integer:
            self._converter = to_int_column
            transformed_col = self.converter(index_col)
        elif index_type == DetectedType.datetime:
            if index_info.metadata is None:
                raise ValueError("Conversion metadata must be provided for datetime indexes.")
            self.metadata = index_info.metadata
            self._converter = to_datetime_column
            self.to_datetime_kwargs = self.metadata["to_datetime_kwargs"]
            transformed_col = self.converter(index_col, **self.to_datetime_kwargs)
        else:
            raise ValueError(f"Not valid index type: {index_type}")

        # check if index column has missing values
        if transformed_col.isnull().any():
            raise ValueError("Index column contains missing values.")

        # check if all values are unique
        if transformed_col.nunique() / len(transformed_col) != 1:
            raise ValueError("Index column contains duplicated values.")

        # index checks specific for forecasting
        # evenly spaced dates
        if is_datetime(transformed_col) and not pd.infer_freq(pd.Index(transformed_col)):
            raise ValueError("DateTime index column not evenly spaced.")

        # consecutive integers
        if transformed_col.dtype == "int64":
            index_start_from_0 = transformed_col - transformed_col.iloc[0]
            index_len = len(transformed_col)
            if not index_start_from_0.equals(pd.Series(range(index_len), index=transformed_col.index)):
                raise ValueError("Integer index column not evenly spaced with spacing 1.")

        self.fitted = True

        logger.info(f"- name: {index_info.name}")
        logger.info(f"- type: {index_type}")

        return transformed_col

    def transform(self, index_col: Optional[pd.Series], index_size: Optional[int] = None) -> pd.Series:
        """Transforms the index column. If index_col is given, returns
         the index_col, converted to the detected type, using the converter and
         converter metadata. Otherwise, it returns a default index column with
         range(start, index_size).

        Args:
            index_col:
                The index column.
            index_size:
                Size of index column. If index_col is given, this is ignored.
        Returns:
             pd.Series:
                The converted index_col if it is given or a new default index column.
        """

        if not self.fitted:
            raise ValueError("Index column handler is not fitted.")

        if self.index_name is None and index_col is not None:
            raise ValueError("Index column handler was fitted for the defaultIndex.")

        if self.index_name != self.DEFAULT_NAME and index_col is None:
            raise ValueError(
                f"Index column handler was fitted on {self.index_name} but no column is given for transform."
            )

        if index_col is None and index_size is None:
            raise ValueError("Transform method requires index size or index column.")

        if index_col is None:
            if index_size is None:
                raise ValueError("Index size must be provided if no index column is given.")
            return pd.Series(
                range(self.start, self.start + index_size),
                name=self.DEFAULT_NAME,
            )

        try:
            if self.to_datetime_kwargs is not None:
                transformed_col = self.converter(index_col, **self.to_datetime_kwargs)
            else:
                transformed_col = self.converter(index_col)
        except:
            raise ValueError(f"Transform method was given an invalid index column.")

        # check if index column has missing values
        if transformed_col.isnull().any():
            raise ValueError("Index column contains missing values.")

        # check if all values are unique
        if transformed_col.nunique() / len(transformed_col) != 1:
            raise ValueError("Index column contains duplicated values.")

        return transformed_col

    @property
    def converter(self) -> Converter:
        if self._converter is None:
            raise AttributeError("The converter must be initialized during fitting.")
        return self._converter
