from typing import List, Set, Dict, Optional

from pydantic import BaseModel


from evoml_api_models import MlTask


from evoml_preprocessor.preprocess.models import (
    ColumnInfo,
    ColumnOptions,
    ConfigOptions,
    PreprocessConfig,
)


class TimeSeriesFeatureHandlerConfig(BaseModel):
    index_name: Optional[str]
    ml_task: MlTask
    model_names: List[str]
    info_map: Dict[str, ColumnInfo]
    transformation_options: Dict[int, ColumnOptions]
    ignored_features: List[int]
    required_features: List[int]
    future_covariates_indices: List[int]
    window_size: int
    horizon: int
    label_name: str


def time_series_feature_handler_config_adapter(
    config: PreprocessConfig,
    info_map: Dict[str, ColumnInfo],
    config_options: Optional[ConfigOptions] = None,
) -> TimeSeriesFeatureHandlerConfig:

    if config_options is None:
        config_options = ConfigOptions()

    return TimeSeriesFeatureHandlerConfig(
        index_name=config.indexColumn,
        ml_task=config.mlTask,
        model_names=[x.name for x in config.models],
        info_map=info_map,
        transformation_options=config_options.transformation_options,
        ignored_features=config_options.ignored_features,
        required_features=config_options.required_features,
        future_covariates_indices=config_options.future_covariates_indices,
        window_size=config.windowSize,
        horizon=config.timeSeriesHorizon,
        label_name=config.labelColumn,
    )
