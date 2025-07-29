# ───────────────────────────────── imports ────────────────────────────────── #
# Dependencies
from typing import Dict, Optional

import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.feature_generation._base import FeatureGenerationHandler
from evoml_preprocessor.preprocess.models import PreprocessConfig

# ──────────────────────────────────────────────────────────────────────────── #


class TimeseriesFeatureGenerationHandler(FeatureGenerationHandler):
    """The feature generation handler for timeseries data. Currently, it does nothing."""

    def __init__(self, config: PreprocessConfig):
        super().__init__(config)

    def fit_transform_report(
        self, data: pd.DataFrame, encoded_label: pd.Series, scores: Optional[Dict[str, float]]
    ) -> pd.DataFrame:
        return data

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        return data

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
