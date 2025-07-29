"""Defines the pydantic models for preprocessor's config"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from enum import Enum
from multiprocessing import cpu_count
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

# Dependencies
from evoml_api_models import (
    BaseTypes,
    ColumnAnomalies,
    ColumnDefaultTrialOptions,
    ColumnStatistics,
    ColumnTag,
    DetectedType,
    MlTask,
)
from pydantic import BaseModel, BaseSettings, Field, root_validator, validator
from pydantic.types import StrictInt

# Module
from evoml_preprocessor.decomposition.enum import DimReduction
from evoml_preprocessor.preprocess.generator.operations import BinaryOpLiteral, UnaryOpLiteral
from evoml_preprocessor.preprocess.models.enum import (
    Aggregation,
    AllEncoders,
    AllScalers,
    Block,
    Covariate,
    DateOptions,
    EncoderSearchSpace,
    Filter,
    GenericOption,
    ImputeStrategy,
    ModelOption,
    RollingOperation,
    ScalerSearchSpace,
    SelectionMethod,
    SelectionMetric,
)
from evoml_preprocessor.utils.string_enum import StrEnum

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #

# ──────────────────────────────────────────────────────────────────────────── #
#                        Transformation Options Data                           #
# ──────────────────────────────────────────────────────────────────────────── #

ImputeValue = Union[float, int, str, None]
"""Type alias for user-provided values to impute missing data"""


class Slug(BaseModel):
    """a slug is a key/value pair that can be used to represent categorical encoders, numeric encoders, embedding
    process and scaler encoders

    @NOTE: needs clarity, this is really used to define a search space for either encoders/scalers
    """

    slugKey: Block
    slugValue: Union[EncoderSearchSpace, ScalerSearchSpace]


class Impute(BaseModel):
    """This model describes the options for imputing missing data"""

    strategy: ImputeStrategy = ImputeStrategy.AUTO
    value: Optional[ImputeValue] = None


class FeatureOverrides(BaseModel):
    """This model describes the options for overriding the default feature"""

    columnIndex: int
    filter: Filter = Filter.AUTO
    covariate: Covariate = Covariate.PAST
    derivedColumns: Optional[List[DateOptions]] = None
    rolling: List[RollingOperation] = []
    encoderSlugs: List[Slug] = []
    scalerSlugs: List[Slug] = []
    impute: Impute = Impute()


class TransformationOptions(BaseModel):
    """This model describes the options for overriding the default feature"""

    detectedType: DetectedType
    impute: Impute = Impute()
    encoderSlugs: List[Slug] = []
    scalerSlugs: List[Slug] = []
    featureOverrides: List[FeatureOverrides] = []


# ──────────────────────────────────────────────────────────────────────────── #
#                                Model Data                                    #
# ──────────────────────────────────────────────────────────────────────────── #


class InputParameter(BaseModel):
    """This model describes the input parameters for a model"""

    parameterName: str
    parameterType: str
    minValue: Optional[Union[StrictInt, float]]
    maxValue: Optional[Union[StrictInt, float]]
    values: List[Any]
    defaultValue: Any


class ModelParameter(BaseModel):
    """This model describes the parameters for a model"""

    inputParameters: List[InputParameter]


class ModelDefinition(BaseModel):
    """This model describes the definition for a model"""

    name: str
    parameters: Optional[ModelParameter]


# ──────────────────────────────────────────────────────────────────────────── #
#                                Splitting Data                                #
# ──────────────────────────────────────────────────────────────────────────── #


class SplitMethod(StrEnum):
    """This model describes the splitting method

    @TODO: can remove the type: ignore once we capitalise enums
    """

    percentage = "percentage"
    subset = "subset"
    index = "index"  # type: ignore
    presplit = "pre-split"
    nosplit = "no-split"


class SplitMethodOptions(BaseModel):
    """This model describes the splitting method options"""

    _ranges_description = "for 'index' & 'subset' methods only"
    method: SplitMethod = SplitMethod.percentage
    trainPercentage: Optional[float] = Field(default=0.8, gt=0, lt=1, description="Required for method == 'percentage'")
    subsetColumnName: Optional[str] = Field(default=None, description="Required for method == 'subset'", example="city")
    trainRangeFrom: Any = Field(default=None, description=_ranges_description)
    trainRangeTo: Any = Field(default=None, description=_ranges_description)
    testRangeFrom: Any = Field(default=None, description=_ranges_description)
    testRangeTo: Any = Field(default=None, description=_ranges_description)

    @root_validator
    def method_validation(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Applies conditional validation depending on the method"""

        method: SplitMethod = values["method"]

        if method == SplitMethod.index:
            for key in (
                "trainRangeFrom",
                "trainRangeTo",
                "testRangeFrom",
                "testRangeTo",
            ):
                index = values.get(key)

                if isinstance(index, str) and index.isnumeric():
                    values[key] = int(index)
                    index = values[key]
                assert isinstance(index, int) and 0 <= index
        elif method == SplitMethod.subset:
            assert isinstance(values.get("subsetColumnName"), str)
        elif method == SplitMethod.percentage:
            assert isinstance(values.get("trainPercentage"), float)

        return values


