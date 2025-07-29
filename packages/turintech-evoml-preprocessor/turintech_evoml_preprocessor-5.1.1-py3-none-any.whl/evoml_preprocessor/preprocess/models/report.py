# Standard Library
from enum import Enum
from typing import Dict, List, Optional, Union

# Private Dependencies
from evoml_api_models import DetectedType

# Dependencies
from pydantic import BaseModel, Field, validator

from evoml_preprocessor.preprocess.generator.models import FeatureGenerationReport

# Module
from evoml_preprocessor.preprocess.models import (
    Block,
    CategoricalEncoder,
    EmbeddingTransformer,
    GenericOption,
    ImputeStrategy,
    NumericEncoder,
    ReasonDropped,
    ScalerEncoder,
)
from evoml_preprocessor.preprocess.models.enum import ProteinEmbeddingTransformer
from evoml_preprocessor.preprocess.selector.models import FeatureSelectionReport

# ──────────────────────────────────────────────────────────────────────────── #

Encoder = Union[
    GenericOption,
    NumericEncoder,
    CategoricalEncoder,
    EmbeddingTransformer,
    ProteinEmbeddingTransformer,
    None,
]
Scaler = Union[GenericOption, ScalerEncoder]


def to_pascal(name: str) -> str:
    if "-" in name:
        return "".join([word.capitalize() for word in name.split("-")])
    return name


def get_encoder(name: str) -> Encoder:
    encoder_map: Dict[str, Encoder] = {
        "OrdinalEncoder": CategoricalEncoder.ORDINAL_ENCODER,
        "OneHotEncoder": CategoricalEncoder.ONE_HOT_ENCODER,
        "BackwardDifferenceEncoder": CategoricalEncoder.BACKWARD_DIFFERENCE_ENCODER,
        "CatBoostEncoder": CategoricalEncoder.CAT_BOOST_ENCODER,
        "HelmertEncoder": CategoricalEncoder.HELMERT_ENCODER,
        "TargetEncoder": CategoricalEncoder.TARGET_ENCODER,
        "LogEncoder": NumericEncoder.LOG_ENCODER,
        "SquareEncoder": NumericEncoder.SQUARE_ENCODER,
        "ReciprocalEncoder": NumericEncoder.RECIPROCAL_ENCODER,
        # Text embedders
        "tfidf": EmbeddingTransformer.TFIDF,
        "DistilbertBaseUncased": EmbeddingTransformer.DISTILBERT_BASE_UNCASED,
        "BertBaseUncased": EmbeddingTransformer.BERT_BASE_UNCASED,
        "RobertaBase": EmbeddingTransformer.ROBERTA_BASE,
        "AlbertBaseV2": EmbeddingTransformer.ALBERT_BASE_V2,
        "gpt2": EmbeddingTransformer.GPT2,
        "XlnetBaseCased": EmbeddingTransformer.XLNET_BASE_CASED,
        "ElectraBaseDiscriminator": EmbeddingTransformer.ELECTRA_BASE_DISCRIMINATOR,
        "AllMiniLML6V2": EmbeddingTransformer.ALL_MINI_LM_L6_V2,
        "AllMiniLML12V2": EmbeddingTransformer.ALL_MINI_LM_L12_V2,
        "AllMpnetBaseV2": EmbeddingTransformer.ALL_MPNET_BASE_V2,
        "AllDistilrobertaV1": EmbeddingTransformer.ALL_DISTILROBERTA_V1,
        "CodebertBase": EmbeddingTransformer.CODEBERT_BASE,
        "ProtBert": ProteinEmbeddingTransformer.PROT_BERT,
        "ProtBertBFD": ProteinEmbeddingTransformer.PROT_BERT_BFD,
        "ProtElectraDiscriminatorBfd": ProteinEmbeddingTransformer.PROT_ELECTRA_DISCRIMINATOR_BFD,
        "none": None,
    }

    # Add the items with multiple labels
    multi_label_items: Dict[str, Encoder] = {
        "LabelEncodingTransformer": CategoricalEncoder.LABEL_ENCODER,
        "LabelEncoder": CategoricalEncoder.LABEL_ENCODER,
        "FeatureHasher": CategoricalEncoder.HASH_ENCODER,
        "HashEncoder": CategoricalEncoder.HASH_ENCODER,
        "PowerTransformer": NumericEncoder.POWER_ENCODER,
        "PowerEncoder": NumericEncoder.POWER_ENCODER,
        "QuantileTransformer": NumericEncoder.QUANTILE_TRANSFORM_ENCODER,
        "quantile-transform-encoder": NumericEncoder.QUANTILE_TRANSFORM_ENCODER,
    }

    encoder_map.update(multi_label_items)

    if name in encoder_map:
        return encoder_map[name]
    else:
        raise ValueError(f"Encoder ({name}) not found")


