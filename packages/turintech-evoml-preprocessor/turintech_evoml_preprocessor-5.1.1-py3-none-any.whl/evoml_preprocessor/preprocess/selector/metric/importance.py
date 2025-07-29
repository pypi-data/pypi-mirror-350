import numpy as np
import pandas as pd
from typing import Iterable
from evoml_api_models import MlTask
from sklearn.utils import resample

from evoml_preprocessor.preprocess.models import ModelOption
from evoml_preprocessor.preprocess.selector.metric import Metric
from evoml_preprocessor.preprocess.selector.ranking import (
    gbm_feature_ranking,
    lr_feature_ranking,
    rf_feature_ranking,
    svm_feature_ranking,
    tree_feature_ranking,
)
from evoml_preprocessor.preprocess.selector.util import MetricParameters, MetricType
from evoml_preprocessor.search.decorators import normalize


class FeatureImportanceMetric(Metric):
    def __init__(self, parameters: MetricParameters):
        """Feature importance metric

        This is a wrapper around the sklearn feature importance functions.
        It returns the feature importance score for each feature. Since this is
        a supervised metric, it is more expensive to compute but typically
        yields more helpful results. Another issue is that it can overfit to
        the model used to compute the feature importance. One way to mitigate
        this is to use multiple models, potentially coupled with bootstrapping
        the data.

        Args:
            parameters: contains all useful feature importance metric parameters
        """
        if parameters.ml_task not in {MlTask.classification, MlTask.regression}:
            raise ValueError("ml task unsuitable for this metric")
        super().__init__(parameters)
        self._metric_type = MetricType.WRAPPER

        self.model = parameters.model
        self.subsample = 1.0 if parameters.subsample is None else parameters.subsample
        self.n_subsamples = 1 if parameters.n_subsamples is None else parameters.n_subsamples
        self.sample_with_replacement = (
            parameters.sample_with_replacement if parameters.sample_with_replacement is not None else False
        )
        self.rng = parameters.rng

    @property
    def name(self) -> str:
        return "feature-importance"

    def importances(self, X: pd.DataFrame, y: pd.Series) -> np.ndarray:
        if self.model == ModelOption.LINEAR:
            return lr_feature_ranking(self.ml_task, X.to_numpy(), y.to_numpy())
        elif self.model == ModelOption.TREE:
            return tree_feature_ranking(self.ml_task, X.to_numpy(), y.to_numpy())
        elif self.model == ModelOption.RANDOM_FOREST:
            return rf_feature_ranking(self.ml_task, X.to_numpy(), y.to_numpy())
        elif self.model == ModelOption.GRADIENT_BOOSTING:
            return gbm_feature_ranking(self.ml_task, X.to_numpy(), y.to_numpy())
        elif self.model == ModelOption.SUPPORT_VECTOR_MACHINE:
            return svm_feature_ranking(self.ml_task, X.to_numpy(), y.to_numpy())
        else:
            raise ValueError("Unknown model")

    @normalize
    def _evaluate(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:

        # quick preprocess on data to remove NaN
        n_features = len(X.columns)  # number of features
        importances = np.zeros((self.n_subsamples, n_features), dtype=float)
        seeds = self.rng.integers(1, 1000000, self.n_subsamples)

        for j in range(self.n_subsamples):
            if self.subsample == 1.0:
                x_sub, y_sub = X, y
            else:
                n_samples = int(self.subsample * len(X))
                x_sub, y_sub = resample(
                    X,
                    y,
                    replace=self.sample_with_replacement,
                    n_samples=n_samples,
                    random_state=seeds[j],
                    stratify=y,
                )
            if not isinstance(x_sub, pd.DataFrame):
                raise TypeError(f"x_sub should be a pandas DataFrame. Received: {type(x_sub)}.")
            if not isinstance(y_sub, pd.Series):
                raise TypeError(f"y_sub should be a pandas Series. Received: {type(y_sub)}.")
            importances[j, :] = self.importances(x_sub, y_sub)

        self.report.draw = True
        self.report.wrapper_model = self.model

        return pd.Series(np.nanmean(importances, axis=0), index=X.columns, name="feature_importances")
