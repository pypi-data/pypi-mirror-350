import logging
from typing import Dict, List, get_args

import pandas as pd
from evoml_api_models import BaseTypes, DetectedType
from evoml_utils.convertors.detected_types import to_float_column, to_int_column

from evoml_preprocessor.preprocess.handlers.feature.utils import extract_slug
from evoml_preprocessor.preprocess.models import ColumnInfo, ColumnOptions, ConfigOptions, PreprocessConfig
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, Covariate, Filter, ImputeStrategy

logger = logging.getLogger("preprocessor")


def _get_config_options(config: PreprocessConfig) -> ConfigOptions:
    # Transformation options
    # → reorganise the options provided in the config into a structure
    # suitable for the current algorithms.
    # • list of ignored indexes
    # • map {index → options}
    ignored_features = []
    required_features = []
    future_covariates_indices = []
    transformation_options: Dict[int, ColumnOptions] = {}

    for options in config.transformationOptions:
        # First, we attribute the options of the feature override list (they
        # have priority)
        # loki copies over default column settings to featureOverrides
        for override in options.featureOverrides:
            # encoder
            tmp_encoder_slug = extract_slug(override.encoderSlugs)
            encoder_slug = None
            if isinstance(tmp_encoder_slug, get_args(AllEncoders)):
                encoder_slug = tmp_encoder_slug

            # scaler
            tmp_scaler_slug = extract_slug(override.scalerSlugs)
            scaler_slug = None
            if isinstance(tmp_scaler_slug, get_args(AllScalers)):
                scaler_slug = tmp_scaler_slug

            # imputer
            impute_strategy = override.impute.strategy
            if impute_strategy not in list(ImputeStrategy):
                impute_strategy = ImputeStrategy.AUTO

            transformation_options[override.columnIndex] = ColumnOptions(
                encoder=encoder_slug,
                scaler=scaler_slug,
                imputeStrategy=impute_strategy,
                imputeValue=override.impute.value,
                rolling=override.rolling,
                derivedColumns=override.derivedColumns,
            )

            if override.filter == Filter.DROP:
                ignored_features.append(override.columnIndex)
            elif override.filter == Filter.KEEP:
                required_features.append(override.columnIndex)

            if override.covariate == Covariate.FUTURE:
                future_covariates_indices.append(override.columnIndex)

    config_options = ConfigOptions(
        ignored_features=ignored_features,
        required_features=required_features,
        future_covariates_indices=future_covariates_indices,
        transformation_options=transformation_options,
    )
    return config_options


def validate_data(data: pd.DataFrame, col_infos: List[ColumnInfo]) -> pd.DataFrame:
    """Validates the data by checking if the columns are of the correct type.
    Args:
        data:
            The dataset.
        col_infos:
            List of column infos.
    Returns:
        validated data.
    """

    for col_info in col_infos:
        # ignore additional columns not in the original dataset
        if col_info.name not in data:
            logger.warning(f"Detected column {col_info.name} was not found in the dataset.")
            continue

        column = data[col_info.name]

        if col_info.baseType == BaseTypes.integer and not pd.api.types.is_integer_dtype(column):
            data[col_info.name] = to_int_column(column)
        elif col_info.detectedType == DetectedType.float and (
            col_info.baseType == BaseTypes.string or not pd.api.types.is_float_dtype(column)
        ):
            data[col_info.name] = to_float_column(column)
        elif col_info.detectedType == DetectedType.categorical and not (
            pd.api.types.is_object_dtype(column) or pd.api.types.is_string_dtype(column)
        ):
            data[col_info.name] = column.astype(str)
    return data
