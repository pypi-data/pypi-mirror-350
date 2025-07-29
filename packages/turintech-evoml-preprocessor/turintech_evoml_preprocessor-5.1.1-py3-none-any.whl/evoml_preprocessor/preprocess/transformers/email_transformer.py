# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, List, Optional, Tuple

# Dependencies
import pandas as pd
from email_validator import ValidatedEmail

# Private Dependencies
from evoml_api_models import DetectedType
from evoml_utils.convertors.detected_types import to_email_objs_column

# Module
from evoml_preprocessor.preprocess.models import Block, CategoricalEncoder, GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.encoders.categorical.hash_encoder import HashEncoder
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class EmailTransformer(Transformer):
    """
    This class transforms an email column by splitting the column into two: domain and local part.
    These two components are then encoded using a hash encoding scheme.
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

        # impute
        self.impute_setting = DetectedType.email

        # encoder/scaler
        self._domain_encoder: Optional[HashEncoder] = None
        self._local_part_encoder: Optional[HashEncoder] = None
        self.scaler = None

        # reporting
        self.all_columns = []

    @staticmethod
    def split_email(x: Optional[ValidatedEmail]) -> Tuple[str, str]:
        if x is not None and type(x).__name__ == "ValidatedEmail":
            return x.domain, x.local_part
        return "", ""

    def _init_report(self) -> None:
        super()._init_report()
        if self.encoder_slug == GenericOption.NONE:
            self.blocks = [Block.EMAIL]
            self.encoders = [GenericOption.NONE]
        else:
            self.blocks = [Block.EMAIL_DOMAIN, Block.EMAIL_LOCAL_PART]
            self.encoders = [
                CategoricalEncoder.HASH_ENCODER,
                CategoricalEncoder.HASH_ENCODER,
            ]

        self.columns = [self.name]
        self.all_columns = [[self.name]]

    def _init_operations(self, data: pd.Series[Any]) -> None:
        if self.encoder_slug != GenericOption.NONE:
            self.encoder_slug = GenericOption.AUTO
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER
            return

        # transformation settings
        self.scaler_slug = GenericOption.NONE

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data
        return to_email_objs_column(data)

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:
        if self.encoder_slug == GenericOption.NONE:
            return data.to_frame()

        email_parts = data.apply(EmailTransformer.split_email)
        domain = email_parts.apply(lambda x: x[0])
        local_part = email_parts.apply(lambda x: x[1])

        if not self.fitted:
            self._domain_encoder = HashEncoder(
                name=f"{self.name}_{self.blocks[0].value.lower()}",
                length=Transformer.HASH_LENGTH,
            )
            self._local_part_encoder = HashEncoder(
                name=f"{self.name}_{self.blocks[1].value.lower()}",
                length=Transformer.HASH_LENGTH,
            )

            domain_df = self.domain_encoder.fit_transform(domain)
            local_part_df = self.local_part_encoder.fit_transform(local_part)

            self.columns = self.domain_encoder.columns + self.local_part_encoder.columns
            self.all_columns = [self.domain_encoder.columns, self.local_part_encoder.columns]
        else:
            domain_df = self.domain_encoder.transform(domain)
            local_part_df = self.local_part_encoder.transform(local_part)

        data_df = domain_df
        for column in local_part_df.columns:
            data_df[column] = local_part_df[column]

        return data_df

    @property
    def domain_encoder(self) -> HashEncoder:
        if self._domain_encoder is None:
            raise ValueError("Domain encoder must be set during fitting.")
        return self._domain_encoder

    @property
    def local_part_encoder(self) -> HashEncoder:
        if self._local_part_encoder is None:
            raise ValueError("Local encoder must be set during fitting.")
        return self._local_part_encoder
