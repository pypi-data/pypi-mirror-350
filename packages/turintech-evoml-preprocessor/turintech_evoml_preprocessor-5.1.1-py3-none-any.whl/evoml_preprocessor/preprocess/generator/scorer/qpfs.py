from __future__ import annotations

from itertools import chain
from typing import List

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.scorer._base import FeatureScorer
from evoml_preprocessor.preprocess.selector.selector import QPFSelector
from evoml_preprocessor.types.pandas import IndexedSeries


class QpfsScorer(FeatureScorer):
    def __init__(self, ml_task: MlTask, rng: np.random.Generator):
        super().__init__(ml_task, rng)
        self.selector = QPFSelector.default(self.ml_task)

    def score(
        self, generated_features: List[GeneratedFeatureNode], y: pd.Series[float], n_limit: int, final: bool = False
    ) -> IndexedSeries[GeneratedFeatureNode, float]:
        """Uses mRMR to score features

        mRMR is nice because it only considers features up to `n_limit` and it
        accounts for collinearity and correlation with target. It is modified
        to weight relevancy lower (resulting in less correlated generated
        features)

        Args:
            generated_features: the features to score
            y: the target
            n_limit: maximum number of non-zero scores
            final: is this the final epoch?

        Returns:
            Scores as an IndexedSeries, indexed by feature (wrapper around
            pandas series providing type support for the index).
        """
        all_features = list(chain(self.original_features, generated_features))
        X = self._feature_nodes_to_dataframe(all_features)

        self.selector.fit(X, y, n_limit)
        scores = self.selector.scores.combined
        pd_scores = pd.Series(scores.values, index=all_features)
        pd_scores = pd_scores.mask(pd_scores.rank(method="min", ascending=False) > n_limit, 0.0)
        return pd_scores  # type: ignore
