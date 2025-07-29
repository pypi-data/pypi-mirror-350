"""Defines the abstract interface for splitting data"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import ColumnInfo, MlTask

# Module
from evoml_preprocessor.preprocess.models import SplitMethod, SplitMethodOptions
from evoml_preprocessor.splitting.abstract_factory import AbstractFactory

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["DataSplitting", "SplitData", "splitting_factory"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


@dataclass
class SplitData:
    # Using a dataclass allows flexibility to expose more data subsets in the
    # future (validation?) while still keeping a common interface
    train: pd.DataFrame
    test: Optional[pd.DataFrame] = None


class DataSplitting(ABC):
    """Abstract interface to split a dataset into train and test"""

    LOGGER = logging.getLogger("preprocessor")

    def __init__(self, options: SplitMethodOptions):
        self.options = options

    @abstractmethod
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
        """Performs the data split on the data given at instantiation"""


splitting_factory = AbstractFactory[SplitMethod, DataSplitting]()
