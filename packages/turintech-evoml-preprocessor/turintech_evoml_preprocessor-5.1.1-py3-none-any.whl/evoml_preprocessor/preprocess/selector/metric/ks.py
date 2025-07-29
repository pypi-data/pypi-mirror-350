import pandas as pd
from evoml_api_models import MlTask
from scipy.stats import ks_2samp

from evoml_preprocessor.preprocess.selector.metric import Metric
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType
from evoml_preprocessor.search.decorators import normalize


class KSRelevancyMetric(Metric):
    def __init__(self, parameters: MetricParameters):
        """Kolmogorov-Smirnov metric

        This is a wrapper around the scipy ks_2samp function. It returns the
        ks statistic for each feature. This is similar to the f-test metric.

        Args:
            parameters: the metric parameters
        """
        if parameters.ml_task != MlTask.classification:
            raise ValueError("ml task unsuitable for this metric")
        super().__init__(parameters)
        self._metric_type = MetricType.FILTER

    @property
    def name(self) -> str:
        return "kolmogorov-smirnov"

    @normalize
    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        ks_results = [0.0] * len(X.columns)
        for i, col in enumerate(X.columns):
            ks_col = [ks_2samp(X.loc[y == cval, col], X.loc[y != cval, col])[0] for cval in y.unique()]
            ks_results[i] = sum(ks_col) / len(ks_col)
        return pd.Series(ks_results, index=X.columns)
