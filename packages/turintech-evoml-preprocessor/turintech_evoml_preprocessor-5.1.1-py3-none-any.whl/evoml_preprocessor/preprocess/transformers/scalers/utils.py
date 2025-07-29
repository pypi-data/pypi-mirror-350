from typing import Dict, Tuple, Type, Union

from evoml_preprocessor.preprocess.models import GenericOption, ScalerEncoder
from evoml_preprocessor.preprocess.transformers.scalers.gauss_rank_scaler import GaussRankScaler
from evoml_preprocessor.preprocess.transformers.scalers.identity_scaler import IdentityScaler
from evoml_preprocessor.preprocess.transformers.scalers.max_abs_scaler import MaxAbsScaler
from evoml_preprocessor.preprocess.transformers.scalers.min_max_scaler import MinMaxScaler
from evoml_preprocessor.preprocess.transformers.scalers.robust_scaler import RobustScaler
from evoml_preprocessor.preprocess.transformers.scalers.standard_scaler import StandardScaler


def init_scaler(
    scaler_slug: str,
) -> Tuple[
    Union[
        IdentityScaler,
        MinMaxScaler,
        StandardScaler,
        MaxAbsScaler,
        RobustScaler,
        GaussRankScaler,
    ],
    Union[ScalerEncoder, GenericOption],
]:
    """Initialize and return the scaler based on the provided encoder slug.
    Args:
        scaler_slug (str):
            Slug corresponding to the desired encoder.
    Returns:
        Encoder or None:
            The initialized encoder instance or None if no valid encoder slug is provided.
    """

    scalers: Dict[
        Union[GenericOption, ScalerEncoder],
        Union[Type[MinMaxScaler], Type[StandardScaler], Type[MaxAbsScaler], Type[RobustScaler], Type[GaussRankScaler]],
    ] = {
        GenericOption.AUTO: MinMaxScaler,
        ScalerEncoder.MIN_MAX_SCALER: MinMaxScaler,
        ScalerEncoder.STANDARD_SCALER: StandardScaler,
        ScalerEncoder.MAX_ABS_SCALER: MaxAbsScaler,
        ScalerEncoder.ROBUST_SCALER: RobustScaler,
        ScalerEncoder.GAUSS_RANK_SCALER: GaussRankScaler,
    }

    if scaler_slug == GenericOption.AUTO:
        scaler_slug = ScalerEncoder.MIN_MAX_SCALER

    if scaler_slug in scalers:
        scaler_class = scalers[scaler_slug]
        return scaler_class(), scaler_slug

    scaler_slug = GenericOption.NONE

    return IdentityScaler(), scaler_slug
