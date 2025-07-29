from __future__ import annotations

from itertools import chain
from typing import List

import numpy as np
import pandas as pd
from evoml_api_models import MlTask
from lightgbm import LGBMClassifier, LGBMRegressor
from numpy.typing import NDArray

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.scorer import FeatureScorer
from evoml_preprocessor.types.pandas import IndexedSeries


class LgbmScorer(FeatureScorer):
    def __init__(self, ml_task: MlTask, rng: np.random.Generator) -> None:
        super().__init__(ml_task, rng)
        self.regularization = 1.0

    def score(
        self, generated_features: List[GeneratedFeatureNode], y: pd.Series[float], n_limit: int, final: bool = False
    ) -> IndexedSeries[GeneratedFeatureNode, float]:
        """Uses a wrapper based model with L1 regularization to score features

        Model is gradient boosting (less performant, and better for gradient
        boosting models, while resulting typically in worse performance for
        linear models).

        L1 regularization is nice because it scales weights for redundant
        features to zero, resulting in a convenient way to select features.
        In case this isn't strict enough, we mask features until the maximum
        number of non-zero scores is equal to `n_limit`.

        Args:
            generated_features: the features to score
            y: the target
            n_limit: maximum number of non-zero scores
            final: is this the final epoch?

        Returns:
            Scores as an IndexedSeries, indexed by feature (wrapper around
            pandas series providing type support for the index).
        """
        model = (
            LGBMClassifier(n_estimators=40, reg_alpha=self.regularization, importance_type="gain")
            if self.ml_task == MlTask.classification
            else LGBMRegressor(n_estimators=40, reg_alpha=self.regularization, importance_type="gain")
        )

        # Concatenate all features to create the X data
        all_features = list(set(chain(self.original_features, generated_features)))
        X = self._feature_nodes_to_dataframe(all_features)

        model.fit(X.values, y.values)

        scores: NDArray[np.float64] = model.feature_importances_
        if scores.sum() < 1e-6:
            # adjust regularization for next run, since lasso is too strict
            self.regularization /= 2

        if scores.min() > 1e-6:
            # adjust regularization for next run, since lasso isn't doing enough work
            self.regularization *= 2

        pd_scores: pd.Series[float] = pd.Series(scores, index=all_features)
        pd_scores = pd_scores.mask(pd_scores.rank(method="min", ascending=False) > n_limit, 0.0)
        return pd_scores  # type: ignore
