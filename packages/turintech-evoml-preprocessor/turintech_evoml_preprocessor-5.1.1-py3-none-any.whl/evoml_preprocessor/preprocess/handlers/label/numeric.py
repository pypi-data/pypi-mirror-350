"""Implements the processing of numeric label columns"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional, Tuple, Dict, Any

import numpy as np

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType
import evoml_utils.convertors as convertors

# Module
from evoml_preprocessor.preprocess.handlers.label._base import LabelHandler
from evoml_preprocessor.preprocess.models import ColumnInfo, ColumnOptions, ImputeStrategy, PreprocessConfig
from evoml_preprocessor.preprocess.transformers.imputers.utils import init_imputer
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")

# Static constants
SKEWNESS_THRESHOLD = conf_mgr.preprocess_conf.SKEWNESS_THRESHOLD
# ──────────────────────────────────────────────────────────────────────────── #


class NumericLabelHandler(LabelHandler):
    """This class provides methods to fit and transform numerical label columns"""

    def __init__(
        self, config: PreprocessConfig, column_info: ColumnInfo, column_options: Optional[ColumnOptions] = None
    ):
        super().__init__(config, column_info, column_options)

        self.converter = None
        self.converter_metadata: Dict[str, Any] = {}
        self.imputer = None

        # TODO: remove label mapping
        self.label_mappings = [0, 0]

        # set defaults
        if self.impute_strategy == ImputeStrategy.AUTO:
            if self.is_timeseries:
                self.impute_strategy = ImputeStrategy.FORWARD_FILL
            else:
                self.impute_strategy = ImputeStrategy.MEDIAN

    def _fit_transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Finds and sets private attributes needed for the transformation of
        the label column.

        We only convert and impute numeric columns - no encoding is performed
        """
        # convert
        label_col = self._convert(label_col)

        # impute
        self.imputer, self.impute_strategy, self.impute_value = init_imputer(
            detected_type=self.detected_type,
            strategy=self.impute_strategy,
            value=self.impute_value,
            metadata=self.converter_metadata,
            column=label_col,
        )

        # TODO: resolve typing issue. This is fine because
        # label transform is always 1->1, but the general imputer
        # is n->m
        label_col = self.imputer.fit_transform(label_col)

        self.fill_value = self.imputer.value

        return label_col, None

    def transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Applies the transformation as determined by the `fit` (or
        `fit_transform`) method.
        """
        # @TODO: implement this interface as mutating the `label_col` argument
        # to optimise memory usage
        # → change the converter functions to either have an optional `inplace`
        # argument, or to always mutate the given series.
        if not self.fitted:
            raise ValueError("Call `fit_transform` before calling this method")

        # convert
        elif self.converter is not None:
            label_col = self.converter(label_col, **self.converter_metadata)

        # TODO: resolve typing issue. This is fine because
        # label transform is always 1->1, but the general imputer
        # is n->m
        assert self.imputer is not None
        label_col = self.imputer.transform(label_col)
        return label_col, None

    def _convert(self, label_col: pd.Series) -> pd.Series:
        label_col.replace([np.inf, -np.inf], np.nan, inplace=True)

        converters_dict = {
            DetectedType.integer: convertors.detected_types.to_int_column,
            DetectedType.float: convertors.detected_types.to_float_column,
            DetectedType.currency: convertors.detected_types.convert_currency_column,
            DetectedType.fraction: convertors.detected_types.convert_fraction_column,
            DetectedType.percentage: convertors.detected_types.convert_percentage_column,
        }

        if self.detected_type in converters_dict:
            self.converter = converters_dict[self.detected_type]
            label_col = self.converter(label_col)
        elif self.detected_type == DetectedType.unit_number:
            self.converter = convertors.detected_types.convert_unit_number_column
            if self.metadata is None:
                raise AttributeError("Conversion metadata must be supplied for the unit type.")
            self.converter_metadata = self.metadata
            label_col = self.converter(label_col, **self.converter_metadata)
        elif self.detected_type in [DetectedType.categorical, DetectedType.binary]:
            self._process_classifier_data(label_col)
        else:
            raise ValueError(f"Unsupported type for target column: {self.detected_type}")

        return label_col

    def _process_classifier_data(self, label_col: pd.Series) -> None:
        logger.warning(
            f"Target column type is {self.detected_type}. We advise you to use a numeric "
            f"target column for a {self.ml_task} problem. Otherwise, please consider "
            "using classification problem type."
        )
        if not pd.api.types.is_numeric_dtype(label_col):
            raise ValueError(
                f"Target column type needs to be numeric for a {self.ml_task} "
                f"problem but it is {self.detected_type}."
            )

    def inverse_transform(self, transformed_label_col: pd.Series) -> pd.Series:
        return transformed_label_col
