# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Dict, Optional

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.generator.feature_generation import FeatureGenerator
from evoml_preprocessor.preprocess.handlers.feature_generation._base import FeatureGenerationHandler
from evoml_preprocessor.preprocess.models import PreprocessConfig
from evoml_preprocessor.preprocess.selector.selector import RelevanceSelector

# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class DefaultFeatureGenerationHandler(FeatureGenerationHandler):
    """The default feature generation handler. It generates features based on the configuration."""

    feature_generator: Optional[FeatureGenerator]

    def __init__(self, config: PreprocessConfig):
        super().__init__(config)
        self.feature_generator = None
        self.selection_scores: Optional[Dict[str, float]] = None

    def fit_transform_report(
        self, data: pd.DataFrame, encoded_label: pd.Series, scores: Optional[Dict[str, float]]
    ) -> pd.DataFrame:
        """Initializes the feature generator and generates the features.

        This is the same as `fit_transform`, but it also takes the selection
        scores as an argument. This solves the problem of the feature generator
        needing a ranking of the most useful features, which is already computed
        as a byproduct of feature selection, and we don't want to redefine the
        `fit_transform` method, which has an expected signature.

        Args:
            data: (pd.DataFrame)
                X
            encoded_label: (pd.Series)
                y
            scores: Optional[Dict[str, float]:
                Currently a mapping between the feature names and the scores.

                Can be extended to a dataclass in the future, if more
                information is needed in feature generation.

        Returns:
            pd.DataFrame:
                The data with the generated features.
        """
        # exclude non-numeric cols from feature generation process
        non_numeric_col_names = data.select_dtypes(exclude=["number"]).columns
        non_numeric_indices = [data.columns.get_loc(column) for column in non_numeric_col_names]
        non_numeric_cols = pd.DataFrame(index=data.index)
        if not non_numeric_col_names.empty:
            non_numeric_cols = data[non_numeric_col_names]
            if non_numeric_cols.shape[1] == data.shape[1]:
                logger.warning("No numeric features found. Skipping feature generation.")
                return data
            data = data.drop(non_numeric_col_names, axis=1)

        # In the case where feature selection wasn't called, or encountered
        # some early stopping condition, we need to compute the scores via
        # some other (computationally cheap) method
        if data.shape[1] <= 1:
            self.selection_scores = {data.columns[0]: 1.0}
        elif not scores and self.options.enable:
            selector = RelevanceSelector.default(self.ml_task)
            selector.fit(data, encoded_label, data.shape[1])
            self.selection_scores = selector.scores.combined.to_dict()
        else:
            self.selection_scores = scores

        generated_data = self.fit_transform(data, encoded_label)
        # if non_numeric cols merge with generated_data
        for position, column in zip(non_numeric_indices, non_numeric_col_names):
            generated_data.insert(position, column, non_numeric_cols[column])
        return generated_data

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Initializes the feature generator and generates the features.
        Args:
            data (pd.DataFrame):
                The data to generate features for.
            encoded_label (pd.Series):
                The encoded label.
        Returns:
            pd.DataFrame:
                The data with the generated features.
        """

        if self.is_timeseries or not self.options.enable:
            return data

        # This is a messy approach since we want to preserve the
        # `fit_transform` signature, but we also want to pass the scores
        if self.selection_scores is None:
            raise ValueError("Selection scores not loaded")

        self.feature_generator = FeatureGenerator.from_generation_options(
            self.ml_task, self.selection_scores, self.options
        )

        logger.info(" Feature Generation ".center(60, "-"))

        result = self.feature_generator.fit_transform(data, encoded_label)

        n_generated = len(self.feature_generator.generated_features)
        if n_generated > 0:
            logger.info(f"→ generated {n_generated} features")

        logger.info(f"→ feature generation succcessful")

        return result

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generates the features.
        Args:
            data (pd.DataFrame):
                The data to generate features for.
        Returns:
            pd.DataFrame:
                The data with the generated features.
        """

        if self.feature_generator is not None:
            data = self.feature_generator.transform(data)
        return data
