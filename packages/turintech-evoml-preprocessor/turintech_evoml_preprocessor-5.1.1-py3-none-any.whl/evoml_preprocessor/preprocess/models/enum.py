# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
# Standard Library
from __future__ import annotations

# Dependencies
from enum import Enum
from typing import Dict, List, Union

# Private Dependencies
from evoml_api_models import DetectedType

# Module
from evoml_preprocessor.utils.string_enum import StrEnum


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
class GenericOption(StrEnum):
    """Generic options for all modules."""

    AUTO = "auto"
    NONE = "none"


class CategoricalEncoder(StrEnum):
    """Categorical encoding options."""

    LABEL_ENCODER = "label-encoder"
    ONE_HOT_ENCODER = "one-hot-encoder"
    ORDINAL_ENCODER = "ordinal-encoder"
    HASH_ENCODER = "hash-encoder"
    BACKWARD_DIFFERENCE_ENCODER = "backward-difference-encoder"
    CAT_BOOST_ENCODER = "cat-boost-encoder"
    HELMERT_ENCODER = "helmert-encoder"
    TARGET_ENCODER = "target-encoder"
    ENTROPY_BINNING_ENCODER = "entropy-binning-encoder"


class NumericEncoder(StrEnum):
    """Numeric encoding options."""

    LOG_ENCODER = "log-encoder"
    POWER_ENCODER = "power-encoder"
    RECIPROCAL_ENCODER = "reciprocal-encoder"
    SQUARE_ENCODER = "square-encoder"
    QUANTILE_TRANSFORM_ENCODER = "quantile-transform-encoder"

    # forecasting target transformation
    DIFFERENCE = "difference-transform"
    RATIO = "ratio-transform"
    LOG_RATIO = "log-ratio-transform"


class ScalerEncoder(StrEnum):
    """Scaler options."""

    MIN_MAX_SCALER = "min-max-scaler"
    STANDARD_SCALER = "standard-scaler"
    MAX_ABS_SCALER = "maxabs-scaler"
    ROBUST_SCALER = "robust-scaler"
    GAUSS_RANK_SCALER = "gauss-rank-scaler"


class ImputeStrategy(StrEnum):
    # For all types
    CONSTANT = "constant"
    MOST_FREQUENT = "most-frequent"
    AUTO = "auto"
    NONE = "none"

    # For numeric types
    MEDIAN = "median"
    MEAN = "mean"

    # Time series
    FORWARD_FILL = "ffill"
    BACKWARD_FILL = "bfill"
    LINEAR_INTERPOLATE = "linear"
    SPLINE_INTERPOLATE = "spline"
    MOVING_AVERAGE = "moving-average"
    POLYNOMIAL_INTERPOLATE = "polynomial"


class ReasonDropped(StrEnum):
    """Reasons why a column was dropped."""

    DUPLICATE_COLUMN = "dropped duplicate column"
    NULL = "dropped null column"
    DROPPED_BY_USER = "dropped by user"
    VALUES_TOO_CLOSE = "dropped as values are too close"
    HIGH_MISSING_RATE = "dropped due to high missing value rate"
    HIGH_UNIQUE_VALUES = "dropped due to high unique values"
    FEATURE_SELECTOR = "dropped in feature selector"
    UNSUPPORTED_TYPE = "dropped unsupported type"
    CONSTANT_VALUE = "dropped constant value"
    DATA_PREPARATION = "dropped in data preparation"
    DATA_LEAK = "dropped potential data leak"
    PERFECT_CORRELATION_WITH_TARGET = "dropped due to perfect correlation with target"
    ID = "id column"
    DEPRECATED = "dropped due to being deprecated"


class Filter(StrEnum):
    """Filter options."""

    KEEP = "keep"
    DROP = "drop"
    AUTO = "auto"


class Covariate(StrEnum):
    """Covariate options for forecasting."""

    FUTURE = "future"
    PAST = "past"


class DateOptions(StrEnum):
    UNIX_TIMESTAMP = "unix-timestamp"
    DAY_OF_WEEK = "day-of-week"
    DAY_OF_YEAR = "day-of-year"
    WEEK_OF_YEAR = "week-of-year"
    IS_WEEKEND = "is-weekend"
    QUARTER = "quarter"
    RELATIVE_YEAR = "relative-year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"


class RollingOperation(StrEnum):
    MEAN = "mean"
    STD = "std"
    MIN = "min"
    MAX = "max"
    MEDIAN = "median"
    ZSCORE = "zscore"
    SKEW = "skewness"  # This only works if the window size is >= 3
    KURT = "kurtosis"
    DIFFERENCE = "difference"
    RETURN = "return"
    LOG_RETURN = "log-return"

    @property
    def display_name(self) -> str:
        return self.value


