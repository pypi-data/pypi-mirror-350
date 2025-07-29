"""
Various feature ranking methods for use in feature selection
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Union

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import MlTask
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Lasso, LogisticRegression, Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, LinearSVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

# ──────────────────────────────────────────────────────────────────────────── #


def _handle_zero(val: Union[int, float]) -> Union[int, float]:
    """Handle zero values in denominator"""
    return 1 if val == 0 else val


def rf_feature_ranking(ml_task: MlTask, x_np: np.ndarray, y_np: np.ndarray) -> np.ndarray:
    """Random forest feature ranking
    Args:
        ml_task:
            ML task
        x_np:
            Feature matrix
        y_np:
            Target vector
    Returns:
        Feature importance vector
    """
    if ml_task == MlTask.classification:
        rf_model = RandomForestClassifier(random_state=1, n_estimators=100, max_depth=4)
    elif ml_task == MlTask.regression:
        rf_model = RandomForestRegressor(random_state=1, n_estimators=100, max_depth=4)
    else:
        raise NotImplementedError(f"Unsupported ML task: {ml_task}")
    rf_model.fit(x_np, y_np)
    feature_importances = np.abs(rf_model.feature_importances_)
    return feature_importances / _handle_zero(np.sum(feature_importances))


def lr_feature_ranking(ml_task: MlTask, x_np: np.ndarray, y_np: np.ndarray) -> np.ndarray:
    """Linear feature ranking
    Args:
        ml_task:
            ML task
        x_np:
            Feature matrix
        y_np:
            Target vector
    Returns:
        Feature importance vector
    """
    if ml_task == MlTask.classification:
        # Other options: use l1 with threshold level=1e-5
        lr_model = LogisticRegression(penalty="l2", C=1.0, random_state=1, solver="lbfgs", multi_class="multinomial")
    elif ml_task == MlTask.regression:
        lr_model = Lasso(alpha=1.0)
    else:
        raise NotImplementedError(f"Unsupported ML task: {ml_task}")
    lr_model.fit(x_np, y_np)
    coefs = np.abs(lr_model.coef_)
    if coefs.ndim > 1:
        coefs = coefs.mean(axis=0)
    return coefs / _handle_zero(np.sum(coefs))


def gbm_feature_ranking(ml_task: MlTask, x_np: np.ndarray, y_np: np.ndarray) -> np.ndarray:
    """Gradient boosting machine feature ranking.
    Args:
        ml_task:
            ML task.
        x_np:
            Feature matrix.
        y_np:
            Target vector.
    Returns:
        np.array:
            Feature importance vector.
    """
    if ml_task == MlTask.classification:
        gbm_model = LGBMClassifier(random_state=1, n_estimators=100, max_depth=4)
    elif ml_task == MlTask.regression:
        gbm_model = LGBMRegressor(random_state=1, n_estimators=100, max_depth=4)
    else:
        raise NotImplementedError(f"Unsupported ML task: {ml_task}")
    gbm_model.fit(x_np, y_np)
    feature_importances = gbm_model.feature_importances_
    return feature_importances / _handle_zero(np.sum(feature_importances))


def svm_feature_ranking(ml_task: MlTask, x_np: np.ndarray, y_np: np.ndarray) -> np.ndarray:
    """Support vector machine feature ranking
    Args:
        ml_task:
            ML task.
        x_np:
            Feature matrix.
        y_np:
            Target vector.
    Returns:
        np.array:
            Feature importance vector.
    """
    if ml_task == MlTask.classification:
        svm_model = LinearSVC(penalty="l1", dual=False, random_state=1)
    elif ml_task == MlTask.regression:
        svm_model = LinearSVR(loss="epsilon_insensitive", random_state=1)
    else:
        raise NotImplementedError(f"Unsupported ML task: {ml_task}")
    svm_model.fit(x_np, y_np)
    coefs = np.abs(svm_model.coef_)
    return coefs / _handle_zero(np.sum(coefs))


def tree_feature_ranking(ml_task: MlTask, x_np: np.ndarray, y_np: np.ndarray) -> np.ndarray:
    """Decision tree feature ranking
    Args:
        ml_task:
            ML task.
        x_np:
            Feature matrix.
        y_np:
            Target vector.
    Returns:
        np.array:
            Feature importance vector.
    """
    if ml_task == MlTask.classification:
        tree_model = DecisionTreeClassifier(criterion="entropy", max_depth=None, random_state=1)
    elif ml_task == MlTask.regression:
        tree_model = DecisionTreeRegressor(random_state=0)
    else:
        raise NotImplementedError(f"Unsupported ML task: {ml_task}")
    tree_model.fit(x_np, y_np)
    feature_importances = tree_model.feature_importances_
    return np.abs(feature_importances) / _handle_zero(np.sum(np.abs(feature_importances)))
