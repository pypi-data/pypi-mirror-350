from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

import evoml_preprocessor.types.dtype as dtype
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class ReciprocalEncoder(Encoder[dtype.Float64, dtype.Float64]):
    def __init__(self) -> None:
        """Initialize the ReciprocalEncoder."""
        self.min_threshold_positive = 0.001
        self.min_threshold_negative = -0.001
        self.reciprocal_pos_min = 0.001
        self.reciprocal_neg_max = 0.001
        self.median = np.nan
        self.fitted = False

    def fit(self, X: Series[dtype.Float64], y: Optional[SeriesTarget] = None) -> None:
        # Handle missing values
        nan_mask = np.isnan(X)
        # @mypy: nanmedian is flexible enough to return any float but we know input=output=float
        self.median = np.nanmedian(X)  # type: ignore
        X[nan_mask] = self.median

        # Calculate reciprocal_pos_min and reciprocal_neg_max
        pos_mask = X > self.min_threshold_positive
        if np.sum(pos_mask) > 0:
            self.reciprocal_pos_min = 0.5 * np.min(X[pos_mask])

        neg_mask = X < self.min_threshold_negative
        if np.sum(neg_mask) > 0:
            self.reciprocal_neg_max = 0.5 * np.max(X[neg_mask])

        self.fitted = True

    def transform(self, X: Series[dtype.Float64]) -> DataFrame[dtype.Float64]:
        if not self.fitted:
            raise ValueError("Reciprocal encoder not fitted")

        # Handle missing values
        nan_mask = np.isnan(X)
        X[nan_mask] = self.median

        # @data: no copy
        X_np = X.to_numpy()

        # Handle zero values
        zero_mask = X_np == 0
        positive_count = np.sum(X_np > 0, axis=0)
        negative_count = np.sum(X_np < 0, axis=0)
        zero_condition = positive_count >= negative_count

        X_np = np.where(
            zero_mask,
            np.where(zero_condition, self.reciprocal_pos_min, self.reciprocal_neg_max),
            X_np,
        )

        # Handle positive values close to zero
        pos_close_to_zero_mask = (X_np <= self.min_threshold_positive) & (X_np > 0)
        X_np = np.where(pos_close_to_zero_mask, self.reciprocal_pos_min, X_np)

        # Handle negative values close to zero
        neg_close_to_zero_mask = (X_np >= self.min_threshold_negative) & (X_np < 0)
        X_np = np.where(neg_close_to_zero_mask, self.reciprocal_neg_max, X_np)

        # Calculate the reciprocal
        X_np = np.reciprocal(X_np)
        transformed: Series[dtype.Float64] = pd.Series(X_np, name=X.name, index=X.index)  # type: ignore
        return transformed.to_frame()
