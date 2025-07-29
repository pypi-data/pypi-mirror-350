# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, List, Optional, Union

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType
from evoml_utils.convertors.detected_types import convert_percentage_column

# Module
from evoml_preprocessor.preprocess.models import Block, GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.models.report import TransformationBlock
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.encoders.utils import get_default_numeric_encoding, init_encoder
from evoml_preprocessor.preprocess.transformers.utils import is_numeric_column_categorical
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class PercentageTransformer(Transformer):
    """Auto encoding methods for percentage data type columns"""

    encoder_slug: AllEncoders
    scaler_slug: AllScalers

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
    ) -> None:
        super().__init__(column_info, encoder, scaler, impute_strategy, impute_value, derived_columns)

        self.is_categorical = False
        self.scaler = None
        self.encoder = None
        self.impute_setting = DetectedType.percentage
        self.block = Block.PERCENTAGE

    def _init_operations(self, data: pd.Series[Any]) -> None:
        if self.encoder_slug is None:
            if self.scaler_slug is None:
                self.scaler_slug = ScalerEncoder.STANDARD_SCALER
            return

        if self.encoder_slug != GenericOption.AUTO:
            return

        if is_numeric_column_categorical(data):
            self.encoder_slug = None
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER

        # select encoder based on data skew
        self.encoder_slug = get_default_numeric_encoding(data, self.name)

        if self.scaler_slug is None or self.scaler_slug == GenericOption.AUTO:
            self.scaler_slug = ScalerEncoder.STANDARD_SCALER

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data
        return convert_percentage_column(data)

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series] = None) -> NumericArray:
        if self.encoder_slug == GenericOption.NONE:
            return data.to_frame()

        if self.encoder is None:
            self.encoder = init_encoder(self.encoder_slug)
            return self.encoder.fit_transform(data)

        return self.encoder.transform(data)

    def _report(self) -> None:
        self.transformation_block.append(
            TransformationBlock(
                block_name=self.block,
                encoder_name=self.encoder_slug,
                scaler_name=self.scaler_slug,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )
