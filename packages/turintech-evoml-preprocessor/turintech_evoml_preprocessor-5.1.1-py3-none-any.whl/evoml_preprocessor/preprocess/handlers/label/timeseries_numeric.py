"""Implements the processing of numeric label columns for timeseries tasks"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional, Tuple

# Dependencies
import pandas as pd
import numpy as np

# Module
from evoml_preprocessor.preprocess.handlers.index import TimeSeriesIndexHandler
from evoml_preprocessor.preprocess.handlers.label.numeric import NumericLabelHandler
from evoml_preprocessor.preprocess.handlers.utils import TimeseriesLabelMixin
from evoml_preprocessor.preprocess.models import (
    ColumnInfo,
    ColumnOptions,
    PreprocessConfig,
    GenericOption,
    NumericEncoder,
)

# ──────────────────────────────────────────────────────────────────────────── #
DEFAULT_INDEX_NAME = TimeSeriesIndexHandler.DEFAULT_NAME
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class TimeseriesNumericLabelHandler(TimeseriesLabelMixin, NumericLabelHandler):
    """This class provides methods to fit and transform numerical label columns for timeseries"""

    def __init__(self, config: PreprocessConfig, column_info: ColumnInfo, column_options: ColumnOptions):
        super().__init__(config, column_info, column_options)

        if config.windowSize is None:
            raise ValueError("Window size must be set when dealing with time series.")
        self.window_size: int = config.windowSize
        self.rolling = config.rolling or []
        self.horizon = config.timeSeriesHorizon
        # save fitted label in _fit_transform, this is then used by transform
        self.fitted_original: Optional[pd.Series] = None
        self.fitted_label: Optional[pd.Series] = None

        # by default - dont transform target
        if self.encoder_slug == GenericOption.AUTO:
            self.encoder_slug = GenericOption.NONE

    def encode(self, label_col: pd.Series) -> pd.Series:
        # keep track of unencoded label
        encoded_original = label_col.copy()

        # perform encoding
        encoded_col = self._apply_predefined_encoding(label_col)

        if self.fitted_label is not None:
            # handler fitted, fill leading nans using saved unencoded fitted label
            encoded_col = self._fill_leading_nans(encoded_col, encoded_original)
        else:
            # save unencoded fitted label
            self.fitted_original = encoded_original.iloc[-(self.horizon + self.window_size) :]
            self.fitted_label = encoded_col.copy()
        return encoded_col

    def _apply_predefined_encoding(self, label_col: pd.Series) -> pd.Series:
        if self.encoder_slug == NumericEncoder.DIFFERENCE:
            label_col = label_col.diff(self.horizon)
        elif self.encoder_slug == NumericEncoder.RATIO:
            label_col = label_col / label_col.shift(self.horizon)
        elif self.encoder_slug == NumericEncoder.LOG_RATIO:
            label_col = np.log(label_col / label_col.shift(self.horizon))
        return label_col

    def _fill_leading_nans(self, encoded_col: pd.Series, encoded_original: pd.Series) -> pd.Series:
        """Fills leading NaN values in the encoded columns using the corresponding fitted_label values.

        The function identifies the index of the first non-NaN value in the `encoded_col` series and applies a mask
        for the indices upto it. For these leading NaN values, suitable data from `self._fitted_label` is used for
        substitution. Subsequently, it fills any remaining missing values in `encoded_col`.
        """

        # find the index of the first non-NaN value
        first_valid_index = encoded_col.first_valid_index()

        # if there are leading NaN values
        if first_valid_index is not None and first_valid_index != encoded_col.index[0]:
            # form a binary mask for leading NaN values
            mask = encoded_col.index < first_valid_index
            num_nan = mask.sum()

            sub_encoded_original = encoded_original.iloc[:num_nan]
            fitted_original = self.fitted_original.reindex(self.fitted_original.index.union(sub_encoded_original.index))
            missing = sub_encoded_original.combine_first(fitted_original)
            encoded_missing = self._apply_predefined_encoding(missing)
            encoded_missing = encoded_missing.dropna()

            # synchronize the indices of encoded_col and fitted_for_nulls
            fitted_for_nulls = encoded_missing.reindex_like(encoded_col)

            # replace the leading NaNs with encoded values that incorated values from self._fitted_original
            encoded_col[mask] = encoded_col[mask].fillna(fitted_for_nulls[mask])

        # fill any missing values
        encoded_col = encoded_col.ffill().fillna(0)
        return encoded_col

    def _fit_transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Finds and sets private attributes needed for the transformation of
        the label column.

        Args:
            label_col (pd.Series): label column to be transformed.

        Returns:
            tuple: Transformed label column, Extra label features if any or None.
        """
        # compute the maximum allowed horizon
        max_horizon = len(label_col) - (self.horizon + self.window_size) + 1
        if self.horizon > max_horizon:
            raise ValueError(f"The forecast horizon {self.horizon} exceeds the maximum allowed limit {max_horizon}")

        # apply convert, impute and encode
        encoded_col, extra_label_features = super()._fit_transform(label_col)
        encoded_col = self.encode(encoded_col)

        # early return
        if self.window_size == 0:
            return encoded_col, extra_label_features

        # create lags and rolling window features for target_column
        label_features = self._create_features(encoded_col, self.window_size, self.rolling, self.horizon)

        # fill missing values
        label_features = label_features.ffill().fillna(0)

        # finalize label features
        extra_label_features = self.drop_na_and_merge(label_features, extra_label_features)

        # update mapping
        self.update_encoded_to_original_map(list(label_features.columns), str(self.name))

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

        if not encoded_col.isna().all():
            # apply convert, impute and encode
            encoded_col, extra_label_features = super().transform(encoded_col)
            encoded_col = self.encode(encoded_col)

        # early return
        if self.window_size == 0:
            return encoded_col, extra_label_features

        # select last_window for lags
        fitted_index = pd.Series(self.fitted_label.index)
        last_window = self.select_window_based_on_train_test_sets_relation(
            encoded_col, fitted_index, self.window_size, self.fitted_label, self.horizon
        )

        # this is the case where no label is given in the test data
        encoded_col = self.update_fitted_data_with_unseen(encoded_col)

        # append last window  if exists
        encoded_col_expanded = self.prepare_data_for_prediction(encoded_col, last_window, self.window_size)

        label_features = self._create_features(encoded_col_expanded, self.window_size, self.rolling, self.horizon)

        # fill any missing values
        if encoded_col.isna().all():
            label_features = label_features.iloc[0].to_frame().T
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
            # retrieve the portion of the encoded column that comes after the last index in the fitted labels
            unseen_data = encoded_col[encoded_col.index > self.fitted_label.index[-1]]

            # update the fitted labels by concatenating with the unseen data
            self.fitted_label = pd.concat([self.fitted_label, unseen_data])
        return encoded_col

    def update(self, label_col: pd.Series) -> None:
        """Updates the fitted label data with the given unseen label values.

        Args:
            label_col (pd.Series): unseen values of label.
        """

        if not self.fitted:
            raise ValueError("Call `fit` before calling this method.")
        if self.fitted_label is None:
            raise ValueError("Label handler has not been fitted properly: _fitted_label is missing.")

        # update fitted data with new data
        unseen_data = label_col[label_col.index > self.fitted_label.index[-1]]
        self.fitted_label = pd.concat([self.fitted_label, unseen_data])
