# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Dict, Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType

# Module
from evoml_preprocessor.preprocess.handlers.feature._base import FeatureHandler
from evoml_preprocessor.preprocess.handlers.feature.utils import (
    check_dropped_ts,
    convert_column,
    select_temporal_column_encoding,
)
from evoml_preprocessor.preprocess.models import (
    ColumnOptions,
    ReasonDropped,
)
from evoml_preprocessor.preprocess.transformers.type_aliases import Converter
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr
from evoml_preprocessor.preprocess.handlers.feature.forecasting.config import ForecastingFeatureHandlerConfig


# ──────────────────────────────────────────────────────────────────────────── #
CONF = conf_mgr.preprocess_conf  # Alias for readability

logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class ForecastingFeatureHandler(FeatureHandler):
    def __init__(self, config: ForecastingFeatureHandlerConfig):
        self.config = config
        super().__init__()
        # Values used by transform that will be set by fit
        self.converters: Dict[str, Optional[Converter]] = {}
        self.converters_metadata: Dict[str, Optional[str]] = {}

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Fits and transforms the features in data.
        Args:
            data:
                The dataset including the encoded label column.
            label_name:
                The label column name.
        Returns:
            pd.DataFrame:
                The dataframe with the encoded features
        """

        data_encoded = pd.DataFrame(index=data.index)

        for col_info in self.config.info_map.values():
            _name = col_info.name
            _index = col_info.columnIndex

            if _name == str(encoded_label.name) or (
                _name == self.config.index_name and col_info.detectedType != DetectedType.datetime
            ):
                # has been preprocessed first
                continue

            if _index in self.config.ignored_features:
                # These columns were de-selected by user
                self.drop_column(col_info, ReasonDropped.DROPPED_BY_USER)
                continue

            # check whether the column should be dropped
            can_drop = _index not in self.config.required_features and _name != self.config.index_name
            reason_dropped = check_dropped_ts(col_info)
            if reason_dropped is not None and can_drop:
                self.drop_column(col_info, reason_dropped)
                continue

            if _index in self.config.transformation_options:
                col_ops = self.config.transformation_options[_index]
            else:
                col_ops = ColumnOptions()

            # Find encoding
            encoder, converter, converter_metadata = select_temporal_column_encoding(col_info, col_ops)

            # Update encoding dictionaries
            self.encoders[_name] = encoder
            self.converters[_name] = converter
            self.converters_metadata[_name] = converter_metadata

            # Convert if needed
            data_col = convert_column(data[_name], converter, converter_metadata)

            logger.info(f"→ Fit and transform column {_name}")

            # Fit transform
            transformed_col = encoder.fit_transform(data_col, encoded_label)
            data_encoded = data_encoded.join(transformed_col)

            # Update mapping
            self.update_encoded_to_original_map(list(transformed_col.columns), col_info.name)

            # Update future covariates - datetime index is by default a future covariate
            if _index in self.config.future_covariates_indices or _name == self.config.index_name:
                self.future_covariates_names.update(transformed_col.columns)

            # Report
            self.report_encoder(data_col, col_info, encoder, not can_drop)

        self.fitted = True

        return data_encoded

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transforms the features of data.
        Note: The data may include the label column
        Args:
            data:
                The dataset that contains the features to be encoded.
        Returns:
            pd.DataFrame:
                Thee encoded features.
        """
        if not self.fitted:
            raise ValueError("Forecasting feature handler is not fitted.")

        data_encoded = pd.DataFrame(index=data.index)

        for col in self.encoders:
            if col in data:
                # Convert if needed
                data_col = convert_column(data[col], self.converters[col], self.converters_metadata[col])

                # Transform column
                transformed_col = self.encoders[col].transform(data_col)

                data_encoded = data_encoded.join(transformed_col)

        return data_encoded
