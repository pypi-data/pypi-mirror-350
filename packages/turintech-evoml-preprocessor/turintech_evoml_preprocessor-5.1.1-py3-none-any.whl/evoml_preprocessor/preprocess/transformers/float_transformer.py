# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, List, Optional

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType
from evoml_utils.convertors.detected_types import to_float_column

# Module
from evoml_preprocessor.preprocess.models import Block, GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.models.report import TransformationBlock
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.encoders.utils import init_encoder
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class FloatTransformer(Transformer):
    """
    The float type data denotes raw float data type. This class transforms a float
    column using the set of encoders defined in ENCODER_LIST. Auto implies the
    dataset is just scaled using MinMaxScaler.
    """

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

        self.impute_setting = DetectedType.float
        self.encoder = None
        self.scaler = None

    def _init_report(self) -> None:
        super()._init_report()

        self.blocks = [Block.FLOAT]
        self.encoders = [self.encoder_slug]

    def _init_operations(self, data: pd.Series[Any]) -> None:
        # TODO this ought to be done in the _impute method?
        data.replace([np.inf, -np.inf], np.nan, inplace=True)

        if self.encoder_slug == GenericOption.AUTO:
            self.encoder_slug = None

        if self.encoder_slug is None and self.scaler_slug == GenericOption.AUTO:
            self.scaler_slug = ScalerEncoder.STANDARD_SCALER
        elif self.encoder_slug is None and self.scaler_slug is None:
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data
        return to_float_column(data)

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:
        if self.encoder is None:
            self.encoder = init_encoder(self.encoder_slug)
            return self.encoder.fit_transform(data)

        return self.encoder.transform(data)

    def _report(self) -> None:
        self.transformation_block.append(
            TransformationBlock(
                block_name=Block.FLOAT,
                encoder_name=self.encoder_slug,
                scaler_name=self.scaler_slug,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )
