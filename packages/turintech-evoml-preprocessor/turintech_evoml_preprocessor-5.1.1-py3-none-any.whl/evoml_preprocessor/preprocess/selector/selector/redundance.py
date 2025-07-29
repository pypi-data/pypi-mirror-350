import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import SelectionMetric, SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import FLOOR, SelectorParameters, SingleSelectionMetric, aggregate


class RedundanceSelector(Selector):
    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self._report = SelectionMethodReport(method=SelectorType.REDUNDANCE)

    @classmethod
    def default(cls, ml_task: MlTask) -> "RedundanceSelector":
        return cls(
            SelectorParameters(
                redundancy=SingleSelectionMetric.from_selector(ml_task, metric=SelectionMetric.PEARSON),
            )
        )

    @property
    def name(self) -> str:
        return "redundancy"

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit redundance filter selector

        This performs the following steps:
        1. Calculate redundance scores for each feature in X using the
        redundance metric
        2. Aggregate the redundance scores using the redundance aggregation
        option

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target
            n (int):
                The number of features to select
        """
        self.init_fit(X, y, n)
        redundancy = self.redundancy_metric.matrix_evaluate(X)

        scores = aggregate(redundancy, self.redundancy_aggregation)
        self.scores.redundancy_agg = scores
        self.scores.combined = scores

        self.selected_features = scores.nsmallest(n).index

        self._generate_report()

    def _generate_report(self) -> None:
        super()._generate_report()
        self.report.redundancyMetricReport = None
