from __future__ import annotations

import re
from typing import List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder as _OneHotEncoder

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class OneHotEncoder(Encoder[dtype.Categorical, dtype.Uint8]):
    """
    Encoder for performing one-hot encoding.

    This encoder transforms categorical variables into a one-hot numeric array.
    Each category is converted to a binary column where 1 indicates the presence
    of the category and 0 indicates its absence.

    Column Naming Convention:
    -------------------------
    Output columns are named using the pattern: "{column_name}_onehot{index}_{category_value}"
    where:
    - column_name: The original column name passed during initialization
    - index: The numeric index of the category (1-based)
    - category_value: The actual category value, sanitized and truncated if needed
      (spaces and special characters are replaced with underscores,
      values longer than 15 characters are truncated)

    Examples:
    - For a column "color" with values ["red", "green", "blue"], the encoder will produce:
      "color_onehot1_red", "color_onehot2_green", "color_onehot3_blue"
    - For a column "status" with value "pending approval", the encoder will produce:
      "status_onehot1_pending_approval"

    Inherits the Encoder class.
    """

    slug = CategoricalEncoder.ONE_HOT_ENCODER
    columns: List[str]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._encoder = None

    @property
    def encoder(self) -> _OneHotEncoder:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def _sanitize_category_value(self, value, max_length: int = 15) -> str:
        """
        Sanitize category values for use in column names.

        Args:
            value: The category value to sanitize
            max_length: Maximum length for the sanitized value before truncation

        Returns:
            A sanitized string suitable for use in a column name
        """
        # Convert to string and truncate if needed
        value_str = str(value)
        if len(value_str) > max_length:
            value_str = value_str[:max_length] + "..."

        # Replace spaces and special characters with underscores
        sanitized = re.sub(r"[^a-zA-Z0-9]", "_", value_str)

        # Ensure the value doesn't start with a number (for valid identifier)
        if sanitized and sanitized[0].isdigit():
            sanitized = f"v_{sanitized}"

        return sanitized

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        # @pyright: confusion over possible dtypes
        self._encoder = _OneHotEncoder(sparse_output=False, handle_unknown="ignore", dtype=np.uint8)  # type: ignore

        # @data: no copy
        X_np = X.to_numpy().reshape(-1, 1)

        self.encoder.fit(X_np)

        # Get the actual category values
        categories = self.encoder.categories_[0]

        # Create descriptive column names combining index and sanitized category values
        self.columns = [
            f"{self.name}_onehot{i+1}_{self._sanitize_category_value(cat)}" for i, cat in enumerate(categories)
        ]

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Uint8]:
        X_np = X.to_numpy().reshape(-1, 1)

        transformed = self.encoder.transform(X_np)

        return pd.DataFrame(transformed, columns=self.columns, index=X.index)  # type: ignore
