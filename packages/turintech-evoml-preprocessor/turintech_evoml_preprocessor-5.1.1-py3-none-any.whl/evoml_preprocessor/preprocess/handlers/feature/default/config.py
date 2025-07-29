from typing import List, Dict, Optional


from pydantic import BaseModel


from evoml_api_models import MlTask


from evoml_preprocessor.preprocess.models import (
    ColumnInfo,
    ColumnOptions,
    ConfigOptions,
    PreprocessConfig,
)


class DefaultFeatureHandlerConfig(BaseModel):
    ml_task: MlTask
    model_names: List[str]
    info_map: Dict[str, ColumnInfo]
    transformation_options: Dict[int, ColumnOptions]
    ignored_features: List[int]
    required_features: List[int]
    label_name: str


def default_feature_handler_config_adapter(
    config: PreprocessConfig,
    info_map: Dict[str, ColumnInfo],
    config_options: Optional[ConfigOptions] = None,
) -> DefaultFeatureHandlerConfig:

    if config_options is None:
        config_options = ConfigOptions()

    return DefaultFeatureHandlerConfig(
        ml_task=config.mlTask,
        model_names=[x.name for x in config.models],
        info_map=info_map,
        transformation_options=config_options.transformation_options,
        ignored_features=config_options.ignored_features,
        required_features=config_options.required_features,
        label_name=config.labelColumn,
    )
