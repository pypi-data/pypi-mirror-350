# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Dict, List, Optional, Set

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import convert_graph
from evoml_api_models.builder import get_builder  # type: ignore
from evoml_api_models.graphs import (  # type: ignore
    BarChartData,
    ColumnChart,
    Graph,
    GraphDataType,
    GraphType,
    HighchartsGraph,
    StackEnum,
)

# Module
from evoml_preprocessor.preprocess.models import Aggregation, ModelOption
from evoml_preprocessor.preprocess.models.report import PreprocessingReport
from evoml_preprocessor.preprocess.selector.util import aggregate

# ──────────────────────────────────────────────────────────────────────────── #


def prepare_data_and_generate_graph(
    feature_scores: Dict[ModelOption, Dict[str, float]],
    aggregation: Aggregation,
) -> Optional[HighchartsGraph]:
    """Function that gets the top 10 features (if 10 exist or otherwise all of
    them) with the best aggregated importance, then get the feature importance
    values for each model and normalizes them, proceeding to call the function
    that constructs the highchart json for the feature aggregation graph.

    Args:
        report:
            contains the feature importance arrays
    Returns:
        feature_aggregation_graph (dict):
            A dictionary containing the highchart json representation of a feature
    """
    # number of features for each model should be consistent
    nr_features = [len(feature_scores[model]) for model in feature_scores]
    if len(set(nr_features)) != 1:
        return None

    feature_importances = pd.DataFrame(feature_scores)
    feature_importances_agg = aggregate(feature_importances, aggregation)
    feature_importances_agg.sort_values(ascending=False, inplace=True)
    feature_importances = feature_importances.loc[feature_importances_agg.index]

    return construct_aggregated_feature_importance_graph(feature_importances)


def construct_aggregated_feature_importance_graph(feature_importance: pd.DataFrame) -> HighchartsGraph:
    """Uses the feature data (importance, names, models) in order to generate
    a dictionary with the structure of a highchart feature importance
    aggregation graph in the form of a stacking column graph and then uses
    convert_graph function from api models to format the graph.

    Args:
        feature_importance (np.ndarray):
            Feature importance values for each model, for the top features (size
            nr_models X 10)
        feature_names: (np.ndarray):
            Feature names of the top features
        models (Set[str]):
            List containing the model names used to calculate the feature
            importance
    Returns:
        HighchartsGraph:
            constructed graph
    """

    graph_builder = get_builder(ColumnChart)
    graph_builder.title = "Aggregated Feature Importance Graph"

    graph_builder.xAxis.categories = feature_importance.index.tolist()
    graph_builder.xAxis.title = "Feature Names"

    graph_builder.yAxis.min = 0
    graph_builder.yAxis.title = "Feature Importance"
    graph_builder.stacking = StackEnum.normal
    graph_builder.labels = feature_importance.index.tolist()

    graph_builder.data = []
    graph_builder.data.extend(
        BarChartData(
            name=model_name,
            data=[float(format(element, ".3f")) for element in fi],
            type=GraphDataType.column,
            zIndex=None,
            additionalInfo=None,
            color=None,
        )
        for model_name, fi in feature_importance.iteritems()
    )

    converted_graph = convert_graph(
        Graph[ColumnChart](
            type=GraphType.columnChart,
            graphJson=graph_builder.build(),
            description=None,
            graphFields=None,
            context=None,
        )
    )

    # we keep just the information we need
    converted_graph.data["xAxis"] = {
        "title": converted_graph.data["xAxis"]["title"],
        "categories": converted_graph.data["xAxis"]["categories"],
    }
    converted_graph.data["yAxis"] = {
        "title": converted_graph.data["yAxis"]["title"],
        "min": converted_graph.data["yAxis"]["min"],
    }
    return converted_graph


def create_feature_aggregation_graph(
    report: PreprocessingReport,
) -> Optional[HighchartsGraph]:
    """Function that extracts data from the feature report part of the
    preprocessing and calls function that creates the desired graph.
    Args:
        report (dict):
            The larger report to be summarised that conforms to
            the model PreprocessReport in evoml-api-models.
    Returns:
        feature_aggregation_graph:
            A feature importance aggregation graph.
    """
    feature_report = report.multiColumnStatistics.featureSelectionReport

    # This expects that the feature importance report is in MRMR has a metric
    # We also might have feature importance as a separate selection metric
    # like the previous implementation. If this is the case, need to
    # make this more flexible or restructure the report
    if feature_report is None:
        return None

    # First feature selection method that has feature importance will
    # consider the most features, so we can use that
    feature_importances = {}
    aggregation = None
    for method in feature_report.selectionMethods:
        aggregation = method.relevancyAggregation
        for metric in method.relevancyMetricReports:
            if metric.wrapper_model is None:
                continue
            # implies that the metric is feature importance
            feature_importances[metric.wrapper_model] = metric.scores
        if feature_importances:
            break

    if not feature_importances or aggregation is None:
        return None

    return prepare_data_and_generate_graph(feature_importances, aggregation)
