# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
import warnings
from typing import Any, List, Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType

# Module
from evoml_preprocessor.preprocess.models import Block, CategoricalEncoder, GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.models.report import TransformationBlock
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.encoders.utils import (
    CategoricalEncoderInstanceType,
    init_categorical_encoder,
)
from evoml_preprocessor.types.numpy import NumericArray
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

warnings.filterwarnings("ignore", category=FutureWarning)

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
CONF = conf_mgr.preprocess_conf  # Alias for readability
# ──────────────────────────────────────────────────────────────────────────── #


class CategoricalTransformer(Transformer):
    """The class transforms a categorical column encoding it using the encoder
    slug selected in the constructor.

    The missing value of categorical type data is imputed. Then the encoder scheme
    selected in the constructor is used to encode the values. The thresholds are defined
    by ONE_HOT_ENCODING_THRESHOLD and LABEL_ENCODING_THRESHOLD respectively.

    The one hot encoding API from sklearn can handle 'unseen' data automatically. To
    handle the 'unseen data' for the hash encoding and label encoding, an
    'unseen' type data needed to be added manually.
    """

    encoder_slug: (
        AllEncoders  # during _init_operations we restrict the encoder_slug to Union[GenericOption, CategoricalEncoder]
    )
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

        # Aliases
        self.is_special_categorical = self.metadata.get("is_special_categorical", False) if self.metadata else False

        # State
        self.impute_setting = DetectedType.categorical

        # Operations
        self._encoder: Optional[CategoricalEncoderInstanceType] = None
        self.scaler = None

        # Report
        self.all_columns = []

    def _init_fit(self, data):
        self.name = str(data.name)

        if not self.skip_transform:
            return

        if data.dtype in [int, float]:
            logger.warning(f"Column {self.name} encoder was set as None.")
        else:
            logger.warning(
                f"Column {self.name} categorical encoder was specified as None. "
                f"However, this column contains non-numeric values."
            )

    def _init_report(self) -> None:
        super()._init_report()
        self.blocks = [Block.CATEGORICAL]

    def _init_operations(self, data: pd.Series[Any]) -> None:
        if self.encoder_slug == GenericOption.NONE:
            self.encoders = [GenericOption.NONE]
            return

        # encoder is invalid
        if self.encoder_slug not in list(CategoricalEncoder):
            self.encoder_slug = GenericOption.AUTO

        # set default encoder
        if self.is_special_categorical and self.encoder_slug != GenericOption.NONE:
            self.encoder_slug = CategoricalEncoder.ENTROPY_BINNING_ENCODER
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER
        elif self.encoder_slug is None or self.encoder_slug == GenericOption.AUTO:
            num_unique_values = data.nunique()

            if num_unique_values <= CONF.ONE_HOT_ENCODING_THRESHOLD:
                slug = CategoricalEncoder.ONE_HOT_ENCODER
            elif CONF.ONE_HOT_ENCODING_THRESHOLD < num_unique_values <= CONF.LABEL_ENCODING_THRESHOLD:
                slug = CategoricalEncoder.HASH_ENCODER
            else:
                slug = CategoricalEncoder.ORDINAL_ENCODER

            self.encoder_slug = slug

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        """
        @FIXME:
            This is a temporary fix while we resolve the 'no impute' option issue. Beforehand
            a redundant check was made that always resolved to true, so we were effectively
            imputing even if no impute was requested.

            if not pd.api.types.is_string_dtype(data):

        """
        data = data.astype(str)
        return data

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:
        if not self.fitted:
            self._encoder = (init_categorical_encoder(self.encoder_slug))(name=self.name)
            data_df = self.encoder.fit_transform(data, label)
        else:
            data_df = self.encoder.transform(data)

        self.columns = self.encoder.columns
        return data_df

    def _report(self) -> None:
        """
        Generates a transformation report for the Transformer.
        """
        self.transformation_block.append(
            TransformationBlock(
                block_name=Block.CATEGORICAL,
                encoder_name=self.encoder_slug,
                scaler_name=self.scaler_slug,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )

    @property
    def encoder(self) -> CategoricalEncoderInstanceType:
        if self._encoder is None:
            raise ValueError("Encoder should be set during fitting.")
        return self._encoder
