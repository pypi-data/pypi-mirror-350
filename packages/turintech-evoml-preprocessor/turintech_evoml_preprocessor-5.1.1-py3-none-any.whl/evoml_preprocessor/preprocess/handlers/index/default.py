"""implements index handler interface for non time series tasks"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.index._base import IndexHandler
from evoml_preprocessor.preprocess.models import ColumnInfo

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class DefaultIndexHandler(IndexHandler):
    """The index handler for non timeseries data. Currently, it does nothing."""

    def fit_transform(
        self,
        index_col: Optional[pd.Series],
        index_info: Optional[ColumnInfo],
        index_size: Optional[int] = None,
    ) -> Optional[pd.Series]:
        """Returns None as no index is expected for non-timeseries tasks.
        Args:
            index_col: index column, expected to be None
            index_info: index column info, expected to be None
            index_size: index size, expected to be None

        Returns: none

        """
        # For non-timeseries, we need the index column to be None
        if index_col is not None:
            logger.warning(f"Expected no index column for task {self.ml_task}, found {index_col.name}")
        return None

    def transform(
        self,
        index_col: Optional[pd.Series],
        index_size: Optional[int] = None,
    ) -> Optional[pd.Series]:
        """Returns None as no index is expected for non-timeseries tasks.
        Args:
            index_col: index column, expected to be None
            index_size: index size, expected to be None

        Returns: None

        """
        # For non-timeseries, we need the index column to be None
        return None
