# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.feature_selection.config import FeatureSelectionConfig
from evoml_preprocessor.preprocess.models import ColumnInfo, ReasonDropped
from evoml_preprocessor.preprocess.models.report import FeatureReport
from evoml_preprocessor.preprocess.selector.models import FeatureSelectionReport

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class FeatureSelectionHandler(ABC):
    """The feature selection handler interface. It selects features based on the
    configuration. This is an abstract class implementation used by the default
    feature selection handler and the timeseries feature selection handler.

    Please note that the input data for fit_transform_report and fit_transform
    should not contain the label column. The label column should be passed
    separately as a pd.Series.

    To add a new feature selection handler, you need to implement the following methods:
        - fit_transform_report
        - _feature_selection

    _feature_selection is used as part of the fit_transform method
    and is responsible for the actual feature selection.

    """

    def __init__(self, config: FeatureSelectionConfig):
        self.ml_task = config.mlTask
        self.is_timeseries = config.isTimeseries
        self.options = config.featureSelectionOptions
        self.feature_selector = None
        self.sel_columns: Optional[List[str]] = None
        self.original_columns: Optional[Set[str]] = None
        self.required_cols: Optional[pd.DataFrame] = None
        self.non_numeric_cols: Optional[pd.DataFrame] = None
        self.required_encoded_columns: List[str] = []

        # reporting
        self.reports: List[FeatureReport] = []
        self.removed_cols: List[str] = []

    @abstractmethod
    def fit_transform_report(
        self, data: pd.DataFrame, encoded_label: pd.Series
    ) -> Tuple[pd.DataFrame, Optional[Dict[str, float]]]: ...

    def _initial_preparation(self, data: pd.DataFrame) -> Tuple[bool, pd.Index, pd.Index]:
        """Initial preparation of the data before feature selection.

        Args:
            data (pd.DataFrame): The data to be preprocessed.

        Returns:
            bool: A flag indicating whether feature selection should be performed.
            pd.Index: The required feature names.
            pd.Index: The non-numeric feature names.

        """

        # identify required columns and exclude them from feature selection process
        required_feature_names = pd.Index(self.get_required_encoded_columns())
        non_numeric_col_names = data.select_dtypes(exclude=["number", "bool"]).columns.difference(
            required_feature_names
        )

        if len(required_feature_names) >= data.shape[1] - 1:
            logger.warning("Skipping feature selection as there are not enough not required columns.")
            return False, pd.Index([]), pd.Index([])
        if len(non_numeric_col_names) + len(required_feature_names) >= data.shape[1] - 1:
            logger.warning("Skipping feature selection as there are not enough not required numeric columns.")
            return False, pd.Index([]), pd.Index([])

        return True, required_feature_names, non_numeric_col_names

    @abstractmethod
    def _feature_selection(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Performs feature selection on the data.
        This method is the core of the selection process.

        Args:
            data (pd.DataFrame): The data to be preprocessed.
            encoded_label (pd.Series): The encoded label column.

        Returns:
            pd.DataFrame: The preprocessed data.

        """

        raise NotImplementedError()

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Performs feature selection on the data. It sets the necessary
        attributes of the handler and return the processed data.

        Args:
            data (pd.DataFrame): The data to be preprocessed.
            encoded_label (pd.Series): The encoded label column.

        Returns:
            pd.DataFrame: The preprocessed data.

        """

        self.sel_columns = list(data.columns)
        self.removed_cols = []

        flag, required_col_names, non_numeric_col_names = self._initial_preparation(data)
        if not flag:
            return data

        number_of_preprocessed_columns = data.shape[1]

        # remove columns here (in-place) and ensure they're added back in place afterward
        # this is more memory efficient, and should be fast enough as long as there
        # aren't too many required/non-numeric columns
        self.required_cols = pd.DataFrame(index=data.index)
        self.non_numeric_cols = pd.DataFrame(index=data.index)
        for col in required_col_names:
            self.required_cols[col] = data.pop(col)
        for col in non_numeric_col_names:
            self.non_numeric_cols[col] = data.pop(col)

        # Save the set of original columns
        self.original_columns = set(data.columns)
        logger.info(f"→ original number of features: {len(self.original_columns)}")
        data_selected = self._feature_selection(data, encoded_label)

        # add columns (try to be as memory efficient as possible here, this
        # should be fast enough as long as there aren't too many required/non-numeric
        # columns
        for i, col in enumerate(required_col_names):
            if col not in data_selected:
                data_selected.insert(i, col, self.required_cols[col])
            if col not in data:
                data.insert(i, col, self.required_cols.pop(col))
        for col in non_numeric_col_names:
            data_selected[col] = self.non_numeric_cols[col]
            data[col] = self.non_numeric_cols.pop(col)

        if data_selected.shape[1] == number_of_preprocessed_columns:
            return data_selected

        # Identify columns removed by feature selector
        removed_col = self.original_columns - set(data_selected.columns)

        # update attrs columns
        self.sel_columns = list(data_selected.columns)
        self.removed_cols = list(removed_col)

        logger.info(f"→ number of features after selection: {len(self.sel_columns)}")
        logger.info("→ feature selection successful")

        return data_selected

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.feature_selector is not None:
            data = data[[s for s in self.sel_columns if s in data.columns]]

        return data

    # ---------------------------- report methods ---------------------------- #
    @property
    def report(self) -> Optional[FeatureSelectionReport]:
        # @TODO: clean that
        if self.feature_selector is not None:
            return self.feature_selector.report_builder.report
        return None

    def drop_column(self, col_info: ColumnInfo, reason: ReasonDropped) -> None:
        """Utility function reporting that a column was dropped and the reason why.

        Args:
            col_info: information of the dropped column
            reason: why the column was dropped

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

    def set_required_encoded_columns(self, required_encoded_columns: List[str]) -> None:
        """Utility function to map the required columns to the encoded columns if the
        map indexes to names exists.

        Args:
            required_encoded_columns: list of required encoded columns

        Returns:
            None
        """

        self.required_encoded_columns = required_encoded_columns

    def get_required_encoded_columns(self) -> List[str]:
        return self.required_encoded_columns
