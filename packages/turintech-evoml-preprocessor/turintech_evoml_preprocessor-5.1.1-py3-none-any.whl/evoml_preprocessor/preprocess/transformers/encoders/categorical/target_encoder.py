from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd
from category_encoders import TargetEncoder as _TargetEncoder

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class TargetEncoder(Encoder[dtype.Categorical, dtype.Float64]):
    """
    Encoder for performing target encoding using the TargetEncoder from category_encoders library.
    Inherits the Encoder base class.
    """

    slug = CategoricalEncoder.TARGET_ENCODER
    columns: List[str]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._encoder: Optional[_TargetEncoder] = None
        self.columns = [name]
        self.fill_median_value = None

    @property
    def encoder(self) -> _TargetEncoder:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = _TargetEncoder(smoothing=10, return_df=False)  # Instantiate the encoder
        self.encoder.fit(X, y)  # Fit the encoder

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Float64]:
        # @data: new object
        transformed = self.encoder.transform(X)

        # The encoder can produce NaN values that we need to impute
        medians = np.nanmedian(transformed, axis=0)
        for i in range(transformed.shape[1]):
            nan_indices = np.isnan(transformed[:, i])
            if any(nan_indices):
                transformed[nan_indices, i] = medians[i]

        return pd.DataFrame(transformed, columns=self.columns, index=X.index)  # type: ignore
