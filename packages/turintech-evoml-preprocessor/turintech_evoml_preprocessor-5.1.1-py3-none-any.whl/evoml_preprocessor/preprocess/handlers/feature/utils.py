# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import List, Optional, Tuple


# Dependencies
import pandas as pd


# Private Dependencies
from evoml_api_models import BaseTypes, DetectedType
from evoml_utils.convertors import type_to_convert_function


# Module
from evoml_preprocessor.preprocess.models import (
    CategoricalEncoder,
    ColumnInfo,
    ColumnOptions,
    GenericOption,
    ImputeStrategy,
    ReasonDropped,
    Slug,
    TypeSubsets,
)
from evoml_preprocessor.preprocess.models.enum import AllEncoders
from evoml_preprocessor.preprocess.transformers import (
    CategoricalTransformer,
    DateTransformer,
    FloatTransformer,
    Transformer,
)
from evoml_preprocessor.preprocess.transformers.type_aliases import Converter
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")

CONF = conf_mgr.preprocess_conf  # Alias for readability
# ──────────────────────────────────────────────────────────────────────────── #


def select_temporal_column_encoding(
    column_info: ColumnInfo,
    column_option: ColumnOptions,
) -> Tuple[Transformer, Optional[Converter], Optional[str]]:
    """Selects transformer for the column based on the information in
    column_info. If needed (based on the column type), it will also return a
    converter function and any metadata needed to use the converter function.

    Args:
        column_info (ColumnInfo): Information about a column.

    Returns:
        Transformer: A transformer suitable to encode the input column
        Converter | None: a converter if needed or None otherwise
        str | None: metadata for the converter if needed or None otherwise.

    """

    _type = column_info.detectedType
    _index = column_info.columnIndex

    encoder_slug = column_option.encoder
    scaler_slug = column_option.scaler
    impute_strategy = column_option.imputeStrategy
    impute_value = column_option.imputeValue

    converter = None
    converter_metadata = None

    # default for impute strategy - both numeric and categorical
    if impute_strategy is None or impute_strategy == ImputeStrategy.AUTO:
        if _type in TypeSubsets.NUMERIC.value:
            impute_strategy = ImputeStrategy.FORWARD_FILL
        else:
            impute_strategy = ImputeStrategy.CONSTANT

    if _type in TypeSubsets.NUMERIC.value or (
        _type == DetectedType.sample_id and column_info.baseType == BaseTypes.integer
    ):
        encoder = FloatTransformer(
            column_info=column_info,
            encoder=encoder_slug,
            scaler=scaler_slug,
            impute_strategy=impute_strategy,
            impute_value=impute_value,
        )

        converter = type_to_convert_function(_type)
        if _type == DetectedType.unit_number:
            if column_info.metadata is None:
                raise ValueError("Conversion metadata must be set for the unit type.")
            converter_metadata = column_info.metadata["unit"]

    elif _type == DetectedType.datetime:
        # no lags for dates
        encoder = DateTransformer(
            column_info=column_info,
            impute_strategy=impute_strategy,
            impute_value=impute_value,
        )

    elif _type in TypeSubsets.CATEGORICAL_TS.value or (
        _type == DetectedType.sample_id and column_info.baseType == BaseTypes.string
    ):

        # default encoder selection
        if encoder_slug is None or encoder_slug == GenericOption.AUTO:
            if column_info.statsUniqueValuesCount <= conf_mgr.preprocess_conf.ONE_HOT_ENCODING_THRESHOLD:
                encoder_slug = CategoricalEncoder.ONE_HOT_ENCODER
            else:
                encoder_slug = CategoricalEncoder.ORDINAL_ENCODER

        encoder = CategoricalTransformer(
            column_info=column_info,
            encoder=encoder_slug,
            impute_strategy=impute_strategy,
            impute_value=impute_value,
        )

    else:
        logger.error("%s type is not supported.", _type)
        raise ValueError(f"Not supported column type: {_type}")

    return encoder, converter, converter_metadata


def get_missing_values_ratio(data: pd.Series) -> float:
    # approximate ratio if the number of rows is too high
    rows = data.shape[0]
    MAX_ROWS = min(1000, rows)
    if rows > MAX_ROWS:
        sample = data.sample(MAX_ROWS)
        return sample.isnull().sum() / len(sample)
    return data.isnull().mean()


def extract_slug(slug_list: List[Slug]) -> Optional[AllEncoders]:
    slug = to_slug_list(slug_list)
    if len(slug) > 0:
        return slug[0]
    return None  # [] → None


def to_slug_list(column: List[Slug]) -> List[AllEncoders]:
    # converts a list of Slug objects to a list of encoders
    slug_list = []
    for item in column:
        slug_list.extend(item.slugValue)
    return slug_list


def convert_column(data_col: pd.Series, converter: Optional[Converter], metadata: Optional[str]) -> pd.Series:
    """Converts the given column using the converter and metadata given. If
    no converter is given, returns the original column.

    Args:
        data_col: column to be converted
        converter: function that can be used for the conversion or None if
        no conversion is needed
        metadata: information needed for the conversion or None if no
        information is needed

    Returns:
        pd.Series: the converted or original column

    """
    if isinstance(data_col.dtype, pd.CategoricalDtype):
        data_col = data_col.astype("object")

    if converter is None:
        return data_col

    # Convert column if needed
    if metadata is not None:
        # @pyright: need to fix use the utils type converter definition consistently
        return converter(data_col, metadata)  # type: ignore
    return converter(data_col)


def check_dropped_ts(col_info: ColumnInfo) -> Optional[ReasonDropped]:
    """Decides if a column needs to be dropped for a timeseries task and returns
     the reason why. If the column does not need to be dropped, None is returned.

    Args:
        col_info: information about a column

    Returns:
         Optional[ReasonDropped]: the reason why a column needs to be
         dropped or None otherwise

    """

    col_type = col_info.detectedType
    missing_rate = col_info.statsMissingValuesRatio
    unique_values_ratio = col_info.statsUniqueValuesRatio

    if col_info.isDeleted:
        return ReasonDropped.DUPLICATE_COLUMN

    if missing_rate == 1:
        # All missing values
        return ReasonDropped.NULL

    if col_type == DetectedType.unary and missing_rate < CONF.UNARY_MISSING_RATE:
        # We only drop unary columns with small missing rate as unary
        # columns with large missing rates are considered binary columns
        return ReasonDropped.CONSTANT_VALUE

    if col_type != DetectedType.unary and missing_rate >= CONF.DROP_MISS_VALUE_RATE:
        # High missing rate
        logger.warning(
            "Dropping %s: too many missing values (%s)",
            col_info.name,
            f"{col_info.statsMissingValuesRatio:.0%}",
        )
        return ReasonDropped.HIGH_MISSING_RATE

    if (
        col_type in TypeSubsets.CATEGORICAL_TS.value
        and unique_values_ratio >= CONF.DROP_UNIQUE_VALUE_RATIO
        and col_type != DetectedType.datetime
    ):
        # High unique values ratio
        return ReasonDropped.HIGH_UNIQUE_VALUES

    if col_type == DetectedType.sample_id:
        return ReasonDropped.ID

    if col_type in TypeSubsets.UNSUPPORTED_TS.value:
        return ReasonDropped.UNSUPPORTED_TYPE

    return None
