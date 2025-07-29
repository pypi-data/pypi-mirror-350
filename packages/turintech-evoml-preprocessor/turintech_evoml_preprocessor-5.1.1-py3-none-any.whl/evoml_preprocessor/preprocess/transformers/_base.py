"""
This module contains the Transformer class,
the base class defining the API for column-specific transformers.
"""

# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from abc import ABC
from typing import Any, Dict, List, Optional, Union

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, RobustScaler, StandardScaler

# Module
from evoml_preprocessor.preprocess.models import ImputeStrategy, ImputeValue
from evoml_preprocessor.preprocess.models.config import ColumnInfo
from evoml_preprocessor.preprocess.models.enum import (
    AllEncoders,
    AllScalers,
    CategoricalEncoder,
    DateOptions,
    EmbeddingTransformer,
    GenericOption,
    ImputeSubsets,
    NumericEncoder,
    ProteinEmbeddingTransformer,
    ScalerEncoder,
)
from evoml_preprocessor.preprocess.models.report import Block, Encoder, TransformationBlock
from evoml_preprocessor.preprocess.transformers.imputers._base import Imputer
from evoml_preprocessor.preprocess.transformers.imputers.utils import init_imputer
from evoml_preprocessor.preprocess.transformers.scalers.gauss_rank_scaler import GaussRankScaler
from evoml_preprocessor.preprocess.transformers.scalers.identity_scaler import IdentityScaler
from evoml_preprocessor.preprocess.transformers.scalers.utils import init_scaler
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
allowed_types = {
    GenericOption,
    ScalerEncoder,
    NumericEncoder,
    CategoricalEncoder,
    EmbeddingTransformer,
    ProteinEmbeddingTransformer,
}


