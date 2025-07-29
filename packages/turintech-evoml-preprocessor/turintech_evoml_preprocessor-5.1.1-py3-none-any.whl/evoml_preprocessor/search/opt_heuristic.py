import logging
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
from evoml_api_models import DetectedType
from sklearn.preprocessing import StandardScaler

from evoml_preprocessor.preprocess.models import (
    CategoricalEncoder,
    GenericOption,
    ImputeStrategy,
    NumericEncoder,
    ScalerEncoder,
)
from evoml_preprocessor.preprocess.models.enum import AllCategorical, AllNumeric, AllScalers
from evoml_preprocessor.preprocess.transformers import CategoricalTransformer, FloatTransformer
from evoml_preprocessor.preprocess.transformers.imputers.utils import init_imputer
from evoml_preprocessor.search.encoder_space import EncoderSpace
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

logger = logging.getLogger("preprocessor")
CONF = conf_mgr.preprocess_conf  # Alias for readability


@dataclass
class Statistics:
    """Collection of statistics for numerical data"""

    positive: pd.Series
    zero_mean: pd.Series
    unity_var: pd.Series
    high_corr: pd.Series


@dataclass
class ScaledStatistics:
    """Statistics for scaled data"""

    positive: pd.Series
    positive_skew: pd.Series
    negative_skew: pd.Series
    high_kurtosis: pd.Series
    vhigh_kurtosis: pd.Series
    low_kurtosis: pd.Series


def _raw_analysis(data: pd.DataFrame, label: pd.Series) -> Statistics:
    """Performs analysis on raw numerical data.
    Args:
        data:
            Raw data (numerical).
        label:
            Target column.
    Returns:
        A collection of pandas series that contain booleans for each feature,
        that describe the statistics of each feature.
    """
    expected: pd.Series = data.mean(axis=0)
    variance: pd.Series = (data - expected).var(axis=0)
    label_correlation: pd.Series = data.corrwith(label)
    minimum: pd.Series = data.min(axis=0)

    return Statistics(
        zero_mean=expected.round(1) == 0,
        unity_var=variance.round(1) == 1,
        high_corr=label_correlation.abs() >= 0.5,
        positive=minimum > 0.0,
    )


def _gaussian_analysis(data: pd.DataFrame, not_encoded: pd.Index) -> ScaledStatistics:
    """Performs analysis on gaussian scaled data.
    Args:
        data:
            Raw data (numerical).
        not_encoded:
            Pandas index of columns that have not been encoded.
    Returns:
        A collection of pandas series that contain booleans for each feature,
        that describe the statistics of each feature.
    """

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[not_encoded])
    scaled_data = pd.DataFrame(
        scaled_data,
        index=data[not_encoded].index,
        columns=data[not_encoded].columns,
    )

    # NOTE here the data is stored as a pandas object, and pandas mean()
    # skips NA values, also that these definitions are simplified by the
    # scaling we have performed
    skew: pd.Series = (scaled_data**3).mean(axis=0)
    kurtosis: pd.Series = (scaled_data**4).mean(axis=0)
    minimum: pd.Series = data.min(axis=0)

    return ScaledStatistics(
        positive=(minimum > 0.0)[not_encoded],
        positive_skew=skew > 1.0,
        negative_skew=skew < -1.0,
        high_kurtosis=kurtosis > 10.0,
        vhigh_kurtosis=kurtosis > 100.0,
        low_kurtosis=kurtosis < 2.0,
    )


def _pick_numeric(encoder: AllNumeric, encoder_space: List[AllNumeric]) -> AllNumeric:
    """Picks a numeric encoding option from the heuristic choice and the user choices.
    Args:
        encoder:
            Heuristic choice.
        encoder_space:
            User choices.
    Returns:
        Final heuristic choice.
    """

    if len(encoder_space) == 1:
        return encoder_space[0]
    elif encoder in encoder_space:
        return encoder
    else:
        return GenericOption.AUTO


def _pick_categorical(encoder: AllCategorical, encoder_space: List[AllCategorical]) -> AllCategorical:
    """Picks a categorical encoding option from the heuristic choice and the user choices.
    Args:
        encoder:
            Heuristic choice.
        encoder_space:
            User choices.
    Returns:
        Final heuristic choice.
    """

    if len(encoder_space) == 1:
        return encoder_space[0]
    elif encoder in encoder_space:
        return encoder
    else:
        return GenericOption.AUTO


