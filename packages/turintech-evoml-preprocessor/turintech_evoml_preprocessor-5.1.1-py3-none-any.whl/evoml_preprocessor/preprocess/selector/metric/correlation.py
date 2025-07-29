from math import prod

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from evoml_preprocessor.preprocess.models import SelectionMetric
from evoml_preprocessor.preprocess.selector.metric import Metric
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType


class CorrelationMetric(Metric):
    def __init__(self, parameters: MetricParameters):
        """Correlation metric

        This metric is a wrapper around the pandas correlation function. It
        returns the absolute value of the correlation between each feature and
        the target. This is not the best measure of feature usefulness, but
        it is a simple and fast metric, so is quite ideal for redundancy
        calculations.

        Args:
            parameters: the metric parameters
        """
        super().__init__(parameters)
        self.metric = parameters.metric
        self._metric_type = MetricType.FILTER

    @property
    def name(self) -> str:
        return f"{self.metric.value} correlation"

    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        if self.metric in {SelectionMetric.PEARSON, SelectionMetric.SPEARMAN}:
            # @pyright: doesn't recognise that self.metric.value is guaranteed to be of type Literal["pearson", "spearman"]
            return X.corrwith(other=y, method=self.metric.value).fillna(0).abs()  # type: ignore
        raise ValueError("correlation method not recognized")

    def self_corr_pandas(self, arr: pd.DataFrame) -> pd.DataFrame:
        if self.metric in {SelectionMetric.PEARSON, SelectionMetric.SPEARMAN}:
            # @pyright: doesn't recognise that self.metric.value is guaranteed to be of type Literal["pearson", "spearman"]
            return arr.corr(method=self.metric.value).fillna(0).abs()  # type: ignore
        raise ValueError("correlation method not recognized")

    def self_corr_numpy(self, arr: pd.DataFrame) -> pd.DataFrame:
        # this has been tested to be faster than the pandas implementation for large matrices
        if self.metric == SelectionMetric.SPEARMAN:
            arr = arr.apply(rankdata, axis=0)
        elif self.metric != SelectionMetric.PEARSON:
            raise NotImplementedError("only pearson correlation is implemented")

        arr_np = arr.to_numpy(dtype=np.float64)
        arr_np -= arr_np.mean(axis=0)
        arr_np /= arr_np.std(axis=0)

        return pd.DataFrame(np.abs(np.dot(arr_np.T, arr_np)) / arr.shape[0], index=arr.columns, columns=arr.columns)

    def matrix_evaluate(self, arr: pd.DataFrame) -> pd.DataFrame:
        size_threshold = 500_000

        if prod(arr.shape) > size_threshold:
            return self.self_corr_numpy(arr)
        return self.self_corr_pandas(arr)

    def matrix_evaluate_numpy(self, arr: pd.DataFrame, other: pd.DataFrame) -> np.ndarray:
        """This is a numpy implementation of the pandas `corr` function

        It is a little slower overall than the pandas implementation, possibly
        due to the overhead of converting to numpy arrays. However, it is
        capable of performing a sampled correlation calculation, which can
        be useful for datasets with a large number of features and should work
        quite easily with QPFS with nystrom sampling.

        Args:
            arr (pd.DataFrame): the first DataFrame.
            other (pd.DataFrame): the second DataFrame.

        Returns:
            np.ndarray: the correlation matrix.

        """
        if self.metric == SelectionMetric.SPEARMAN:
            arr = arr.apply(rankdata, axis=0)
            other = other.apply(rankdata, axis=0)
        elif self.metric != SelectionMetric.PEARSON:
            raise NotImplementedError("only pearson correlation is implemented")

        arr = arr.to_numpy(dtype=np.float64)
        arr -= arr.mean(axis=0)
        arr /= arr.std(axis=0)

        other = other.to_numpy(dtype=np.float64)
        other -= other.mean(axis=0)
        other /= other.std(axis=0)

        return np.abs(np.dot(other.T, arr)) / arr.shape[0]
