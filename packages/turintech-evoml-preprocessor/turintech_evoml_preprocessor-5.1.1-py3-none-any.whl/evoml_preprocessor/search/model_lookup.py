"""Helping us identify the best model for a given task."""

import logging
from typing import List

from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import ModelOption
from evoml_preprocessor.search.representative_models import RepresentativeModelClf as RCLF
from evoml_preprocessor.search.representative_models import RepresentativeModelReg as RREG

logger = logging.getLogger(__name__)
memory_logger = logging.getLogger("memory")


def model_lookup(config_model: List) -> list:
    """Returns a list of models to be sequentially trained and evaluated.
    Args:
        config_model:
            list of models selected by the user in a trial
    Returns:
        model_list:
            list of models we propose to use for evaluating a group transformations in a search space to identify the best one
    """

    lookup = {
        "fista_classifier": ModelOption.LINEAR,
        "ard_regressor": ModelOption.LINEAR,
        "elastic_net_regressor": ModelOption.LINEAR,
        "elastic_net_cv_regressor": ModelOption.LINEAR,
        "lassolars_regressor": ModelOption.LINEAR,
        "lasso_regressor": ModelOption.LINEAR,
        "lasso_cv_regressor": ModelOption.LINEAR,
        "gpu_lasso_regressor": ModelOption.LINEAR,
        "ridge_regressor": ModelOption.LINEAR,
        "ridge_classifier": ModelOption.LINEAR,
        "kernel_ridge_regressor": ModelOption.LINEAR,
        "gpu_ridge_regressor": ModelOption.LINEAR,
        "ridge_cv_regressor": ModelOption.LINEAR,
        "ridge_cv_classifier": ModelOption.LINEAR,
        "linear_regressor": ModelOption.LINEAR,
        "gpu_linear_regressor": ModelOption.LINEAR,
        "logistic_regression_classifier": ModelOption.LINEAR,
        "logistic_regression_cv_classifier": ModelOption.LINEAR,
        "gpu_logistic_regression_classifier": ModelOption.LINEAR,
        "orthogonal_matching_pursuit_regressor": ModelOption.LINEAR,
        "passive_aggressive_regressor": ModelOption.LINEAR,
        "passive_aggressive_classifier": ModelOption.LINEAR,
        "perceptron_classifier": ModelOption.LINEAR,
        "random_sample_consensus_regressor": ModelOption.LINEAR,
        "sgd_classifier": ModelOption.LINEAR,
        "sgd_regressor": ModelOption.LINEAR,
        "gpu_sgd_regressor": ModelOption.LINEAR,
        "saga_classifier": ModelOption.LINEAR,
        "sag_classifier": ModelOption.LINEAR,
        "sag_regression": ModelOption.LINEAR,
        "linearsvr_regressor": ModelOption.LINEAR,
        "gpu_elastic_net_regressor": ModelOption.LINEAR,
        "gpu_sgd_classifier": ModelOption.LINEAR,
        "fastai_regressor": ModelOption.LINEAR,
        "fastai_classifier": ModelOption.LINEAR,
        "least_angle_regressor": ModelOption.LINEAR,
        "saga_regressor": ModelOption.LINEAR,
        "huber_regressor": ModelOption.LINEAR,
        "fista_regressor": ModelOption.LINEAR,
        "svrg_classifier": ModelOption.LINEAR,
        "pls_regressor": ModelOption.LINEAR,
        "sdca_classifier": ModelOption.LINEAR,
        "sdca_regressor": ModelOption.LINEAR,
        "cd_classifier": ModelOption.LINEAR,
        "cd_regressor": ModelOption.LINEAR,
        "gaussian_process_classifier": ModelOption.LINEAR,
        "gaussian_process_regressor": ModelOption.LINEAR,
        "linear_discriminant_analysis_classifier": ModelOption.LINEAR,
        "kneighbors_classifier": ModelOption.NEAREST_NEIGHBOUR,
        "kneighbors_regressor": ModelOption.NEAREST_NEIGHBOUR,
        "nearest_centroid_classifier": ModelOption.NEAREST_NEIGHBOUR,
        "radius_neighbors_regressor": ModelOption.NEAREST_NEIGHBOUR,
        "radius_neighbors_classifier": ModelOption.NEAREST_NEIGHBOUR,
        "gpu_kneighbors_regressor": ModelOption.NEAREST_NEIGHBOUR,
        "gpu_kneighbors_classifier": ModelOption.NEAREST_NEIGHBOUR,
        "bagging_regressor": ModelOption.RANDOM_FOREST,
        "bagging_classifier": ModelOption.RANDOM_FOREST,
        "stacking_regressor": ModelOption.RANDOM_FOREST,
        "extra_tree_classifier": ModelOption.RANDOM_FOREST,
        "extra_trees_classifier": ModelOption.RANDOM_FOREST,
        "extra_tree_regressor": ModelOption.RANDOM_FOREST,
        "ensemble_vote_classifier": ModelOption.RANDOM_FOREST,
        "catboost_regressor": ModelOption.RANDOM_FOREST,
        "catboost_classifier": ModelOption.RANDOM_FOREST,
        "gpu_catboost_classifier": ModelOption.RANDOM_FOREST,
        "gpu_catboost_regressor": ModelOption.RANDOM_FOREST,
        "adagrad_classifier": ModelOption.RANDOM_FOREST,
        "adagrad_regressor": ModelOption.RANDOM_FOREST,
        "theil_sen_regressor": ModelOption.RANDOM_FOREST,
        "random_forest_regressor": ModelOption.RANDOM_FOREST,
        "random_forest_classifier": ModelOption.RANDOM_FOREST,
        "gpu_random_forest_regressor": ModelOption.RANDOM_FOREST,
        "gpu_random_forest_classifier": ModelOption.RANDOM_FOREST,
        "kernel_svc_classifier": ModelOption.SUPPORT_VECTOR_MACHINE,
        "linearsvc_classifier": ModelOption.SUPPORT_VECTOR_MACHINE,
        "gpu_svr_regressor": ModelOption.SUPPORT_VECTOR_MACHINE,
        "svr_regressor": ModelOption.SUPPORT_VECTOR_MACHINE,
        "svm_classifier": ModelOption.SUPPORT_VECTOR_MACHINE,
        "nusvc_classifier": ModelOption.SUPPORT_VECTOR_MACHINE,
        "nusvr_regressor": ModelOption.SUPPORT_VECTOR_MACHINE,
        "gpu_svm_classifier": ModelOption.SUPPORT_VECTOR_MACHINE,
        "xgboost_regressor": ModelOption.GRADIENT_BOOSTING,
        "xgboost_classifier": ModelOption.GRADIENT_BOOSTING,
        "gpu_xgboost_classifier": ModelOption.GRADIENT_BOOSTING,
        "stacking_classifier": ModelOption.GRADIENT_BOOSTING,
        "gpu_xgboost_regressor": ModelOption.GRADIENT_BOOSTING,
        "adaboost_classifier": ModelOption.GRADIENT_BOOSTING,
        "adaboost_regressor": ModelOption.GRADIENT_BOOSTING,
        "gradient_boosting_regressor": ModelOption.GRADIENT_BOOSTING,
        "gradient_boosting_classifier": ModelOption.GRADIENT_BOOSTING,
        "ensemble_vote_regressor": ModelOption.GRADIENT_BOOSTING,
        "decision_tree_classifier": ModelOption.TREE,
        "decision_tree_regressor": ModelOption.TREE,
        "lightgbm_regressor": ModelOption.TREE,
        "lightgbm_classifier": ModelOption.TREE,
        "lightgbm": ModelOption.TREE,
        "label_propagation_classifier": ModelOption.NETWORK,
        "label_spreading_classifier": ModelOption.NETWORK,
        "mlp_classifier": ModelOption.NETWORK,
        "mlp_regressor": ModelOption.NETWORK,
        "bernoulli_naivebayes_classifier": ModelOption.BAYESIAN,
        "gaussian_naivebayes_classifier": ModelOption.BAYESIAN,
        "gpu_multinomial_naivebayes_classifier": ModelOption.BAYESIAN,
        "bayesian_ridge_regressor": ModelOption.BAYESIAN,
        "quadratic_discriminant_analysis_classifier": ModelOption.BAYESIAN,
    }

    # lookup all model options corresponding to config_model
    models = [lookup[cmodel] for cmodel in config_model if cmodel in lookup]

    # default model is linear
    if not models:
        models.append(ModelOption.LINEAR)

    # remove duplicates in models
    remove_duplicates = list(set(models))

    return remove_duplicates


