from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
from evoml_api_models.optimisation import MlTask

from evoml_preprocessor.preprocess.generator.feature_generation import GeneratedFeatureNode
from evoml_preprocessor.types.pandas import IndexedSeries


class FeatureScorer:
    """'abstract' base class for scoring new features

    Defines a set of methods that all builders must have:
    - `score`: returns a pandas series of scores for each feature
    """

    def __init__(self, ml_task: MlTask, rng: np.random.Generator) -> None:
        self.ml_task = ml_task
        self.rng = rng

        self.original_features: List[GeneratedFeatureNode] = []

    def load_original_features(self, original_features: List[GeneratedFeatureNode]) -> None:
        self.original_features = original_features

    def score(
        self, generated_features: List[GeneratedFeatureNode], y: pd.Series[float], n_limit: int, final: bool = False
    ) -> IndexedSeries[GeneratedFeatureNode, float]:
        raise NotImplementedError

    # ------------------------------------------ utils ------------------------------------------- #
    # Utils method to share common code between scorers (could be moved to functions)
    @staticmethod
    def _feature_nodes_to_dataframe(features: List[GeneratedFeatureNode]) -> pd.DataFrame:
        """Utils to concatenate a list of feature nodes into a single dataframe."""
        # Convert to a list of series and account for potential 'None' series
        features_series = [feature.values for feature in features if feature.values is not None]
        assert len(features_series) == len(features), "Some features are missing values"

        return pd.concat(features_series, axis=1)


__all__ = ["FeatureScorer"]