# ──────────────────────────────────────────────────────────────────────────── #
#                              Validation Method                               #
# ──────────────────────────────────────────────────────────────────────────── #


class ValidationMethod(StrEnum):
    """Enumeration of the supported validation methods.
    This links 1 ↔ 1 with a model defining parameters (options) for each of this
    enumeration's members.
    """

    cross_validation = "cross-validation"
    holdout = "holdout"
    sliding_window = "sliding-window"
    expanding_window = "expanding-window"
    forecast_holdout = "forecast-holdout"


class CrossValidationOptions(BaseModel):
    """Individual parameters for the 'cross-validation' method"""

    keepOrder: bool = False


class HoldoutOptions(BaseModel):
    """Individual parameters for the 'holdout' method"""

    keepOrder: bool = False


class ValidationMethodOptions(BaseModel):
    """This model describes the options for the validation method"""

    method: ValidationMethod = ValidationMethod.cross_validation
    crossValidationOptions: Optional[CrossValidationOptions] = CrossValidationOptions()
    holdoutOptions: Optional[HoldoutOptions] = Field(default=None, description="Required for method == 'holdout'")

    @property
    def keep_order(self) -> bool:
        if self.method == ValidationMethod.cross_validation:
            assert self.crossValidationOptions is not None
            return self.crossValidationOptions.keepOrder
        elif self.method == ValidationMethod.holdout:
            assert self.holdoutOptions is not None
            return self.holdoutOptions.keepOrder
        return False


# ──────────────────────────────────────────────────────────────────────────── #
#                       Feature Selection Options Data                         #
# ──────────────────────────────────────────────────────────────────────────── #


