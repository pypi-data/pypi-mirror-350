"""Implements the generic split data interface using an algorithm splitting by
index
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional

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
# ──────────────────────────────────────────────────────────────────────────── #


class IndexSplit(DataSplitting):
    """SplittingFactory implementation for IndexSplit"""

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
        """splitting train/test files based on predefined row indexes
        Args:
            data (pd.DataFrame):
                data to split
            label_name (str):
                name of the label column
            ml_task (MlTask):
                ml task used
            ref_column (Optional[ColumnInfo]):
                reference column to split by
            keep_order (bool):
                whether to keep the order of the data
            test_data (Optional[pd.DataFrame]):
                test data to split
        Returns:
            SplitData:
                split data
        """
        # user options
        train_from = self.options.trainRangeFrom
        train_to = self.options.trainRangeTo
        test_from = self.options.testRangeFrom
        test_to = self.options.testRangeTo

        self.LOGGER.info("Splitting based on index range")
        self.LOGGER.info("→ train dataset from indices %s to %s", train_from, train_to)
        self.LOGGER.info("→ test dataset from indices %s to %s", test_from, test_to)

        # resetting values if they are out of range
        min_value = 0
        max_value = data.shape[0] - 1
        train_from = min_value if (train_from <= min_value or train_from >= max_value) else int(train_from)
        train_to = max_value if train_to > max_value else int(train_to)
        test_from = min_value if (test_from < min_value or test_from >= max_value) else int(test_from)
        test_to = max_value if test_to > max_value else int(test_to)

        # select index splits
        data_train = data.loc[train_from:train_to]
        data_test = data.loc[test_from:test_to]

        # identify invalid indices
        invalid_order = keep_order and not (
            data_train.index.is_monotonic_increasing or data_test.index.is_monotonic_increasing
        )
        invalid_conditions = {
            "overlap": pd.Interval(train_from, train_to).overlaps(pd.Interval(test_from, test_to)),
            "invalid_training_set": data_train[label_name].nunique(dropna=True) == 1,
            "invalid_index": index_name is not None and data_train[index_name].max() > data_test[index_name].min(),
            "invalid_order": invalid_order,
        }

        if any(invalid_conditions.values()):
            self.LOGGER.error("→ index range is overlapping or the train dataset contains only one label.")
            self.LOGGER.warning("→ using stratified split instead of index split")

            datay = data.loc[:, label_name]
            datax = data.drop(label_name, axis=1)

            data_y_to_stratify = datay if ml_task == MlTask.classification else None

            split_params = {"shuffle": True, "stratify": data_y_to_stratify, "test_size": 0.2}
            if keep_order:
                split_params["shuffle"] = False
                split_params.pop("stratify")

            x_train, x_test, y_train, y_test = train_test_split(datax, datay, **split_params)

            if not isinstance(x_train, pd.DataFrame):
                raise TypeError(f"x_train is expected to a be a pandas DataFrame. Received {type(x_train)}")
            if not isinstance(x_test, pd.DataFrame):
                raise TypeError(f"x_test is expected to a be a pandas DataFrame. Received {type(x_test)}")
            if not isinstance(y_train, pd.Series):
                raise TypeError(f"y_train is expected to a be a pandas Series. Received {type(y_train)}")
            if not isinstance(y_test, pd.Series):
                raise TypeError(f"y_test is expected to a be a pandas Series. Received {type(y_test)}")

            data_train = x_train.join(y_train)
            data_test = x_test.join(y_test)

        return SplitData(train=data_train, test=data_test)


splitting_factory.register(SplitMethod.index, IndexSplit)
