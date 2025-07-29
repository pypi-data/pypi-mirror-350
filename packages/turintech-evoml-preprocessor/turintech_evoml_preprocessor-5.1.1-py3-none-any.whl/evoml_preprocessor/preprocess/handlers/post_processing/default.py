import logging

import pandas as pd

from evoml_preprocessor.decomposition.dimensionality_reduction import DimensionalityReductionWrapper
from evoml_preprocessor.preprocess.handlers.post_processing._base import PostProcessingHandler
from evoml_preprocessor.preprocess.models import PreprocessConfig

logger = logging.getLogger("preprocessor")


class DefaultPostProcessingHandler(PostProcessingHandler):
    """
    Default dimensionality reduction handler. Does not perform any dimensionality reduction.
    """

    def __init__(self, config: PreprocessConfig):
        """
        Initialize the DefaultPostProcessingHandler.

        Args:
            config (PreprocessConfig): The preprocess config.

        Example:
            handler = DefaultPostProcessingHandler(config)
        """
        super().__init__(config)

    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the dimensionality reduction model to the data and apply dimensionality reduction.

        Args:
            data (pd.DataFrame): The input data to fit and transform.

        Returns:
            pd.DataFrame: The transformed data.

        Example:
            transformed_data = handler.fit_transform(data)
        """
        # No dimensionality reduction
        if not self.dimensionality_reduction_options.enable:
            return data

        logger.info(" Dimensionality Reduction ".center(60, "-"))

        self.model = DimensionalityReductionWrapper(self.dimensionality_reduction_options, self.seed)
        embedding = self.model.fit_transform(data)

        return embedding

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply dimensionality reduction to the data using the fitted model.

        Args:
            data (pd.DataFrame): The input data to transform.

        Returns:
            pd.DataFrame: The transformed data.

        Example:
            transformed_data = handler.transform(data)
        """
        if self.model is None:
            return data

        embedding = self.model.transform(data)

        return embedding