def model_lookup_cluster(config_models: List[str], ml_task: MlTask, lookup_limit: int = 1) -> List[ModelOption]:
    """Selects a set of representative models from model names.

    This function expects a list of strings used to look up models in
    utils.representative_models.py. Only models included in the clustering
    analysis are added here. All other models are assumed some default
    representation, or mapped to a model included via the `generalisations`
    dictionary. To be used by `search_enigma.evaluate()`.

    Args:
        config_models:
            Optional[List[str]], names of models. If None, a default representative model is selected.
        ml_task:
            MlTask, expects classification or regression, otherwise raises ValueError.
        lookup_limit:
            int (default=1), can limit the number of representative models selected.
    Returns:
        List:
            List of models with defined hyperparameters (it is expected that these models have a fit and predict method).
    """

    # TODO consider reducing some of these sets
    if ml_task == MlTask.classification:
        default_model = RCLF.RIDGE_CLASSIFIER
    elif ml_task == MlTask.regression:
        default_model = RREG.RIDGE_REGRESSION
    else:
        raise NotImplementedError(f"Unsupported ML task: {ml_task}")
    if lookup_limit == 0:
        lookup_limit = len(RCLF)

    generalisations = {
        # CLASSIFICATION MODELS
        "ridge_cv_classifier": "ridge_classifier",
        "gpu_logistic_regression_classifier": "logistic_regression_classifier",
        "logistic_regression_cv_classifier": "logistic_regression_classifier",
        "gpu_sgd_classifier": "sgd_classifier",
        "gpu_kneighbors_classifier": "kneighbors_classifier",
        "kernel_svc_classifier": "svm_classifier",
        "gpu_svm_classifier": "svm_classifier",
        "gpu_catboost_classifier": "catboost_classifier",
        "gpu_random_forest_classifier": "random_forest_classifier",
        "gpu_xgboost_classifier": "xgboost_classifier",
        "gpu_multinomial_naivebayes_classifier": "gaussian_naivebayes_classifier",
        # REGRESSION MODELS
        "elastic_net_cv_regressor": "elastic_net_regressor",
        "lasso_cv_regressor": "lasso_regressor",
        "gpu_lasso_regressor": "lasso_regressor",
        "gpu_ridge_regressor": "ridge_regressor",
        "gpu_linear_regressor": "linear_regressor",
        "gpu_sgd_regressor": "sgd_regressor",
        "gpu_kneighbors_regressor": "kneighbors_regressor",
        "gpu_catboost_regressor": "catboost_regressor",
        "gpu_random_forest_regressor": "random_forest_regressor",
        "gpu_svr_regressor": "svr_regressor",
        "gpu_xgboost_regressor": "xgboost_regressor",
    }

    lookup = {
        # CLASSIFICATION MODELS
        "ridge_classifier": [
            RCLF.RIDGE_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
        ],
        "logistic_regression_classifier": [
            RCLF.SAG_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.EXTRA_TREE_CLASSIFIER,
            RCLF.ADAGRAD_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.SDCA_CLASSIFIER,
            RCLF.SVRG_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
        ],
        "fista_classifier": [RCLF.SGD_CLASSIFIER, RCLF.ADAGRAD_CLASSIFIER, RCLF.SAG_CLASSIFIER, RCLF.SVRG_CLASSIFIER],
        "sgd_classifier": [
            RCLF.SGD_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.SDCA_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.SAG_CLASSIFIER,
            RCLF.ADAGRAD_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.SVRG_CLASSIFIER,
        ],
        "gaussian_process_classifier": [RCLF.LABEL_PROPAGATION_CLASSIFIER],
        "perceptron_classifier": [
            RCLF.RIDGE_CLASSIFIER,
            RCLF.SAG_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
            RCLF.SVRG_CLASSIFIER,
        ],
        "passive_aggressive_classifier": [
            RCLF.RIDGE_CLASSIFIER,
            RCLF.SAG_CLASSIFIER,
            RCLF.ADAGRAD_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.SVRG_CLASSIFIER,
        ],
        "linear_discriminant_analysis_classifier": [
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
        ],
        "sag_classifier": [RCLF.SAG_CLASSIFIER, RCLF.RIDGE_CLASSIFIER, RCLF.SVRG_CLASSIFIER],
        "saga_classifier": [RCLF.SAG_CLASSIFIER, RCLF.SVRG_CLASSIFIER, RCLF.SDCA_CLASSIFIER],
        "sdca_classifier": [
            RCLF.SDCA_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.ADAGRAD_CLASSIFIER,
            RCLF.SAG_CLASSIFIER,
            RCLF.SVRG_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "svrg_classifier": [
            RCLF.SVRG_CLASSIFIER,
            RCLF.SDCA_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
            RCLF.SAG_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
        ],
        "cd_classifier": [RCLF.ADAGRAD_CLASSIFIER],
        "decision_tree_classifier": [
            RCLF.EXTRA_TREE_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "lightgbm_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.EXTRA_TREE_CLASSIFIER, RCLF.ADAGRAD_CLASSIFIER],
        "gradient_boosting_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.EXTRA_TREE_CLASSIFIER],
        "hist_gradient_boosting_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.EXTRA_TREE_CLASSIFIER],
        "xgboost_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.EXTRA_TREE_CLASSIFIER],
        "random_forest_classifier": [
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.EXTRA_TREE_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "catboost_classifier": [
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.EXTRA_TREE_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "extra_tree_classifier": [RCLF.EXTRA_TREE_CLASSIFIER, RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.RIDGE_CLASSIFIER],
        "extra_trees_classifier": [
            RCLF.EXTRA_TREE_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "bagging_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.EXTRA_TREE_CLASSIFIER],
        "mlp_classifier": [RCLF.EXTRA_TREE_CLASSIFIER, RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.ADAGRAD_CLASSIFIER],
        "label_propagation_classifier": [
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
        ],
        "label_spreading_classifier": [
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "ensemble_vote_classifier": [RCLF.ENSEMBLE_VOTE_CLASSIFIER],
        "svm_classifier": [
            RCLF.SVRG_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "nusvc_classifier": [
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.RIDGE_CLASSIFIER,
        ],
        "linear_svc_classifier": [
            RCLF.SDCA_CLASSIFIER,
            RCLF.ADAGRAD_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
        ],
        "gaussian_nb_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER],
        "bernoulli_nb_classifier": [RCLF.ADAGRAD_CLASSIFIER, RCLF.RADIUS_NEIGHBORS_CLASSIFIER],
        "quadratic_discriminant_analysis_classifier": [
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
        ],
        "kneighbors_classifier": [RCLF.LABEL_PROPAGATION_CLASSIFIER],
        "nearest_centroid_classifier": [RCLF.NEAREST_CENTROID_CLASSIFIER],
        "radius_neighbors_classifier": [RCLF.RIDGE_CLASSIFIER, RCLF.RADIUS_NEIGHBORS_CLASSIFIER],
        "adagrad_classifier": [
            RCLF.ADAGRAD_CLASSIFIER,
            RCLF.EXTRA_TREE_CLASSIFIER,
            RCLF.LABEL_PROPAGATION_CLASSIFIER,
            RCLF.SVRG_CLASSIFIER,
            RCLF.GRADIENT_BOOSTING_CLASSIFIER,
            RCLF.RADIUS_NEIGHBORS_CLASSIFIER,
            RCLF.SAG_CLASSIFIER,
            RCLF.SGD_CLASSIFIER,
        ],
        "adaboost_classifier": [RCLF.GRADIENT_BOOSTING_CLASSIFIER, RCLF.EXTRA_TREE_CLASSIFIER],
        # REGRESSION MODELS
        "linear_regressor": [RREG.RIDGE_REGRESSION],
        "ridge_regressor": [RREG.SAG_REGRESSION, RREG.RIDGE_REGRESSION, RREG.LINEARSVR_REGRESSION],
        "lasso_regressor": [
            RREG.ELASTIC_NET_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.ADAGRAD_REGRESSION,
        ],
        "elastic_net_regressor": [
            RREG.ELASTIC_NET_REGRESSION,
            RREG.RIDGE_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.ADAGRAD_REGRESSION,
        ],
        "least_angle_regressor": [RREG.SGD_EPSILON_REGRESSION],
        "lassolars_regressor": [
            RREG.SAG_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.ADAGRAD_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.ELASTIC_NET_REGRESSION,
        ],
        "bayesian_ridge_regressor": [RREG.RIDGE_REGRESSION],
        "ard_regressor": [RREG.LINEARSVR_REGRESSION],
        "sgd_regressor": [
            RREG.SGD_EPSILON_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.SAG_REGRESSION,
            RREG.ADAGRAD_REGRESSION,
            RREG.LINEARSVR_REGRESSION,
        ],
        "passive_aggressive_regressor": [RREG.SAG_REGRESSION, RREG.LINEARSVR_REGRESSION],
        "theil_sen_regressor": [RREG.RIDGE_REGRESSION],
        "svr_regressor": [RREG.SGD_HUBER_REGRESSION, RREG.SGD_EPSILON_REGRESSION, RREG.SVR_REGRESSION],
        "linearsvr_regressor": [RREG.LINEARSVR_REGRESSION, RREG.ADAGRAD_REGRESSION],
        "kneighbors_regressor": [RREG.KNEIGHBORS_REGRESSION],
        "radius_neighbors_regressor": [RREG.RADIUS_NEIGHBORS_REGRESSION, RREG.SGD_EPSILON_REGRESSION],
        "pls_regressor": [RREG.RIDGE_REGRESSION],
        "decision_tree_regressor": [
            RREG.RIDGE_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.GRADIENT_BOOSTING_REGRESSION,
        ],
        "extra_tree_regressor": [
            RREG.RIDGE_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.GRADIENT_BOOSTING_REGRESSION,
        ],
        "mlp_regressor": [RREG.LINEARSVR_REGRESSION],
        "gradient_boosting_regressor": [
            RREG.GRADIENT_BOOSTING_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
        ],
        "random_forest_regressor": [RREG.GRADIENT_BOOSTING_REGRESSION],
        "adaboost_regressor": [RREG.GRADIENT_BOOSTING_REGRESSION],
        "bagging_regressor": [RREG.GRADIENT_BOOSTING_REGRESSION],
        "hist_gradient_boosting_regressor": [
            RREG.GRADIENT_BOOSTING_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.RIDGE_REGRESSION,
        ],
        "catboost_regressor": [RREG.GRADIENT_BOOSTING_REGRESSION],
        "lightgbm_regressor": [RREG.LIGHTGBM_REGRESSION],
        "adagrad_regressor": [
            RREG.ADAGRAD_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.SAG_REGRESSION,
            RREG.LINEARSVR_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
        ],
        "cd_regressor": [RREG.LINEARSVR_REGRESSION, RREG.RIDGE_REGRESSION],
        "fista_regressor": [RREG.ADAGRAD_REGRESSION, RREG.SGD_HUBER_REGRESSION, RREG.SAG_REGRESSION],
        "sag_regressor": [RREG.SAG_REGRESSION],
        "saga_regressor": [RREG.SVR_REGRESSION],
        "sdca_regressor": [
            RREG.ELASTIC_NET_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
            RREG.SVR_REGRESSION,
        ],
        "xgboost_regressor": [
            RREG.GRADIENT_BOOSTING_REGRESSION,
            RREG.SGD_EPSILON_REGRESSION,
            RREG.SGD_HUBER_REGRESSION,
        ],
    }

    # substitute certain models (e.g. gpu ridge -> ridge)
    config_models = [generalisations[cmodel] if cmodel in generalisations else cmodel for cmodel in config_models]
    config_models = list(set(config_models))

    def get_lookup_model(model: str) -> List:
        if model not in lookup:
            return [default_model]
        reps = lookup[model]
        return reps[:lookup_limit]

    # get list of representative models
    models = [m for cmodel in config_models for m in get_lookup_model(cmodel)]

    # default model is ridge classifier
    if not models:
        models.append(default_model)

    # remove duplicates in models, sort for testing reproducability
    remove_duplicates = sorted(list(set(models)))
    rep_models = [m.model for m in remove_duplicates]

    # limit number of models
    min_models = rep_models[:lookup_limit]

    return min_models
