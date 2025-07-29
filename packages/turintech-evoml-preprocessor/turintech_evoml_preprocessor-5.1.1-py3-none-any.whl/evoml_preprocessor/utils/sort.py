from typing import Dict, Optional, Tuple, Union
import logging

import pandas as pd

from evoml_api_models import DetectedType
from evoml_utils.convertors.detected_types import to_datetime_column, to_int_column

from evoml_preprocessor.preprocess.models import ColumnInfo
from evoml_preprocessor.preprocess.models.conversion_kwargs import ToDatetimeKwargs, ToIntegerKwargs

logger = logging.getLogger(__name__)


def sort_datasets_index(
    dataset: pd.DataFrame,
    index: str,
    info_map: Dict[str, ColumnInfo],
    test_dataset: Optional[pd.DataFrame] = None,
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """Sorts dataset and test_dataset with respect to indexColumn given in config.
    Args:
        dataset:
            Dataframe containing the original data.
        test_dataset:
            Separate dataframe containing the original test data.
        config:
            PreprocessConfig object
        types:
            List of ColumnInfo objects for columns in datasets.
    Returns:
        Sorted datasets with respect to indexColumn. If indexColumn is None, returns the input datasets in the given form.
    """

    index_info = info_map[index]  # Index must be in the map

    conversion_kwargs: Union[ToDatetimeKwargs, ToIntegerKwargs]
    if index_info.detectedType == DetectedType.datetime:
        converter = to_datetime_column
        if index_info.metadata is None:
            raise ValueError("Conversion metadata is required when the index is of datetime type.")
        conversion_kwargs = ToDatetimeKwargs(**index_info.metadata["to_datetime_kwargs"])
    elif index_info.detectedType == DetectedType.integer:
        converter = to_int_column
        conversion_kwargs = ToIntegerKwargs()
    else:
        raise ValueError("Invalid index selected")

    # Create a new temporary column with converted index
    dataset["__temp_index__"] = converter(dataset[index], **conversion_kwargs.dict())

    # Sort by the temporary column and then drop it
    dataset.sort_values(by="__temp_index__", inplace=True)
    dataset.drop(columns=["__temp_index__"], inplace=True)

    if test_dataset is not None:
        # Convert index column in test dataset and sort
        test_dataset["__temp_index__"] = converter(test_dataset[index], **conversion_kwargs.dict())
        test_dataset.sort_values(by="__temp_index__", inplace=True)
        test_dataset.drop(columns=["__temp_index__"], inplace=True)

    return dataset, test_dataset
