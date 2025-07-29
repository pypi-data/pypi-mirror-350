from __future__ import annotations

from itertools import chain
from typing import List, Union

import numpy as np
import pandas as pd
from evoml_api_models import MlTask
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.preprocessing import StandardScaler

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.scorer import FeatureScorer
from evoml_preprocessor.types.pandas import IndexedSeries


class LassoScorer(FeatureScorer):
    def __init__(self, ml_task: MlTask, rng: np.random.Generator) -> None:
        super().__init__(ml_task, rng)
        self.regularization = 10 if ml_task == MlTask.classification else 0.01

    def set_model(self) -> Union[LogisticRegression, Lasso]:
        if self.ml_task == MlTask.classification:
            c = 1 / self.regularization if self.regularization > 0.0 else 0.0
            return LogisticRegression(C=c, penalty="l1", solver="saga")
        return Lasso(alpha=self.regularization)

    def score(
        self, generated_features: List[GeneratedFeatureNode], y: pd.Series[float], n_limit: int, final: bool = False
    ) -> IndexedSeries[GeneratedFeatureNode, float]:
        """Uses a wrapper based model with L1 regularization to score features

        Model is linear (performant, and more reliable on general models)

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
        model = self.set_model()

        scaler = StandardScaler()

        all_features = list(set(chain(self.original_features, generated_features)))
        X = self._feature_nodes_to_dataframe(all_features)
        X = scaler.fit_transform(X)

        model.fit(X, y)

        if self.ml_task == MlTask.classification:
            scores = np.abs(model.coef_).mean(axis=0)
        else:
            scores = np.abs(model.coef_)

        if scores.sum() < 1e-6:
            # adjust regularization for next run, since lasso is too strict
            self.regularization /= 2
        if scores.min() > 1e-6:
            # adjust regularization for next run, since lasso isn't doing enough work
            self.regularization *= 2

        pd_scores: pd.Series[float] = pd.Series(scores, index=all_features)
        pd_scores = pd_scores.mask(pd_scores.rank(method="min", ascending=False) > n_limit, 0.0)
        return pd_scores  # type: ignore
