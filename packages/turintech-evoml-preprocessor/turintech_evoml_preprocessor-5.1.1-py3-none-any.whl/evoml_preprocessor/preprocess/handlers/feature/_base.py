# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Set

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.models import (
    ColumnInfo,
    ReasonDropped,
)
from evoml_preprocessor.preprocess.models.report import FeatureReport
from evoml_preprocessor.preprocess.transformers import Transformer


# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class FeatureHandler(ABC):
    """Abstract interface for the methods preprocessing the features"""

    def __init__(
        self,
    ):
        self.fitted = False

        self.encoders: Dict[str, Transformer] = {}

        self.future_covariates_names: Set[str] = set()

        # reports
        self.reports: List[FeatureReport] = []
        self.removed_cols: List[str] = []
        self.encoded_to_original_map: Dict[str, str] = {}
        self.dropped_count = 0

    @abstractmethod
    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Fits and transforms the features in data. That is, it fits and
        transforms the columns of data that are not the label or the index
        column.
        Args:
            data:
                The original dataset with the label column being encoded (may include label column).
            label_name:
                The name of label column.
        Returns:
            pd.DataFrame:
                The dataframe with the encoded features.
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transforms the features of data.
        Note: the data may include the label column
        Args:
            data:
                The dataset that contains the features to be encoded (may include label column).
        Returns:
            pd.DataFrame:
                The dataframe with the encoded features.
        """
        raise NotImplementedError

    # ---------------------------- report methods ---------------------------- #
    def drop_column(self, col_info: ColumnInfo, reason: ReasonDropped) -> None:
        """Utility function reporting that a column was dropped and the reason why.
        Args:
            col_info:
                Information on the dropped column.
            reason:
                Enum denoting why the column was dropped.
        Returns:
            None
        """
        self.reports.append(
            FeatureReport(
                column_name=col_info.name,
                column_index=col_info.columnIndex,
                detected_type=col_info.detectedType,
                reason_dropped=reason,
                impute_count=None,
                required_by_user=None,
                transformation_block=None,
            )
        )
        self.removed_cols.append(col_info.name)
        self.dropped_count += 1

    def report_encoder(
        self, column: pd.Series, col_info: ColumnInfo, encoder: Transformer, is_required: bool = False
    ) -> None:
        """Reports the encoder used for a given column
        Args:
            column:
                The column that was encoded.
            col_info:
                Information on the column.
            encoder:
                The encoder used to encode the column.
            is_required:
                Whether the column was required or not.
        Returns:
            None
        """
        self.reports.append(
            FeatureReport(
                column_name=col_info.name,
                column_index=col_info.columnIndex,
                detected_type=col_info.detectedType,
                impute_count=int(column.isnull().sum()),
                transformation_block=encoder.transformation_block,
                required_by_user=is_required,
                reason_dropped=None,
            )
        )

    def update_encoded_to_original_map(self, encoded_names: List[str], original_name: str) -> None:
        """Adds the encoded_names to original_name mapping to a map that keeps all
         the encoded to original mappings.
        Args:
            encoded_names:
                The list of the names of the encoded columns, generated
                after encoding the column with the given original name.
            original_name:
                Column name before encoding.
        Returns:
            None
        """
        for encoded_name in encoded_names:
            self.encoded_to_original_map[encoded_name] = original_name

    def update(self, label_col: pd.Series, index_col: pd.Series) -> None:  # pragma: no cover
        """Updates the fitted label data with the given unseen label values on the
        corresponding index positions.
        Args:
            label_col:
                Unseen values of label.
            index_col:
                Index column.
        Returns:
            None.
        """
        pass
