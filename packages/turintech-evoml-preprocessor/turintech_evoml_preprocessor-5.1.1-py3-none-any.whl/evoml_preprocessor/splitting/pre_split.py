"""Implements the generic split data interface using an algorithm splitting by
using (user provided) pre-split files
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import ColumnInfo, MlTask

# Module
from evoml_preprocessor.preprocess.models import SplitMethod
from evoml_preprocessor.splitting.interface import DataSplitting, SplitData, splitting_factory

# ──────────────────────────────────────────────────────────────────────────── #


logger = logging.getLogger("preprocessor")


class PreSplit(DataSplitting):
    """SplittingFactory implementation for PreSplit.

    This is the case when the user provides pre-split test file. The preprocessor is trained on the train file and tested on the test file.
    Therefore, the data is not split by the preprocessor.
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
        data_train = data
        if test_data is None:
            raise ValueError("Splitting method is presplit, but no test file is provided.")
        if set(test_data.columns) != set(data_train.columns):
            logger.warning(
                "The names of the columns in the test file are not the same as "
                "in the train file. It will be checked whether all required "
                "columns are included."
            )
        data_test = test_data
        logger.info("Using user provided test file (pre-split)")

        return SplitData(train=data_train, test=data_test)


splitting_factory.register(SplitMethod.presplit, PreSplit)
