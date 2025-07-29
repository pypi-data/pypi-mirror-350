from __future__ import annotations

from typing import List, Optional

import numpy as np
import numpy.typing as npt
import pandas as pd
from category_encoders import HelmertEncoder as _HelmertEncoder

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class HelmertEncoder(Encoder[dtype.Categorical, dtype.Float64]):
    """
    Encoder for performing Helmert encoding.
    Inherits the Encoder class.

    Example:
        encoder = HelmertEncoder()
        transformed_data = encoder.transform(data)
    """

    slug = CategoricalEncoder.HELMERT_ENCODER
    columns: List[str]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._encoder: Optional[_HelmertEncoder] = None
        self.fill_median_value = None

    @property
    def encoder(self) -> _HelmertEncoder:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = _HelmertEncoder(return_df=False)
        self.encoder.fit(X, y)
        self.columns = [f"{self.name}_{i}_helmert" for i in range(1, len(self.encoder.feature_names_out_) + 1)]

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Float64]:
        # @pyright: dynamic type output of encoder
        transformed: npt.NDArray[np.float64] = self.encoder.transform(X)  # type: ignore

        # The encoder can produce NaN values that we need to impute
        medians = np.nanmedian(transformed, axis=0)
        for i in range(transformed.shape[1]):
            nan_indices = np.isnan(transformed[:, i])
            if any(nan_indices):
                transformed[nan_indices, i] = medians[i]

        return pd.DataFrame(transformed, columns=self.columns, index=X.index)  # type: ignore
