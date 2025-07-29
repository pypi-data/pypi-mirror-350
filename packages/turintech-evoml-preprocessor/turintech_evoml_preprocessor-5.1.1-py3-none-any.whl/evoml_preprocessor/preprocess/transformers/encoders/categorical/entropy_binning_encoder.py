from __future__ import annotations

from typing import List, Optional

import pandas as pd

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.preprocess.transformers.encoders.categorical.entropy_binning import EntropyBinning
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class EntropyBinningEncoder(Encoder[dtype.Categorical, dtype.Int64]):
    """
    Encoder for performing entropy binning encoding.
    Inherits the Encoder class.

    Example:
        encoder = EntropyBinningEncoder()
        transformed_data = encoder.transform(data)
    """

    slug = CategoricalEncoder.ENTROPY_BINNING_ENCODER
    columns: List[str]

    def __init__(self, name: str) -> None:
        """
        Initialize the EntropyBinningEncoder.
        """
        super().__init__()
        self.name = name
        self._encoder: Optional[EntropyBinning] = None
        self.scaler = None
        self.columns = [self.name]

    @property
    def encoder(self) -> EntropyBinning:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = EntropyBinning()
        self._encoder.fit_transform(X)

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Int64]:
        # Transform the data using the encoder
        transformed = self.encoder.transform(X)
        return pd.Series(transformed, name=self.name, index=X.index).to_frame()  # type: ignore

    def fit_transform(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> DataFrame[dtype.Int64]:
        self._encoder = EntropyBinning()
        transformed = self._encoder.fit_transform(X)
        return pd.Series(transformed, name=self.name, index=X.index).to_frame()  # type: ignore
