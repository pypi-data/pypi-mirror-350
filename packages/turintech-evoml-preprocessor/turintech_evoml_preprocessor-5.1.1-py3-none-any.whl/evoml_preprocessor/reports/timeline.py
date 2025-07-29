# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from collections import Counter
from typing import List

# Private Dependencies
from evoml_api_models import Graph, GraphType, HighchartsGraph, TimelineReport, TimelineStep, convert_graph
from evoml_api_models.builder import Builder, get_builder  # type: ignore

# Module
from evoml_preprocessor.preprocess.models.config import ColumnInfo, PreprocessConfig
from evoml_preprocessor.preprocess.models.report import (
    FeatureReport,
    PreprocessingReport,
    FeatureGenerationReport,
    FeatureSelectionReport,
)
from evoml_preprocessor.reports.utils import _list_to_string

# Dependencies


# ----------------------- Preprocessing Steps Timeline ----------------------- #
#              step A                          step C
#                 ▲                              ▲
#                 │                              │
#          ┌──────┴───────┬───────────────┬──────┴──────┬───────────────┐
#          │              │               │             │               │
#          └──────────────┴───────┬───────┴─────────────┴───────┬───────┘
#                                 │                             │
#                                 ▼                             ▼
#                               step B                        step D
def summarise_preprocess_report(
    config: PreprocessConfig, report: PreprocessingReport, types: List[ColumnInfo]
) -> HighchartsGraph:
    """Generates a condensed preprocessor report

    The default preprocess report is more verbose than perhaps needed at the moment.
    This summariser will put it into the exact format currently required.
    NB: For now in the preprocessor we don't log the individual duration of steps
    as they happen concurrently, so we just set it to 0. Instead, we only log the
    overall time. The arguments have already been pre-validated by the other
    preprocessor steps (this is the last step to run).

    Args:
        config (PreprocessConfig):
            Preprocessor configuration
        report (PreprocessingReport):
            The larger report to be summarised
        types (List[ColumnInfo):
            The standard list of column info provided to main.py in preprocessor
    Returns:
        HighchartsGraph:
            A TimelineReport model converted to be displayed by Highcharts

    """

    # initialise the model builder
    timeline_builder = get_builder(TimelineReport)

    timeline_builder.name = "Preprocess Timeline"
    timeline_builder.duration = round(report.totalPreprocessingTime, 1)
    timeline_builder.data = []

    # alias to help with readability
    column_reports = report.singleColumnStatistics
    multi_column_reports = report.multiColumnStatistics
    total_columns = multi_column_reports.columnCountBeforePreprocessing
    feature_handler_transformed_columns = multi_column_reports.columnCountAfterFeatureHandler

    # append type detection step
    types_step = get_types_timeline(types)
    timeline_builder.data.append(types_step)

    # append encoding step
    data_encoding = get_encoding(column_reports, feature_handler_transformed_columns, total_columns)
    timeline_builder.data.append(data_encoding)

    # append feature selection step
    if config.featureSelectionOptions.enable and report.multiColumnStatistics.featureSelectionReport is not None:
        feature_selection = get_feature_selection_timeline(report)
        timeline_builder.data.append(feature_selection)

    # append feature generation step
    if config.featureGenerationOptions.enable and report.multiColumnStatistics.featureGenerationReport is not None:
        feature_generation = get_feature_generator_timeline(report)
        timeline_builder.data.append(feature_generation)

    # Validate the timeline report with our model
    timeline_report = Graph[TimelineReport](
        type=GraphType.timelineReport,
        graphJson=timeline_builder.build(),
        description=None,
        graphFields=None,
        context=None,
    )
    return convert_graph(timeline_report)


def get_types_timeline(types: List[ColumnInfo]) -> TimelineStep:
    # Generate the type_summary
    type_list = [col.detectedType for col in types]
    type_list = list(Counter(type_list).items())
    name_count = ""
    for index, tup in enumerate(type_list):
        name_count += f"{tup[0]}({tup[1]})"
        if index == len(type_list) - 1:
            name_count += "."
        elif index == len(type_list) - 2:
            name_count += " and "
        else:
            name_count += ", "
    type_info = f"{len(set(type_list))} unique column types were found in this dataset. <br></br>"
    type_info += (
        "<div style='overflow-wrap:break-word;word-wrap:break-word;hyphens:auto;white-space"
        f": normal;'> <b> Column Type(no. columns detected): </b> <br></br> {name_count} </div>"
    )
    types_step = TimelineStep(
        name="<b>Type Detection</b>",
        description=f"Automatically detected {len(set(type_list))} data types and performed basic statistical analysis",
        information=[type_info],
        duration=None,
    )
    return types_step


