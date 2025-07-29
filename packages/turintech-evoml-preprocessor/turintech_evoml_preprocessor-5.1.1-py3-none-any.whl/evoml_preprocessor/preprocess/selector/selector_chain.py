from typing import Optional

import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import FeatureSelectionOptions
from evoml_preprocessor.preprocess.selector.report_builder import FeatureSelectionReportBuilder
from evoml_preprocessor.preprocess.selector.selector import UnarySelector, build_selector
from evoml_preprocessor.preprocess.selector.util import SelectorChainParameters


class SelectorChain:
    def __init__(self, parameters: SelectorChainParameters):
        """Selector chain, used to chain multiple selectors together.

        This describes the standard pipeline for feature selection in EvoML.
        It takes a list of selectors and applies them sequentially.

        Args:
            parameters (SelectorChainParameters): Parameters for the selector
            chain.
        """
        self.selectors = [build_selector(step.selector, step.parameters) for step in parameters.steps]
        self.weights = [step.weight for step in parameters.steps]
        self.report_builder = FeatureSelectionReportBuilder()
        self.selected_features = pd.Index([])

    @classmethod
    def from_selection_options(cls, ml_task: MlTask, selection_options: FeatureSelectionOptions) -> "SelectorChain":
        """Build a selector chain from a FeatureSelectionOptions object.

        This is a convenience method for building a selector chain from the
        user provided options. These options are converted into internal
        parameters, which are designed to be more flexible.

        Args:
            ml_task: The ML task
            selection_options: The user provided options

        Returns:
            A selector chain
        """
        parameters = SelectorChainParameters.from_selection_options(ml_task, selection_options)
        return cls(parameters)

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Fit the selector chain, storing the results in a report.

        Args:
            X: The features
            y: The target
            n: Number of features to select
        """
        self.report_builder.add_original_data(X.columns)
        if len(self.selectors) == 0:
            return

        nx = len(X.columns)
        for i, selector in enumerate(self.selectors[:-1]):
            target_n = int(nx - (nx - n) * self.weights[i])
            if isinstance(selector, UnarySelector):
                target_n = 0
            X_tmp = selector.fit_transform(X, y, target_n, inplace=False)
            if X_tmp is None:
                raise ValueError("fit_transform should return a pandas DataFrame when inplace is False.")
            X = X_tmp
            self.report_builder.add_selector(selector.report)
            nx = len(X.columns)

        self.selectors[-1].fit(X, y, n)
        self.selected_features = self.selectors[-1].selected_features
        self.report_builder.add_selector(self.selectors[-1].report)
        self.report_builder.add_selected_data(self.selected_features)

    def transform(self, X: pd.DataFrame, inplace: bool = True) -> Optional[pd.DataFrame]:
        """Transform the data using the results from `fit`.

        Args:
            X: The features
            inplace: Whether to perform the transformation in place

        Returns:
            The transformed data if `inplace` is True, otherwise `X` is updated.
        """
        for selector in self.selectors:
            if not inplace:
                X = selector.transform(X, inplace=False)
            else:
                selector.transform(X, inplace=inplace)

        return X

    def fit_transform(self, X: pd.DataFrame, y: pd.Series, n: int, inplace: bool = True) -> Optional[pd.DataFrame]:
        """Fit and transform the data.

        Args:
            X: The features
            y: The target
            n: Number of features to select
            inplace: Whether to perform the transformation in place

        Returns:
            The transformed data if `inplace` is True, otherwise `X` is updated.
        """
        self.fit(X, y, n)
        return self.transform(X, inplace=inplace)
