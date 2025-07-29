from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.selector.metric import (
    ConstantMetric,
    Metric,
    build_redundancy_metric,
    build_relevancy_metric,
)
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.util import SelectorParameters


@dataclass
class SelectorScores:
    """Container for scores from a selector.

    This is used to store the scores from a selector, and the breakdown
    in terms of relevancy and redundancy scores.

    The `combined` score is the final score used for this selector.
    The `redunancy` score is an aggregate of the redundancy scores
    """

    relevancy: pd.Series
    redundancy: pd.Series
    combined: pd.Series

    @classmethod
    def empty(cls, features: pd.Index) -> "SelectorScores":
        return cls(
            relevancy=pd.Series(0, index=features),
            redundancy=pd.Series(0, index=features),
            combined=pd.Series(0, index=features),
        )

    def save(self) -> Dict[str, float]:
        return self.combined.to_dict()


class Selector:
    def __init__(
        self,
        parameters: SelectorParameters,
        rng: np.random.Generator = np.random.default_rng(42),
    ) -> None:
        """Selector base class.

        This is used to define atomic and composite
        feature selection methods. Defines an interface for feature selection
        that provides public `fit`, `transform`, and `fit_transform` methods.

        This also contains some internal init methods that are used on
        construction to convert the options into metric objects, so they
        can be used in the `fit` method.

        Args:
            parameters (SelectorParameters):
                Options for feature selection, currently a container for
                all options, not just ones specific for this selector
            rng (np.random.Generator):
                Optional random number generator, used for certain selectors /
                metrics
        """
        self.rng = rng
        self.fitted_features: pd.Index = pd.Index([])
        self.selected_features: pd.Index = pd.Index([])
        self._report: Optional[SelectionMethodReport] = None
        self._scores: Optional[SelectorScores] = None
        self._relevancy_metrics: Optional[List[Metric]] = (
            [build_relevancy_metric(metric.metric, metric.parameters) for metric in parameters.relevancy]
            if parameters.relevancy is not None
            else [ConstantMetric.default()]
        )
        self._redundancy_metric: Optional[Metric] = (
            build_redundancy_metric(parameters.redundancy.metric, parameters.redundancy.parameters)
            if parameters.redundancy is not None
            else ConstantMetric.default()
        )
        self.relevancy_aggregation = parameters.relevancy_aggregation
        self.redundancy_aggregation = parameters.redundancy_aggregation
        self.parallel: bool = parameters.parallel

    @classmethod
    def default(cls, ml_task: MlTask) -> "Selector":
        return cls(SelectorParameters())

    @property
    def report(self) -> SelectionMethodReport:
        if self._report is None:
            raise AttributeError("Report has not been generated yet, run `fit` first")
        return self._report

    @property
    def scores(self) -> SelectorScores:
        if self._scores is None:
            raise AttributeError("Scores have not been calculated yet, run fit first")
        return self._scores

    @property
    def relevancy_metrics(self) -> List[Metric]:
        if self._relevancy_metrics is None:
            raise AttributeError("Relevancy metrics have not been set.")
        return self._relevancy_metrics

    @property
    def redundancy_metric(self) -> Metric:
        if self._redundancy_metric is None:
            raise AttributeError("Redundancy metric has not been set.")
        return self._redundancy_metric

    @property
    def name(self) -> str:
        raise NotImplementedError

    def init_fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit the selector to the data.

        This is an external method that performs the feature selection.
        Selected features are stored in `self.selected_features`.

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target
            n (int):
                The number of features to select
        """
        self.fitted_features = X.columns
        self.selected_features = self.fitted_features
        self._scores = SelectorScores.empty(self.fitted_features)

        self._report = SelectionMethodReport()
        self.report.nColumnsTarget = n
        self.report.method = f"{self.name}"

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        raise NotImplementedError

    def transform(self, X: pd.DataFrame, inplace: bool = True) -> Optional[pd.DataFrame]:
        """Transform the data.

        This is an external method that applies the feature selection results
        to the data.

        Args:
            X (pd.DataFrame):
                The features
            inplace (bool):
                Whether to perform the transformation in place
        """
        if inplace:
            return X.drop([col for col in X.columns if col not in self.selected_features], axis=1, inplace=True)
        else:
            return X[self.selected_features]

    def fit_transform(self, X: pd.DataFrame, y: pd.Series, n: int, inplace: bool = True) -> Optional[pd.DataFrame]:
        """Fit and transform the data.

        This is an external method that performs the feature selection and
        applies the results to the data.

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target
            n (int):
                The number of features to select
            inplace (bool):
                Whether to perform the transformation in place
        """
        self.fit(X, y, n)
        return self.transform(X, inplace=inplace)

    def _generate_report(self) -> None:
        """Generate report for the feature selection process.

        Currently, this method only describes the overall pipeline.
        It does not break down step by step details.

        Returns:
            SelectionMrmrReport:
                The report
        """
        self.report.method = f"{self.name}"
        self.report.nColumnsSelected = len(self.selected_features)
        self.report.nColumnsRemoved = len(self.fitted_features) - len(self.selected_features)
        self.report.featuresSelected = self.selected_features.tolist()
        self.report.featuresRemoved = self.fitted_features.difference(self.selected_features).tolist()
        self.report.relevancyAggregation = self.relevancy_aggregation
        self.report.redundancyAggregation = self.redundancy_aggregation
        self.report.finalScores = self.scores.combined.to_dict()
