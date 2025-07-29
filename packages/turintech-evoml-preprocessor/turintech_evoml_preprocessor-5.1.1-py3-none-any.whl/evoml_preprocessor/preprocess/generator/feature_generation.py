# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Dict, List

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.generator.builder import feature_builder_factory
from evoml_preprocessor.preprocess.generator.models import GeneratedFeature
from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.pool import FeatureGenerationPool
from evoml_preprocessor.preprocess.generator.report_builder import FeatureGenerationReportBuilder
from evoml_preprocessor.preprocess.generator.scorer import feature_scorer_factory
from evoml_preprocessor.preprocess.generator.util import (
    FeatureBuilderType,
    GeneratorParameters,
    is_invalid,
    is_invalid_feature,
)
from evoml_preprocessor.preprocess.models import FeatureGenerationOptions

# Module
from evoml_preprocessor.types.pandas import IndexedSeries
from evoml_preprocessor.utils.sample import get_sample

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
MAX_ROWS = 500
# ──────────────────────────────────────────────────────────────────────────── #


class FeatureGenerator:
    """This class processes a dataframe of labeled data and generates
    additional features.

    There are two main stages for generating new features:
        1. Generate a bunch of new features from mathematical
        operations specified by the user, with some building algorithm
        specified by the user.
        2. As the number of new features reaches the batch size
        filter out features using a feature selection process (like
        mRMR, or a wrapper method).
            -> Repeat ´feature_generation_epochs´ times

    The above structure is implemented in 'fit_transform' method.

    Args:
        selection_scores (Dict[str, float]): Dictionary of feature names
            and their selection scores.
        parameters (GeneratorParameters): Parameters for the feature
            generation process.
    """

    def __init__(self, selection_scores: Dict[str, float], parameters: GeneratorParameters):
        self.selection_scores = selection_scores

        self.original_features: List[str] = []
        self.generated_features: FeatureGenerationPool = FeatureGenerationPool()
        self.builder = feature_builder_factory(parameters.builder_type, parameters.builder_parameters)
        self.scorer = feature_scorer_factory(parameters.scorer_type, parameters.ml_task, parameters.rng)

        self.n_new_features = parameters.n_new_features
        self.feature_generation_epochs = parameters.n_epochs
        self.ml_task = parameters.ml_task
        self.report_builder = FeatureGenerationReportBuilder()

        self.n_batch = self.scaling_factor(self.n_new_features, 10, 4)
        self.n_epoch = self.scaling_factor(10, 10, 4)
        self.n_init = 20
        self.n_recurring = 10

        if self.builder.type == FeatureBuilderType.POLYNOMIAL:
            self.n_batch = 10
            self.feature_generation_epochs = 1
        elif self.builder.type == FeatureBuilderType.GROW_SAMPLED:
            self.n_batch = self.scaling_factor(10, 10, 4)
            self.n_epoch = self.scaling_factor(15, 15, 4)
        elif self.builder.type == FeatureBuilderType.GENETIC:
            self.n_batch = self.scaling_factor(15, 15, 4)
            self.n_epoch = self.scaling_factor(20, 20, 2)

    def scaling_factor(self, n: int, lim: int, s: int) -> int:
        """Scaling factor for certain generation parameters

        This defines a piecewise function that is constant below a threshold
        and linear scaling above this threshold. This function depends on the
        number of new feature the user wants to generate

        Args:
            n: default value (if limit not met)
            lim: threshold for piecewise function
            s: scaling factor above the threshold

        Returns:
            int: scaled value based on target number of features
        """
        if self.n_new_features < lim:
            return n
        # @mypy: (int - int) is incorrectly evaluated to Any
        return n + self.n_new_features - lim // s  # type: ignore

    @classmethod
    def from_generation_options(
        cls, ml_task: MlTask, selection_scores: Dict[str, float], generation_options: FeatureGenerationOptions
    ) -> FeatureGenerator:
        parameters = GeneratorParameters.from_generation_options(ml_task, generation_options)
        return cls(selection_scores, parameters)

    def _feature_generation_epoch(self, epoch: int, y: pd.Series[float]) -> None:
        """A single iteration of the feature generation process.

        - Each epoch generates a set of candidate features with the builder.
        - These `candidates` cannot have already been generated before.
        - If there are too many `candidates`, feature selection filters them
        down in batches and stores this in `best_candidates`
        - A final feature selection process is run at the end of the epoch to
        reach a specified target number of generated features, if there are too
        many `best_candidates`

        Args:
            epoch: Epoch number, used to determine whether we are on the final
                epoch
            y: The target, used in feature selection
        """

        # add the best original features back to the pool
        self.generated_features.regenerate_pool()
        self.scorer.load_original_features(self.generated_features.get_features())

        # spawn new pools for candidates and best candidates
        # candidates start empty but remember all past generated features, so
        # only new features are considered
        candidates = self.generated_features.spawn_new_pool()
        best_candidates = self.generated_features.spawn_new_pool()

        generated_features_all = list(self.builder.build(self.generated_features.get_features()))

        for feature in generated_features_all:
            # check for identical name before generating the data
            if candidates.is_duplicate_name(feature):
                continue
            feature.generate_data()
            if is_invalid_feature(feature):
                continue
            # add feature (if the feature is new)
            candidates.add_generated_feature(feature)

        # We score on the candidates and the features at the beginning of
        # the epoch
        scores = self.scorer.score(candidates.get_features(), y, self.n_batch, final=False)

        for feature, score in scores.items():  # type: ignore
            # only add to `best_candidates` if the best scores are new
            # features. This means that a batch may result is zero
            # additions to `best_candidates`, if selected features are from
            # the epoch start
            feature: GeneratedFeatureNode  # type: ignore
            if score > 0 and not is_invalid_feature(feature):
                best_candidates.add_generated_feature(feature)
        candidates.clear_pool()

        n_epoch = self.n_new_features if epoch == self.feature_generation_epochs - 1 else self.n_epoch
        if len(best_candidates) + len(self.generated_features) > n_epoch:
            scores = self.scorer.score(
                best_candidates.get_features(),
                y,
                n_epoch,
                final=epoch == self.feature_generation_epochs - 1,
            )
            for feature, score in scores.items():
                if score > 0:
                    self.generated_features.add_generated_feature(feature)
                else:
                    self.generated_features.remove_generated_feature(feature)
        else:
            self.generated_features.update_pool(best_candidates)

    def fit(self, data: pd.DataFrame, encoded_label: pd.Series[float]) -> None:
        # Feature generation is expensive, so only sample a subset of the data
        self.generated_features.clear()
        self.original_features = data.columns.tolist()

        sampled_index = get_sample(encoded_label, MAX_ROWS, task=self.ml_task)
        X_sample = data.loc[sampled_index]
        y_sample = encoded_label.loc[sampled_index]

        scores = pd.Series(self.selection_scores)
        desc_sorted_scores: IndexedSeries[str, float] = scores.sort_values(ascending=False)  # type: ignore

        # Select initial features by scores
        init_features = desc_sorted_scores.index[: self.n_init]
        x_primitives_init: pd.DataFrame = X_sample[init_features.intersection(X_sample.columns)]

        recurring_features = desc_sorted_scores.index[: self.n_recurring]
        x_primitives_recurring: pd.DataFrame = X_sample[recurring_features.intersection(X_sample.columns)]

        # Add original features to pool
        for _, feature in x_primitives_init.items():
            self.generated_features.add_feature(feature)
        for _, feature in x_primitives_recurring.items():
            self.generated_features.add_regenerated_feature(feature)

        # This is the main logic of the feature generation
        for epoch in range(self.feature_generation_epochs):
            self._feature_generation_epoch(epoch, y_sample)

        # Remove original features from the generated features
        self.generated_features.remove_names(self.original_features)

        self.generate_report(encoded_label)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        if len(self.generated_features) == 0:
            logger.warning("- no features were generated")
            return data

        @lru_cache(maxsize=None)
        def recursive_parsing_calculation(node: GeneratedFeatureNode) -> pd.Series[float]:
            if node.operation is None:
                # @mypy: during feature generation all series are float
                return data[node.name]  # type: ignore
            generated_feature = node.call_operation([recursive_parsing_calculation(child) for child in node.children])
            generated_feature.index = data.index
            if pd.api.types.is_float_dtype(generated_feature):
                return generated_feature.astype(np.float64)
            return generated_feature  # type: ignore

        generated = {}
        for i, feature in enumerate(self.generated_features):

            # Compute if any required features are missing. If so, skip this generated feature.
            received_features = set(data.columns)
            missing_features = set(feature.formula.features) - received_features
            if missing_features:
                continue

            generated_ = recursive_parsing_calculation(feature)
            if is_invalid(generated_):
                # we assume the feature is valid if it reaches this point
                # because it passed the is_invalid check previously
                # this is to allow us to investigate generated features
                logger.warning(f"Generated Feature {feature} is invalid")
            generated[f"generated_feature_{i}"] = generated_

        self.n_new_features = len(generated)

        return pd.concat((data, pd.DataFrame(generated)), axis=1)

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series[float]) -> pd.DataFrame:
        self.fit(data, encoded_label)
        return self.transform(data)

    def generate_report(self, encoded_label: pd.Series[float]) -> None:
        for i, feature in enumerate(self.generated_features):
            assert feature.values is not None
            correlation = feature.values.corr(encoded_label)
            if pd.isna(correlation):
                correlation = 0.0
            self.report_builder.append_generated_feature_info(
                GeneratedFeature.from_feature_formula(
                    feature.simplified_formula.formula,
                    feature.formula,
                    f"generated_feature_{i}",
                    feature.preorder,
                    correlation,
                )
            )
