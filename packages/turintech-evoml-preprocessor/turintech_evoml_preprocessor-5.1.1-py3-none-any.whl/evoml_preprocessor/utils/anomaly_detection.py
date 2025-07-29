from typing import List
import logging
import pandas as pd


logger = logging.getLogger("preprocessor")


def get_rows_with_duplicate_index(df: pd.DataFrame, index_column: str) -> List[int]:
    """Removes rows with duplicate values in the specified index column, keeping only the first occurrence.
    Logs a warning about the number of duplicates and lists the first few dropped indexes.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        index_column (str): The column to be used as the index for identifying duplicates.

    Returns:
        pd.DataFrame: A DataFrame with duplicate values in the specified index column removed.
    """
    # ---------------------- removing duplicate index for timeseries ------------------------ #
    if index_column not in df.columns:
        raise ValueError(f"Column '{index_column}' does not exist in the DataFrame.")

    duplicated_mask = df[index_column].duplicated(keep="first")
    duplicated_count = duplicated_mask.sum()

    if duplicated_count > 0:
        dropped_indexes = df.loc[duplicated_mask, index_column]
        displayed_count = min(10, len(dropped_indexes))
        logging.warning(
            f"{duplicated_count} duplicate value(s) found in column '{index_column}'. Only the first row for each duplicate value is kept. "
            f"Displaying {displayed_count} dropped value(s): {list(dropped_indexes[:displayed_count])}"
        )

    return list(df[duplicated_mask].index)
