# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
from typing import Any

# Dependencies
import numpy as np
import pandas as pd

# Module
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# Private Dependencies


# ──────────────────────────────────────────────────────────────────────────── #


def is_numeric_column_categorical(data: pd.Series[Any]) -> bool:
    """Helps judge if the data encoded from categorical data.
    Args:
        data:
            Numpy array of data.
    Returns:
        bool:
            Boolean value indicating if the data is categorical.
    """

    return np.count_nonzero(data) <= conf_mgr.preprocess_conf.CATEGORICAL_DATA_THRESHOLD