class Block(StrEnum):
    # encoders we can currently set using the frontend
    CATEGORICAL = "categorical"
    FLOAT = "basicFloat"
    FRACTION = "fraction"
    INTEGER = "basicInteger"
    PERCENTAGE = "percentage"
    UNIT_NUMBER = "unitNumber"
    # encoders we cannot set using the frontend
    TARGET = "target"
    DATE = "dateTime"
    IP = "ipAddress"
    LABEL_ENCODING = "label-encoding"
    LIST = "list"
    URL = "url"
    URL_NETLOC = "url_netloc"
    URL_PATH = "url_path"
    URL_FRAGMENT = "url_fragment"
    TEXT = "text"
    UNARY = "unary"
    BINARY = "binary"
    CURRENCY = "currency"
    EMAIL = "email"
    PHONE = "phoneNumber"
    ADDRESS = "address"
    MAP = "map"
    SAMPLE_ID = "ID"
    BARCODE = "barcode"
    BANKCODE = "bankCode"
    DUPLICATE = "duplicate"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"
    CURRENCY_VALUE = "currency_value"
    CURRENCY_SIGN = "currency_sign"
    PHONE_COUNTRY = "phoneNumber_country"
    PHONE_NATIONAL = "phoneNumber_national"
    GEO_LOCATION = "geoLocation"
    GEO_LOCATION_CITY = "geoLocation_city"
    GEO_LOCATION_STATE = "geoLocation_state"
    GEO_LOCATION_COUNTRY = "geoLocation_country"
    EMAIL_DOMAIN = "email_domain"
    EMAIL_LOCAL_PART = "email_region"
    ADDRESS_CITY = "address_city"
    ADDRESS_COUNTRY = "address_country"
    ADDRESS_STREET = "address_street"
    BANKCODE_BUSINESS_PREFIX = "bankcode_business_prefix"
    BANKCODE_BUSINESS_SUFFIX = "bankcode_business_suffix"
    BANKCODE_COUNTRY = "bankcode_country"
    BANKCODE_BRANCH = "bankcode_branch"
    BANKCODE_BANK = "bankcode_bank"
    BANKCODE_ACCOUNT = "bankcode_account"
    BARCODE_ACCOUNT = "barcode_country"
    BARCODE_GROUP = "barcode_group"
    BARCODE_PUBLISHER = "barcode_publisher"
    BARCODE_TITLE = "barcode_title"
    BARCODE_COUNTRY = "barcode_country"
    BARCODE_MANUFACTURER = "barcode_manufacturer"
    PROTEIN_SEQUENCE = "proteinSequence"


class EmbeddingTransformer(StrEnum):
    # Predefined accepted models for embedding process
    # Runtime embeddings
    # auto is the default approach
    TFIDF = "tfidf"
    # https://huggingface.co/distilbert-base-uncased
    DISTILBERT_BASE_UNCASED = "distilbert-base-uncased"
    # https://huggingface.co/bert-base-uncased
    BERT_BASE_UNCASED = "bert-base-uncased"
    # https://huggingface.co/roberta-base
    ROBERTA_BASE = "roberta-base"
    # https://huggingface.co/albert-base-v2
    ALBERT_BASE_V2 = "albert-base-v2"
    # https://huggingface.co/gpt2
    GPT2 = "gpt2"
    # https://huggingface.co/xlnet-base-cased
    XLNET_BASE_CASED = "xlnet-base-cased"
    # https://huggingface.co/google/electra-base-discriminator
    ELECTRA_BASE_DISCRIMINATOR = "electra-base-discriminator"
    # https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
    ALL_MINI_LM_L6_V2 = "all-MiniLM-L6-v2"
    # https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2
    ALL_MINI_LM_L12_V2 = "all-MiniLM-L12-v2"
    # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
    ALL_MPNET_BASE_V2 = "all-mpnet-base-v2"
    # https://huggingface.co/sentence-transformers/all-distilroberta-v1
    ALL_DISTILROBERTA_V1 = "all-distilroberta-v1"
    # https://huggingface.co/microsoft/codebert-base
    CODEBERT_BASE = "codebert-base"

    def get_huggingface_encoder(self) -> str:
        SENTENCE_TRANSFORMERS_PREFIX = "sentence-transformers/"
        prefix: Dict[str, str] = {
            EmbeddingTransformer.ELECTRA_BASE_DISCRIMINATOR: "google/",
            EmbeddingTransformer.ALL_MINI_LM_L6_V2: SENTENCE_TRANSFORMERS_PREFIX,
            EmbeddingTransformer.ALL_MINI_LM_L12_V2: SENTENCE_TRANSFORMERS_PREFIX,
            EmbeddingTransformer.ALL_MPNET_BASE_V2: SENTENCE_TRANSFORMERS_PREFIX,
            EmbeddingTransformer.ALL_DISTILROBERTA_V1: SENTENCE_TRANSFORMERS_PREFIX,
            EmbeddingTransformer.CODEBERT_BASE: "microsoft/",
        }
        if self.value in prefix:
            return prefix[self.value] + self.value
        return self.value


