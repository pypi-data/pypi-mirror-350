"""Implements the processing of categorical label columns"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional, Tuple

# Dependencies
import pandas as pd

from evoml_preprocessor.preprocess.handlers.label._base import LabelHandler

# Module
from evoml_preprocessor.preprocess.models import (
    CategoricalEncoder,
    ColumnInfo,
    ColumnOptions,
    PreprocessConfig,
)
from evoml_preprocessor.preprocess.transformers import LabelEncodingTransformer

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class CategoricalLabelHandler(LabelHandler):
    """This class provides methods to fit and transform categorical label columns"""

    def __init__(
        self, config: PreprocessConfig, column_info: ColumnInfo, column_options: Optional[ColumnOptions] = None
    ):
        super().__init__(config, column_info, column_options)

        # the only categorical encoder used is labelencoder
        self.encoder_slug = CategoricalEncoder.LABEL_ENCODER
        self.encoder: Optional[LabelEncodingTransformer] = None

    def _fit_transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        self.encoder = LabelEncodingTransformer(
            impute_strategy=self.impute_strategy, impute_value=self.impute_value, encoder=self.encoder_slug
        )
        self.encoder.base_type = self.base_type
        self.name = label_col.name
        encoded_col = self.encoder.fit_transform(label_col)[label_col.name]
        # label_col.astype(int).update(encoded_col) commenting for now because of dtype @simon

        # Remove the last class, which is the "unseen" class
        # The string selected for the unseen class guarantees that it will be the last class
        classes = self.encoder.encoder.classes_
        if classes is None:
            raise AttributeError("The encoder classes should be recorded during fitting.")
        label_mappings = [classes[i] for i in range(len(classes) - 1)]
        self.label_mappings = label_mappings

        return encoded_col, None

    def transform(self, label_col: pd.Series) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
        """Applies the transformation as determined by the `self.fit_label_column`
        method.
        """
        # @TODO: implement this interface as mutating the `label_col` argument
        # to optimise memory usage
        if not self.fitted:
            raise ValueError("The encoder should be set by first calling fit.")

        assert self.encoder is not None
        encoded_col = self.encoder.transform(label_col)[label_col.name]
        # label_col.update(encoded_col) commenting for now because of dtype @simon

        return encoded_col, None

    def inverse_transform(self, transformed_label_col: pd.Series) -> pd.Series:
        assert self.encoder is not None, "Call `fit_transform` before calling this method"
        return self.encoder.inverse_transform(transformed_label_col)
