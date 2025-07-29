"""This module defines an interface for the subset of Preprocessor's
functionality dealing with the index column (index handler)
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from abc import ABC, abstractmethod
from typing import Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import MlTask
from evoml_api_models.builder.builder import get_builder, Builder
from pydantic import ValidationError

# Module
from evoml_preprocessor.preprocess.models import ColumnInfo
from evoml_preprocessor.preprocess.models.report import FeatureReport

# ──────────────────────────────────────────────────────────────────────────── #


class IndexHandler(ABC):
    """Abstract interface for the methods preprocessing the index column"""

    feature_builder: Builder[FeatureReport]

    def __init__(self, ml_task: MlTask):
        self.ml_task = ml_task
        self.feature_builder = get_builder(FeatureReport)
        self.feature_builder.impute_count = 0
        self.feature_builder.transformation_block = []
        self.fitted = False  # To prevent using transform before fit

    @abstractmethod
    def fit_transform(
        self,
        index_col: Optional[pd.Series],
        index_info: Optional[ColumnInfo],
        index_size: Optional[int] = None,
    ) -> Optional[pd.Series]:
        """Fits and transforms the index column (if it exists).
        Args:
            index_info:
                Column info for the index column
            index_col:
                The index column.
            index_size:
                The size of the index column, it is used in case that the index column is not in the data and a new column is created.
        Returns:
            Optional[pd.Series()]:
                The index column if it exists or if a new one is created, None otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def transform(
        self,
        index_col: Optional[pd.Series],
        index_size: Optional[int] = None,
    ) -> Optional[pd.Series]:
        """Transforms the index column (if it exists).
        Args:
            index_col:
                Index column.
            index_size:
                Index size, it is used in case the index column is not in the data and a new column is created.

        Returns:
            Optional[pd.Series]:
                The index column if it exists or if a new one is created, None otherwise.
        """
        raise NotImplementedError()

    # ---------------------------- report methods ---------------------------- #
    @property
    def feature_report(self) -> Optional[FeatureReport]:
        """Returns the feature report for the index column"""
        try:  # Validation for this specific model is cheap
            return self.feature_builder.build()
        except ValidationError:
            return None
