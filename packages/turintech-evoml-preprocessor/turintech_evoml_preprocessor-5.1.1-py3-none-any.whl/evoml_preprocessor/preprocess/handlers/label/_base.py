"""This module defines an interface for the subset of Preprocessor's
functionality dealing with the label column (label handler)
"""

import logging

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

# Dependencies
import pandas as pd

# Private dependencies
from evoml_api_models.builder import get_builder  # type: ignore

# Module
from evoml_preprocessor.preprocess.models import (
    Block,
    ColumnInfo,
    ColumnOptions,
    ImputeStrategy,
    PreprocessConfig,
)
from evoml_preprocessor.preprocess.models.report import FeatureReport, TransformationBlock
from evoml_preprocessor.preprocess.transformers.type_aliases import LabelMapping
from evoml_preprocessor.preprocess.models.enum import AllEncoders, GenericOption

logger = logging.getLogger("preprocessor")

# ──────────────────────────────────────────────────────────────────────────── #


class LabelHandler(ABC):
    """Abstract interface for the methods preprocessing the label column"""

    def __init__(
        self, config: PreprocessConfig, column_info: ColumnInfo, column_options: Optional[ColumnOptions] = None
    ):
        self.name = None
        self.column_names = None
        self.ml_task = config.mlTask
        self.is_timeseries = config.isTimeseries

        self.column_index = column_info.columnIndex
        self.base_type = column_info.baseType
        self.detected_type = column_info.detectedType
        self.metadata = column_info.metadata

        if column_options is not None:
            self.impute_strategy = column_options.imputeStrategy
            self.impute_value = column_options.imputeValue

            if isinstance(column_options.encoder, list):
                self.encoder_slug = column_options.encoder[0]
            else:
                self.encoder_slug = column_options.encoder if column_options.encoder else GenericOption.AUTO

            if isinstance(column_options.scaler, list):
                self.scaler_slug = column_options.scaler[0]
            else:
                self.scaler_slug = column_options.scaler if column_options.scaler else GenericOption.AUTO
        else:
            self.impute_strategy = ImputeStrategy.AUTO
            self.impute_value = None
            self.encoder_slug = GenericOption.AUTO
            self.scaler_slug = GenericOption.AUTO

        self.feature_builder = get_builder(FeatureReport)
        self.block_builder = get_builder(TransformationBlock)

        self.encoded_to_original_map: Dict[str, str] = {}
        self.label_mappings = None
        self.fitted = False

    @abstractmethod
    def _fit_transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Fits and transforms the label column.

        Args:
            label_col (pd.Series): label column to be transformed.

        Returns:
            pd.Series: Transformed label column.
            pd.DataFrame | None: Extra label features (if any).

        """

        raise NotImplementedError()

    @abstractmethod
    def transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Transforms the label column.

        Args:
            label_col (pd.Series): Label column.

        Returns:
            pd.Series: The encoded label column.
            pd.DataFrame | None: Any extra features created from the label column.

        """

        raise NotImplementedError()

    @abstractmethod
    def inverse_transform(self, transformed_label_col: pd.Series) -> pd.Series:
        """Inverse transforms the label column."""
        raise NotImplementedError()

    def fit_transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Fits and transforms the label column.

        Args:
            label_col (pd.Series): label column to be transformed.

        Returns:
            pd.Series: Transformed label column.
            pd.DataFrame | None: Extra label features (if any).

        """
        self.name = label_col.name
        assert self.name is not None
        self.column_names = [self.name]

        self._check_values(label_col)

        encoded_col, extra_label_features = self._fit_transform(label_col)

        self._report()

        self.fitted = True
        return encoded_col, extra_label_features

    def _check_values(self, label_col: pd.Series) -> None:
        # catch value error early, we are unable to proceed if all values in the label column are invalid (null)
        if label_col.isnull().all():
            logger.error("all values in the Label Column are null:  %s", label_col.name)
            raise ValueError("All values in the Label Column are invalid")

    def get_label_mappings(self) -> LabelMapping:
        return self.label_mappings

    def update(self, label_col: pd.Series) -> None:  # pragma: no cover
        """Updates the fitted label data with the given unseen label values.

        Args:
            label_col (pd.Series): unseen values of label.

        """
        pass

    def update_encoded_to_original_map(self, encoded_names: List[str], original_name: str) -> None:
        """Adds the encoded_names to original_name mapping to a map that keeps all
         the encoded to original mappings.

        Args:
            encoded_names (List[str]): The list of the names of the encoded columns,
                generated after encoding the column with the given original name.
            original_name (str): Column name before encoding.

        """
        for encoded_name in encoded_names:
            self.encoded_to_original_map[encoded_name] = original_name

    # ---------------------------- report methods ---------------------------- #
    def _report(self) -> None:
        """Initializes the report for the label column.

        Args:
            label_info (ColumnInfo): label column info.

        """
        self.feature_builder.column_name = self.name
        self.feature_builder.column_index = self.column_index
        self.feature_builder.base_type = self.base_type
        self.feature_builder.detected_type = self.detected_type

        self.block_builder.block_name = Block.TARGET
        self.block_builder.column_names = self.column_names
        self.block_builder.encoder_name = self.encoder_slug
        self.block_builder.impute_strategy = self.impute_strategy

    @property
    def feature_report(self) -> FeatureReport:
        """Returns the feature report for the label column."""
        self.feature_builder.transformation_block = [self.block_builder]
        return self.feature_builder.build()
