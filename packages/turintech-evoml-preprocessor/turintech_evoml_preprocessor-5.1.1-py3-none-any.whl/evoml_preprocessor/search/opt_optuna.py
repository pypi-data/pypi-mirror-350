# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import hashlib
import json
import logging
from typing import Dict, List

# Dependencies
import numpy as np
import optuna
import pandas as pd

# Private Dependencies
from evoml_api_models import MlTask
from optuna.samplers import TPESampler
from sklearn.metrics import f1_score, mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split
from threadpoolctl import threadpool_limits

from evoml_preprocessor.search.model_lookup import model_lookup_cluster

# Module
from evoml_preprocessor.preprocess.transformers import Transformer
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
ColNameType = str
MethodNameType = str
# random state used by optuna and sklearn split function to ensure reproducibility
random_state = 42
#  number of optuna trials to run
n_trials = 80


class EncoderSearchOptuna:
    """This classes using optuna to find the optimal encoder/scaler combinations in the search space.
    The evaluation function is a predefined ml function we lookup based on the models present in the config and task.
    """

    def __init__(
        self,
        search_space: Dict[ColNameType, Dict[MethodNameType, Dict]],
        base_df: pd.DataFrame,
        data_label: pd.Series,
        ml_task: MlTask,
        ml_models: List[str],
    ):
        self.search_space = search_space
        self.base_df = base_df
        self.y = data_label.to_numpy()
        self.ml_task = ml_task
        self.best_params = {}
        # identify a set of models to evaluate trials
        self.ml_models = model_lookup_cluster(ml_models, ml_task, 3)
        self.metric = "f1_macro" if self.ml_task == MlTask.classification else "neg_mean_squared_error"
        self.min_bincount = (
            min(pd.value_counts(data_label)) if self.ml_task == MlTask.classification else base_df.shape[0]
        )

    def build_df(self, options: Dict[str, str]) -> pd.DataFrame:
        """Get the complete dataset from joining the data under search with the base data.
        Args:
            options (Dict):
                The transformation parameters to specify how the columns are transformed, in the format of
                {column_name: method_name}. It uses the method names to retrieve their corresponding transformed
                data from the search space.
        Returns:
            pd.DataFrame:
                The complete data that can be used to fit/test ml models.
        """

        if self.base_df.shape[1] == 0:
            all_cols = []
        else:
            all_cols = [self.base_df]

        for key, value in options.items():
            temp_col = self.search_space[key][value]["transformed_col"]
            all_cols.append(temp_col)

        # include only numeric columns with no missing values
        df = pd.concat(all_cols, axis=1).dropna(axis=1, how="any").select_dtypes(include=["number"])

        return df

    def objective(self, trial: optuna.Trial) -> float:
        trial_options = {}
        evaluated: Dict[str, float] = {}

        # select the transformation options for each column in the search space
        for column, options in self.search_space.items():
            available_options = list(options.keys())
            # if there is only one option, we select it, otherwise we use optuna to select
            if len(available_options) == 1:
                op = available_options[0]
            else:
                op = trial.suggest_categorical(column, available_options)
            trial_options.update({column: op})

        # early break if all options are the same
        kwargs_hash = hashlib.md5(json.dumps(trial_options).encode()).hexdigest()
        if kwargs_hash in evaluated:
            result = evaluated[kwargs_hash]
            return result

        # build the data using base data and the selected transformation options for each column
        X = self.build_df(trial_options)

        # no numeric columns, return nan
        if X.shape[1] == 0:
            evaluated[kwargs_hash] = np.nan
            return np.nan

        # calculate the cross-validation score
        folds = min(2, self.min_bincount)
        max_score = np.nan

        try:
            with threadpool_limits(limits=conf_mgr.preprocess_conf.THREADS):
                for model in self.ml_models:
                    if self.min_bincount < 2:
                        # classes with only one instance, we cannot stratify, this is needed for Encoder Search as it is executed on a sample
                        x_train, x_test, y_train, y_test = train_test_split(
                            X,
                            self.y,
                            test_size=0.2,
                            random_state=random_state,
                        )

                        model.fit(x_train, y_train)
                        y_pred = model.predict(x_test)
                        if self.ml_task == MlTask.classification:
                            score = f1_score(y_test, y_pred, average="macro")
                        else:
                            score = -1 * mean_squared_error(y_test, y_pred)
                    else:
                        # Calculate the cross-validation F1/MSE scores using
                        score = np.mean(cross_val_score(model, X, self.y, cv=folds, scoring=self.metric, n_jobs=1))
        except (TypeError, ValueError, KeyError):
            # to be skipped over when calculating mean
            score = np.nan

        if np.isnan(max_score) or score > max_score:
            max_score = score

        # update the evaluated dictionary to avoid re-evaluating
        evaluated[kwargs_hash] = max_score

        return max_score

    def search(self) -> Dict[str, Transformer]:
        """Run the optimisation process.
        Returns:
            Dict:
                The best parameters found. Format: {column_name: method_name}
        """
        # the direction of optimisation is maximise as we use the negative MSE for regression and F1 for classification

        # bypass the search if only one options is available for each column
        operation_counts = all(len(options) == 1 for options in self.search_space.values())
        if operation_counts:
            logger.warning("Bypassing encoder search as only one option is available for each column.")
            return self.select_first_available()

        # Run the hyperparameter search using Optuna
        optuna.logging.set_verbosity(optuna.logging.CRITICAL)

        # these search items only have one option, so we can skip them in optuna, and add them to the best_params
        no_search_needed = [(key, list(val.keys())[0]) for key, val in self.search_space.items() if len(val) == 1]
        for key, value in no_search_needed:
            self.best_params[key] = value

        # the direction of optimisation is maximise as we use the negative MSE for regression and F1 for classification
        sampler = TPESampler(seed=random_state)
        study = optuna.create_study(sampler=sampler, direction="maximize")
        study.optimize(self.objective, n_trials=n_trials)

        # identify whether optuna found a solution
        try:
            _ = study.best_value
        except ValueError:
            logger.error("Encoder search is unable to find a solution.")
            return self.select_first_available()

        # update the best_params with the best options found by optuna
        self.best_params.update(study.best_params)

        logger.info(f"→ search result: {self.best_params}")

        return self.retrieve_optimal_encoders(self.best_params)

    def select_first_available(self) -> Dict[str, Transformer]:
        best_params = {}
        for column, options in self.search_space.items():
            best_params[column] = next(iter(options))
        return self.retrieve_optimal_encoders(best_params)

    def retrieve_optimal_encoders(self, best_params) -> Dict[str, Transformer]:
        # here we are retrieving the optimal encoders found
        optimal_encoders = {}
        for col, method in best_params.items():
            # Getting encoder selected for a particular col
            encoder = self.search_space[col][method]["transformer"]
            optimal_encoders[col] = encoder
        return optimal_encoders