class Transformer(ABC):
    """Base class defining the API for column-specific transformers.

    This class should not be instantiated directly, rather a subclass should be instantiated.
    For example: EmbeddingTransformer, FloatTransformer, CurrencyTransformer...

    Attributes:
        encoder_slug(Union[str, None]):
            The encoder to use to transform the data.
        scaler_slug(Union[str, None]):
            The scaler to use to scale the data.
        column_info(Union[ColumnInfo, None]):
            Info relating to the column currently being preprocessed.
        impute_strategy(ImputeStrategy):
            Strategy to deal with missing values.
        impute_value(Union[str, int, float, None]):
            Specific value to impute if the strategy is to impute a constant.
    """

    # CLASS
    HASH_LENGTH = 5
    DEFAULT_COLUMN_NAME = "X"

    # INSTANCE
    encoder_slug: AllEncoders
    scaler_slug: AllScalers
    columns: List[str]
    date_options: Optional[List[DateOptions]]
    scaler: Union[IdentityScaler, MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler, GaussRankScaler, None]

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
    ) -> None:
        """Transformer object modifies a feature so that it is compatible with a machine learning model.

        For an external interface, this class should provide two functions,
        - `fit_transform`, which 'fits' all the components to training data, and (since the pipeline
            is sequential), transforms the training data, returning machine learning ready data in
            the form of a `pd.DataFrame` (with one or more features)
        - `transform`, which implies that the object (and all components in the pipeline for this object)
            have been fit.

        Args:
            column_info: the settings for the transformation of the input feature, configures
                the transformer for the expected data.
            encoder: the initial encoder setting, if a valid encoder is provided, this will
                be used as long as the transformer is compatible with that encoder. Otherwise,
                a default will be chosen.
            scaler: the initial scaler settings, if a valid scaler is provided, this will
                be used as long as the transformer is compatible with that scaler. Otherwise,
                a default will be chosen.
            impute_strategy: the initial impute strategy setting, if a valid impute strategy
                is provided, this will be used as long as the transformer is compatible
                with that scaler. Otherwise, a default will be chosen.
            impute_value: the impute value, which will be used if the impute strategy expects
                one. The type should match up to the data and strategy.
        """
        self.column_info = column_info
        self.impute_strategy = impute_strategy
        self.impute_value = impute_value
        self.date_options = derived_columns

        # Aliases
        self.metadata: Dict[str, Any] = {}
        if self.column_info is not None and self.column_info.metadata is not None:
            self.metadata = self.column_info.metadata

        self.name: str = Transformer.DEFAULT_COLUMN_NAME
        self.hash_length = Transformer.HASH_LENGTH  # in case we want to expose this in the future
        self.skip_transform = False

        # State
        self.fitted = False
        self.impute_setting: Optional[DetectedType] = None
        self.columns = []

        # Reporting
        self.encoders: List[Encoder] = []
        self.all_columns: List[List[str]] = []
        self.blocks: List[Block] = []
        self.transformation_block: List[TransformationBlock] = []

        # Operations
        # @TODO, need to ensure that the inputs never have type list here.
        if isinstance(encoder, list):
            encoder = encoder[0]  # type: ignore
        if isinstance(scaler, list):
            scaler = scaler[0]  # type: ignore

        if encoder is not None and type(encoder) not in allowed_types:
            raise ValueError(f"Encoder {encoder} is invalid")

        if encoder == GenericOption.NONE:
            self.skip_transform = True

        self.imputer: Optional[Imputer] = None
        self.encoder_slug: AllEncoders = encoder
        self.scaler_slug: AllScalers = scaler

    def _init_fit(self, data: pd.Series[Any]) -> None:
        """This initialises any settings that need to occur before `fit`.

        We only take action if the encoder_slug is set to GenericOption.NONE,
        which skips any transformation operations after impute (even if the
        data is non-numeric)

        However, choosing None as an encoder can potentially break later parts of the
        code. Therefore, a warning is set, and an appropriate impute value is specified.

        If the impute strategy is not set to ImputeSubsets.CONSTANT_VALUE,
        a warning is issued, informing that the encoder is set to None, but the impute
        strategy is invalid. The impute strategy will then be set to constant.

        @TODO there's currently a case where data is not `pd.Series`, which
            causes some issues when extracting the column name. This should be
            fixed.

        Args:
            data (pd.Series):
                Single column :class:`pd.DataFrame` to process.

        """
        self.name = str(data.name)

        if not self.skip_transform:
            return

        if self.impute_strategy == ImputeStrategy.AUTO:
            self.impute_strategy = ImputeStrategy.CONSTANT

        if self.impute_strategy not in ImputeSubsets.CONSTANT_VALUE.value:
            logger.warning(
                f"Encoder is set to None, but impute strategy is {self.impute_strategy}, "
                f"which is invalid. Impute strategy will be set to constant."
            )
            self.impute_strategy = ImputeStrategy.CONSTANT

    def _init_report(self) -> None:
        """Initialises the reporting attributes.

        This method should be extended by subclasses in the case where the output
        columns depend on user input.
        """
        self.columns = [self.name]
        self.transformation_block.clear()

    def _init_operations(self, data: pd.Series[Any]) -> None:
        """Initialises the operations to be performed on the data.

        Operations include
        - impute
        - encode
        - scale

        Note that this initialisation **must** be done after the data has been
        converted to a valid column.

        Args:
            data (pd.Series):
                Single column :class:`pd.DataFrame` to process.
        """
        pass

    def fit_transform(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> pd.DataFrame:
        """Fits and transforms the input data.

        Args:
            data (pd.Series):
                Single column `pd.Dataframe` to process.
            label_col (pd.Series, optional):
                Single column `pd.Dataframe` corresponding to the preprocessed
                label column.

        Returns:
            pd.DataFrame:
                The preprocessed version of the column (`data`).
        """
        if not isinstance(data, pd.Series):
            raise ValueError("Data must be a single column `pd.DataFrame`.")
        if label is not None and not isinstance(label, pd.Series):
            raise ValueError("Label must be a single column `pd.DataFrame`.")

        # Force a refit
        self.fitted = False

        # Initialise
        self._init_fit(data)
        self._init_report()

        # Preparation
        data = self._convert(data)
        self._init_operations(data)

        # Operations
        data = self._impute(data)
        data_df = self._encode(data, label)
        data_df = self._scale(data_df)

        # Post-Operations
        self._report()
        self.fitted = True

        return data_df

    def transform(self, data: pd.Series[Any]) -> pd.DataFrame:
        """
        Transforms a column using an already fitted transformer.

        Args:
            data (pd.Series):
                Single column :class:`pd.DataFrame` to process.

        Returns:
            pd.DataFrame:
                The preprocessed version of the column (`data`).

        Raises:
            NotImplementedError:
                If the subclass has not implemented this method.
        """
        if not isinstance(data, pd.Series):
            raise ValueError("Data must be a `pd.Series`.")

        # Preparation
        data = self._convert(data)

        # Operations
        data = self._impute(data)
        data_df = self._encode(data)
        data_df = self._scale(data_df)

        return data_df

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        """
        Converts the data to a valid column if the encoder_slug is not set to NONE.

        Args:
            data: The data to be converted.

        Returns:
            pd.Series: The converted data.
        """
        return data

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:
        """Encode the data.
        Args:
            data (pd.Series):
                Data to be encoded.

        Returns:
            np.ndarray:
                The encoded data.
        """
        return data

    def _scale(self, data: NumericArray) -> NumericArray:
        """
        Scales the encoded data using self.scaler_slug provided.
        If self.scaler_slug = GenericOption.AUTO; then MinMaxScaler is used

        Args:
            data: The data to be scaled.

        Returns:
            np.ndarray:
        """
        if self.scaler is None:
            self.scaler, slug = init_scaler(self.scaler_slug)
            data_scaled = self.scaler.fit_transform(data)

            if slug != self.scaler_slug:
                self.scaler_slug = slug
        else:
            data_scaled = self.scaler.transform(data)

        return data_scaled

    def _impute(self, data: pd.Series[Any]) -> pd.Series[Any]:
        """Impute missing values in the data.
        Args:
            data (pd.Series):
                Data to be imputed.

        Returns:
            pd.Series:
                Imputed data.
        """
        if self.imputer is None:
            if self.impute_setting is None:
                raise ValueError("Impute setting must be set during initialization.")
            self.imputer, self.impute_strategy, self.impute_value = init_imputer(
                detected_type=self.impute_setting,
                strategy=self.impute_strategy,
                value=self.impute_value,
                metadata=self.metadata,
                column=data,
            )
            data = self.imputer.fit_transform(data)
            self.impute_value = self.imputer.value
            return data

        return self.imputer.transform(data)

    def _report(self) -> None:
        """
        Generates a transformation report for the Transformer.
        """
        new_blocks = [
            TransformationBlock(
                block_name=block,
                encoder_name=encoder,
                scaler_name=self.scaler_slug,
                impute_strategy=self.impute_strategy,
                column_names=column,
                column_dropped=None,
                reason_dropped=None,
            )
            for block, encoder, column in zip(self.blocks, self.encoders, self.all_columns)
        ]

        self.transformation_block.extend(new_blocks)
