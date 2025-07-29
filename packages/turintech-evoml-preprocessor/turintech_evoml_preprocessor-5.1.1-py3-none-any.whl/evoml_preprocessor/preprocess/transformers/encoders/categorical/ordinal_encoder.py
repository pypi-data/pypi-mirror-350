from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder as _OrdinalEncoder

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class OrdinalEncoder(Encoder[dtype.Categorical, dtype.Int16]):
    """
    Encoder for performing ordinal encoding.
    Inherits the Encoder class.

    @NOTE: we choose the target dtype as 16-bit integer
    which gives us a maximum supported number of unique values
    of 65536. It's entirely possible to get higher cardinality
    categorical features, but these features aren't useful and
    some more fancy text encoding would probably be needed.

    Example:
        encoder = OrdinalEncoder()
        transformed_data = encoder.transform(data)
    """

    slug = CategoricalEncoder.ORDINAL_ENCODER
    columns: List[str]

    def __init__(self, name: str, columns: Optional[List[str]] = None) -> None:
        super().__init__()
        self.name = name
        self._encoder: Optional[_OrdinalEncoder] = None
        self.columns = columns or [self.name]

    @property
    def encoder(self) -> _OrdinalEncoder:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        self._encoder = _OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-1, dtype=np.int16)  # type: ignore

        X_np = X.to_numpy().reshape(-1, 1)

        self.encoder.fit(X_np)  # Fit the encoder on the data
        self.name = str(X.name)

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Uint16]:
        X_np = X.to_numpy().reshape(-1, 1)

        transformed = self.encoder.transform(X_np)
        return pd.DataFrame(transformed, columns=self.columns, index=X.index)  # type: ignore
