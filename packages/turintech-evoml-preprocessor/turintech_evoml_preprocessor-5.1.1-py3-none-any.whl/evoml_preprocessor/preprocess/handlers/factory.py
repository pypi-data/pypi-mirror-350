from typing import Dict, Tuple


# Private Dependencies
from evoml_api_models import MlTask
from evoml_api_models.builder import get_builder, Builder  # type: ignore

# Module
from evoml_preprocessor.preprocess.handlers.data_preparation import (
    DefaultDataPreparationHandler,
    TimeseriesDataPreparationHandler,
    DataPreparationHandler,
)
from evoml_preprocessor.preprocess.handlers.feature import (
    DefaultFeatureHandler,
    ForecastingFeatureHandler,
    TimeseriesFeatureHandler,
    FeatureHandler,
)
from evoml_preprocessor.preprocess.handlers.feature_generation import (
    DefaultFeatureGenerationHandler,
    TimeseriesFeatureGenerationHandler,
    FeatureGenerationHandler,
)
from evoml_preprocessor.preprocess.handlers.feature_selection import (
    DefaultFeatureSelectionHandler,
    TimeseriesFeatureSelectionHandler,
    FeatureSelectionHandler,
)
from evoml_preprocessor.preprocess.handlers.index import (
    DefaultIndexHandler,
    ForecastingIndexHandler,
    TimeSeriesIndexHandler,
    IndexHandler,
)
from evoml_preprocessor.preprocess.handlers.label import (
    CategoricalLabelHandler,
    NumericLabelHandler,
    TimeseriesCategoricalLabelHandler,
    TimeseriesNumericLabelHandler,
    LabelHandler,
)
from evoml_preprocessor.preprocess.handlers.post_processing._base import PostProcessingHandler

from evoml_preprocessor.preprocess.handlers.post_processing.default import DefaultPostProcessingHandler
from evoml_preprocessor.preprocess.handlers.post_processing.timeseries import TimeseriesPostProcessingHandler
from evoml_preprocessor.preprocess.models import ColumnInfo, PreprocessConfig
from evoml_preprocessor.preprocess.handlers.feature import (
    time_series_feature_handler_config_adapter,
    forecasting_feature_handler_config_adapter,
    default_feature_handler_config_adapter,
)
from evoml_preprocessor.utils.validation import _get_config_options


def handler_factory(
    config: PreprocessConfig,
    info_map: Dict[str, ColumnInfo],
) -> Tuple[
    DataPreparationHandler,
    IndexHandler,
    FeatureHandler,
    FeatureGenerationHandler,
    FeatureSelectionHandler,
    PostProcessingHandler,
    LabelHandler,
]:
    """Initializes the handlers for each preprocessing step based on the mlTask.

    The mlTask is used to determine which handlers to use for each
    preprocessing step. The different tasks:
    - classification
    - regression
    - forecasting
    - timeseries classification
    - timeseries regression

    The different handlers allow us to have a modular design where each step
    can be replaced by a different implementation.

    The handlers are:
    - label_handler (LabelHandler): handles the label column
        (the column we want to predict)
    - index_handler (IndexHandler): handles the index column (if any)
    - feature_handler (FeatureHandler): handles the feature columns
        (columns that are not the label or index)
    - fs_handler (FeatureSelectionHandler): handles the feature selection step (if any)
    - fg_handler (FeatureGenerationHandler): handles the feature generation
        (feature engineering)
    - data_preparation_handler (DataPreparationHandler): handles the data preparation

    Args:
        config (PreprocessConfig): PreprocessConfig object containing generic
            information about the dataset.
        info_map (Dict[str, ColumnInfo]): Dictionary where the keys are the names
            of the columns and values the corresponding ColumnInfo objects.

    """

    data_preparation_handler = data_preparation_handler_factory(config, info_map)
    index_handler = index_handler_factory(config)
    feature_handler = feature_handler_factory(config, info_map)
    feature_generation_handler = feature_generation_handler_factory(config)
    feature_selection_handler = feature_selection_handler_factory(config)
    label_handler = label_handler_factory(config, info_map)
    post_processing_handler = post_processing_handler_factory(config)

    return (
        data_preparation_handler,
        index_handler,
        feature_handler,
        feature_generation_handler,
        feature_selection_handler,
        post_processing_handler,
        label_handler,
    )