class ImportanceOptions(BaseModel):
    """This model describes the options for the feature importance method"""

    subsample: float = Field(default=1.0, description="proportion of the dataset to subsample", ge=0.0, le=1.0)
    nEstimators: int = Field(
        default=1, description="number of estimators to use for ensembling feature importance", ge=1
    )
    sampleWithReplacement: bool = Field(default=False, description="if true, samples with replacement")
    modelOptions: List[ModelOption] = Field(
        default=[ModelOption.RANDOM_FOREST],
        description="a collection of model types for feature importance calculations",
    )
    importanceAggregation: Aggregation = Field(
        default=Aggregation.RANK, description="the method by which feature importance calculations are combined"
    )
    drawGraph: bool = Field(
        default=True,
        description="if true, a highcharts compatible graph is obtained from the report for feature importance",
    )

    @root_validator(allow_reuse=True)
    def ensure_model_options_exist(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures that the model options are valid"""

        if len(values["modelOptions"]) == 0:
            values["modelOptions"] = {ModelOption.RANDOM_FOREST}
        return values


class MrmrOptions(BaseModel):
    """This model describes the options for the mRMR feature selection method"""

    linear: bool = Field(
        default=False,
        description=(
            "if true, mrmr relevancy and redundancy are combined linearly using the `redundancyWeight` to set the ratio"
            " between them. If false, takes the quotient of relevance over redundance"
        ),
    )
    redundancyWeight: float = Field(
        default=0.1, description="weight of the redundancy score if `linear` is true", ge=0.0
    )
    importanceWeight: float = Field(
        default=0.1,
        description="weight of feature importance if `selectionMethod` is `mrmr-importance`",
        ge=0.0,
        le=1.0,
    )
    calcScores: bool = False


class QpfsOptions(BaseModel):
    """This model describes the options for the QPFS feature selection method"""

    nystrom: Literal["auto", "yes", "no"] = Field(
        default="auto",
        description="whether to use nystrom approximation. if auto, "
        "it is used if the number of features exceeds a set threshold",
    )


class FilterOptions(BaseModel):
    """This model describes the options for the filter feature selection method"""

    redundanceFirst: bool = Field(
        default=True,
        description=(
            "if true, filters via redundancy metric first and then relevancy. If false, filters via relevancy metric"
            " first and then redundancy. This does nothing if only one metric is selected"
        ),
    )
    redundancyWeight: float = Field(
        default=0.25,
        description=(
            "if thresholds are not set, we assume a fixed target for the number of features. This weight value helps to"
            " determine the number of features to filter by the redundance method versus the relevance method. This"
            " does nothing if only one metric is selected"
        ),
        ge=0.0,
        le=1.0,
    )
    relevancyThreshold: float = Field(
        default=1.0,
        description=(
            "threshold for relevancy filtering. If the most relevant feature has a score of 1.0, any value with a score"
            " less than the value will be filtered out. If this is set to 1.0, then no filtering is done via threshold"
        ),
        ge=0.0,
        le=1.0,
    )
    redundancyThreshold: float = Field(
        default=1.0,
        description=(
            "threshold for redundancy filtering. If the most redundant feature has a score of 1.0, any value with a"
            " score less than the value will be filtered out. If this is set to 1.0, then no filtering is done via"
            " threshold"
        ),
        ge=0.0,
        le=1.0,
    )


class FeatureSelectionOptions(BaseModel):
    """This model describes the options for the feature selection method"""

    # general selection options
    enable: bool = True
    enableSequential: bool = False
    noOfFeatures: Optional[int] = None
    enforceNoOfFeatures: bool = False

    # framework options
    selectionMethod: SelectionMethod = SelectionMethod.MRMR
    relevancyMetrics: List[SelectionMetric] = [SelectionMetric.F_TEST]
    redundancyMetric: SelectionMetric = SelectionMetric.PEARSON
    relevancyAggregation: Aggregation = Aggregation.MEAN
    redundancyAggregation: Aggregation = Aggregation.MEAN

    # specific options
    importanceOptions: ImportanceOptions = ImportanceOptions()
    importanceFuncs: List[Any] = []
    mrmrOptions: MrmrOptions = MrmrOptions()
    qpfsOptions: QpfsOptions = QpfsOptions()
    filterOptions: FilterOptions = FilterOptions()


# ──────────────────────────────────────────────────────────────────────────── #
#                       Feature Generation Options Data                        #
# ──────────────────────────────────────────────────────────────────────────── #


class FeatureGenerationOptions(BaseModel):
    """This model describes the options for the feature generation method"""

    enable: bool = True
    noOfNewFeatures: int = Field(default=20, example=20, ge=1, le=50)
    unaryOps: List[UnaryOpLiteral] = list(UnaryOpLiteral)
    binaryOps: List[BinaryOpLiteral] = list(BinaryOpLiteral)
    epochs: int = Field(default=5, example=5, ge=1, le=10)


# ──────────────────────────────────────────────────────────────────────────── #
#                       Dimensionality Reduction Options                       #
# ──────────────────────────────────────────────────────────────────────────── #


class DimensionalityReductionOptions(BaseModel):
    enable: bool = False
    method: DimReduction = DimReduction.SVD
    noOfComponents: int = 100


# ──────────────────────────────────────────────────────────────────────────── #
#                                Config Data                                   #
# ──────────────────────────────────────────────────────────────────────────── #


def check_text_encoding_for_non_nlp_models(values: Dict[str, Any]) -> Dict[str, Any]:
    """Checks that the text encoding option is not GenericOptions.NONE and overrides it with GenericOptions.AUTO if so
    while logging a warning. This is for validating text encoding options when non-nlp models are used."""
    for transformation in values.get("transformationOptions", []):
        if transformation.detectedType != DetectedType.text:
            continue
        for feature_override in transformation.featureOverrides:
            slug = feature_override.encoderSlugs[0]
            if feature_override.filter != Filter.DROP and slug.slugValue[0] == GenericOption.NONE:
                slug.slugValue[0] = GenericOption.AUTO
                logger.warning(
                    "All text columns must be encoded by the preprocessor in order to use non-transformer "
                    "based ML models. The encoders for text columns will be automatically selected."
                )
    return values


def check_text_encoding_for_nlp_models(values: Dict[str, Any]) -> Dict[str, Any]:
    """Checks that the text encoding option is GenericOptions.NONE and overrides it if not while logging a warning. This
    is for validating text encoding options when nlp models are used."""
    for transformation in values.get("transformationOptions", []):
        if transformation.detectedType != DetectedType.text:
            continue
        for feature_override in transformation.featureOverrides:
            slug = feature_override.encoderSlugs[0]
            if feature_override.filter != Filter.DROP and slug.slugValue[0] != GenericOption.NONE:
                slug.slugValue[0] = GenericOption.NONE
                logger.warning(
                    "Text columns must not be encoded by the preprocessor if we are fine-tuning transformer"
                    "models. Text encoding has been turned off."
                )
    return values


def count_features(transformation: TransformationOptions, text_count: int, target_count: int) -> Tuple[int, int]:
    for feature_override in transformation.featureOverrides:
        if feature_override.filter == Filter.DROP:
            continue
        if transformation.detectedType in [DetectedType.text, DetectedType.protein_sequence]:
            text_count += 1
            slug = feature_override.encoderSlugs[0]
            if slug.slugValue[0] not in [GenericOption.NONE, GenericOption.AUTO]:
                raise ValueError(
                    "NLP models can only have text encoders set to None or Auto, please update the encoder options."
                )
            slug.slugValue[0] = GenericOption.NONE
        else:
            target_count += 1
    return text_count, target_count


def validate_feature_counts(text_count: int, target_count: int) -> None:
    # Ensure there's at least one and at most two text fields.
    assert 1 <= text_count <= 2, "NLP models require one or two text columns."
    # Ensure there's exactly one target field.
    assert target_count == 1, "NLP models require one non-text column."


class PreprocessOptions(BaseModel):
    """This model describes the options for the preprocessing method"""

    splittingMethodOptions: SplitMethodOptions = SplitMethodOptions()
    models: List[ModelDefinition] = []
    transformationOptions: List[TransformationOptions] = []
    mlTask: MlTask
    featureSelectionOptions: FeatureSelectionOptions = FeatureSelectionOptions()
    featureGenerationOptions: FeatureGenerationOptions = FeatureGenerationOptions()
    validationMethodOptions: ValidationMethodOptions = ValidationMethodOptions()
    featureDimensionalityReductionOptions: DimensionalityReductionOptions = DimensionalityReductionOptions()

    @validator("models")
    def check_all_models_are_compatible(cls, models: List[ModelDefinition]) -> List[ModelDefinition]:
        """This validator checks that all models are compatible with the ml task"""
        if len(models) > 0:
            val = [model.name.startswith("nlp_") for model in models]
            assert all(val) or not any(val), (
                "All models must be either NLP or non-NLP. Combinations of such models "
                "should be handled in separate trials."
            )
        return models

    @root_validator(allow_reuse=True)
    def check_nlp_trial_compatibility(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        models: List[ModelDefinition] = values.get("models", [])

        # Check if any nlp models
        any_nlp_models = any(model.name.startswith("nlp_") for model in models)

        if not any_nlp_models:
            return check_text_encoding_for_non_nlp_models(values)

        values = check_text_encoding_for_nlp_models(values)

        if "transformationOptions" not in values:
            # This case means that transformationOptions had a validation error
            return values

        text_count, target_count = 0, 0
        for transformation in values.get("transformationOptions", []):
            text_count, target_count = count_features(transformation, text_count, target_count)

        validate_feature_counts(text_count, target_count)

        # Feature Selection and Generation are ignored for NLP datasets
        values["featureSelectionOptions"].enable = False
        values["featureGenerationOptions"].enable = False
        return values


class DatasetConfig(BaseModel):
    """Dataset config with the minimal information needed to load a dataset"""

    encoding: Optional[str] = "utf-8"
    delimiter: Optional[str] = None

    # The index column is accepted as both index or name, but the main code will
    # use the name
    indexColumn: Optional[str] = None
    indexColumnIndex: Optional[int] = None

    labelColumn: str  # needed to load the data (@TODO: shouldn't be)


class PreprocessConfig(PreprocessOptions, DatasetConfig):
    """Main config for the preprocessor merging different models"""

    labelColumn: str

    # Timeseries
    indexColumn: Optional[str] = None
    isTimeseries: bool = False
    # Needed for creating windows in time series regression/classification
    windowSize: Optional[int] = 5
    timeSeriesHorizon: int = 1
    rolling: Optional[List[RollingOperation]] = []
    # Not exposed to frontend
    createTargetLags: bool = True

    # Data cleaning
    original_headers: List[Optional[str]] = []
    cleaned_headers: List[Optional[str]] = []

    # Seed
    seed: int = 41

    @root_validator(allow_reuse=True)
    def forecasting_is_timeseries(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """The forecasting MlTask implies that we're processing a timeseries. To
        avoid inconsistencies in the boolean, we consider `mlTask` more
        reliable, and should overwrite `isTimeseries` when mlTask is forecasting
        """

        ml_task = values["mlTask"]  # mlTask is required
        if ml_task == MlTask.forecasting:
            values["isTimeseries"] = True  # previous value does not matter

        return values


# ──────────────────────────────────────────────────────────────────────────── #
#                                Column Data                                   #
# ──────────────────────────────────────────────────────────────────────────── #


class QuickColumnInfo(BaseModel):
    # used in quick mode of type detector
    columnIndex: int = Field(..., example=7)
    name: str = Field(..., example="column 7")
    baseType: BaseTypes = Field(..., example="string")


class BaseColumnInfo(QuickColumnInfo):
    # Core components of the column info, all required
    # -> Intermediate level
    detectedType: DetectedType = Field(..., example="integer")
    confidenceScore: float = 0
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="information to be used by the preprocessor")


class GenericColumnStatistics(BaseModel):
    statsUniqueValuesRatio: float = 0
    statsUniqueValuesCount: int = 0
    statsMissingValuesRatio: float = 0
    statsMissingValuesCount: int = 0
    statsValuesCount: int = 0


class ColumnInfo(BaseColumnInfo, GenericColumnStatistics):
    """Model gathering all information and statistics about a single column of
    a dataset, generated using the dataset analysis step.
    This model is used to register a column's info in the database.
    """

    # More advanced components, all optionals and/or empty default values
    defaultTrialOptions: Optional[ColumnDefaultTrialOptions] = None
    statistics: List[ColumnStatistics] = []
    tags: List[ColumnTag] = []
    anomalies: Optional[ColumnAnomalies] = None
    isDeleted: bool = False


class ColumnInfoList(BaseModel):
    """Model gathering all information and statistics about a dataset, generated"""

    __root__: List[ColumnInfo]


class ColumnOptions(BaseModel):
    """Model gathering all options for a single column of a dataset, generated"""

    encoder: Union[AllEncoders, List[AllEncoders], None] = [GenericOption.AUTO]
    scaler: Union[AllScalers, List[AllScalers], None] = [GenericOption.NONE]
    imputeStrategy: ImputeStrategy = ImputeStrategy.AUTO
    imputeValue: Optional[ImputeValue] = None
    rolling: Optional[List[RollingOperation]] = None
    derivedColumns: Optional[List[DateOptions]] = None


class ConfigOptions(BaseModel):
    """Reconfigure config options so they are in a structure more usable by the preprocessor"""

    ignored_features: List[int] = []
    required_features: List[int] = []
    future_covariates_indices: List[int] = []
    transformation_options: Dict[int, ColumnOptions] = {}


# ──────────────────────────────────────────────────────────────────────────── #
#                        Parallelization Configuration                         #
# ──────────────────────────────────────────────────────────────────────────── #
class ParallelisationOptions(BaseSettings):
    """
    Used to access the PREPROCESS_THREADS environment variable to consistently
    control the behaviour of joblib parallelization in the code.
    """

    threads: int = int(cpu_count() * 0.5)

    class Config(BaseSettings.Config):
        env_prefix = "preprocess_"


__all__ = [
    "Slug",
    "Impute",
    "FeatureOverrides",
    "TransformationOptions",
    "InputParameter",
    "ImputeValue",
    "ModelParameter",
    "ModelDefinition",
    "SplitMethod",
    "SplitMethodOptions",
    "ValidationMethod",
    "CrossValidationOptions",
    "HoldoutOptions",
    "ValidationMethodOptions",
    "FeatureSelectionOptions",
    "FeatureGenerationOptions",
    "PreprocessOptions",
    "DatasetConfig",
    "PreprocessConfig",
    "QuickColumnInfo",
    "BaseColumnInfo",
    "GenericColumnStatistics",
    "ColumnInfo",
    "ColumnInfoList",
    "ColumnOptions",
    "ParallelisationOptions",
    "FeatureSelectionOptions",
    "ImportanceOptions",
    "MrmrOptions",
    "FilterOptions",
    "ConfigOptions",
]