def _pick_scaler(scaler: AllScalers, scaler_space: List[AllScalers]) -> AllScalers:
    """Picks a numeric scaling option from the heuristic choice and the user choices.
    Args:
        scaler:
            Heuristic choice.
        scaler_space:
            User choices.
    Returns:
        Final heuristic choice.
    """

    if len(scaler_space) == 1:
        return scaler_space[0]
    elif scaler in scaler_space:
        return scaler
    else:
        return GenericOption.AUTO


def _get_numeric_transformers(
    features: pd.Index, encoder: AllNumeric, scaler: AllScalers, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Helper that creates a dictionary of transformers.

    For each feature, create a transformer for the given encoder and scaler
    combination, as long as they exist in the list of user permitted values.

    Args:
        features:
            Feature names as a pandas index.
        encoder:
            Heuristic choice.
        scaler:
            Heuristic choice.
        spaces:
            User choices.
    Returns:
        Dictionary of transformers for the features given.
    """

    return {
        feature: FloatTransformer(
            encoder=_pick_numeric(encoder, spaces[feature].encoders),
            scaler=_pick_scaler(scaler, spaces[feature].scalers),
        )
        for feature in features
    }


def _get_transformers_correlated(
    not_encoded: pd.Index, statistics: Statistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that have correlation with the target.
    Args:
        not_encoded:
            List of features to consider.
        statistics:
            Statistics to help decide which features are encoded.
        spaces:
            User defined search space.
    Returns:
        Dictionary of transformers for the features given.
    """

    return _get_numeric_transformers(
        not_encoded[statistics.high_corr], GenericOption.NONE, ScalerEncoder.MAX_ABS_SCALER, spaces
    )


def _get_transformers_inverse(
    not_encoded: pd.Index, statistics: ScaledStatistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that are determined to have an inverse normal distribution.
    Args:
        not_encoded:
            List of features to consider.
        statistics:
            Statistics to help decide which features are encoded.
        spaces:
            User defined search space.
    Returns:
        Dictionary of transformers for the features given.
    """

    return _get_numeric_transformers(
        not_encoded[
            ((statistics.positive_skew & statistics.high_kurtosis & ~statistics.vhigh_kurtosis) & statistics.positive)
        ],
        NumericEncoder.RECIPROCAL_ENCODER,
        ScalerEncoder.STANDARD_SCALER,
        spaces,
    )


def _get_transformers_skewed(
    not_encoded: pd.Index, statistics: ScaledStatistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that are determined to have a skewed normal distribution.
    Args:
        not_encoded:
            List of features to consider.
        statistics:
            Statistics to help decide which features are encoded.
        spaces:
            User defined search space.
    Returns:
        Dictionary of transformers for the features given
    """

    return _get_numeric_transformers(
        not_encoded[
            (statistics.positive_skew & ~(statistics.low_kurtosis | statistics.high_kurtosis))
            | (statistics.negative_skew & ~statistics.low_kurtosis)
        ],
        NumericEncoder.POWER_ENCODER,
        ScalerEncoder.STANDARD_SCALER,
        spaces,
    )


def _get_transformers_normal(
    not_encoded: pd.Index, statistics: ScaledStatistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that are determined to have a normal distribution.
    Args:
        not_encoded:
            list of features to consider
        statistics:
            statistics to help decide which features are encoded
        spaces:
            user defined search space
    Returns:
        dictionary of transformers for the features given
    """

    return _get_numeric_transformers(
        not_encoded[
            ~(statistics.positive_skew | statistics.negative_skew)
            & ~(statistics.low_kurtosis | statistics.high_kurtosis)
        ],
        GenericOption.NONE,
        ScalerEncoder.STANDARD_SCALER,
        spaces,
    )


def _get_transformers_lognormal(
    not_encoded: pd.Index, statistics: ScaledStatistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that are determined to have a lognormal distribution.
    Args:
        not_encoded:
            list of features to consider
        statistics:
            statistics to help decide which features are encoded
        spaces:
            user defined search space
    Returns:
        dictionary of transformers for the features given
    """

    return _get_numeric_transformers(
        not_encoded[((statistics.positive_skew & statistics.vhigh_kurtosis) & statistics.positive)],
        NumericEncoder.LOG_ENCODER,
        ScalerEncoder.STANDARD_SCALER,
        spaces,
    )


def _get_transformers_uniform(
    not_encoded: pd.Index, statistics: ScaledStatistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that are determined to have a uniform distribution
    Args:
        not_encoded:
            list of features to consider
        statistics:
            statistics to help decide which features are encoded
        spaces:
            user defined search space
    Returns:
        dictionary of transformers for the features given
    """

    return _get_numeric_transformers(
        not_encoded[(~(statistics.positive_skew | statistics.negative_skew) & statistics.low_kurtosis)],
        NumericEncoder.QUANTILE_TRANSFORM_ENCODER,
        ScalerEncoder.MAX_ABS_SCALER,
        spaces,
    )


def _get_transformers_spread(
    not_encoded: pd.Index, statistics: ScaledStatistics, spaces: Dict[str, EncoderSpace]
) -> Dict[str, FloatTransformer]:
    """Handles features that are determined to have a spread normal distribution
    Args:
        not_encoded:
            list of features to consider
        statistics:
            statistics to help decide which features are encoded
        spaces:
            user defined search space
    Returns:
        dictionary of transformers for the features given
    """

    return _get_numeric_transformers(
        not_encoded[(~(statistics.positive_skew | statistics.negative_skew) & statistics.high_kurtosis)],
        GenericOption.NONE,
        ScalerEncoder.GAUSS_RANK_SCALER,
        spaces,
    )


def heuristic_selector_numeric(
    data: pd.DataFrame, search_space: Dict[str, EncoderSpace], label: pd.Series
) -> Dict[str, FloatTransformer]:
    """Skips optuna in favour of a rule-based system that scales to
    large feature spaces more effectively

    The strategy here is to treat each feature individually, irrespective
    of the target. We aim to make uniform-like distributions more uniform
    and all other distributions more gaussian. We also aim to scale the
    features in a way that preserves sign if that is deemed important,
    enforces unity variance in the case of gaussian distributions, and a
    fixed scale if there are not too many anomalous values.

    If the feature is already determined to be gaussian (zero mean, unity
    variance), we assume some feature engineering has already taken place
    and we leave the feature untouched.

    Args:
        data:
            numeric data
        search_space:
            user selected possible encodings
        label:
            target data
    Returns:
        dictionary of final heuristic chosen encoders
    """

    not_encoded = data.columns
    optimal_encoders: Dict[str, FloatTransformer] = {}

    if data.empty:
        return optimal_encoders

    # analysis with raw data
    statistics = _raw_analysis(data[not_encoded], label)
    # @TODO can use operator in python 3.9
    optimal_encoders.update(_get_transformers_correlated(not_encoded, statistics, search_space))
    not_encoded = not_encoded.difference(pd.Index(optimal_encoders.keys()))

    # ensures values are not too large for float dtype and imputation
    # impute data to prevent errors in analysis. This imputation is not used in the final model.
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    imputer, _, _ = init_imputer(detected_type=DetectedType.float, strategy=ImputeStrategy.MEDIAN)
    data_imputed = data.apply(imputer.fit_transform)

    # analysis with scaled data
    if not_encoded.empty:
        return optimal_encoders

    scaled_statistics = _gaussian_analysis(data_imputed, not_encoded)
    scaled_selections = [
        _get_transformers_normal,
        _get_transformers_inverse,
        _get_transformers_lognormal,
        _get_transformers_skewed,
        _get_transformers_uniform,
        _get_transformers_spread,
    ]
    for func in scaled_selections:
        optimal_encoders.update(func(not_encoded, scaled_statistics, search_space))
    not_encoded = not_encoded.difference(pd.Index(optimal_encoders.keys()))

    for feature in not_encoded:
        optimal_encoders[feature] = FloatTransformer(
            encoder=_pick_numeric(GenericOption.NONE, search_space[feature].encoders),
            scaler=_pick_scaler(GenericOption.NONE, search_space[feature].scalers),
        )
    return optimal_encoders


def heuristic_selector_categorical(
    data: pd.DataFrame, search_space: Dict[str, EncoderSpace]
) -> Dict[str, CategoricalTransformer]:
    """Applies basic logic to handle categorical columns.

    num_classes > 10 -> hash encoding
    num_classes <= 10 -> one hot encoding

    Args:
        data:
            categorical data columns.
        search_space:
            user provided search space.
    Returns:
        Dict[str, CategoricalTransformer]:
            dictionary of final heuristic chosen encoders.
    """

    return (
        {}
        if data.empty
        else {
            feature: (
                CategoricalTransformer(
                    encoder=_pick_categorical(CategoricalEncoder.HASH_ENCODER, search_space[feature].encoders)
                )
                if data[feature].nunique() > CONF.ONE_HOT_ENCODING_THRESHOLD
                else CategoricalTransformer(
                    encoder=_pick_categorical(CategoricalEncoder.ONE_HOT_ENCODER, search_space[feature].encoders)
                )
            )
            for feature in data.columns
        }
    )
