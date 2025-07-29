# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Dict, List, Set, Tuple, Union

# Dependencies
import pandas as pd
import numpy as np

# Private Dependencies
from evoml_api_models import DetectedType
from sklearn.feature_selection import VarianceThreshold

# Module
from evoml_preprocessor.preprocess.handlers.data_preparation._base import DataPreparationHandler
from evoml_preprocessor.preprocess.models import (
    ColumnInfo,
    ConfigOptions,
    FeatureSelectionOptions,
    PreprocessConfig,
    ReasonDropped,
    SelectionMethod,
    SelectionMetric,
)
from evoml_preprocessor.preprocess.models.report import FeatureReport
from evoml_preprocessor.preprocess.selector.selector_chain import SelectorChain
from evoml_preprocessor.preprocess.selector.util import calculate_number_features
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")

CONF = conf_mgr.preprocess_conf  # Alias for readability
# ──────────────────────────────────────────────────────────────────────────── #


class DefaultDataPreparationHandler(DataPreparationHandler):
    """The default data preparation handler.
    This stage is only applied for large datasets. For small datasets, the data preparation stage is skipped.
    This stage helps to reduce the number of features and the number of rows in the dataset.
    """

    def __init__(self, config: PreprocessConfig, info_map: Dict[str, ColumnInfo], config_options: ConfigOptions):
        super().__init__(config, info_map, config_options)

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """
        The steps implemented are:
            1) stage 1: filter unwanted columns
            2) stage 2: filter columns with unique traits:
                1) correlation with target is low and we have a high number of missing values
                2) correlation with target = 1
            3) stage 3: filter columns based on variance threshold and correlation
            4) stage 4: apply feature selection QPFS
        """

        logger.info(" Start Data Preparation ".center(60, "-"))
        logger.info(f"Initial number of features: {data.shape[1]}")

        label_name = str(encoded_label.name)

        # identify required columns and exclude them from data preparation process
        # split X = [X, required_col_slice]
        data, required_col_slice = self.get_required_column_slice(label_name, data, self.required_column_names)

        # stage 1: filter unwanted columns
        # Check each column as per the defined criteria and register as dropped
        # Note: we only append column names to self.removed_cols
        removed_columns = self.stage1_filter_unwanted_columns(label_name)
        data = self.update_dropped_columns(removed_columns, data)

        # Rejoin the required columns (if there were any)
        if self.required_column_names:
            data = pd.concat([data, required_col_slice], axis=1)

        # -------------------------- safety checks --------------------------- #
        assert len(self.removed_cols) == len(self.reports)

        logger.info(f"Features after data preparation {data.shape[1]}")

        self.fitted = True
        return data

    def get_required_column_slice(
        self, label_name: str, X: pd.DataFrame, required_feature_names: List
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Exclude required columns from X"""
        if label_name in X.columns:
            required_feature_names.append(label_name)

        required_col_slice = pd.DataFrame(index=X.index)
        if required_feature_names:
            required_col_slice = X.loc[:, required_feature_names]
            X.drop(required_feature_names, axis=1, inplace=True)
        return X, required_col_slice

    def stage1_filter_unwanted_columns(self, label_name: str) -> Dict:
        """Stage 1: filter columns based on user options and type detection"""
        removed_columns = {}
        for col_info in self.info_map.values():
            # aliases for code readability
            _name, _index = col_info.name, col_info.columnIndex

            # column specified as required by the user
            if _index in self.required_features_idx:
                continue

            # ignore unary dropped columns and label column
            if _name == label_name:
                continue

            # skip over index column
            if _name == self.index_name:
                continue

            # drop columns filtered out by users through the frontend
            if _index in self.ignored_features:
                logger.info(
                    "→ dropped %s as it is set as ignored by user",
                    _name,
                )
                removed_columns.update({_name: ReasonDropped.DROPPED_BY_USER})
                continue

            # duplicate detection detected by type detector
            if col_info.isDeleted:
                logger.info(
                    "→ dropped %s (index %s) as it is detected as a duplicate",
                    _name,
                    col_info.columnIndex,
                )
                removed_columns.update({_name: ReasonDropped.DUPLICATE_COLUMN})
                continue

            # drop columns detected as unary by type detector
            if col_info.detectedType == DetectedType.unary:
                logger.info(
                    "→ dropped %s as it is detected as a constant",
                    _name,
                )
                removed_columns.update({_name: ReasonDropped.CONSTANT_VALUE})
                continue

        return removed_columns

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted:
            return X

        # remove the same columns dropped in the data preparation stage
        filtered_removed_cols = [col for col in self.removed_cols if col in X.columns]
        return X.drop(columns=filtered_removed_cols, inplace=False)

    def update_dropped_columns(self, col_dict: dict, data: pd.DataFrame) -> pd.DataFrame:
        """add dict of dropped columns to the report"""
        for key, value in col_dict.items():
            col_info = self.info_map[key]
            self.drop_column_report(col_info, value)

        self.removed_cols.extend(list(col_dict.keys()))

        original_column_names = set(data.columns)
        names = list(original_column_names - set(self.removed_cols) - set(self.required_column_names))
        return data.loc[:, names]

    def drop_column_report(self, col_info: ColumnInfo, reason: ReasonDropped) -> None:
        self.reports.append(
            FeatureReport(
                column_name=col_info.name,
                column_index=col_info.columnIndex,
                detected_type=col_info.detectedType,
                reason_dropped=reason,
                impute_count=None,
                required_by_user=None,
                transformation_block=None,
            )
        )
