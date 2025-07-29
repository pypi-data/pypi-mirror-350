import pandas as pd
from evoml_api_models import MlTask
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

from evoml_preprocessor.preprocess.selector.metric import Metric
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType
from evoml_preprocessor.search.decorators import normalize


class MutualInformationMetric(Metric):
    def __init__(self, parameters: MetricParameters):
        """Mutual information metric

        This is a wrapper around the sklearn mutual information functions.
        It returns the mutual information score for each feature. This is
        more expensive to compute and benchmarking tests suggest that it does
        not perform as well as the other metrics either.

        Args:
            parameters: the metric parameters
        """
        if parameters.ml_task not in {MlTask.classification, MlTask.regression}:
            raise ValueError("ml task unsuitable for this metric")
        super().__init__(parameters)
        self._metric_type = MetricType.FILTER

    @property
    def name(self) -> str:
        return "mutual-information"

    @normalize
    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        def evaluate_feature(feature: pd.DataFrame, y: pd.Series) -> float:
            # This makes a copy local to the parallel job while memory inefficient,
            # this avoids corruption from other jobs
            if self.ml_task == MlTask.classification:
                return mutual_info_classif(feature.to_frame(), y)[0]
            else:  # regression
                return mutual_info_regression(feature.to_frame(), y)[0]

        return X.apply(lambda col: evaluate_feature(col, y)).fillna(0.0)
