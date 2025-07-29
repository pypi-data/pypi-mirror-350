# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
import re
from typing import Any, List, Optional, Tuple
from urllib.parse import urlparse

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import BaseTypes, DetectedType
from evoml_utils.convertors import type_to_convert_function

# Module
from evoml_preprocessor.preprocess.models import Block, CategoricalEncoder, GenericOption, ImputeStrategy, ScalerEncoder
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.encoders.categorical.hash_encoder import HashEncoder
from evoml_preprocessor.preprocess.transformers.scalers.identity_scaler import IdentityScaler
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.numpy import NumericArray, StringArray
from evoml_preprocessor.types.pandas import Series

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class UrlTransformer(Transformer):
    """Transformer for URL columns.
    Attributes:
        name (str): name of the transformer
        columns (list): list of columns
        detected_type (DetectedType): detected type of the column
        encoder_slug (str): encoder slug
        scaler_slug (str): scaler slug
        impute_strategy (ImputeStrategy): impute strategy
        impute_value (str): impute value
        netloc_encoder (FeatureHasher): encoder for netloc
        path_encoder (FeatureHasher): encoder for path
        fragment_encoder (FeatureHasher): encoder for fragment
        scaler (MinMaxScaler): scaler
    """

    encoder_slug: AllEncoders
    scaler_slug: AllScalers

    url_pattern = re.compile(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    )

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
    ):
        super().__init__(column_info, encoder, scaler, impute_strategy, impute_value, derived_columns)

        # impute
        self.impute_setting = DetectedType.url

        # encoders/scaler
        self._netloc_encoder: Optional[HashEncoder] = None
        self._path_encoder: Optional[HashEncoder] = None
        self._fragment_encoder: Optional[HashEncoder] = None
        self.scaler = IdentityScaler()

    @staticmethod
    def split_url(s: str) -> Tuple[str, str, str]:
        if not isinstance(s, str) or not UrlTransformer.url_pattern.fullmatch(s):
            netloc = ""
            path = ""
            fragment = ""
        else:
            url_obj = urlparse(s)
            netloc = url_obj.netloc
            path = url_obj.path
            fragment = url_obj.params + url_obj.query + url_obj.fragment
        return netloc, path, fragment

    @staticmethod
    def parse_urls(
        data: Series[dtype.String],
    ) -> Tuple[Series[dtype.String], Series[dtype.String], Series[dtype.String]]:
        """Parse the urls into netloc, path, and fragment.

        TODO: this would be more efficient if we used pandas
        and vectorized the parsing

        Args:
            data (np.ndarray):
                data to be parsed
        Returns:
            (list, list, list):
                netloc, path, and fragment lists
        """

        parsed_data = data.apply(UrlTransformer.split_url)
        return (
            parsed_data.apply(lambda x: x[0]),
            parsed_data.apply(lambda x: x[1]),
            parsed_data.apply(lambda x: x[2]),
        )

    def _init_operations(self, data: pd.Series[str]) -> None:
        if self.encoder_slug != GenericOption.NONE:
            self.encoder_slug = GenericOption.AUTO
            self.scaler_slug = ScalerEncoder.MIN_MAX_SCALER
            return

        # transformation settings
        self.type = BaseTypes.string
        self.scaler_slug = GenericOption.NONE

    def _init_report(self) -> None:
        if self.encoder_slug == GenericOption.NONE:
            self.all_columns = [[self.name]]
            self.encoders = [GenericOption.NONE]
            self.blocks = [Block.URL]
        else:
            self.encoders = [
                CategoricalEncoder.HASH_ENCODER,
                CategoricalEncoder.HASH_ENCODER,
                CategoricalEncoder.HASH_ENCODER,
            ]
            self.blocks = [Block.URL_NETLOC, Block.URL_PATH, Block.URL_FRAGMENT]

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data
        # @pyright: we need to fix the TypeConvertor alias in utils
        return type_to_convert_function("url")(data)  # type: ignore

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:

        if self.encoder_slug == GenericOption.NONE:
            self.columns = [self.name]
            return data.to_frame()

        # parse
        netloc, path, fragment = self.parse_urls(data)

        if not self.fitted:
            self._netloc_encoder = HashEncoder(
                name=f"{self.name}_{self.blocks[0].value.lower()}",
                length=Transformer.HASH_LENGTH,
            )
            self._path_encoder = HashEncoder(
                name=f"{self.name}_{self.blocks[1].value.lower()}",
                length=Transformer.HASH_LENGTH,
            )
            self._fragment_encoder = HashEncoder(
                name=f"{self.name}_{self.blocks[2].value.lower()}",
                length=Transformer.HASH_LENGTH,
            )

            netloc_df = self.netloc_encoder.fit_transform(netloc)
            path_df = self.path_encoder.fit_transform(path)
            fragment_df = self.fragment_encoder.fit_transform(fragment)

            self.columns = self.netloc_encoder.columns + self.path_encoder.columns + self.fragment_encoder.columns
            self.all_columns = [
                self.netloc_encoder.columns,
                self.path_encoder.columns,
                self.fragment_encoder.columns,
            ]

        else:
            netloc_df = self.netloc_encoder.transform(netloc)
            path_df = self.path_encoder.transform(path)
            fragment_df = self.fragment_encoder.transform(fragment)

        data_df = netloc_df
        for column in path_df.columns:
            data_df[column] = path_df[column]
        for column in fragment_df.columns:
            data_df[column] = fragment_df[column]

        return data_df

    @property
    def netloc_encoder(self) -> HashEncoder:
        if self._netloc_encoder is None:
            raise ValueError("Netloc encoder must be set during fitting.")
        return self._netloc_encoder

    @property
    def path_encoder(self) -> HashEncoder:
        if self._path_encoder is None:
            raise ValueError("Path encoder must be set during fitting.")
        return self._path_encoder

    @property
    def fragment_encoder(self) -> HashEncoder:
        if self._fragment_encoder is None:
            raise ValueError("Fragment encoder must be set during fitting.")
        return self._fragment_encoder
