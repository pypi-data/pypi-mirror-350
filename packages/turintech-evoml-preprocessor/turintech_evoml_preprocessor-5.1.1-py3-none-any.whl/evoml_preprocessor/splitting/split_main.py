"""This file provides a higher level of interaction with the splitting step
required when preprocessing a dataset from stract (see the main).
"""

import logging
from typing import Dict, Optional, Union

import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import ColumnInfo, PreprocessConfig

from .interface import SplitData, splitting_factory

# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


def split(
    data: pd.DataFrame,
    config: PreprocessConfig,
    info_map: Dict[str, ColumnInfo],
    test_data: Optional[pd.DataFrame] = None,
) -> SplitData:
    """Crafts the inputs of the `DataSplitter.split` method given the context
    available in the main, then call the correct implementation of
    `DataSplitter` to split the provided data.
    """
    label_name = config.labelColumn
    map_back = False
    no_missing = data[label_name].isnull().sum()
    original_label_column = data[label_name].copy()

    if data[label_name].nunique() == 1:
        raise ValueError(f"Column {label_name} has only one unique value, cannot proceed with training.")

    logger.info(" Splitting ".center(60, "-"))

    # if there are 5 or less missing values, drop them, otherwise impute with empty string
    # we temporarily impute the missing values with the empty string to avoid errors in stratified splitting
    if config.mlTask == MlTask.classification and no_missing > 0:
        if no_missing <= 5:
            data.dropna(subset=label_name, inplace=True)
        else:
            fill_value: Union[int, float, str]
            # impute with empty string to help stratified splitting identify the class of the missing values as a separate class
            if pd.api.types.is_object_dtype(data[label_name]):
                fill_value = " "
            elif pd.api.types.is_float_dtype(data[label_name]):
                fill_value = 0.0
            elif pd.api.types.is_integer_dtype(data[label_name]):
                fill_value = 0
            else:
                raise ValueError(f"Unsupported dtype {data[label_name].dtype} for column {label_name}")

            data[label_name] = data[label_name].fillna(fill_value)
            if data[label_name].dtype == "object":
                data[label_name] = data[label_name].astype(str)

            map_back = True

    # retrieve splitting options from config and check if we need to keep the order
    splitting_options = config.splittingMethodOptions
    keep_order = False
    if config.validationMethodOptions is not None:
        keep_order = config.validationMethodOptions.keep_order

    # Need to retrieve type for subset splitting option
    ref_col_info = info_map.get(splitting_options.subsetColumnName)

    # Choose the correct algorithm implementation for the split method and split the data
    split_method = splitting_options.method
    data_splitter = splitting_factory.create(split_method, splitting_options)

    if data_splitter is None:
        raise ValueError(f"No registered implementation for the split method {split_method}")

    # perform the split
    result = data_splitter.split(
        data=data,
        label_name=config.labelColumn,
        ml_task=config.mlTask,
        ref_column=ref_col_info,
        keep_order=config.isTimeseries or keep_order,
        test_data=test_data,
        index_name=config.indexColumn,
    )

    # undo temporary imputation
    if map_back:
        result.train[config.labelColumn] = original_label_column[result.train.index]
        result.test[config.labelColumn] = original_label_column[result.test.index]

    return result