class ProteinEmbeddingTransformer(StrEnum):
    # https://huggingface.co/Rostlab/prot_bert
    PROT_BERT = "prot-bert"
    # https://huggingface.co/Rostlab/prot_bert_bfd
    PROT_BERT_BFD = "prot-bert-bfd"
    # https://huggingface.co/Rostlab/prot_electra_discriminator_bfd
    PROT_ELECTRA_DISCRIMINATOR_BFD = "prot-electra-discriminator-bfd"

    def get_huggingface_encoder(self) -> str:
        ROSTLAB_PREFIX = "Rostlab/"
        prefix: Dict[str, str] = {
            ProteinEmbeddingTransformer.PROT_BERT: ROSTLAB_PREFIX,
            ProteinEmbeddingTransformer.PROT_BERT_BFD: ROSTLAB_PREFIX,
            ProteinEmbeddingTransformer.PROT_ELECTRA_DISCRIMINATOR_BFD: ROSTLAB_PREFIX,
        }
        if self.value in prefix:
            return prefix[self.value] + self.value.replace("-", "_")
        return self.value


# Enumerator for model options to be immutable and constant.
class ModelOption(StrEnum):
    # Model options
    LINEAR = "lasso-regressor"
    NEAREST_NEIGHBOUR = "nearest-neighbour"
    RANDOM_FOREST = "random-forest"
    SUPPORT_VECTOR_MACHINE = "support-vector-machine"
    GRADIENT_BOOSTING = "lightgbm"
    TREE = "decision-tree"
    NETWORK = "network"
    BAYESIAN = "bayesian"
    CORRELATION = "correlation"
    AUTO = "auto"

    def display(self) -> str:
        # Go from 'kebab-case' to 'Kebab Case'
        return " ".join([word.capitalize() for word in self.value.split("-")])


class SelectionMetric(StrEnum):
    # Selection metrics
    KOLMOGOROV_SMIRNOV = "kolmogorov-smirnov"
    FEATURE_IMPORTANCE = "feature-importance"
    F_TEST = "f-test"
    PEARSON = "pearson"
    SPEARMAN = "spearman"
    MUTUAL_INFORMATION = "mutual-information"
    NONE = "none"


class Aggregation(StrEnum):
    # Aggregation methods
    MEAN = "mean"
    MAX = "max"
    RANK = "rank"


class SelectionMethod(StrEnum):
    # Selection pipelines
    MRMR = "mrmr"
    FILTER = "filter"
    RANKING = "ranking"
    LINEAR = "linear"
    RANDOM = "random"
    MRMR_IMPORTANCE = "mrmr-importance"
    QPFS = "qpfs"


class SelectorType(StrEnum):
    # Selector types
    LINEAR = "linear"
    RANDOM = "random"
    MRMR = "mrmr"
    RELEVANCE = "relevance"
    REDUNDANCE = "redundance"
    UNARY = "unary"
    QPFS = "qpfs"


class Tags(StrEnum):
    # Tags
    TARGET = "target"
    LIMITED_OUTLIERS_NUMBER = "limited outliers number"
    MEDIUM_OUTLIERS_NUMBER = "medium outliers number"
    SUBSTANTIAL_OUTLIERS_NUMBER = "substantial outliers number"
    IMBALANCED = "imbalanced"
    BALANCED = "balanced"
    ALMOST_BALANCED = "almost balanced"
    EXTREMELY_IMBALANCED = "extremely imbalanced"
    INCONSISTENT_DATA = "inconsistent data"
    AMBIGUOUS_DATA_TYPE = "ambiguous data type"
    HIGH_CARDINALITY = "high cardinality"
    LOW_VARIANCE = "low variance"
    HIGH_SKEW = "high skewness"
    EXCESS_ZEROES = "excess zeroes"
    NORMAL_DISTRIBUTION = "normal distribution"
    ALL_UNIQUE = "all unique"
    CONSTANT_COUNTRY = "constant country"
    VARIOUS_COUNTRIES = "various countries"
    CONSTANT_DOMAIN = "constant domain"
    NESTED_LISTS = "nested lists"
    NESTED_MAPS = "nested maps"
    NULL_COLUMN = "null column"
    INCOMPLETE_BINARY = "incomplete binary"
    DATA_LEAK = "potential data leak"
    REQUIRED_BY_USER = "required by user"


