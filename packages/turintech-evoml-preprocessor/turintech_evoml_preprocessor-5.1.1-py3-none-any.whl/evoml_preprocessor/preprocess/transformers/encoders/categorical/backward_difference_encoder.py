from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd
from category_encoders import BackwardDifferenceEncoder as _BackwardDifferenceEncoder

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class BackwardDifferenceEncoder(Encoder[dtype.Categorical, dtype.Float64]):
    """
    Encoder for performing backward difference encoding.
    Inherits the Encoder class.

    Example:
        encoder = BackwardDifferenceEncoder()
        transformed_data = encoder.transform(data)
    """

    slug = CategoricalEncoder.BACKWARD_DIFFERENCE_ENCODER
    columns: List[str]

    def __init__(self, name: str) -> None:
        """
        Initialize the BackwardDifferenceEncoder.
        """
        super().__init__()
        self._encoder = None
        self.fill_median_value = None
        self.name = name
        self.columns: List[str] = []

    @property
    def encoder(self) -> _BackwardDifferenceEncoder:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = _BackwardDifferenceEncoder(cols=[0], return_df=False)  # Instantiate the encoder

        # @data: no copy is made here
        X_np = X.to_numpy().reshape(-1, 1)

        self.encoder.fit(X_np)  # Fit the encoder on the data
        self.columns = [f"{self.name}_{i}_backdiff" for i in range(1, len(self.encoder.feature_names_out_) + 1)]

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Float64]:
        # @data: no copy is made here
        X_np = X.to_numpy().reshape(-1, 1)

        # @data: new object
        transformed = self.encoder.transform(X_np)

        # The encoder can produce NaN values that we need to impute
        medians = np.nanmedian(transformed, axis=0)
        for i in range(transformed.shape[1]):
            nan_indices = np.isnan(transformed[:, i])
            if any(nan_indices):
                transformed[nan_indices, i] = medians[i]

        return pd.DataFrame(transformed, columns=self.columns, index=X.index)  # type: ignore
