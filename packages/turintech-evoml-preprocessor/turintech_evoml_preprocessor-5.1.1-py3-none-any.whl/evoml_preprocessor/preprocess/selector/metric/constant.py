import pandas as pd

from evoml_preprocessor.preprocess.selector.metric import Metric
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType


class ConstantMetric(Metric):
    def __init__(self, parameters: MetricParameters):
        """Constant metric
        This metric can be used as a null option for a particular selector. For
        example, if a linear selector has a constant redundancy metric, then it
        becomes a simple relevancy filter selector. This is useful for
        flexibility of the API.

        Args:
            parameters: the metric parameters
        """
        super().__init__(parameters)
        self.metric = parameters.metric
        self.constant = 1.0
        self._metric_type = MetricType.NONE

    @property
    def name(self) -> str:
        return "constant"

    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        return pd.Series(self.constant, index=X.columns)

    def matrix_evaluate(self, arr: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame(self.constant, columns=arr.columns, index=arr.columns)
