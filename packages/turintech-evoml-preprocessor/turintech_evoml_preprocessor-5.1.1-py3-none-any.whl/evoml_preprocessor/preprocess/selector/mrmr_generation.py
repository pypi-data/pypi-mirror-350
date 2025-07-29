import logging
from typing import Dict, Optional

import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import Aggregation, SelectionMetric
from evoml_preprocessor.preprocess.selector.selector import MrmrSelector
from evoml_preprocessor.preprocess.selector.util import SelectorParameters, SingleSelectionMetric, aggregate

logger = logging.getLogger("preprocessor")


class MrmrGenerationSelector(MrmrSelector):

    feature_lengths: Optional[Dict[str, int]]

    def __init__(self, parameters: SelectorParameters, feature_lengths: Optional[Dict[str, int]] = None):
        super().__init__(parameters)
        self.feature_lengths = feature_lengths

    @classmethod
    def default(cls, ml_task: MlTask) -> "MrmrGenerationSelector":
        return cls(
            SelectorParameters(
                relevancy=[SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.F_TEST)],
                redundancy=SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON),
            )
        )

    def calc_relevancy(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        """Modifies the relevancy calculation to take into account the
        feature complexity.

        During feature generation, we can calculate the length of each
        feature. Original features have a length of 1. The length of the
        geneated feature is the number of operations plus the number of times
        features are used.

        Examples:
        1. A + B -> 3
        2. A + A + B -> 5
        3. A ** 2 + B -> 4

        This is used to penalize features that are too complex. The relevancy
        score is multiplied by some factor in the range (0.85, 1) depending on
        the complexity.

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target

        Returns:
            pd.Series:
                The relevancy scores
        """
        if self.feature_lengths is None:
            logger.warning("No generated feature information found, using default relevancy calculation")
            return super().calc_relevancy(X, y)

        features = X.columns
        relevancy_scores = pd.DataFrame(0.001, index=features, columns=[m.name for m in self.relevancy_metrics])
        for m in self.relevancy_metrics:
            relevancy_scores[m.name] = m.evaluate(X, y)
        relevancy_scores_agg = aggregate(relevancy_scores, self.relevancy_aggregation) ** 0.6
        feature_lengths = pd.Series(self.feature_lengths)
        return relevancy_scores_agg * feature_lengths.apply(lambda x: 1 if x < 9 else max(0.75, 1 - (x - 9) / 40))
