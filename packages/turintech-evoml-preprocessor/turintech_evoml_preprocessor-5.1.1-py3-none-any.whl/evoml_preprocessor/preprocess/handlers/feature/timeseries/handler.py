# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Dict, Optional

import numpy as np

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
from evoml_preprocessor.preprocess.handlers.index import TimeSeriesIndexHandler
from evoml_preprocessor.preprocess.handlers.utils import LaggedFeatureMixin, RollingWindowMixin, check_test_after_train
from evoml_preprocessor.preprocess.models import (
    ColumnOptions,
    ReasonDropped,
)
from evoml_preprocessor.preprocess.transformers import DateTransformer
from evoml_preprocessor.preprocess.transformers.type_aliases import Converter
from evoml_preprocessor.preprocess.handlers.feature.timeseries.config import TimeSeriesFeatureHandlerConfig


# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
DEFAULT_INDEX = TimeSeriesIndexHandler.DEFAULT_NAME
# ──────────────────────────────────────────────────────────────────────────── #


class TimeseriesFeatureHandler(RollingWindowMixin, LaggedFeatureMixin, FeatureHandler):
    def __init__(self, config: TimeSeriesFeatureHandlerConfig):
        self.config = config
        super().__init__()
        # Values used by fit_transform and transform
        if self.config.window_size is None:
            raise ValueError("Window size must be set for time series.")
        # Values used by transform that will be set by fit
        self.converters: Dict[str, Optional[Converter]] = {}
        self.converters_metadata: Dict[str, Optional[str]] = {}
        self.fitted_data = pd.DataFrame()
        # To prevent using transform before fit_transform
        self.fitted: bool = False

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Fits and transforms the features in data based on the selected encoding.

        Notes:
            Currently, the evoML platform does not allow for window_size to be 0
            or negative.

        Args:
            data (pd.DataFrame): Original dataset with the label column and
                the index_column being encoded.
                We assume that the index_column.name == data.index.name
            encoded_label (pd.Series): Encoded label column.

        Returns:
            pd.DataFrame: dataframe with the encoded features

        """
        self.config.label_name = str(encoded_label.name)
        data_encoded = pd.DataFrame(index=data.index)

        if self.config.window_size >= data_encoded.shape[0]:
            raise ValueError(
                f"Window size ({self.config.window_size}) is greater or equal to the train set size ({data_encoded.shape[0]})"
            )

        if self.config.window_size == 0:
            logger.warning("lagging not performed; window size selected is 0")
            return data_encoded

        # Check that index exists in data
        if self.config.index_name not in data.columns:
            raise ValueError(f"Index {self.config.index_name} not in data.")

        # Consistency between the data and the column type info
        if self.config.index_name in self.config.info_map:
            assert set(self.config.info_map.keys()) == set(data.columns)
        else:
            assert set(self.config.info_map.keys()) == set(data.columns) - {self.config.index_name}

        # Save data
        self.fitted_data = data

        for col_info in self.config.info_map.values():
            col = col_info.name
            _index = col_info.columnIndex

            if col == self.config.label_name or (
                col == self.config.index_name and col_info.detectedType != DetectedType.datetime
            ):
                # label column has already been processed
                continue

            if _index in self.config.ignored_features:
                # These columns were de-selected by user
                self.drop_column(col_info, ReasonDropped.DROPPED_BY_USER)
                continue

            # Check whether the column should be dropped
            can_drop = _index not in self.config.required_features and col != data.index.name
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
            self.encoders[col] = encoder
            self.converters[col] = converter
            self.converters_metadata[col] = converter_metadata

            # Convert if needed
            data_col = convert_column(data[col], converter, converter_metadata)

            # Fit transform
            transformed_col = encoder.fit_transform(data_col)

            # create lags and rolling window features for non-datetime columns
            if col_info.detectedType != DetectedType.datetime:
                derived_features = pd.DataFrame(index=transformed_col.index)

                # create lags for past covariates only
                if _index not in self.config.future_covariates_indices:
                    lags = self.create_lags(
                        data=transformed_col, window_size=self.config.window_size, horizon=self.config.horizon
                    )
                    derived_features = pd.concat([derived_features, lags], axis=1)
                else:
                    # allows us to include future covariates
                    derived_features = transformed_col

                # rolling window features with window size < 2 are meaningless
                if (
                    _index in self.config.transformation_options
                    and self.config.window_size > 1
                    and np.issubdtype(
                        (
                            transformed_col.dtypes[0]
                            if isinstance(transformed_col, pd.DataFrame)
                            else transformed_col.dtype
                        ),
                        np.number,
                    )
                ):
                    rolling_features = self.create_all_rolling_window_features(
                        data=transformed_col,
                        window_size=self.config.window_size,
                        rolling=self.config.transformation_options[_index].rolling,
                        horizon=self.config.horizon,
                    )
                    derived_features = pd.concat([derived_features, rolling_features], axis=1)

                data_encoded = data_encoded.join(derived_features)
                self.update_encoded_to_original_map(list(derived_features.columns), col_info.name)
            else:
                data_encoded = data_encoded.join(transformed_col)

                # Update mapping
                self.update_encoded_to_original_map(list(transformed_col.columns), col_info.name)

            # Report
            self.report_encoder(data_col, col_info, encoder, not can_drop)

        # drop first self.config.window_size rows
        if not data_encoded.columns.empty:
            data_encoded = data_encoded.iloc[self.config.window_size :]

        # fill any missing values
        data_encoded = data_encoded.ffill().bfill().fillna(0)

        # If empty dataframe, reset the index
        if data_encoded.shape[0] == 0:
            data_encoded = pd.DataFrame(index=data.index)

        self.fitted = True

        return data_encoded

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transforms the features of data.

        Args:
            data (pd.DataFrame): The dataset that contains the features to be
                encoded and the encoded index. It may include the label column.

        Returns:
            pd.DataFrame: Dataframe with the encoded features.

        """

        data_encoded = pd.DataFrame(index=data.index)

        if self.config.window_size == 0:  # currently impossible
            logger.warning("lagging not performed; window size selected is 0")
            return data_encoded

        if not self.fitted:
            raise ValueError("Timeseries feature handler is not fitted.")

        index = self.config.index_name

        # Select last_window for lags
        last_window = self.get_last_window(data, index)

        # update fitted data with new data
        unseen_data = data[data[index] > self.fitted_data[index].iloc[-1]]
        self.fitted_data = pd.concat([self.fitted_data, unseen_data])

        if last_window is not None:
            data = pd.concat([last_window, data])

        if data.shape[0] <= self.config.window_size:
            logger.warning(
                "Test set does not contain enough data for a"
                " prediction. We repeat some of the data so that "
                "we have a whole window to make a prediction."
            )
            extra_rows = pd.concat([data.iloc[0, :].to_frame().T] * (self.config.window_size + 1 - data.shape[0]))
            extra_rows.index = pd.Index([f"extra_{i}" for i in range(extra_rows.shape[0])])
            data = pd.concat([extra_rows, data])

        temp_encoded_data = pd.DataFrame(index=data.index)
        temp_encoded_data.index.name = data_encoded.index.name

        for col in self.encoders:

            if col not in data:
                continue

            # Convert if needed
            data_col = convert_column(data[col], self.converters[col], self.converters_metadata[col])

            # Transform column
            transformed_col = self.encoders[col].transform(data_col)

            # if the column is a date column, we don't create lags and rolling window features
            if isinstance(self.encoders[col], DateTransformer):
                temp_encoded_data = pd.concat([temp_encoded_data, transformed_col], axis=1)
                continue

            col_info = self.config.info_map[col]

            derived_features = pd.DataFrame(index=transformed_col.index)

            # create lags for past covariates only
            if col_info.columnIndex not in self.config.future_covariates_indices:
                lags = self.create_lags(
                    data=transformed_col, window_size=self.config.window_size, horizon=self.config.horizon
                )
                derived_features = pd.concat([derived_features, lags], axis=1)
            else:
                derived_features = transformed_col

            # rolling window features with window size < 2 are meaningless
            if (
                col_info.columnIndex in self.config.transformation_options
                and self.config.window_size > 1
                and np.issubdtype(
                    transformed_col.dtypes[0] if isinstance(transformed_col, pd.DataFrame) else transformed_col.dtype,
                    np.number,
                )
            ):
                rolling_features = self.create_all_rolling_window_features(
                    data=transformed_col,
                    window_size=self.config.window_size,
                    rolling=self.config.transformation_options[col_info.columnIndex].rolling,
                    horizon=self.config.horizon,
                )
                derived_features = pd.concat([derived_features, rolling_features], axis=1)

            temp_encoded_data = pd.concat([temp_encoded_data, derived_features], axis=1)

        # drop first self.config.window_size rows
        if not temp_encoded_data.columns.empty:
            data_encoded = temp_encoded_data.iloc[self.config.window_size + self.config.horizon - 1 :]

        # fill any missing values
        data_encoded = data_encoded.ffill().bfill().fillna(0)

        # If empty dataframe, reset the index
        if data_encoded.shape[0] == 0:
            data_encoded = pd.DataFrame(index=data.index)

        return data_encoded

    def get_last_window(self, data: pd.DataFrame, index: str) -> pd.Index:
        # check if the test set starts after train
        is_test_after_train = check_test_after_train(data[index], self.fitted_data[index])
        # required cols will be used to select columns from fitted data
        cols_needed_for_last_window = list(data.columns)
        # Most common case: test set starts after train set
        if is_test_after_train:
            last_window = self.fitted_data.iloc[-(self.config.window_size + self.config.horizon - 1) :].loc[
                :, cols_needed_for_last_window
            ]
            last_window.index = pd.Index([i for i in last_window.index])

        # test set is in the range of train data
        elif data[index].iloc[0] in self.fitted_data[index].values:
            # test start is in training data
            first_index = data[index].iloc[0]
            # find location in train data of first index
            location = self.fitted_data[index].index[self.fitted_data[index].to_list().index(first_index)]
            if not isinstance(location, (int, np.integer)):
                raise TypeError(f"Location is not an integer. Received: {type(location)}")
            start_window = max(location - (self.config.horizon + self.config.window_size - 1), 0)
            last_window = self.fitted_data.iloc[start_window:location].loc[:, cols_needed_for_last_window]
            last_window.index = pd.Index([i for i in last_window.index])

        else:
            raise ValueError(
                "The test set incorrectly precedes the training set in the timeline. "
                "Please review and ensure your data is chronologically ordered."
            )

        return last_window
