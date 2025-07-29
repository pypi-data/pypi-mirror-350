import pandas as pd
from evoml_api_models import MlTask
from sklearn.feature_selection import f_classif, f_regression

from evoml_preprocessor.preprocess.selector.metric import Metric
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType
from evoml_preprocessor.search.decorators import normalize


class FTestMetric(Metric):
    def __init__(self, parameters: MetricParameters):
        """F-test metric

        This is a wrapper around the sklearn f-test functions. It returns the
        f-test score for each feature. For classification, this is the ANOVA
        F-value between the label for each sample and the feature. For
        regression, it is a modification of the pearson correlation. This is
        another simple and fast metric, typically used as a relevancy metric
        in MRMR.

        Args:
            parameters: the metric parameters
        """
        if parameters.ml_task not in {MlTask.classification, MlTask.regression}:
            raise ValueError("ml task unsuitable for this metric")
        super().__init__(parameters)
        self._metric_type = MetricType.FILTER

    @property
    def name(self) -> str:
        return "f-test"

    @normalize
    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        return (
            pd.Series(f_classif(X, y)[0], index=X.columns)
            if self.ml_task == MlTask.classification
            else pd.Series(f_regression(X, y)[0], index=X.columns)
        )
