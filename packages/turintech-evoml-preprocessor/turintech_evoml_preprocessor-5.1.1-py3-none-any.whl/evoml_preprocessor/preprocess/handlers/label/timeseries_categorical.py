"""Implements the processing of categorical label columns for timeseries tasks"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional, Tuple

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.label.categorical import CategoricalLabelHandler
from evoml_preprocessor.preprocess.handlers.utils import TimeseriesLabelMixin
from evoml_preprocessor.preprocess.models import ColumnInfo, ColumnOptions, PreprocessConfig

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class TimeseriesCategoricalLabelHandler(TimeseriesLabelMixin, CategoricalLabelHandler):
    """This class provides methods to fit and transform categorical label columns for timeseries"""

    def __init__(self, config: PreprocessConfig, column_info: ColumnInfo, column_options: ColumnOptions):
        super().__init__(config, column_info, column_options)
        if config.windowSize is None:
            raise ValueError("The window size must be set for preprocessing time series.")
        self.window_size: int = config.windowSize
        self.rolling = config.rolling or []
        self.horizon = config.timeSeriesHorizon
        # save fitted label in _fit_transform, this is then used by transform
        self._fitted_label: Optional[pd.Series] = None

    def _fit_transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Finds and sets private attributes needed for the transformation of
        the label column.

        Args:
            label_col (pd.Series): label column to be transformed.

        Returns:
            pd.Series: Transformed label column.
            pd.DataFrame | None: Extra label features (if any).

        """
        # compute the maximum allowed horizon
        max_horizon = len(label_col) - (self.horizon + self.window_size) + 1
        if self.horizon > max_horizon:
            raise ValueError(f"The forecast horizon {self.horizon} exceeds the maximum allowed limit {max_horizon}")

        # perform initial transformations
        encoded_col, extra_label_features = super()._fit_transform(label_col)

        # save label
        self._fitted_label = encoded_col.copy()

        # early return when window size = 0
        if self.window_size == 0:
            return encoded_col, extra_label_features

        # create lags and rolling window features for target_column
        label_features = self._create_features(encoded_col, self.window_size, self.rolling, self.horizon)

        # We shouldn't backfill for time series. Still sure if this makes sense. Shall we forward fill before generating
        # rolling window features so the rolling windows don't contains nans? Also shouldn't we drop any remaining nans
        # instead of filling with zeros?
        label_features = label_features.ffill().fillna(0)

        # finalize label features
        extra_label_features = self.drop_na_and_merge(label_features, extra_label_features)

        # update mapping
        self.update_encoded_to_original_map(list(label_features.columns), str(self.name))

        # update feature report
        # self.block_builder.column_names.extend(label_features.columns)

        return encoded_col, extra_label_features

    def transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Applies the transformation as determined by the `fit`
        (or `fit_transform`) method.

        Args:
            label_col (pd.Series): label column to be transformed.

        Returns:
            pd.Series: Transformed label column.
            pd.DataFrame | None: Extra label features (if any).

        """
        encoded_col, extra_label_features = label_col, None

        if self.window_size == 0:
            encoded_col, extra_label_features = super().transform(label_col)
            return encoded_col, extra_label_features

        if self.fitted_label is None:
            raise ValueError("Label handler has not been fitted properly: fitted label is missing.")

        # select last_window for lags
        fitted_index = pd.Series(self.fitted_label.index)
        last_window = self.select_window_based_on_train_test_sets_relation(
            encoded_col, fitted_index, self.window_size, self.fitted_label, self.horizon
        )

        # this is the case where no label is given in the test data
        encoded_col = self.update_fitted_data_with_unseen(encoded_col)

        # append last window  if exists
        encoded_col_expanded = self.prepare_data_for_prediction(encoded_col, last_window, self.window_size)

        # create lags and rolling window features for target_column
        label_features = self._create_features(encoded_col_expanded, self.window_size, self.rolling, self.horizon)

        # if the input label was empty, we only save one row for the prediction as we can only create lags for one row
        if encoded_col.isna().all():
            label_features = label_features.iloc[0].to_frame().T

        # We shouldn't backfill for time series. Still sure if this makes sense. Shall we forward fill before generating
        # rolling window features so the rolling windows don't contains nans? Also shouldn't we drop any remaining nans
        # instead of filling with zeros?
        label_features = label_features.ffill().fillna(0)

        # merge label lags (if any) with extra label features
        extra_label_features = self.drop_na_and_merge(label_features, extra_label_features)

        return encoded_col, extra_label_features

    def update_fitted_data_with_unseen(self, encoded_col: pd.Series) -> pd.Series:
        """
        Updates the fitted data by incorporating the unseen data.

        Args:
            encoded_col (pd.Series): The original column
        Note:
            The function changes the state of the object by modifying self.fitted_label attribute.
            It does not return any value. 'Unseen data' refers to the new data that the model
            has not encountered during the fitting phase.
        """
        # check if the encoded column has any meaningful (non-NaN) values
        if not encoded_col.isna().all():
            encoded_col, extra_label_features = super().transform(encoded_col)

            # retrieve the portion of the encoded column that comes after the last index in the fitted labels
            unseen_data = encoded_col[encoded_col.index > self.fitted_label.index[-1]]

            # update the fitted labels by concatenating with the unseen data
            self._fitted_label = pd.concat([self.fitted_label, unseen_data])
        return encoded_col

    def update(self, label_col: pd.Series) -> None:
        """Updates the fitted label data with the given unseen label values.

        Args:
            label_col (pd.Series): unseen values of label.
        """

        if not self.fitted:
            raise ValueError("Call `fit` before calling this method.")
        if self.fitted_label is None:
            raise ValueError("Label handler has not been fitted properly: fitted_label is missing.")

        # update fitted data with new data
        unseen_data = label_col[label_col.index > self.fitted_label.index[-1]]
        self._fitted_label = pd.concat([self.fitted_label, unseen_data])

    @property
    def fitted_label(self) -> pd.Series:
        if self._fitted_label is None:
            raise AttributeError("The handler has not been fitted yet.")
        return self._fitted_label
