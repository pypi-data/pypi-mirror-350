import logging
from typing import List, Optional, Union

import numpy as np
import pandas as pd
import scipy.stats as stats
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from evoml_preprocessor.preprocess.handlers.index import TimeSeriesIndexHandler
from evoml_preprocessor.preprocess.models.enum import RollingOperation

DEFAULT_INDEX_NAME = TimeSeriesIndexHandler.DEFAULT_NAME

logger = logging.getLogger("preprocessor")


def check_index_start(
    index_column: pd.Series,
    fitted_index: pd.Series,
    index_start: Optional[Union[int, str]],
) -> bool:
    """Decides if the index column starts from the index_start. In the case of a
    default index column, the function returns True. The supported index types
    are integers and datetime. If fitted_index and index_column are not of the
    same type or if index_start is None and index is not the default one, a
    ValueError is raised.

    Args:
        index_column (pd.Series): Integer or datetime type.
        fitted_index (pd.Series): Integer or datetime type.
        index_start (int | str | None): the index which will be checked if matches
            the first entry of the index_column. None if a default index is given.

    Returns:
         bool: True if index_start matches first entry of index_column or if the
            index_column is the default index.

    Raises:
        ValueError: If the index column and the fitted index are not of the same type.
        ValueError: If the index column and the fitted index have different names.
        ValueError: If the index column is not of type int64 or datetime.
        ValueError: If the index column is not the default one and index_start is None.

    """

    check = False

    if fitted_index.dtype != index_column.dtype:
        raise ValueError(
            f"Timeseries feature handler was fitted with an index of a different type {fitted_index.dtype}."
        )

    if fitted_index.name != index_column.name:
        raise ValueError(f"Timeseries feature handler was fitted with a different index column {fitted_index.name}.")

    if index_start is None and index_column.name != DEFAULT_INDEX_NAME:
        raise ValueError("Timeseries feature handler was not fitted properly: test index start is missing.")

    # check the default index case
    if index_column.name == DEFAULT_INDEX_NAME:
        return True

    if index_column.dtype == "int64":
        assert index_start is not None
        # integer index
        if index_column.iloc[0] == int(index_start):
            check = True
    elif is_datetime(fitted_index):
        # datetime index
        if index_start is None:
            raise ValueError("Index start must be supplied for datetime indexes.")
        if index_column.iloc[0] == pd.to_datetime(index_start):
            check = True
    else:
        raise ValueError(f"Not supported index type: {index_column.dtype}")

    return check


def check_test_after_train(index_column: pd.Series, fitted_index: pd.Series) -> bool:
    """Decides if the index column starts after the fitted index. In the case of a
    default index column, the function returns True. The supported index types
    are integers and datetime. If fitted_index and index_column are not of the
    same type a ValueError is raised.

    Args:
        index_column (pd.Series): Integer or datetime type.
        fitted_index (pd.Series): Integer or datetime type.

    Returns:
        bool: True if index column starts after the fitted index. Otherwise, it returns False.

    Raises:
        ValueError: If the index column and the fitted index are not of the same type.
        ValueError: If the index column and the fitted index have different names.
        ValueError: If the index column is not of type int64 or datetime.

    """

    check = False

    if fitted_index.dtype != index_column.dtype:
        raise ValueError(
            f"Timeseries feature handler was fitted with an index of a different type {fitted_index.dtype}."
        )

    if fitted_index.name != index_column.name:
        raise ValueError(f"Timeseries feature handler was fitted with a different index column {fitted_index.name}.")

    # check the default index case
    if index_column.name == DEFAULT_INDEX_NAME:
        return True

    if fitted_index.dtype == "int64" or is_datetime(fitted_index):
        if index_column.iloc[0] > fitted_index.iloc[-1]:
            check = True
    else:
        raise ValueError(f"Not supported index type: {index_column.dtype}")

    return check


class LaggedFeatureMixin:
    """A mixin class to provide lag functionality."""

    def create_lags(self, data: pd.DataFrame, window_size: int, horizon: int) -> pd.DataFrame:
        """Creates a dataframe that contains shifted copies of data. In total
        self.window_size columns are created, with shift in [1, self.window_size].

        Args:
            data (pd.DataFrame): A column that is going to be shifted.
            window_size (int): Window size considered for lagging.
            horizon (int): The gap between the target and latest lagged past covariate features.

        Returns:
            pd.DataFrame: A dataframe with the shifted columns of data.

        Raises:
            ValueError: If window_size is negative.

        """

        if window_size < 0:
            raise ValueError(f"Window size {window_size} must be a non-negative number.")

        # create lagged Series, for lag up to window size
        lagged_data = pd.DataFrame(index=data.index)
        for column in data:
            # create lagged Series, for lag up to window size
            for lag in range(horizon, window_size + horizon):
                lagged_data[f"{data[column].name}_lag{lag}"] = data[column].shift(lag)

        return lagged_data


