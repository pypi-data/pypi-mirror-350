from __future__ import annotations

from enum import Enum
from typing import Any

from lightgbm import LGBMClassifier, LGBMRegressor
from lightning.impl.adagrad import AdaGradClassifier, AdaGradRegressor
from lightning.impl.sag import SAGClassifier, SAGRegressor
from lightning.impl.sdca import SDCAClassifier
from lightning.impl.svrg import SVRGClassifier
from mlxtend.classifier import EnsembleVoteClassifier
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.linear_model import ElasticNet, Ridge, RidgeClassifier, SGDClassifier, SGDRegressor
from sklearn.neighbors import KNeighborsRegressor, NearestCentroid, RadiusNeighborsClassifier, RadiusNeighborsRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.semi_supervised import LabelPropagation
from sklearn.svm import SVR, LinearSVR
from sklearn.tree import ExtraTreeClassifier

from evoml_preprocessor.utils.string_enum import StrEnum


class RepresentativeModelClf(StrEnum):
    """Represents models for classification tasks.
    Args:
        name (str):
            Name of the model.
        model (Any):
            The model.
    Returns:
        RepresentativeModelClf:
            The representative model.
    """

    name: str
    model: Any

    def __new__(cls, name: str, model: Any) -> RepresentativeModelClf:
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.model = model
        return obj

    RIDGE_CLASSIFIER = ("ridge_classifier", RidgeClassifier(alpha=0.1, max_iter=100, tol=3.16, solver="sparse_cg"))
    SAG_CLASSIFIER = (
        "sag_classifier",
        SAGClassifier(
            eta="line-search",
            alpha=0.1,
            beta=0.01,
            loss="smooth_hinge",
            gamma=1.0,
            max_iter=300,
            tol=0.001,
            random_state=42,
        ),
    )
    SGD_CLASSIFIER = (
        "sgd_classifier",
        SGDClassifier(loss="log_loss", penalty="elasticnet", alpha=1.0, l1_ratio=0.0, max_iter=100, tol=0.0001),
    )
    SDCA_CLASSIFIER = (
        "sdca_classifier",
        SDCAClassifier(alpha=1.0, l1_ratio=0.1, loss="squared", max_iter=300, tol=0.0001),
    )
    SVRG_CLASSIFIER = (
        "svrg_classifier",
        SVRGClassifier(eta=0.1, alpha=0.01, n_inner=0.01, loss="log", max_iter=300, tol=0.01),
    )
    EXTRA_TREE_CLASSIFIER = (
        "extra_tree_classifier",
        ExtraTreeClassifier(
            criterion="gini",
            splitter="best",
            max_depth=None,
            min_weight_fraction_leaf=0.0,
            ccp_alpha=0.0,
            min_impurity_decrease=0.1,
        ),
    )
    ADAGRAD_CLASSIFIER = (
        "adagrad_classifier",
        AdaGradClassifier(eta=0.1, alpha=0.01, l1_ratio=1, loss="modified_huber", n_iter=10),
    )
    GRADIENT_BOOSTING_CLASSIFIER = (
        "lightgbm_classifier",
        LGBMClassifier(
            boosting_type="gbdt",
            max_depth=5,
            n_estimators=50,
            reg_alpha=0.1,
            reg_lambda=1.0,
        ),
    )
    ENSEMBLE_VOTE_CLASSIFIER = (
        "ensemble_vote_classifier",
        EnsembleVoteClassifier(
            clfs=[RandomForestClassifier(), MLPClassifier()],
            voting="hard",
            weights=None,
            verbose=0,
            use_clones=True,
            fit_base_estimators=True,
        ),
    )
    RADIUS_NEIGHBORS_CLASSIFIER = (
        "radius_neighbors_classifier",
        RadiusNeighborsClassifier(
            radius=1.0, weights="uniform", algorithm="auto", leaf_size=5, metric="minkowski", p=4
        ),
    )
    NEAREST_CENTROID_CLASSIFIER = ("nearest_centroid_classifier", NearestCentroid(shrink_threshold=0.1))
    LABEL_PROPAGATION_CLASSIFIER = (
        "label_propagation_classifier",
        LabelPropagation(kernel="knn", n_neighbors=9, max_iter=500, tol=0.001),
    )


class RepresentativeModelReg(StrEnum):
    """Representative models for regression tasks.
    Args:
        name (str):
            The name of the model.
        model (Any):
            The model.
    Returns:
        RepresentativeModelReg:
            The representative model.
    """

    name: str
    model: Any

    def __new__(cls, name: str, model: Any) -> RepresentativeModelReg:
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.model = model
        return obj

    ELASTIC_NET_REGRESSION = (
        "elastic_net_regressor",
        ElasticNet(
            alpha=10.0, l1_ratio=0.5, fit_intercept=False, max_iter=100, tol=0.001, positive=True, selection="cyclic"
        ),
    )
    RIDGE_REGRESSION = (
        "ridge_regressor",
        Ridge(alpha=1.0, fit_intercept=True, solver="lsqr"),
    )
    SGD_EPSILON_REGRESSION = (
        "sgd_epsilon_regressor",
        SGDRegressor(
            loss="epsilon_insensitive",
            penalty="l1",
            alpha=0.0001,
            epsilon=1.0,
            learning_rate="constant",
            eta0=0.01,
            max_iter=100,
        ),
    )
    SGD_HUBER_REGRESSION = (
        "sgd_huber_regressor",
        SGDRegressor(
            loss="huber", penalty="l1", alpha=0.0001, epsilon=1.0, learning_rate="constant", eta0=0.01, max_iter=100
        ),
    )
    LINEARSVR_REGRESSION = (
        "linearsvr_regressor",
        LinearSVR(
            epsilon=0.1, C=0.1, fit_intercept=True, intercept_scaling=1.0, loss="epsilon_insensitive", max_iter=1000
        ),
    )
    SAG_REGRESSION = (
        "sag_regressor",
        SAGRegressor(eta="auto", alpha=1.0, beta=0.001, loss="smooth_hinge", gamma=0.001, max_iter=30, tol=0.01),
    )
    SVR_REGRESSION = ("svr_regressor", SVR(C=0.1, kernel="poly", degree=2, coef0=0.1, epsilon=0.1, max_iter=200))
    GRADIENT_BOOSTING_REGRESSION = (
        "gradient_boosting_regressor",
        GradientBoostingRegressor(
            loss="huber", criterion="friedman_mse", learning_rate=0.5, max_depth=3, n_iter_no_change=10
        ),
    )
    LIGHTGBM_REGRESSION = (
        "lightgbm_regressor",
        LGBMRegressor(
            boosting_type="gbdt", num_leaves=10, max_depth=6, n_estimators=100, reg_alpha=0.1, reg_lambda=0.1
        ),
    )
    ADAGRAD_REGRESSION = (
        "adagrad_regressor",
        AdaGradRegressor(eta=0.1, alpha=1.0, l1_ratio=0.2, loss="huber", epsilon=1.0),
    )
    KNEIGHBORS_REGRESSION = (
        "kneighbors_regressor",
        KNeighborsRegressor(n_neighbors=10, weights="distance", algorithm="auto", leaf_size=5, p=2),
    )
    RADIUS_NEIGHBORS_REGRESSION = (
        "radius_neighbors_regressor",
        RadiusNeighborsRegressor(
            radius=1e100, weights="distance", algorithm="auto", leaf_size=5, metric="minkowski", p=2
        ),
    )
