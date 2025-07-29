import math
from typing import Any, Dict, Optional, Tuple, Union

import pandas as pd
from evoml_api_models import BaseTypes, DetectedType
from evoml_utils.convertors import type_to_convert_function

from evoml_preprocessor.preprocess.models import ImputeStrategy, ImputeSubsets, ImputeValue, TypeSubsets
from evoml_preprocessor.preprocess.transformers.imputers._base import Imputer
from evoml_preprocessor.preprocess.transformers.imputers.constant_imputer import ConstantImputer
from evoml_preprocessor.preprocess.transformers.imputers.identity_imputer import IdentityImputer
from evoml_preprocessor.preprocess.transformers.imputers.numeric_imputer import NumericImputer
from evoml_preprocessor.preprocess.transformers.imputers.timeseries_imputer import TimeseriesImputer

DEFAULT_NUMERIC_FILL_VALUE = 0
DEFAULT_FILL_VALUE = ""


def _get_default_impute(detected_type: DetectedType) -> ImputeStrategy:
    """Get the default impute strategy based on the detected type.

    Args:
        detected_type (DetectedType): The detected type of the impute value.

    Returns:
        ImputeStrategy: The default impute strategy for the detected type.
    """
    defaults = {
        BaseTypes.string: ImputeStrategy.CONSTANT,
        DetectedType.url: ImputeStrategy.CONSTANT,
        DetectedType.phone: ImputeStrategy.CONSTANT,
        DetectedType.map: ImputeStrategy.CONSTANT,
        DetectedType.ip: ImputeStrategy.CONSTANT,
        DetectedType.text: ImputeStrategy.CONSTANT,
        DetectedType.email: ImputeStrategy.CONSTANT,
        DetectedType.datetime: ImputeStrategy.CONSTANT,
        DetectedType.barcode: ImputeStrategy.CONSTANT,
        DetectedType.list: ImputeStrategy.CONSTANT,
        DetectedType.bank_code: ImputeStrategy.CONSTANT,
        DetectedType.binary: ImputeStrategy.CONSTANT,
        DetectedType.address: ImputeStrategy.CONSTANT,
        DetectedType.categorical: ImputeStrategy.CONSTANT,
        DetectedType.unit_number: ImputeStrategy.MEDIAN,
        DetectedType.percentage: ImputeStrategy.MEDIAN,
        DetectedType.integer: ImputeStrategy.MEDIAN,
        DetectedType.fraction: ImputeStrategy.MEDIAN,
        DetectedType.float: ImputeStrategy.MEDIAN,
        DetectedType.currency: ImputeStrategy.MEDIAN,
        DetectedType.protein_sequence: ImputeStrategy.CONSTANT,
    }
    return defaults[detected_type]


def init_imputer(
    detected_type: DetectedType,
    strategy: ImputeStrategy = ImputeStrategy.AUTO,
    value: Optional[ImputeValue] = None,
    metadata: Optional[Dict[str, Any]] = None,
    column: Optional[pd.Series] = None,
) -> Tuple[Imputer, ImputeStrategy, ImputeValue]:
    """Impute static columns.
    Args:
        column:
            The data column.
        detected_type:
            The type of the impute value. It can be the DetectedType or the BaseType of the column.
        strategy:
            Enum impute strategy.
        value:
            The constant value used to impute columns.
        metadata:
            The metadata from type_detector, used to parse column in evoml-models converter.
    Returns:
        ImputeValue:
            The imputed column and impute value.
    """
    if strategy is None or strategy not in list(ImputeStrategy):
        strategy = ImputeStrategy.AUTO

    # return identity imputer if impute strategy is None
    if strategy == ImputeStrategy.NONE:
        return IdentityImputer(), ImputeStrategy.NONE, value
    # get auto/default impute value
    if (
        strategy is None
        or strategy == ImputeStrategy.AUTO
        or detected_type in TypeSubsets.NUMERIC_SIMPLE.value
        and strategy in ImputeSubsets.IMPUTE_TS.value
    ):
        strategy = _get_default_impute(detected_type)

    # validation if strategy is numeric but detected type is not
    if (
        detected_type not in TypeSubsets.NUMERIC.value
        and strategy in ImputeSubsets.NUMERIC_ALL.value
        and strategy not in ImputeSubsets.CONSTANT_VALUE.value
    ):
        strategy = _get_default_impute(detected_type)

    # validate/get constant impute value
    if strategy == ImputeStrategy.MOST_FREQUENT:
        if column is None:
            raise ValueError("Column must be provided if the imputation strategy is most frequent.")
        value = get_most_frequent_value(column, detected_type, metadata)
        return ConstantImputer(value=value), ImputeStrategy.MOST_FREQUENT, value

    # validated value is used by NumericImputer and ConstantImputer
    value = validate_constant_impute_value(detected_type, value, metadata)

    if strategy == ImputeStrategy.CONSTANT:
        return ConstantImputer(value=value), ImputeStrategy.CONSTANT, value

    # time series impute options
    if strategy in ImputeSubsets.IMPUTE_TS.value:
        value = get_average_value(data=column, detected_type=detected_type)
        return TimeseriesImputer(impute_strategy=strategy, value=value), strategy, value

    if detected_type in TypeSubsets.NUMERIC.value:
        if value is None:
            raise ValueError("We cannot impute using None.")
        if isinstance(value, str):
            raise ValueError("We cannot use NumericImputer with type str.")
        return NumericImputer(strategy=strategy, fill_value=value), strategy, value

    return ConstantImputer(value=value), ImputeStrategy.CONSTANT, value


