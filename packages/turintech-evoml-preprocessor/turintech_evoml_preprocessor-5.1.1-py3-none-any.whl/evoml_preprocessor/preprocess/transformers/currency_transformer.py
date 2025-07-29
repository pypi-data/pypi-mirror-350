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
from evoml_utils.convertors.detected_types.currency import currency_number_split

# Module
from evoml_preprocessor.preprocess.models import Block, CategoricalEncoder, GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.encoders.categorical.ordinal_encoder import OrdinalEncoder
from evoml_preprocessor.preprocess.transformers.encoders.utils import get_default_numeric_encoding, init_encoder
from evoml_preprocessor.preprocess.transformers.utils import is_numeric_column_categorical
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class CurrencyTransformer(Transformer):
    """
    This class transforms the currency column by splitting it into two numeric portion and currency.

    For the numeric portion:
    The integer type data could be raw integer type data or data encoded from categorical data.
    For the data encoded from categorical data, only missing value is filled.
    For the raw integer type data, the pipeline is filling missing value and conducting power transformation.

    For the currency portion:
    The currency ($, £, ) is transformed using ordinal encoder
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

        # convert
        self.n_currencies = len(self.metadata["allCurrencies"])

        # impute
        self.impute_setting = DetectedType.currency

        # encoder/scaler
        self._currency_encoder: Optional[OrdinalEncoder] = None
        self.scaler = None
        self.encoder = None

        #  reporting
        self.blocks = [Block.CURRENCY_VALUE, Block.CURRENCY_SIGN]
        self.encoders = [self.encoder_slug, CategoricalEncoder.ORDINAL_ENCODER]

        # FIXME: remove this once we formalize the converters
        self.currency = None

    def _init_operations(self, data: pd.Series) -> None:
        if self.encoder_slug is None:
            if self.scaler_slug is None:
                self.scaler_slug = ScalerEncoder.STANDARD_SCALER
            return

        if self.encoder_slug != GenericOption.AUTO:
            return

        if is_numeric_column_categorical(data):
            self.encoder_slug = None
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER

        self.encoder_slug = get_default_numeric_encoding(data, self.name)

        if self.scaler_slug is None or self.scaler_slug == GenericOption.AUTO:
            self.scaler_slug = ScalerEncoder.STANDARD_SCALER

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data
        return self._convert_currency_column(data)

    def _convert_currency_column(self, data: pd.Series[Any]) -> pd.Series[Any]:
        """
        Converts a column of string currency values to a column consisting of the numeric parts of the currency values.
        Any invalid string value is converted to a None value.

        NOTE: This currently overrides the `utils` implementation so that we don't need
        to reconvert the currency column in the case of multiple currencies.

        This allows us to use the same `encode` signature as the other transformers. The issue is that
        now we have an awkward internally stored currency value.

        Args:
            column:
                The input column in pandas.Series format.
        Returns:
            pd.Series:
                The converted column consisting of floats and None values.
        """
        split_data = data.apply(currency_number_split)
        self.currency = split_data.apply(lambda x: x[1])
        return split_data.apply(lambda x: x[0])

    def _encode(self, data: pd.Series, label: Optional[pd.Series] = None) -> NumericArray:
        """Encode the data.
        Args:
            data (np.ndarray):
                Data to be encoded.

        Returns:
            np.ndarray:
                The encoded data.
        """
        if self.encoder is None:
            self.encoder = init_encoder(self.encoder_slug)
            data_df = self.encoder.fit_transform(data)
        else:
            data_df = self.encoder.transform(data)

        # add currency sign encoding
        if self.n_currencies > 1:
            currency_transformed = self._get_categorical_encoding()
            for column in currency_transformed.columns:
                data_df[column] = currency_transformed[column]
            self.columns = [self.name, f"{self.name}_currency"]
            self.all_columns = [[self.name], [f"{self.name}_currency"]]
        else:
            self.columns = [self.name]
            self.all_columns = [[self.name]]

        return data_df

    def _get_categorical_encoding(self) -> pd.DataFrame:
        """Encode the currency data
        Args:
            data (pd.Series):
               The converted currency column (using convert_currency_column).
            original_data (pd.Series):
                The original currency column.
        Returns:
            pd.DataFrame:
                Transformed output data.
        """
        if self.currency is None:
            raise ValueError("Currency number split is not set.")
        if not self.fitted:
            self._currency_encoder = OrdinalEncoder(name=self.name)
            transformed = self.currency_encoder.fit_transform(self.currency)
        else:
            transformed = self.currency_encoder.transform(self.currency)

        return pd.DataFrame(transformed)

    @property
    def currency_encoder(self) -> OrdinalEncoder:
        if self._currency_encoder is None:
            raise ValueError("Currency encoder must be set during fitting.")
        return self._currency_encoder
