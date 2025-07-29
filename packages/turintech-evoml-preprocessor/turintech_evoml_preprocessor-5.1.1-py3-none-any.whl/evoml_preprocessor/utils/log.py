import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
memory_logger = logging.getLogger("memory")


def log_memory(message: str, dataframe: pd.DataFrame, deep: bool = True) -> None:
    """Logs a detailed memory usage for a dataframe. With `deep=True`, gives the
    detail of every column's dtype and memory usage. With `deep=False`, only
    logs the total memory used by the DataFrame.
    Args:
        message (str):
            Message to log.
        dataframe (pd.DataFrame):
            The DataFrame to log.
        deep (bool, optional):
            Whether to log the detailed memory usage. Defaults to True.
    Returns:
        None
    """

    memory = dataframe.memory_usage(deep=True)

    def to_b(n: int) -> str:
        if n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.2f}GB"
        if n >= 1_000_000:
            return f"{n / 1_000_000:.2f}MB"
        if n >= 1_000:
            return f"{n / 1_000:.2f}KB"
        return f"{n}B"

    if not deep:
        memory_logger.debug(
            "%s: %sx%s - %s",
            message,
            len(dataframe.columns),
            len(dataframe),
            to_b(memory.sum()),
        )
        return

    # Build a table with column names, dtypes & memory usage
    dtypes = [  # 'Index' will be a column name, but it's not a valid one
        str((dataframe[col] if col != "Index" else dataframe.index).dtype) for col in memory.index
    ]
    table = np.array(list(zip(memory.index, dtypes, map(to_b, memory))))
    lengths = [max(map(len, table[:, i])) for i in range(len(table[0]))]

    # Constructs unicode table using box characters
    # • note: we're adding +2 to length to account for spaces around cells
    table_str = "┌" + "┬".join("─" * (l + 2) for l in lengths) + "┐\n"
    for i, row in enumerate(table):
        table_str += "│ "
        table_str += " │ ".join(cell.ljust(l) for (cell, l) in zip(row, lengths))
        table_str += " │\n"
        if i < len(table) - 1:
            table_str += "├" + "┼".join("─" * (l + 2) for l in lengths) + "┤\n"

    table_str += "└" + "┴".join("─" * (l + 2) for l in lengths) + "┘"

    memory_logger.debug(
        "\x1b[1m%s\x1b[0m:\n%s\n%sx%s - %s\n",
        message,
        table_str,
        len(dataframe.columns),
        len(dataframe),
        to_b(memory.sum()),
    )