def get_average_value(
    data: pd.Series,
    detected_type: DetectedType,
) -> Any:
    """Selects the average value of a series. Mode is used for non-numerical types, while median is used for numerical types."""
    sample = data.sample(n=1_000, replace=True)
    if detected_type in [
        DetectedType.url,
        DetectedType.phone,
        DetectedType.map,
        DetectedType.ip,
        DetectedType.text,
        DetectedType.email,
        DetectedType.barcode,
        DetectedType.list,
        DetectedType.bank_code,
        DetectedType.binary,
        DetectedType.address,
        DetectedType.categorical,
        DetectedType.protein_sequence,
    ]:
        return sample.mode(dropna=True).iloc[0]
    return sample.median(skipna=True)


def get_most_frequent_value(
    data: pd.Series,
    impute_type: Union[BaseTypes, DetectedType],
    metadata: Optional[Dict[str, Any]] = None,
) -> ImputeValue:
    """Finds the most frequent value for non-numeric columns.
    Args:
        data:
            The data column.
        impute_type:
            The type of the impute value. It can be the DetectedType or the BaseType of the column.
        metadata:
            Optional, in cases where detected type has associated metadata e.g. geo_location
    Returns:
        ImputeValue:
            Most frequent value.
    """

    # Find most frequent value
    most_frequent = data.mode(dropna=True).iloc[0]

    # Map and list structures need to converted to strings, otherwise the
    # imputation step breaks
    if impute_type in [DetectedType.map, DetectedType.list]:
        return str(most_frequent)
    return most_frequent


def transform_impute_value(
    impute_type: Union[BaseTypes, DetectedType],
    metadata: Optional[Dict[str, Any]] = None,
    impute_value: Optional[ImputeValue] = None,
) -> ImputeValue:
    """
    Transforms the impute value based on the type of data and metadata.

    Args:
        impute_type: Specifies the data type of the impute value.
        metadata: Holds additional data details. Empty by default.
        impute_value: The value used for imputation.

    Returns:
        The impute value transformed according to its data type.
    """
    # Transforms the impute value depending on its type and metadata
    if (
        metadata is None
        or impute_type in [DetectedType.float, DetectedType.currency, DetectedType.categorical]
        or impute_value not in list(BaseTypes)
    ):
        if metadata is not None and impute_type != DetectedType.currency:
            # @pyright: the TypeConvertor type has to be fixed in utils
            impute_value = type_to_convert_function(impute_type)(pd.Series([impute_value]), **metadata)[0]  # type: ignore
        else:
            # @pyright: the TypeConvertor type has to be fixed in utils
            impute_value = type_to_convert_function(impute_type)(pd.Series([impute_value]))[0]  # type: ignore

        # sometimes converter returns np.nan instead of None
        if impute_value is not None and isinstance(impute_value, (int, float)) and math.isnan(impute_value):
            impute_value = None

    return impute_value


def validate_constant_impute_value(
    impute_type: Union[BaseTypes, DetectedType],
    impute_value: Optional[ImputeValue] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Optional[ImputeValue]:
    """
    Validates a constant impute_value based on its type.

    Args:
        impute_type: Specifies the data type of the impute value.
        impute_value: The value used for imputation. 'None' by default.
        metadata: Holds additional data details. 'None' by default.

    Returns:
        The validated constant value based on the data type. The validated value would either a properly transformed version of the impute value or, if invalid, default value based on the data type.
    """

    # The transformation of impute value is only applicable if it is not None and not NaN
    if impute_value is not None and not pd.isna(impute_value) and impute_type in list(DetectedType):
        impute_value = transform_impute_value(impute_type, metadata, impute_value)
        # if return value is valid, return
        if impute_value is not None:
            if impute_type in [DetectedType.list, DetectedType.map]:
                impute_value = str(impute_value)
            return impute_value

    # imputing a string when impute_type is basetype string
    if impute_type == BaseTypes.string and isinstance(impute_value, str):
        return impute_value

    # invalid impute_value, using default instead
    if impute_type in TypeSubsets.NUMERIC.value:
        return DEFAULT_NUMERIC_FILL_VALUE
    return DEFAULT_FILL_VALUE
