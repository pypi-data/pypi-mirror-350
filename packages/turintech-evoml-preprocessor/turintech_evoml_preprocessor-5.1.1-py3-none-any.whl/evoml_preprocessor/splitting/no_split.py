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


class NoSplit(DataSplitting):
    """SplittingFactory implementation for NoSplit.
    This is the case when the user trains on the whole dataset and does not want to split it. Therefore, the data is not split.
    In this case, the user has not provided a test file.
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
        logger.warning("No splitting selected. All data will be used for training.")
        # for simplification purposes we keep the same data for train and test.
        # However, we only create the train.csv from the preprocessor
        return SplitData(train=data, test=None)


splitting_factory.register(SplitMethod.nosplit, NoSplit)