def get_feature_generator_timeline(report: PreprocessingReport) -> TimelineStep:
    if report.multiColumnStatistics.featureGenerationReport is None:
        raise ValueError("Feature generation report must be initialized.")
    generation_report: FeatureGenerationReport = report.multiColumnStatistics.featureGenerationReport
    generated_features = generation_report.featuresGenerated
    columns_after_fg = generation_report.totalOriginalColumns + len(generated_features)
    input_columns = set()
    basis_functions = set()
    for generated in generated_features:
        input_columns.update(generated.featuresUsed)
        basis_functions.update(generated.basicFunctions)
    basis_functions_str = _list_to_string(list(basis_functions))
    generated_info = (
        f"Given {generation_report.totalOriginalColumns} input features, {len(generated_features)} "
        "new features "
        f"were generated, resulting in a dataset with {columns_after_fg} features. <br></br>"
    )
    generated_info += (
        "<div style='display:flex;width:400px;'> "
        "<div style='display:flex;width:50%'> "
        "  No. generated features  <br></br> "
        "  Operators used  "
        "</div>"
        f"<div style='display:flex;width:50%'> {len(generated_features)} <br> </br> "
        f"{basis_functions_str} </div>"
    )
    feature_generation = TimelineStep(
        name="<b>Feature Generation</b>",
        description="Generate new insights using existing features",
        information=[generated_info],
        duration=None,
    )
    return feature_generation


def get_feature_selection_timeline(report: PreprocessingReport) -> Builder[TimelineStep]:
    if report.multiColumnStatistics.featureSelectionReport is None:
        raise ValueError("Feature selection report must be set.")
    selection_report: FeatureSelectionReport = report.multiColumnStatistics.featureSelectionReport
    feature_selection = get_builder(TimelineStep)
    feature_selection.name = "<b>Feature Selection</b>"
    feature_selection.description = "Select features with the most predictive power"
    n_selected = selection_report.noSelectedColumns
    n_dropped = selection_report.noOriginalColumns - n_selected
    selected_overall = (
        f"Given {selection_report.noOriginalColumns} input features,"
        f" {n_dropped} were dropped and {n_selected} were "
        "selected."
    )
    selected_info = []
    for i, step in enumerate(selection_report.selectionMethods):
        step_info = f"<b>Pipeline Step {i+1}</b>"
        step_info += "<ul>" f"<li>Method: {step.method}</li><li>Dropped: {step.nColumnsRemoved}</li>"
        if step.relevancyMetricReports:
            step_info += "<li>Relevancy Metrics:"
            step_info += "<ul>"
            for metric in step.relevancyMetricReports:
                step_info += f"<li>{metric.name}</li>"
            step_info += "</ul>"
            step_info += "</li>"
        if step.redundancyMetricReport is not None:
            step_info += f"<li>Redundancy Metric: {step.redundancyMetricReport.name}</li>"
        step_info += "</ul>"
        selected_info.append(step_info)

    feature_selection.information = [selected_overall] + selected_info
    return feature_selection


def get_encoding(
    column_reports: List[FeatureReport], feature_handler_transformed_columns: int, total_columns: int
) -> TimelineStep:
    # Aggregate the per-column stats
    encoders = set()
    scalers = set()
    imputers = set()
    impute_count = 0
    for feature_report in column_reports:
        block = feature_report.transformation_block
        for transformation in block or []:
            if transformation.encoder_name is not None:
                encoders.add(transformation.encoder_name)
            if transformation.scaler_name is not None:
                scalers.add(transformation.scaler_name)
            if transformation.impute_strategy is not None:
                imputers.add(transformation.impute_strategy)

        impute_count += feature_report.impute_count or 0
    # Next, the Data Encoding Summary
    encoders_str = _list_to_string(sorted(list(encoders)))
    scalers_str = _list_to_string(sorted(list(scalers)))
    imputers_str = _list_to_string(sorted(list(imputers)))
    transformation_info = (
        f"Given {total_columns} input features, a machine ready "
        f"dataset with {feature_handler_transformed_columns} columns was generated. <br></br>"
    )
    transformation_info += (
        "<div style='display:flex;width:450px;overflow-wrap:break-word;word-wrap:break-word;hyphens:auto;white-space:"
        " normal;'> <br></br><div style='display:flex;width:30%;'> <b> Encoders </b>  </div> <div"
        f" style='display:flex;width:70%;'> {encoders_str} </div> </div> </br><div"
        " style='display:flex;width:450px;overflow-wrap:break-word;word-wrap:break-word;hyphens:auto;white-space:"
        " normal;'> <div style='display:flex;width:30%;'> <b> Scalers </b> </div> <div"
        f" style='display:flex;width:70%;'> {scalers_str}  </div> </div> <br></br><div"
        " style='display:flex;width:450px;overflow-wrap:break-word;word-wrap:break-word;hyphens:auto;white-space:"
        " normal;'> <div style='display:flex;width:30%;'> <b> Impute Strategies </b> </div> <div"
        f" style='display:flex;width:70%;'> {imputers_str}  </div> </div>"
    )
    data_encoding = TimelineStep(
        name="<b>Data Transformation</b>",
        description="Transform data into a machine ready form",
        information=[transformation_info],
        duration=None,
    )
    return data_encoding