class RollingWindowMixin:
    """A mixin class to provide rolling window functionality."""

    @staticmethod
    def column_rolling_operation(column: pd.Series, window_size: int, operation: RollingOperation) -> pd.Series:
        """Creates a rolling window feature of data using the specified operation.

        Args:
            data (pd.Series): A column that is going to be used for
                creating rolling windows features.
            window_size (int): Window size considered for rolling window features.
            operation (RollingOperation): The operation to apply on the rolling
                window ('mean', 'std', 'min', etc.).

        Returns:
            pd.Series: A dataframe with the rolling window features of data.

        Raises:
            ValueError: If window_size is negative.
        """
        if operation == RollingOperation.ZSCORE:
            rolling_mean = column.rolling(window_size).mean()
            rolling_std = column.rolling(window_size).std()
            return (column - rolling_mean) / rolling_std

        elif operation == RollingOperation.KURT:
            return column.rolling(window_size).apply(lambda x: round(stats.kurtosis(x), 3), raw=True)

        elif operation == RollingOperation.SKEW:
            return column.rolling(window_size).skew()

        elif operation == RollingOperation.MEAN:
            return column.rolling(window_size).mean()

        elif operation == RollingOperation.MEDIAN:
            return column.rolling(window_size).median()

        elif operation == RollingOperation.STD:
            return column.rolling(window_size).std()

        elif operation == RollingOperation.MIN:
            return column.rolling(window_size).min()

        elif operation == RollingOperation.MAX:
            return column.rolling(window_size).max()

        elif operation == RollingOperation.DIFFERENCE:
            return column - column.shift(1)

        # This operation feature only makes sense if we don't use an offset in the scaler
        elif operation == RollingOperation.RETURN:
            return column.pct_change().replace([np.inf, -np.inf], np.nan)

        # This operation is only appropriate if all column values > 0
        elif operation == RollingOperation.LOG_RETURN:
            column_log1p: pd.Series = np.log1p(column.pct_change())
            return column_log1p.replace([np.inf, -np.inf], np.nan)

        else:
            return column

    @staticmethod
    def column_rolling_operations(
        column: pd.Series, window_size: int, operations: List[RollingOperation]
    ) -> pd.DataFrame:
        """Creates a dataframe that contains rolling window features of data using the specified operation.

        Args:
            column (pd.Series): A column that is going to be used for
                creating rolling windows features.
            window_size (int): Window size considered for rolling window features.
            operations (List[RollingOperation]): The operation to apply on the rolling
                window ('mean', 'std', 'min', etc.).

        Returns:
            pd.DataFrame: A dataframe with the rolling window features of data.

        Raises:
            ValueError: If window_size is negative.
        """

        if window_size < 0:
            raise ValueError(f"Window size {window_size} must be a non-negative number.")

        # Define DataFrame to store processed features
        processed_features = pd.DataFrame(index=column.index)

        for operation in operations:
            # Perform operation and add to DataFrame
            r = RollingWindowMixin.column_rolling_operation(column, window_size, operation)

            r.name = f"{column.name}_lagged_rolling_{operation}"
            processed_features = pd.concat([processed_features, r], axis=1)

        return processed_features

    def create_all_rolling_window_features(
        self, data: pd.DataFrame, window_size: int, rolling: List[RollingOperation], horizon: int
    ) -> pd.DataFrame:
        """Creates a dataframe that contains rolling window feature of data using the specified operation.

        Args:
            data (pd.DataFrame): A column that is going to be used for
                creating rolling windows features.
            window_size (int): Window size considered for rolling window features.
            operation (RollingOperation): The operation to apply on the rolling
                window ('mean', 'std', 'min', etc.).
            horizon (int): The gap between the target and latest lagged past covariate features.

        Returns:
            pd.DataFrame: A dataframe with the rolling window features of data.

        Raises:
            ValueError: If window_size is negative.
        """

        if window_size < 0:
            raise ValueError(f"Window size {window_size} must be a non-negative number.")

        # Define DataFrame to store processed features
        processed_features = pd.DataFrame(index=data.index)

        # Iterate over columns individually
        for column in data:
            lagged_data = data[column].shift(horizon)
            for operation in rolling:
                # Perform operation and add to DataFrame
                r = RollingWindowMixin.column_rolling_operation(lagged_data, window_size, operation)

                r.name = f"{column}_lagged_rolling_{operation}"
                processed_features = pd.concat([processed_features, r], axis=1)

        return processed_features

    def _create_features(
        self, label_col: pd.Series, window_size: int, rolling: List[RollingOperation], horizon: int
    ) -> pd.DataFrame:
        """
        Creates lags and rolling window features for target column.

        Args:
            encoded_col (pd.Series): Column for which the features are to be computed.

        Returns:
            pd.DataFrame: Contains the lagged and rolling window features.
        """

        # shift the series based on the given horizon
        features = pd.DataFrame(index=label_col.index)

        if window_size < 1 or horizon < 1:
            raise ValueError(
                f"Context window size and horizon must be positive numbers. Window size: {window_size}. Horizon: {horizon}."
            )

        for window in range(0, window_size):
            shift = horizon + window
            horizon_shift = label_col.shift(shift)
            features[f"{label_col.name}_lag{shift}"] = horizon_shift

        # TODO: calculate rolling window features directly from the lags produced above. This would be safer
        # because it will help prevent leakage. The solution below relies on the exact same lags being recreated
        lagged_data = label_col.shift(horizon)
        for operation in rolling:
            # Perform operation and add to DataFrame
            rolling_shift = RollingWindowMixin.column_rolling_operation(lagged_data, window_size, operation)
            features[f"{label_col.name}_lagged_rolling_{operation}"] = rolling_shift

        # Drop the first window_size + horizon rows, for which we cannot create lags
        features = features.iloc[window_size + horizon - 1 :]

        return features


