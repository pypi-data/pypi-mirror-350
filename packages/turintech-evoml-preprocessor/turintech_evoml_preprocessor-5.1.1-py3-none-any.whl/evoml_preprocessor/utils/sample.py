from typing import List, Optional

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

CONF = conf_mgr.preprocess_conf  # Alias for readability
MIN_CLASS_COUNT = 20


def _get_sample_clf(
    label_column: pd.Series,
    sample_size_target: int,
    class_count_floor_target: int = MIN_CLASS_COUNT,
) -> pd.Index:
    """
    Perform stratified sampling on a label column with a soft target sample size and class count floor.

    Parameters:
    - label_column: pd.Series, the column containing class labels.
    - sample_size_target: int, the soft target number of samples.
    - class_count_floor_target: int, the soft minimum number of instances for each class.

    Returns:
    - pd.Index of sampled indices.
    """
    # Calculate class distributions
    normalized_class_counts = label_column.value_counts(normalize=True)
    actual_class_counts = label_column.value_counts()

    # Determine the effective floor for each class. We can't set the minimum higher than the rarest class.
    effective_class_count_floor = min(class_count_floor_target, actual_class_counts.min())

    # Calculate initial sampled class counts
    sampled_class_counts = (normalized_class_counts * sample_size_target).astype(int)

    # Ensure no class falls below the effective floor. This increases the overall sample size above sample_size_target.
    sampled_class_counts = sampled_class_counts.clip(lower=effective_class_count_floor)

    # Perform stratified sampling
    sampled_indices: List[np.ndarray] = []
    for value, count in sampled_class_counts.items():
        # Skip classes with no sampling requirement
        if count == 0:
            continue
        sampled_indices.append(np.random.choice(label_column[label_column == value].index, size=count, replace=False))

    return pd.Index(np.concatenate(sampled_indices))


def _get_sample_reg(
    label_column: pd.Series,
    sample_size: int,
) -> pd.Index:
    """Sampling for classification datasets
    Args:
        label_column:
            The label column data.
        max_size:
            The sample size.

    Returns:
        A pandas index that can be used to sample rows from some dataset.
    """
    return pd.Index(np.random.choice(label_column.index, sample_size, replace=False))


def get_sample(
    label_column: pd.Series,
    sample_size: int = CONF.SAMPLE_SIZE,
    task: Optional[MlTask] = MlTask.regression,
) -> pd.Index:
    """Selects a random subset of the data to perform the search on. We store this data internally for future use.
    Args:
        label_column:
            The label column data.
        max_size:
            The sample size.
        task:
            The ml task (for stratified sampling)

    Returns:
        A pandas index that can be used to sample rows from some dataset.
    """
    # Check if search_sample size > dataset, then select smallest value
    if len(label_column) >= sample_size:
        if task == MlTask.classification:
            return _get_sample_clf(label_column, sample_size)
        elif task == MlTask.regression:
            return _get_sample_reg(label_column, sample_size)
        else:
            raise NotImplementedError(f"No sampling implemented for {task}")
    else:
        return label_column.index
