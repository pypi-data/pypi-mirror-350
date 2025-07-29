# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Dict

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.data_preparation._base import DataPreparationHandler
from evoml_preprocessor.preprocess.models import ColumnInfo, ConfigOptions, PreprocessConfig

# ──────────────────────────────────────────────────────────────────────────── #


class TimeseriesDataPreparationHandler(DataPreparationHandler):
    """The data preparation handler for timeseries data. Currently, it does nothing."""

    def __init__(self, config: PreprocessConfig, info_map: Dict[str, ColumnInfo], config_options: ConfigOptions):
        super().__init__(config, info_map, config_options)

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        return data

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