class TimeseriesLabelMixin(RollingWindowMixin):
    def select_window_based_on_train_test_sets_relation(
        self, encoded_col: pd.Series, fitted_index: pd.Series, window_size: int, fitted_label: pd.Series, horizon: int
    ) -> pd.Series:
        """
        This function selects the appropriate window for lagging based on the relationship between the train and test sets.

        Args:
            encoded_col (Series): Encoded column.
            fitted_index (Series): Index of the fitted data.
            window_size (int): Size of the rolling window.
            fitted_label (Series): Labels of the fitted data.
            horizon (int): The gap between the target and latest lags.

        Returns:
            Series: Last window selected for lagging.
        """

        index = pd.Series(encoded_col.index)

        # check if we can use fitted information to create lags
        is_test_after_train = check_test_after_train(index, fitted_index)
        last_window = None
        # Most common case: test set starts after train set
        if is_test_after_train:
            last_window = fitted_label.iloc[-(window_size + horizon - 1) :]
            last_window.index = pd.Index([f"train_{i}" for i in last_window.index])

        # test set is in the range of train data
        elif index.iloc[0] in fitted_index.values:
            # find location in train data of first index
            first_index = index.iloc[0]
            location = fitted_index.index[fitted_index.to_list().index(first_index)]
            if not isinstance(location, int):
                raise TypeError(f"Location is expected to be an integer. Received {type(location)}.")
            start_window = max(location - (window_size + horizon - 1), 0)
            last_window = fitted_label.iloc[start_window:location]
            last_window.index = pd.Series([f"train_{i}" for i in last_window.index])

        else:
            raise ValueError(
                "The test set incorrectly precedes the training set in the timeline. "
                "Please review and ensure your data is chronologically ordered."
            )
        return last_window

    def prepare_data_for_prediction(
        self, encoded_col: pd.Series, last_window: pd.Series, window_size: int
    ) -> pd.Series:
        """
        Prepares data for prediction by concatenating 'last_window' and 'encoded_col' series
        and making sure that 'encoded_col' has enough data for prediction.

        Args:
            encoded_col (pd.Series): The encoded column.
            last_window (pd.Series): The last window of data.
            window_size (int): The size of the window for rolling operation.

        Returns:
            pd.Series: The encoded column prepared for prediction.
        """
        # return early if there is no last window
        if last_window is None:
            return encoded_col

        # concatenate data
        encoded_col_expanded = pd.concat([last_window, encoded_col], axis=0)

        # check if encoded_col_expanded contains enough data for prediction
        if len(encoded_col_expanded) > window_size:
            return encoded_col_expanded

        # If not, generate extra rows and append
        logger.warning(
            "Test set does not contain enough data for a"
            " prediction. We repeat some of the data so that "
            "we have a whole window to make a prediction."
        )
        extra_rows_needed = window_size + 1 - len(encoded_col_expanded)
        extra_rows = pd.Series(
            [encoded_col[0]] * extra_rows_needed,
            index=[f"extra_{i}" for i in range(extra_rows_needed)],
            name=encoded_col.name,
        )

        return pd.concat([extra_rows, encoded_col_expanded], axis=0)

    def drop_na_and_merge(
        self, label_features: pd.DataFrame, extra_label_features: Optional[pd.DataFrame]
    ) -> pd.DataFrame:
        """
        This function handles missing data, performs preprocessing tasks and merges label features.

        Args:
           extra_label_features (DataFrame): Extra features to be merged with label_features.
           label_features (DataFrame): Original label features.

        Returns:
           DataFrame: Preprocessed and merged label features.
        """
        # if the input label was empty, we only save one row for prediction
        # as we can only create lags for one row
        if label_features.isna().any().any():
            # fill any missing values
            label_features = label_features.dropna()

        # merge label lags (if any) with extra label features
        if extra_label_features is not None:
            extra_label_features = extra_label_features.join(label_features, how="inner")
        else:
            extra_label_features = label_features
        return extra_label_features
