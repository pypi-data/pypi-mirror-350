# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.models import ColumnInfo, ColumnOptions, ConfigOptions, PreprocessConfig
from evoml_preprocessor.preprocess.models.report import FeatureReport

# ──────────────────────────────────────────────────────────────────────────── #


class DataPreparationHandler(ABC):
    """The data preparation handler interface. This class is responsible for handling the data preparation steps."""

    is_timeseries: bool
    info_map: Dict[str, ColumnInfo]
    index_name: Optional[str]
    removed_cols: List[str]

    def __init__(
        self,
        config: PreprocessConfig,
        info_map: Dict[str, ColumnInfo],
        config_options: ConfigOptions,
    ):
        self.info_map = info_map

        self.index_name = config.indexColumn
        self.ml_task = config.mlTask
        self.is_timeseries = config.isTimeseries
        self.fs_options = config.featureSelectionOptions

        self.column_options: Dict[int, ColumnOptions] = config_options.transformation_options
        self.ignored_features: List[int] = config_options.ignored_features
        self.required_features_idx: List[int] = config_options.required_features
        self.required_column_names = [
            x.name for x in self.info_map.values() if x.columnIndex in self.required_features_idx
        ]

        self.fitted = False

        # reporting
        self.reports: List[FeatureReport] = []
        self.removed_cols = []

    @abstractmethod
    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame: ...

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame: ...

    # ---------------------------- report methods ---------------------------- #
    @property
    def report(self) -> List[FeatureReport]:
        return self.reports
