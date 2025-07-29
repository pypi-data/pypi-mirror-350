# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Optional, Union, Type

# Dependencies
import numpy as np
import pandas as pd
from category_encoders import BinaryEncoder
from scipy.stats import skew

from evoml_preprocessor.preprocess.transformers.encoders.categorical.backward_difference_encoder import (
    BackwardDifferenceEncoder,
)
from evoml_preprocessor.preprocess.transformers.encoders.categorical.cat_boost_encoder import CatBoostEncoder
from evoml_preprocessor.preprocess.transformers.encoders.categorical.entropy_binning_encoder import (
    EntropyBinningEncoder,
)
from evoml_preprocessor.preprocess.transformers.encoders.categorical.hash_encoder import HashEncoder
from evoml_preprocessor.preprocess.transformers.encoders.categorical.helmert_encoder import HelmertEncoder
from evoml_preprocessor.preprocess.transformers.encoders.identity_encoder import IdentityEncoder
from evoml_preprocessor.preprocess.transformers.encoders.numeric.log_encoder import LogEncoder
from evoml_preprocessor.preprocess.transformers.encoders.categorical.one_hot_encoder import OneHotEncoder
from evoml_preprocessor.preprocess.transformers.encoders.categorical.ordinal_encoder import OrdinalEncoder
from evoml_preprocessor.preprocess.transformers.encoders.numeric.power_encoder import PowerEncoder
from evoml_preprocessor.preprocess.transformers.encoders.numeric.quantile_transformer import QuantileEncoder
from evoml_preprocessor.preprocess.transformers.encoders.numeric.reciprocal_encoder import ReciprocalEncoder
from evoml_preprocessor.preprocess.transformers.encoders.numeric.square_encoder import SquareEncoder
from evoml_preprocessor.preprocess.transformers.encoders.categorical.target_encoder import TargetEncoder
from evoml_preprocessor.preprocess.models import NumericEncoder, GenericOption, CategoricalEncoder

from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


def get_default_numeric_encoding(data: Union[np.ndarray, pd.Series], name: str) -> Optional[NumericEncoder]:
    all_positive = np.all(data >= 0)
    skew_level = abs(skew(data))
    if skew_level > conf_mgr.preprocess_conf.SKEWNESS_THRESHOLD:
        logger.warning("Column %s has high skew %s.", name, skew_level)
        if all_positive:
            encoder_slug = NumericEncoder.LOG_ENCODER
        else:
            encoder_slug = NumericEncoder.POWER_ENCODER
    else:
        # Note: None is not the same as GenericOption.NONE
        encoder_slug = None
    return encoder_slug


def init_encoder(encoder_slug: Union[str, None]):
    """Initialize and return the encoder based on the provided encoder slug.
    Args:
        encoder_slug (str):
            Slug corresponding to the desired encoder.
    Returns:
        Encoder or None:
            The initialized encoder instance or None if no valid encoder slug is provided.
    """
    encoders = {
        GenericOption.AUTO: IdentityEncoder,
        GenericOption.NONE: IdentityEncoder,
        NumericEncoder.LOG_ENCODER: LogEncoder,
        NumericEncoder.SQUARE_ENCODER: SquareEncoder,
        NumericEncoder.POWER_ENCODER: PowerEncoder,
        NumericEncoder.RECIPROCAL_ENCODER: ReciprocalEncoder,
        NumericEncoder.QUANTILE_TRANSFORM_ENCODER: QuantileEncoder,
    }

    if encoder_slug in encoders:
        encoder_class = encoders[encoder_slug]
        return encoder_class()
    elif encoder_slug is not None:
        logger.error(f"Column encoder {encoder_slug} is unsupported.")

    # default for auto is None
    return IdentityEncoder()


# Type aliases for all categorical encoder classes
CategoricalEncoderClassType = Union[
    Type[OrdinalEncoder],
    Type[IdentityEncoder],
    Type[OneHotEncoder],
    Type[HashEncoder],
    Type[BackwardDifferenceEncoder],
    Type[CatBoostEncoder],
    Type[TargetEncoder],
    Type[EntropyBinningEncoder],
    Type[HelmertEncoder],
]
CategoricalEncoderInstanceType = Union[
    OrdinalEncoder,
    IdentityEncoder,
    OneHotEncoder,
    HashEncoder,
    BackwardDifferenceEncoder,
    CatBoostEncoder,
    TargetEncoder,
    EntropyBinningEncoder,
    HelmertEncoder,
]


def init_categorical_encoder(encoder_slug: Union[str, None]) -> CategoricalEncoderClassType:
    encoder_methods = {
        GenericOption.AUTO: OrdinalEncoder,
        GenericOption.NONE: IdentityEncoder,
        CategoricalEncoder.ONE_HOT_ENCODER: OneHotEncoder,
        CategoricalEncoder.ORDINAL_ENCODER: OrdinalEncoder,
        CategoricalEncoder.LABEL_ENCODER: OrdinalEncoder,
        CategoricalEncoder.HASH_ENCODER: HashEncoder,
        CategoricalEncoder.BACKWARD_DIFFERENCE_ENCODER: BackwardDifferenceEncoder,
        CategoricalEncoder.CAT_BOOST_ENCODER: CatBoostEncoder,
        CategoricalEncoder.HELMERT_ENCODER: HelmertEncoder,
        CategoricalEncoder.TARGET_ENCODER: TargetEncoder,
        CategoricalEncoder.ENTROPY_BINNING_ENCODER: EntropyBinningEncoder,
    }

    if encoder_slug in encoder_methods:
        encoder_class = encoder_methods[encoder_slug]
        return encoder_class
    else:
        logger.error(f"Column encoder {encoder_slug} is unsupported.")

    # default for auto is None
    return OrdinalEncoder
