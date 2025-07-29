from __future__ import annotations

from typing import List, Optional

import numpy as np
import numpy.typing as npt
import pandas as pd
from sklearn.feature_extraction import FeatureHasher

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

CONF = conf_mgr.preprocess_conf  # Alias for readability


class HashEncoder(Encoder[dtype.Categorical, dtype.Int8]):
    """
    Encoder for performing feature hashing using a hash function.
    Inherits the Encoder class.

    Example:
        encoder = HashEncoder()
        transformed_data = encoder.transform(data)
    """

    slug = CategoricalEncoder.HASH_ENCODER
    columns: List[str]

    def __init__(self, name: str, length: int = CONF.HASH_NUMBER) -> None:
        """
        Initialize the HashEncoder.
        """
        super().__init__()
        self.name = name
        self.length = length
        self._encoder: Optional[FeatureHasher] = None
        self.fill_median_value = None
        self.fill_value = "~unseen~"

    def _prepare_data(self, X: Series[dtype.Categorical]) -> None:
        # Replace None with fill_value
        X.replace(["nan", "None"], self.fill_value, inplace=True)

    @property
    def encoder(self) -> FeatureHasher:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = FeatureHasher(n_features=self.length, input_type="string", dtype=np.int8)  # type: ignore
        # `FeatureHasher` fit method is no-op (only validation)
        self.columns = [f"{self.name}_{i+1}_hash" for i in range(self.length)]  # Set column names

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Int8]:
        # Replace None with fill_value in-place
        self._prepare_data(X)
        # @data: no copy
        X_np = X.to_numpy().reshape(-1, 1)
        # @data: copy for self.encoder.transform
        # @mypy: using sklearn stubs (from microsoft) will raise an error here
        transformed = self.encoder.transform(X_np)
        transformed_dense: npt.NDArray[np.int8] = transformed.todense()
        # @data: copy for type change
        return pd.DataFrame(transformed_dense, columns=self.columns, index=X.index)  # type: ignore
