from typing import Optional

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.selector.models import MetricReport
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType
from evoml_preprocessor.utils.exceptions import NotInitializedError


class Metric:
    def __init__(self, parameters: MetricParameters):
        """Scores one feature against many to produce a set of scores.

        A metric takes in the feature set and the target column and computes a
        score for each feature. If the target here is the target for the ml
        task, the `ml_task` parameter choice is important. Scores are computed
        in `evaluate` and returned as a pandas series of shape (N) where N
        is the number of features.

        Args:
            parameters (MetricParameters): The parameters for the metric
        """
        self._ml_task = parameters.ml_task
        self._report: Optional[MetricReport] = None
        self._metric_type = None

    @classmethod
    def default(cls, ml_task: Optional[MlTask] = None) -> "Metric":
        return cls(MetricParameters(ml_task=ml_task))

    @property
    def ml_task(self) -> MlTask:
        if self._ml_task is None:
            raise NotInitializedError
        return self._ml_task

    @property
    def report(self) -> MetricReport:
        if self._report is None:
            raise AttributeError("Report has not been generated yet, run `evaluate` first")
        return self._report

    @property
    def name(self) -> str:
        return "base"

    @property
    def metric_type(self) -> MetricType:
        if self._metric_type is None:
            raise NotInitializedError
        return self._metric_type

    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        raise NotImplementedError

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        """Evaluate the metric on the feature set and target column.

        Note that no validation is done on the incoming data, since it is
        assumed that this has been checked earlier in the pipeline. MlTask
        should be consistent throughout the preprocessor, and match to the value
        stored here.

        Args:
            X (pd.DataFrame): The feature set
            y (pd.Series): The target column

        Returns:
            pd.Series: The metric scores for each feature
        """
        if self._report is None:
            self._report = MetricReport()
        scores = self._evaluate(X, y)
        self.report.name = self.name
        self.report.scores = scores.to_dict()
        return scores

    def matrix_evaluate(self, arr: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def matrix_evaluate_numpy(self, arr: pd.DataFrame, other: pd.DataFrame) -> np.ndarray:
        raise NotImplementedError
