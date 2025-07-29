import logging
import pandas as pd
import numpy as np
from sklearn.decomposition import FastICA, TruncatedSVD, PCA

from evoml_preprocessor.decomposition.enum import DimReduction
from evoml_preprocessor.preprocess.models.config import DimensionalityReductionOptions

logger = logging.getLogger("preprocessor")


class DimensionalityReductionWrapper:
    """
    Wrapper class for dimensionality reduction algorithms.
    This class can be used to apply various dimensionality reduction techniques on input data.

    Args:
        options (DimensionalityReductionOptions): Options for dimensionality reduction.
        seed (int, optional): Random seed for reproducibility. Defaults to 42.

    Raises:
        ValueError: If the specified dimensionality reduction algorithm is not supported.

    Example:
        options = DimensionalityReductionOptions(method=DimReduction.PCA, noOfComponents=2)
        dr_wrapper = DimensionalityReductionWrapper(options)
        transformed_data = dr_wrapper.fit_transform(data)
    """

    def __init__(self, options: DimensionalityReductionOptions, seed: int = 42):
        self.method = options.method
        self.n_components = options.noOfComponents
        self.fitted = False
        self.data_has_low_dimension = False

        if self.method == DimReduction.SVD:
            self.model = TruncatedSVD(n_components=self.n_components, random_state=seed)
        elif self.method == DimReduction.PCA:
            self.model = PCA(n_components=self.n_components, random_state=seed)
        elif self.method == DimReduction.ICA:
            self.model = FastICA(n_components=self.n_components, random_state=seed)
        else:
            raise ValueError(f"The {self.method} dimensionality reduction algorithm is not supported.")

    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the dimensionality reduction model to the data and apply dimensionality reduction.

        NOTE: dimensionality reduction does not include the target.

        Args:
            data (pd.DataFrame): The input data to fit and transform.

        Returns:
            pd.DataFrame: The transformed data.

        Example:
            transformed_data = dr_wrapper.fit_transform(data)
        """
        self.data_has_low_dimension = self.n_components >= data.shape[1]
        if self.data_has_low_dimension:
            logger.info(
                f"Unable to apply {self.method.get_full_name()} for dimensionality reduction. The requested output size of {self.n_components} is larger than the number of dimensions in the input data ({data.shape[1]})."
            )
            return data

        index = data.index
        original_shape = data.shape

        # Fit the dimensionality reduction model to the data
        self.model.fit(data)

        # Apply dimensionality reduction
        result = self.model.transform(data)
        reduced_shape = result.shape

        self.columns = [f"latent_var_{i}" for i in range(result.shape[1])]
        df = pd.DataFrame(result, index=index, columns=self.columns).astype(np.float64)

        logger.info(
            f"→  applying {self.method.get_full_name()} to reduce dimensions, from {original_shape} to {reduced_shape}."
        )
        self.fitted = True
        return df

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply dimensionality reduction to the data using the fitted model.

        If the requested output size is greater than the input data's number of dimensions,
        or if the dimensionality reduction model has not been fitted yet, the input data will be returned as is.

        Args:
            data (pd.DataFrame): The input data to transform.

        Returns:
            pd.DataFrame: The transformed data.

        Example:
            transformed_data = dr_wrapper.transform(data)
        """
        if not self.fitted:
            logger.warning(f"{self.method.get_full_name()} for dimensionality reduction has not been fitted.")
            return data

        index = data.index

        original_shape = data.shape
        result = self.model.transform(data)
        reduced_shape = result.shape

        df = pd.DataFrame(result, index=index, columns=self.columns).astype(np.float64)

        logger.info(
            f"→  test set: applying {self.method.get_full_name()} to reduce dimensions, from {original_shape} to {reduced_shape}."
        )
        return df