class ImputeSubsets(Enum):
    CONSTANT_VALUE = {
        ImputeStrategy.MOST_FREQUENT,
        ImputeStrategy.CONSTANT,
        ImputeStrategy.FORWARD_FILL,
        ImputeStrategy.BACKWARD_FILL,
        ImputeStrategy.NONE,
    }
    NUMERIC_ALL = {
        ImputeStrategy.MEDIAN,
        ImputeStrategy.MEAN,
        ImputeStrategy.MOST_FREQUENT,
        ImputeStrategy.CONSTANT,
        ImputeStrategy.FORWARD_FILL,
        ImputeStrategy.BACKWARD_FILL,
        ImputeStrategy.LINEAR_INTERPOLATE,
        ImputeStrategy.SPLINE_INTERPOLATE,
        ImputeStrategy.POLYNOMIAL_INTERPOLATE,
        ImputeStrategy.MOVING_AVERAGE,
        ImputeStrategy.NONE,
    }
    NUMERIC_SIMPLE = {
        ImputeStrategy.MEDIAN,
        ImputeStrategy.MEAN,
        ImputeStrategy.MOST_FREQUENT,
        ImputeStrategy.CONSTANT,
        ImputeStrategy.NONE,
    }
    IMPUTE_TS = {
        ImputeStrategy.FORWARD_FILL,
        ImputeStrategy.BACKWARD_FILL,
        ImputeStrategy.LINEAR_INTERPOLATE,
        ImputeStrategy.SPLINE_INTERPOLATE,
        ImputeStrategy.POLYNOMIAL_INTERPOLATE,
        ImputeStrategy.MOVING_AVERAGE,
    }


class TypeSubsets(Enum):
    UNSUPPORTED_TS = {DetectedType.unsupported, DetectedType.unknown, DetectedType.duplicate, DetectedType.geo_location}
    NUMERIC = {
        DetectedType.integer,
        DetectedType.float,
        DetectedType.percentage,
        DetectedType.fraction,
        DetectedType.currency,
        DetectedType.unit_number,
    }
    NUMERIC_SIMPLE = {
        DetectedType.integer,
        DetectedType.percentage,
        DetectedType.fraction,
        DetectedType.currency,
        DetectedType.unit_number,
    }
    DATE = {
        DetectedType.datetime,
    }
    CATEGORICAL_TS = {
        DetectedType.unary,
        DetectedType.binary,
        DetectedType.categorical,
        DetectedType.text,
        DetectedType.url,
        DetectedType.email,
        DetectedType.ip,
        DetectedType.phone,
        DetectedType.address,
        DetectedType.list,
        DetectedType.map,
        DetectedType.barcode,
        DetectedType.bank_code,
        DetectedType.protein_sequence,
        DetectedType.sample_id,
    }


for detected_type in DetectedType:
    assert any(
        detected_type in subset.value for subset in TypeSubsets
    ), f"{detected_type} is not covered by any TypeSubsets"


AllEncoders = Union[
    GenericOption,
    NumericEncoder,
    CategoricalEncoder,
    EmbeddingTransformer,
    ProteinEmbeddingTransformer,
    None,
]


AllNumeric = Union[
    GenericOption,
    NumericEncoder,
]

AllCategorical = Union[
    GenericOption,
    CategoricalEncoder,
]

AllScalers = Union[GenericOption, ScalerEncoder, None]

AllEmbedding = Union[
    GenericOption,
    EmbeddingTransformer,
]

AllProteinEmbedding = Union[
    GenericOption,
    ProteinEmbeddingTransformer,
]

EncoderSearchSpace = Union[
    List[AllNumeric],
    List[AllCategorical],
    List[AllEmbedding],
    List[AllProteinEmbedding],
]

ScalerSearchSpace = List[AllScalers]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "GenericOption",
    "CategoricalEncoder",
    "NumericEncoder",
    "ScalerEncoder",
    "ImputeStrategy",
    "ReasonDropped",
    "Filter",
    "Block",
    "EmbeddingTransformer",
    "ProteinEmbeddingTransformer",
    "ModelOption",
    "Tags",
    "ImputeSubsets",
    "TypeSubsets",
    "SelectionMetric",
    "Aggregation",
    "SelectionMethod",
    "SelectorType",
    "Covariate",
    "RollingOperation",
]
