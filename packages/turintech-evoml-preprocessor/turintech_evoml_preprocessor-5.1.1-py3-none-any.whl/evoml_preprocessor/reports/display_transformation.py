# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import List

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import DataTableGraph

# Module
from evoml_preprocessor.preprocess.models import Tags
from evoml_preprocessor.preprocess.models.config import ColumnInfo, PreprocessConfig
from evoml_preprocessor.preprocess.models.report import PreprocessingReport, TableColumn
from evoml_preprocessor.reports.utils import _create_tag, _to_data_table_format, construct_table_entry


# ─────────────────────── Feature Transformation Table ─────────────────────── #
#             ┌────┬─────┬───────────┬───────────┬─────┬─────┐
#             │ id │ ... │    ...    │    ...    │ ... │ ... │
#             ├────┼─────┼───────────┼───────────┼─────┼─────┤
#             │    │     │           │           │     │     │
#             └────┴─────┴───────────┴───────────┴─────┴─────┘
def summarise_column_tags(
    report: PreprocessingReport,
    config: PreprocessConfig,
    types: List[ColumnInfo],
    data: pd.DataFrame,
) -> DataTableGraph:
    """Creates a table of tags for the preprocessed data.

    To be displayed in the front end for the trials after preprocessing has
    finished.

    Args:
        report (dict):
            The larger report to be summarised that conforms to
            the model PreprocessReport in evoml-api-models.
        config (dict):
            The standard config dict provided to main.py in preprocessor.
        types (dict):
            The standard types dict provided to main.py in preprocessor.
        data (pd.DataFrame):
            The raw (non-transformed) data the preprocessor ran on.
    Raises:
        ValueError:
            Dataframe is None. The preprocessor has to finish successfully to
            start generating this report, so it shouldn't be None. If you managed
            to get this error that's quite messed up.
        ValueError:
            Same as before, how did you get an empty dataframe of size zero???
    Returns:
        DataTableGraph:
            A DataTableGraph wrapping the custom format of the data table
    """

    if data is None:
        raise ValueError(f"{data} is None. Ensure a valid dataframe is passed.")
    if len(data) == 0:
        raise ValueError(f"{data} is empty. Ensure data is being passed.")

    # Create columns to be filled
    indexes = TableColumn(name="id")
    original_names = TableColumn(name="Original Feature")
    encoder_names = TableColumn(name="Encoder")
    scaler_names = TableColumn(name="Scaler")
    type_names = TableColumn(name="Type")
    impute_names = TableColumn(name="Impute Strategy")
    dropped_names = TableColumn(name="Dropped Feature(s)")
    transformed_names = TableColumn(name="Transformed Feature(s)")
    column_tags = TableColumn(name="Tags")

    for feature in report.singleColumnStatistics:
        # Fetch the column info for this feature
        type_info: ColumnInfo = next((sub for sub in types if sub.name == feature.column_name))

        tags: List[str]
        dropped_feature: List[str]

        # captures the case when columns are directly dropped prior to transformation
        if feature.reason_dropped is not None:
            indexes.add(str(type_info.columnIndex))
            original_names.add(feature.column_name)
            type_names.add(feature.detected_type)
            tags = [_create_tag(feature.reason_dropped, "orange")]
            column_tags.add(tags)
            dropped_feature = [feature.column_name]
            dropped_names.add(construct_table_entry(dropped_feature))
            encoder_names.add(None)
            scaler_names.add(None)
            transformed_names.add(None)
            impute_names.add(None)
            continue

        for transformation in feature.transformation_block or []:
            indexes.add(type_info.columnIndex)
            original_names.add(feature.column_name)
            type_names.add(feature.detected_type)
            encoder_names.add(transformation.encoder_name)
            scaler_names.add(transformation.scaler_name)
            impute_names.add(transformation.impute_strategy)

            tags = []

            if feature.required_by_user:
                tags.append(_create_tag(Tags.REQUIRED_BY_USER, "red"))

            for slug in type_info.tags:
                if slug.name in list(Tags):
                    tags.append(_create_tag(slug.name, "blue"))

            if feature.column_name == config.labelColumn:
                tags.append(_create_tag(Tags.TARGET, "grey"))

            dropped_feature = []
            if transformation.reason_dropped is not None:
                if transformation.column_dropped is None:
                    raise ValueError("Column dropped is required.")
                tags.append(_create_tag(transformation.reason_dropped, "red"))
                dropped_feature.append(construct_table_entry(transformation.column_dropped))
            column_tags.add(tags)

            transformed_names.add(construct_table_entry(transformation.column_names))
            dropped_names.add(construct_table_entry(dropped_feature))

    column_tags_table = _to_data_table_format(
        indexes,
        original_names,
        type_names,
        encoder_names,
        scaler_names,
        impute_names,
        dropped_names,
        transformed_names,
        column_tags,
    )

    # Validate the table
    return DataTableGraph(type="dataTable", data=column_tags_table, description=None, graphFields=None, context=None)
