"""This module provides the Minimum Redundancy Maximum Relevancy (mRMR) selector."""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard libraries
from __future__ import annotations

from typing import Optional, Tuple

# Dependencies
import numpy as np
import pandas as pd

# Private dependencies
from evoml_api_models import MlTask

# Module
from evoml_preprocessor.preprocess.models import SelectionMetric, SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import FLOOR, SelectorParameters, SingleSelectionMetric, aggregate


class MrmrSelector(Selector):
    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self._report = SelectionMethodReport(method=SelectorType.MRMR)
        self.linear: bool = parameters.linear
        self.redundancy_weight: float = parameters.redundancy_weight
        self.redundancy_matrix: Optional[pd.DataFrame] = None

    @classmethod
    def default(cls, ml_task: MlTask) -> MrmrSelector:
        return cls(
            SelectorParameters(
                relevancy=[SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.F_TEST)],
                redundancy=SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON),
            )
        )

    @property
    def name(self) -> str:
        return "mrmr"

    def calc_relevancy(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        """Calculate relevancy scores for each feature in X.

        This is an internal helper method for `fit`.

        Each relevancy metric is evaluated for each feature in X and the
        relevancy scores are aggregated using the relevancy aggregation
        option.

        Args:
            X (pd.DataFrame): The features.
            y (pd.Series): The target.

        Returns:
            pd.Series: The relevancy scores for each feature.

        """

        features = X.columns
        relevancy_scores = pd.DataFrame(0.001, index=features, columns=[m.name for m in self.relevancy_metrics])
        for m in self.relevancy_metrics:
            relevancy_scores[m.name] = m.evaluate(X, y)
        return aggregate(relevancy_scores, self.relevancy_aggregation)

    def calc_redundancy(self, selected: pd.Index, not_selected: pd.Index) -> pd.Series:
        """Calculate redundancy scores for each feature in X.

        This is an internal helper method for `fit`.

        The redundancy metric is evaluated for each pair of features in X and
        the redundancy scores are aggregated using the redundancy aggregation.

        Mrmr is more performant since we can limit the redundancy calculation
        to only pairs of features (f, s) where f a feature that has not yet
        been selected and s a feature that has been selected.

        Args:
            selected (pd.Index): The features that have been selected.
            not_selected (pd.Index): The features that have not yet been selected.

        Returns:
            pd.Series: The redundancy scores for each feature.

        """
        if self.redundancy_matrix is None:
            raise ValueError("redundancy_matrix is None, calc_redundancy should be called in fit")
        return aggregate(self.redundancy_matrix.loc[not_selected, selected], self.redundancy_aggregation)

    def _get_best_feature(
        self, relevancy: pd.Series, redundancy: pd.Series, not_selected: pd.Index
    ) -> Tuple[str, float]:
        """Get the best feature based on relevancy and redundancy scores.

        This is an internal helper method for `fit`, which is called
        on each iteration of the algorithm. It returns both the feature to be
        added to the selected features and the score of that feature.

        Args:
            relevancy (pd.Series): The relevancy scores for each feature.
            redundancy (pd.Series): The redundancy scores for each feature.

        Returns:
            Tuple[str, float]: The feature to be added to the
                selected features and the score.

        """

        if self.linear:
            weight = self.redundancy_weight
            score = relevancy - weight * redundancy
        else:
            score = relevancy / redundancy
        score = score[not_selected]

        return score.index[score.argmax()], score.max()

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit the selector to the data.

        The MRMR algorithm is implemented here. It is a greedy algorithm that
        iteratively selects the feature that maximizes the relevancy score
        divided by the redundancy score.

        To begin:
        1. Compute the relevancy score for each feature

        At each iteration:
        1. Compute the redundancy score for each feature not yet selected
        2. Divide the relevancy score by the redundancy score for each feature
        3. Select the feature with the highest score

        This algorithm has cost O(n * m) where n is the number of features and
        m is the features to select.

        Args:
            X (pd.DataFrame): The features.
            y (pd.Series): The target.
            n (int): The number of features to select.

        """

        self.init_fit(X, y, n)  # initial setup
        self.redundancy_matrix = self.redundancy_metric.matrix_evaluate(X)
        self.selected_features = pd.Index([])

        selected: pd.Index = pd.Index([])
        not_selected: pd.Index = X.columns

        relevancy = self.calc_relevancy(X, y)
        self.scores.relevancy.update(relevancy)  # store

        n_iter = min(n, len(X.columns))
        for i in range(n_iter):
            score_relevancy = relevancy[not_selected]

            if i > 0:
                score_redundancy = self.calc_redundancy(selected, not_selected)
            else:
                score_redundancy = pd.Series(1.0, index=X.columns)

            self.scores.redundancy = score_redundancy.fillna(0.0)  # will get overwritten on each iteration
            best_feature, best_score = self._get_best_feature(score_relevancy, score_redundancy, not_selected)
            self.scores.combined[best_feature] = best_score  # store
            self.selected_features = self.selected_features.union([best_feature])
            not_selected = not_selected.drop(best_feature)
            selected = selected.union([best_feature])

        self._generate_report()

    def _generate_report(self) -> None:
        super()._generate_report()
        self.report.relevancyMetricReports = [m.report for m in self.relevancy_metrics]
        # there's an edge case here where redundancy isn't called (if n_features == 1)
        try:
            self.report.redundancyMetricReport = self.redundancy_metric.report
        except AttributeError:
            self.report.redundancyMetricReport = None
