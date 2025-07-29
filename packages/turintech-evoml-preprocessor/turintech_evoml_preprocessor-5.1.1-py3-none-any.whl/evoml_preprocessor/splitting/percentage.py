"""Implements the generic split data interface using an algorithm splitting by
percentage
"""

import logging
import math
import random

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Optional, Tuple

import numpy as np

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import ColumnInfo, MlTask
from sklearn.model_selection import train_test_split

# Module
from evoml_preprocessor.preprocess.models import SplitMethod
from evoml_preprocessor.splitting.interface import DataSplitting, SplitData, splitting_factory

# ──────────────────────────────────────────────────────────────────────────── #


logger = logging.getLogger("preprocessor")


class PercentageSplit(DataSplitting):
    """SplittingFactory implementation for PercentageSplit
    Splitting data into train and test sets using a percentage of the data for the train set and the rest for the test set.

    When the data is not ordered, the split is stratified and shuffled.

    In the case of timeseries, when the data is ordered, the split is not stratified and not shuffled.
    The percentage is defined in the options of the split method.
    """

    def split(
        self,
        data: pd.DataFrame,
        label_name: str,
        ml_task: MlTask,
        ref_column: Optional[ColumnInfo],
        keep_order: bool = False,
        test_data: Optional[pd.DataFrame] = None,
        index_name: Optional[str] = None,
    ) -> SplitData:
        """
        Args:
            data (pd.DataFrame):
                Data to split.
            label_name (str):
                Name of the label column.
            ml_task (MlTask):
                    ml task used
            ref_column (Optional[ColumnInfo]):
                Reference column to split by.
            keep_order (bool):
                Whether to keep the order of the data.
            test_data (Optional[pd.DataFrame]):
                Test data to split.

        Returns:
            SplitData:
                split data
        """
        if self.options.trainPercentage is None:
            raise ValueError("Train percentage must be specified to perform a percentage split.")
        train_percentage: float = self.options.trainPercentage

        logger.info(f"→ splitting using a train percentage of {(train_percentage)*100:2g}%")
        # Split the dataset by percentage
        data_y: pd.Series = data.loc[:, label_name]
        data_x: pd.DataFrame = data.drop(label_name, axis=1)
        # we need to use set to get the unique values instead of the unique function as it fails when called with a series that contains NaN and strings
        n_classes = len(set(data_y))
        unique_ratio = n_classes / float(data_y.shape[0])

        # only shuffle if the data is not ordered (not timeseries)
        # only stratify if the unique ratio is less than 50%
        # setup the train test split
        shuffle = not keep_order
        stratify = False

        # set stratify setting
        if ml_task == MlTask.classification:
            n_samples = data_y.shape[0]

            # The lower bound of the test size should be at least n_classes, or 10 samples, whichever is larger.
            # But it shouldn't exceed 20% of the dataset size unless n_classes is larger than 20% of the dataset size.
            # It has been guaranteed that n_classes * 5 <= dataset size, because the type detection requires at least 5 samples
            # per class for it to be a valid target. Therefore, we limit the lower bound to be <= 20% without checking
            # the n_classes again.
            limit = 1 - min(max(10, n_classes) / n_samples, 0.2)

            if train_percentage > limit:
                logger.warning(
                    f"Train percentage is too high. The train percentage is {(train_percentage)*100:2g}% and the recomended limit is {(limit)*100:2g}%."
                )
                train_percentage = limit

            # Do not try stratified split if the unique ratio is larger than 50%
            stratify = shuffle and unique_ratio <= 0.5

        # train_test_split fails when:
        # - stratify classification and the minimum value count of the label is less than 2
        # - stratify regression - we shuffle instead
        if ml_task == MlTask.classification and stratify and min(data_y.value_counts()) < 2:
            logger.warning(
                "The minimum value count of the label is less than 2. Therefore, stratification is not possible. "
            )
            x_train, x_test, y_train, y_test = PercentageSplit._fallback_split(data_x, data_y, train_percentage)
        else:
            data_y_to_stratify = data_y if stratify else None
            x_train, x_test, y_train, y_test = train_test_split(
                data_x, data_y, train_size=train_percentage, shuffle=shuffle, stratify=data_y_to_stratify
            )

        if not isinstance(x_train, pd.DataFrame):
            raise TypeError(f"x_train is expected to a be a pandas DataFrame. Received {type(x_train)}")
        if not isinstance(x_test, pd.DataFrame):
            raise TypeError(f"x_test is expected to a be a pandas DataFrame. Received {type(x_test)}")
        if not isinstance(y_train, (pd.DataFrame, pd.Series)):
            raise TypeError(f"y_train is expected to a be a pandas DataFrame or Series. Received {type(y_train)}")
        if not isinstance(y_test, (pd.DataFrame, pd.Series)):
            raise TypeError(f"y_test is expected to a be a pandas DataFrame or Series. Received {type(y_test)}")

        data_train = x_train.join(y_train)
        data_test = x_test.join(y_test)

        return SplitData(train=data_train, test=data_test)

    @staticmethod
    def _fallback_split(
        data_x: pd.DataFrame, data_y: pd.Series, train_percentage: float
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        DIY version of stratified sampling to deal with cases SKlearn errors on
        such as:
            - a class only has a single member for classification
        """
        master_y = data_y.reset_index(drop=True)
        master_index = list(master_y.index)

        train_index = []
        for v, count in master_y.value_counts(ascending=True, dropna=False).items():
            # This function will sample by class
            if isinstance(v, float) and np.isnan(v):
                sub_data = master_y[master_y.isnull()]
            else:
                sub_data = master_y[master_y == v]

            # The function ensures each class is represented, we use
            # floor to prevent over-sampling this will mean a smaller
            # sample, but a solution will follow
            sample_count = max(1, math.floor(sub_data.shape[0] * train_percentage))
            sample_index = list(sub_data.sample(n=sample_count).index)
            train_index += sample_index

        # To ensure the number of elements equals the expected as
        # a result of using math.floor We randomly add extra values when
        # needed, this is a rare case only likely when the data is
        # extremely imbalanced and the train percentage is extremely
        # small or alternatively on small data sets.
        count_diff = int(round(train_percentage * master_y.shape[0] - len(train_index)))
        test_index = list(set(master_index) - set(train_index))
        if count_diff > 0:
            random.seed(a=42)
            compensate_sample = random.sample(test_index, count_diff)
            train_index += compensate_sample
            test_index = [i for i in test_index if i not in compensate_sample]

        # Sort the index to keep the train/test split data in its
        # original order
        train_index.sort()
        test_index.sort()

        # Split the data according to their positions
        y_train = data_y.iloc[pd.Index(train_index)]
        y_test = data_y.iloc[pd.Index(test_index)]
        x_train = data_x.iloc[pd.Index(train_index)]
        x_test = data_x.iloc[pd.Index(test_index)]

        return x_train, x_test, y_train, y_test


splitting_factory.register(SplitMethod.percentage, PercentageSplit)
