# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from abc import ABC, abstractmethod
from typing import Dict, Optional

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.generator.feature_generation import FeatureGenerator
from evoml_preprocessor.preprocess.generator.models import FeatureGenerationReport
from evoml_preprocessor.preprocess.models import PreprocessConfig

# ──────────────────────────────────────────────────────────────────────────── #


class FeatureGenerationHandler(ABC):
    """The feature generation handler interface.

    It generates features based on the configuration.
    This is an abstract class implementation used by the default feature
    generation handler and the timeseries feature generation handler.

    """

    def __init__(self, config: PreprocessConfig):
        self.ml_task = config.mlTask
        self.options = config.featureGenerationOptions
        self.is_timeseries = config.isTimeseries
        self.feature_generator: Optional[FeatureGenerator] = None

    @abstractmethod
    def fit_transform_report(
        self, data: pd.DataFrame, encoded_label: pd.Series, scores: Optional[Dict[str, float]]
    ) -> pd.DataFrame: ...

    @abstractmethod
    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame: ...

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame: ...

    # ---------------------------- report methods ---------------------------- #
    @property
    def report(self) -> Optional[FeatureGenerationReport]:
        if self.feature_generator is None:
            return None

        return self.feature_generator.report_builder.report
