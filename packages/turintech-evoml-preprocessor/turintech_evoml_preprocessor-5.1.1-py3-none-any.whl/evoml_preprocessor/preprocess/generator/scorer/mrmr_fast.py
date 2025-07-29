from __future__ import annotations

from itertools import chain
from typing import List

import pandas as pd

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.scorer import FeatureScorer
from evoml_preprocessor.preprocess.selector.mrmr_generation import MrmrGenerationSelector
from evoml_preprocessor.preprocess.selector.selector import RelevanceSelector
from evoml_preprocessor.types.pandas import IndexedSeries


class MrmrFastScorer(FeatureScorer):
    def score(
        self, generated_features: List[GeneratedFeatureNode], y: pd.Series[float], n_limit: int, final: bool = False
    ) -> IndexedSeries[GeneratedFeatureNode, float]:
        """Uses mRMR to score features

        mRMR is nice because it only considers features up to `n_limit` and it
        accounts for collinearity and correlation with target. It is modified
        to weight relevancy lower (resulting in less correlated generated
        features). This scorer is faster than mRMR because it only runs mRMR on
        the final epoch, opting for a filter for all other epochs. The downside
        is that generated features are expected to be more correlated.

        Args:
            generated_features: the features to score
            y: the target
            n_limit: maximum number of non-zero scores
            final: is this the final epoch?

        Returns:
            Scores as an IndexedSeries, indexed by feature (wrapper around
            pandas series providing type support for the index).
        """
        all_features = list(set(chain(self.original_features, generated_features)))

        if final:
            selector = MrmrGenerationSelector.default(self.ml_task)
            selector.feature_lengths = {feature.preorder: len(feature) for feature in all_features}
        else:
            selector = RelevanceSelector.default(self.ml_task)

        X = self._feature_nodes_to_dataframe(all_features)
        selector.fit(X, y, n_limit)
        scores = selector.scores.combined
        scores = scores.mask(scores.rank(method="min", ascending=False) > n_limit, 0.0)
        pd_scores: pd.Series[float] = pd.Series(
            scores.values,
            index=[feature for feature in all_features if feature.preorder in scores.index],
        )
        return pd_scores  # type: ignore
