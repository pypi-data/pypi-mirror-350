from typing import Any, Optional

from evoml_api_models import BaseDefaultConf, conf_factory

from evoml_preprocessor.preprocess.models.config import ParallelisationOptions


class PreprocessSettings(BaseDefaultConf):
    CATEGORICAL_DATA_THRESHOLD: int = 20
    DROP_MISS_VALUE_RATE: float = 0.7
    DROP_UNIQUE_VALUE_RATIO: float = 0.8
    FILL_LABEL_NUMBER: int = 0  # need to be changed
    HASH_NUMBER: int = 8
    LABEL_ENCODING_THRESHOLD: int = 100
    ONE_HOT_ENCODING_THRESHOLD: int = 20
    LABEL_MISSING_THRESHOLD: float = 0.05
    SKEWNESS_THRESHOLD: int = 5
    TASK_THRESHOLD: float = 0.05
    UNARY_MISSING_RATE: float = 0.3
    TEXT_DIMENSION: int = 100
    HIGH_FREQUENCY_UNIQUE_THRESHOLD: int = 10
    ENABLE_FEATURE_SELECTOR: bool = True
    SAMPLE_SIZE: int = 1000
    THREADS: int = ParallelisationOptions().threads
    MULTICOLLINEARITY_CLUSTER_THRESHOLD: int = 1
    HIGH_CORRELATION_THRESHOLD: float = 0.95
    LOW_CORR_COL_COUNT_MIN: int = 5
    MUTUAL_INFORMATION_THRESHOLD: float = 0.95
    ALLOW_SEQUENTIAL: bool = False
    ALLOW_PERMUTATION: bool = False
    ENABLE_ENSEMBLE: bool = True
    PATH_PIPELINE_APPENDIX = "pipeline_appendix"
    EPSILON = 1e-4
    DATA_PREPARATION_THRESHOLD = 500
    MAX_SEARCH_FEATURES: int = 0
    RANDOM_SEED: Optional[int] = None


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                  Preprocess Configuration Factory                             #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


def preprocess_conf_factory(
    _env_file: Optional[str] = ".env", prefix: Optional[str] = None, defaults: Optional[dict] = None, **kwargs: Any
) -> PreprocessSettings:
    """
    This is a factory generating an DataConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_DATA_PATH=/tmp/data
       ...
    """
    return conf_factory(
        config_class=PreprocessSettings, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs
    )
