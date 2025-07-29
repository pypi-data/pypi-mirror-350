import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import SelectionMetric, SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import MetricType, SelectorParameters, SingleSelectionMetric, aggregate


class RelevanceSelector(Selector):
    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self._report = SelectionMethodReport(method=SelectorType.RELEVANCE)

    @classmethod
    def default(cls, ml_task: MlTask) -> "RelevanceSelector":
        return cls(
            SelectorParameters(
                relevancy=[SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.F_TEST)],
            )
        )

    @property
    def name(self) -> str:
        metric_types = {metric.metric_type for metric in self.relevancy_metrics}
        if metric_types == {MetricType.FILTER}:
            return "relevancy filter"
        if metric_types == {MetricType.WRAPPER}:
            return "relevancy wrapper"
        if metric_types >= {MetricType.FILTER, MetricType.WRAPPER}:
            return "relevancy hybrid"
        return "relevancy"

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit relevancy filter selector

        This performs the following steps:
        1. Calculate relevancy scores for each feature in X using the relevancy
        metrics
        2. Aggregate the relevancy scores using the relevancy aggregation option

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target
            n (int):
                The number of features to select
        """
        self.init_fit(X, y, n)
        scores = pd.DataFrame([], index=X.columns, columns=[metric.name for metric in self.relevancy_metrics])
        for metric in self.relevancy_metrics:
            scores[metric.name] = metric.evaluate(X, y)
        scores_agg = aggregate(scores, self.relevancy_aggregation)
        self.scores.relevancy = scores_agg
        self.scores.combined = scores_agg
        self.selected_features = scores_agg.nlargest(n).index

        self._generate_report()

    def _generate_report(self) -> None:
        super()._generate_report()
        self.report.relevancyMetricReports = [metric.report for metric in self.relevancy_metrics]
