import json
import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from evoml_preprocessor.preprocess.transformers.type_aliases import LabelMapping

logger = logging.getLogger("preprocessor")


def save_json(json_obj: Dict[Any, Any], path: Path) -> None:
    """Saves a json to the given path. Indents the json, and raises an exception
    for 'NaN' (Not a Number) values.
    Args:
        json_obj (dict):
            The json to save.
        path (Path):
            The path to save the json to.
    Returns:
        None
    """

    with path.open("w") as fobj:
        json.dump(json_obj, fobj, indent=2, allow_nan=False)


def save_str(json_str: str, path: Path) -> None:
    """Saves a string to a path (expects a pydantic model that has already been
    encoded with json().
    Args:
        json_str (str):
            The string to save.
        path (Path):
            The path to save the string to.
    Returns:
        None
    """

    with path.open("w") as fobj:
        fobj.write(json_str)


def save_data(data: pd.DataFrame, path: Path, use_parquet: bool = False) -> None:
    """Saves a pd.DataFrame to the given path. Saves to csv by default, or to
    parquet if the boolean is true.
    Args:
        data (pd.DataFrame):
            The data to save.
        path (Path):
            The path to save the data to.
        use_parquet (bool):
            Whether to save as parquet or csv. Defaults to False.
    Returns:
        None
    """

    if use_parquet:
        data.to_parquet(path, index=False)
    else:
        data.to_csv(path, index=False)


def save_metadata(path: Path, label_mappings: LabelMapping) -> None:
    """Saves label_mappings the file-system
    Args:
        path (Path):
            Path to save the metadata
    Returns:
        None
    """

    save_json(
        {
            "labelMappings": label_mappings,
        },
        path,
    )
