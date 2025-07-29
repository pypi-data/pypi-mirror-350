# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from enum import Enum
from typing import Any, List

from evoml_api_models import DataTable
from evoml_api_models.builder import get_builder
from evoml_api_models.graphs import DataTableColumn

from evoml_preprocessor.preprocess.models.report import TableColumn

# ──────────────────────────────────────────────────────────────────────────── #


def _create_tag(label: str, colour: str) -> str:
    """Create html tags for a given label and colour.
    To be displayed in the data transformation page in trials. These are the
    coloured tags in the preprocessor table.
    Args:
        label (str):
            The text to be displayed in the preprocessor table.
        colour (str):
            The colour you want the text to be in the tag.
    Raises:
        ValueError:
            You've defined a colour not supported.
        ValueError:
            Your input is of NoneType. Shouldn't be.
    Returns:
        str:
            The final HTML tag to display.
    """
    # @TODO: use an enum here
    ALLOWED_TAGS = [
        "grey",
        "black",
        "cyan",
        "dark_orange",
        "peppermint",
        "orange",
        "blue",
        "green",
        "navy",
        "red",
        "yellow",
    ]

    if colour not in ALLOWED_TAGS:
        raise ValueError(f"{colour} color tag is not in ALLOWED_TAGS")
    if label is None:
        raise ValueError(f"{label} is  of NoneType, pass in a label")

    return f"<span class='tue-tag tue-tag-{ALLOWED_TAGS.index(colour)}'>{label}</span>"


def _to_data_table_format(*columns: TableColumn) -> DataTable:
    """Internal utility function for creating tables for the preprocessing report.
    Generates the data table format used by the front end for displaying the data.
    Args:
        columns (Tuple[TableColumn]):
            A list of table columns containing their name, id and content.
    Raises:
        ValueError:
            All the input columns should have the same size.
        ValueError:
            No columns were provided.
    Returns:
        DataTable:
            A data-table formatted as expected by frontend's custom css module
            for tables.
    """
    # All the lists need to be the same size
    if len(set([len(col.content) for col in columns])) > 1:
        raise ValueError("Inputs for _to_data_table_format should all be the same length")
    if len(columns) == 0:
        raise ValueError("Expected at least 1 column")

    table = get_builder(DataTable)
    table.columns = [DataTableColumn(id=f"col{i}", **col.dict()) for (i, col) in enumerate(columns)]

    table.data_source = []
    for i in range(len(columns[0].content)):
        table.dataSource.append({})
        for j, col in enumerate(table.columns):
            # Handle str | enum | list[str]
            item = columns[j].content[i]
            if isinstance(item, list):
                table.dataSource[-1][col.id] = " ".join(item)
            elif isinstance(item, Enum):
                table.dataSource[-1][col.id] = item.value
            else:
                table.dataSource[-1][col.id] = item
    return table.build()


def construct_table_entry(items: List[str], size_limit: int = 75) -> str:
    """Converts a list of (string) items into a single line, limited to a given
    size (default: 75 chars).
    Does so by joining lines with ', ' and adding a postfix indicating the
    number of hidden items if the line is above the limit.
    Args:
        items (List[str]):
            The list of items to be joined.
        size_limit (int):
            The maximum size of the output string.
    Returns:
        str:
            The joined string.
    """
    # if there is only one item, ignore the size limit
    if len(items) == 1:
        return items[0]
    entry = ", ".join(items)
    # if the whole list fit in the size limit, return the whole list as a string
    if len(entry) <= size_limit:
        return entry
    n_items = len(items)
    postfix = " ({} more)"
    # find the maximum number of items that can fit in the limit
    entry = entry[:size_limit]  # we first cut off the string at the size limit
    last_comma_index = entry.rfind(",")
    if last_comma_index > 0:  # if there is more than one full item in the entry
        # remove anything on and after the last comma
        # (even if the item after the last comma fully fitted in the entry,
        # we still need space for the postfix)
        entry = entry[:last_comma_index]
        n_fitted_items = entry.count(",") + 1
        # try to fit the postfix within the limit, remove more items from the entry if necessary
        # but we should never remove the first item
        entry = ", ".join(items[:n_fitted_items]) + postfix.format(n_items - n_fitted_items)
        while len(entry) > size_limit and n_fitted_items > 1:
            n_fitted_items -= 1
            entry = ", ".join(items[:n_fitted_items]) + postfix.format(n_items - n_fitted_items)
    else:  # there is only one item (or an partial item) in the entry
        # we will have to ignore the size limit and fit at least one item in the entry
        entry = items[0] + postfix.format(n_items - 1)

    return entry


def _list_to_string(data_list: List[Any]) -> str:
    """Internal Utility function

    Converts a list to a string, predominantly for the preprocessing report
    e.g. x = ['a','b','c'] becomes 'a, b and c'
    and
    x = [] becomes 'None'

    Args:
        data_list (list):
            list of values that can be converted to a string
    Raises:
        ValueError:
            When the input list is None
    Returns:
        str:
            The concatenated input as a grammatically correct string
    """

    if data_list is None:
        raise ValueError(f"{data_list} is None. Ensure a valid List is passed.")

    def to_str(item: Any) -> str:
        if isinstance(item, Enum):
            return str(item.value)
        return str(item)

    if len(data_list) == 0:
        return "None"
    if len(data_list) == 1:
        return to_str(data_list[0])
    str_data_list = [to_str(x) for x in data_list]
    return ", ".join(str_data_list[:-1]) + " and " + str_data_list[-1]
