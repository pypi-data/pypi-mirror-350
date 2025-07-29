import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import SelectionMetric, SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import (
    FLOOR,
    SelectorParameters,
    SingleSelectionMetric,
    aggregate,
    minmax_series,
)


class LinearSelector(Selector):
    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self._report = SelectionMethodReport(method=SelectorType.LINEAR)
        self.redundancy_weight: float = parameters.redundancy_weight

    @classmethod
    def default(cls, ml_task: MlTask) -> "LinearSelector":
        return cls(
            SelectorParameters(
                relevancy=SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON),
                redundancy=SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON),
            )
        )

    @property
    def name(self) -> str:
        return "linear"

    def calc_relevancy(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        """Calculate relevancy scores for each feature in X

        This is an internal helper method for `fit`

        Each relevancy metric is evaluated for each feature in X and the
        relevancy scores are aggregated using the relevancy aggregation
        option.

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target

        Returns:
            pd.Series:
                The relevancy scores for each feature
        """
        features = X.columns
        relevancy_scores = pd.DataFrame(FLOOR, index=features, columns=[m.name for m in self.relevancy_metrics])
        for m in self.relevancy_metrics:
            relevancy_scores[m.name] = m.evaluate(X, y)
        return aggregate(relevancy_scores, self.relevancy_aggregation)

    def calc_redundancy(self, X: pd.DataFrame) -> pd.Series:
        """Calculate redundancy scores for each feature in X

        This is an internal helper method for `fit`

        The redundancy metric is evaluated for each pair of features in X and
        the redundancy scores are aggregated using the redundancy aggregation

        Args:
            X (pd.DataFrame):
                The features

        Returns:
            pd.Series:
                The redundancy scores for each feature
        """
        redundancy_scores = self.redundancy_metric.matrix_evaluate(X)
        return aggregate(redundancy_scores, self.redundancy_aggregation)

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit linear filter selector

        This performs the following steps:
        1. Calculate relevancy scores for each feature in X using the relevancy
        metrics
        2. Calculate redundancy scores for each feature in X using the
        redundancy metric
        3. Calculate the final score for each feature by taking a linear
        combination of the relevancy and redundancy scores
        4. Select the top n features with the highest scores

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target
            n (int):
                The number of features to select
        """
        self.init_fit(X, y, n)
        relevance_scores = minmax_series(self.calc_relevancy(X, y))
        self.scores.relevancy = relevance_scores  # store
        redundance_scores = minmax_series(self.calc_redundancy(X))
        self.scores.redundancy = redundance_scores  # store
        scores = relevance_scores - redundance_scores * self.redundancy_weight
        self.scores.combined = scores  # store
        self.selected_features = scores.nlargest(n).index

        self._generate_report()

    def _generate_report(self) -> None:
        super()._generate_report()
        self.report.relevancyMetricReports = [m.report for m in self.relevancy_metrics]
        self.report.redundancyMetricReport = None