def post_processing_handler_factory(config: PreprocessConfig) -> PostProcessingHandler:
    if config.isTimeseries:
        return TimeseriesPostProcessingHandler(config)
    return DefaultPostProcessingHandler(config)


def label_handler_factory(config: PreprocessConfig, info_map: Dict[str, ColumnInfo]) -> LabelHandler:
    label_index = info_map[config.labelColumn].columnIndex
    col_info = info_map[config.labelColumn]
    conf_options = (
        _get_config_options(config).transformation_options[label_index]
        if label_index in _get_config_options(config).transformation_options
        else None
    )

    if config.mlTask == MlTask.classification:
        if config.isTimeseries and config.createTargetLags:
            return TimeseriesCategoricalLabelHandler(config, col_info, conf_options)
        return CategoricalLabelHandler(config, col_info, conf_options)

    if config.mlTask == MlTask.regression:

        if config.isTimeseries and config.createTargetLags:
            return TimeseriesNumericLabelHandler(config, col_info, conf_options)
        return NumericLabelHandler(config, col_info, conf_options)

    if config.mlTask == MlTask.forecasting:
        return NumericLabelHandler(config, col_info, conf_options)

    raise ValueError(f"Unsupported MLTask {config.mlTask}")


def feature_generation_handler_factory(config) -> FeatureGenerationHandler:
    if not config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression]:
        return DefaultFeatureGenerationHandler(config)

    if config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression, MlTask.forecasting]:
        return TimeseriesFeatureGenerationHandler(config)

    raise ValueError(
        f"Unsupported configuration: config.isTimeseries = {config.isTimeseries} and config.mlTask = {config.mlTask}."
    )


def feature_selection_handler_factory(config) -> FeatureSelectionHandler:
    if not config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression]:
        return DefaultFeatureSelectionHandler(config)

    if config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression, MlTask.forecasting]:
        return TimeseriesFeatureSelectionHandler(config)

    raise ValueError(
        f"Unsupported configuration: config.isTimeseries = {config.isTimeseries} and config.mlTask = {config.mlTask}."
    )


def feature_handler_factory(config: PreprocessConfig, info_map: Dict[str, ColumnInfo]) -> FeatureHandler:

    if not config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression]:
        return DefaultFeatureHandler(
            default_feature_handler_config_adapter(config, info_map, _get_config_options(config))
        )

    if config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression]:
        return TimeseriesFeatureHandler(
            time_series_feature_handler_config_adapter(config, info_map, _get_config_options(config))
        )

    if config.isTimeseries and config.mlTask == MlTask.forecasting:
        return ForecastingFeatureHandler(
            forecasting_feature_handler_config_adapter(config, info_map, _get_config_options(config))
        )

    raise ValueError(
        f"Unsupported configuration: config.isTimeseries = {config.isTimeseries} and config.mlTask = {config.mlTask}."
    )


def data_preparation_handler_factory(
    config: PreprocessConfig, info_map: Dict[str, ColumnInfo]
) -> DataPreparationHandler:
    if config.isTimeseries:
        return TimeseriesDataPreparationHandler(config, info_map, _get_config_options(config))
    return DefaultDataPreparationHandler(config, info_map, _get_config_options(config))


def index_handler_factory(config: PreprocessConfig) -> IndexHandler:

    if not config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression]:
        return DefaultIndexHandler(config.mlTask)

    if config.isTimeseries and config.mlTask in [MlTask.classification, MlTask.regression]:
        return TimeSeriesIndexHandler(config.mlTask)

    if config.isTimeseries and config.mlTask == MlTask.forecasting:
        return ForecastingIndexHandler(config.mlTask)

    raise ValueError(
        f"Unsupported configuration: config.isTimeseries = {config.isTimeseries} and config.mlTask = {config.mlTask}."
    )