class TransformationBlock(BaseModel):
    """Captures the transformation process for each block"""

    block_name: Block
    encoder_name: Optional[Encoder]
    scaler_name: Optional[Scaler]
    impute_strategy: Optional[ImputeStrategy]
    column_names: List[str]
    column_dropped: Optional[List[str]]
    reason_dropped: Optional[ReasonDropped]

    @validator("encoder_name", pre=True, always=True, allow_reuse=True)
    @classmethod
    def validate_encoder(cls, encoder: Union[Encoder, str]) -> Optional[Encoder]:
        """Ensures valid encoder enum is returned.

        Args:
            encoder:
                string or Enum (NumericEncoder, CategoricalEncoder or EmbeddingProcesses).
        Returns:
            Optional[Encoder]:
                None or Enum (NumericEncoder, CategoricalEncoder or EmbeddingProcesses).
        """
        # For correct types (enum, str, none), trust pydantic's validation
        if encoder is None:
            return encoder
        if isinstance(encoder, str):
            return encoder
        if isinstance(
            encoder,
            (GenericOption, NumericEncoder, CategoricalEncoder, EmbeddingTransformer, ProteinEmbeddingTransformer),
        ):
            return encoder

        # Remaining cases: given class instances
        name = to_pascal(type(encoder).__name__)
        return get_encoder(name)

    @validator("scaler_name", pre=True, always=True, allow_reuse=True)
    @classmethod
    def validate_scaler(cls, scaler: Union[ScalerEncoder, str, None]) -> Optional[Scaler]:
        """Ensure valid scaler enum is returned.

        Args:
            scaler:
                string or Enum Union[ScalerEncoder, None]
        Returns:
            Optional[ScalerEncoder]:
                None or Enum ScalerEncoder
        """
        # For correct types (enum, str, none), trust pydantic's validation
        if scaler is None:
            return scaler
        if isinstance(scaler, str):
            return scaler
        if isinstance(scaler, (GenericOption, ScalerEncoder)):
            return scaler

        # Remaining cases: given class instances
        name = to_pascal(type(scaler).__name__)
        if name == "MinMaxScaler":
            return ScalerEncoder.MIN_MAX_SCALER
        if name == "StandardScaler":
            return ScalerEncoder.STANDARD_SCALER
        if name == "MaxAbsScaler":
            return ScalerEncoder.MAX_ABS_SCALER
        if name == "RobustScaler":
            return ScalerEncoder.ROBUST_SCALER
        if name == "GaussRankScaler":
            return ScalerEncoder.GAUSS_RANK_SCALER
        raise ValueError(f"Encoder ({name}) not found")


class FeatureReport(BaseModel):
    """The transformation process for each column in a dataset is captured using
    a FeatureReport model.
    The specific transformations performed are captured using a list of
    TransformationBlock models.
    """

    column_name: str
    column_index: int
    detected_type: DetectedType
    impute_count: Optional[int]
    required_by_user: Optional[bool]
    reason_dropped: Optional[ReasonDropped]
    transformation_block: Optional[List[TransformationBlock]]

    @validator("detected_type", pre=True, always=True, allow_reuse=True)
    @classmethod
    def validate_detected_type(cls, name: Union[DetectedType, str]) -> DetectedType:
        """Ensures a valid DetectedType Enum is used.
        Args:
            name:
                string or enum representation of DetectedType
        Returns:
            DetectedType:
                DetectedType enum
        """

        if isinstance(name, DetectedType):
            return name

        if name in list(DetectedType):
            return DetectedType(name)
        raise ValueError(f"DetectedType ({name}) not found")


# ------------------------------- data tables -------------------------------- #
class TableColumn(BaseModel):
    """TableColumn model."""

    name: str
    content: List[Union[str, Enum, List[str], None, int]] = []

    def add(self, item: Union[str, Enum, List[str], None, int]) -> None:
        """Add an item to the content list."""
        self.content.append(item)


# --------------------------- preprocessing report --------------------------- #
class MultiColumnStatistic(BaseModel):
    """Statistics about processing steps affecting multiple columns"""

    # Feature Selection
    featureSelectionReport: Optional[FeatureSelectionReport] = None
    # Feature Generation
    featureGenerationReport: Optional[FeatureGenerationReport] = None

    droppedRows: int = Field(0, ge=0)
    droppedColumns: int = Field(0, ge=0)

    encodedToOriginalMapping: Dict[str, str] = {}

    columnCountBeforePreprocessing: int
    columnCountAfterFeatureHandler: int
    columnCountAfterPreprocessing: int


class PreprocessingReport(BaseModel):
    """Main reporting model gathering feedback on the whole preprocessing
    process from different part of the code.
    This model is internal only, used as a base for generating specialised
    reporting tables & graphs.
    """

    totalPreprocessingTime: float = Field(..., gt=0)
    multiColumnStatistics: MultiColumnStatistic
    singleColumnStatistics: List[FeatureReport] = []
