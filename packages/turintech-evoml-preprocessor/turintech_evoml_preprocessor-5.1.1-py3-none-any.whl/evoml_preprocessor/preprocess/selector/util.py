from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.models import (
    Aggregation,
    FeatureSelectionOptions,
    ImportanceOptions,
    ModelOption,
    SelectionMethod,
    SelectionMetric,
)
from evoml_preprocessor.preprocess.models.enum import SelectorType
from evoml_preprocessor.utils.string_enum import StrEnum

FLOOR = 0.001


class MetricType(StrEnum):
    FILTER = "filter"
    WRAPPER = "wrapper"
    HYBRID = "hybrid"
    NONE = "none"


@dataclass
class MetricParameters:
    metric: SelectionMetric = SelectionMetric.NONE
    model: Optional[ModelOption] = None
    ml_task: Optional[MlTask] = None
    rng: np.random.Generator = np.random.default_rng(42)
    subsample: Optional[int] = None
    n_subsamples: Optional[int] = None
    sample_with_replacement: bool = False

    @classmethod
    def from_selector(cls, ml_task: MlTask, metric: SelectionMetric) -> "MetricParameters":
        return cls(
            ml_task=ml_task,
            metric=metric,
        )

    @classmethod
    def from_importance_selector(
        cls, ml_task: MlTask, model: ModelOption, importance_options: ImportanceOptions
    ) -> "MetricParameters":
        return cls(
            ml_task=ml_task,
            model=model,
            subsample=importance_options.subsample,
            n_subsamples=importance_options.nEstimators,
            sample_with_replacement=importance_options.sampleWithReplacement,
        )


@dataclass
class SingleSelectionMetric:
    metric: SelectionMetric
    parameters: MetricParameters

    @classmethod
    def from_selector(cls, ml_task: MlTask, metric: SelectionMetric) -> "SingleSelectionMetric":
        return cls(
            metric=metric,
            parameters=MetricParameters.from_selector(ml_task, metric),
        )

    @classmethod
    def from_importance_selector(
        cls, ml_task: MlTask, model: ModelOption, importance_options: Optional[ImportanceOptions] = None
    ) -> "SingleSelectionMetric":
        if importance_options is None:
            importance_options = ImportanceOptions()
        return cls(
            metric=SelectionMetric.FEATURE_IMPORTANCE,
            parameters=MetricParameters.from_importance_selector(ml_task, model, importance_options),
        )


@dataclass
class SelectorParameters:
    relevancy: Optional[List[SingleSelectionMetric]] = None
    redundancy: Optional[SingleSelectionMetric] = None
    relevancy_aggregation: Aggregation = Aggregation.MEAN
    redundancy_aggregation: Aggregation = Aggregation.MEAN
    redundancy_weight: float = 1.0
    linear: bool = False
    parallel: bool = False
    nystrom: Literal["auto", "yes", "no"] = "auto"

    @classmethod
    def from_selection_options(cls, ml_task: MlTask, options: FeatureSelectionOptions) -> SelectorParameters:
        relevancy = [
            SingleSelectionMetric.from_selector(ml_task, metric)
            for metric in options.relevancyMetrics
            if metric != SelectionMetric.FEATURE_IMPORTANCE
        ]
        if SelectionMetric.FEATURE_IMPORTANCE in options.relevancyMetrics:
            relevancy.extend(
                [
                    SingleSelectionMetric.from_importance_selector(ml_task, model, options.importanceOptions)
                    for model in options.importanceOptions.modelOptions
                ]
            )
        return cls(
            relevancy=relevancy,
            redundancy=SingleSelectionMetric.from_selector(ml_task, options.redundancyMetric),
            relevancy_aggregation=options.relevancyAggregation,
            redundancy_aggregation=options.redundancyAggregation,
            redundancy_weight=options.filterOptions.redundancyWeight,
            linear=options.mrmrOptions.linear,
            nystrom=options.qpfsOptions.nystrom,
        )

    @classmethod
    def from_importance_options(cls, ml_task: MlTask, options: ImportanceOptions) -> SelectorParameters:
        return cls(
            relevancy=[
                SingleSelectionMetric.from_importance_selector(ml_task, model, options)
                for model in options.modelOptions
            ],
            redundancy=SingleSelectionMetric.from_selector(ml_task, SelectionMetric.NONE),
            relevancy_aggregation=options.importanceAggregation,
            redundancy_aggregation=Aggregation.MEAN,
        )


@dataclass
class SelectorChainStep:
    selector: SelectorType
    weight: float
    parameters: SelectorParameters


@dataclass
class SelectorChainParameters:
    steps: List[SelectorChainStep]

    @classmethod
    def from_selection_options(cls, ml_task: MlTask, options: FeatureSelectionOptions) -> SelectorChainParameters:
        unary_step = SelectorChainStep(
            SelectorType.UNARY, 1.0, SelectorParameters.from_selection_options(ml_task, options)
        )

        # all presets from user selection
        if options.selectionMethod == SelectionMethod.FILTER:
            if options.redundancyMetric is SelectionMetric.NONE:
                if options.relevancyMetrics <= {SelectionMetric.NONE}:
                    return cls(
                        steps=[
                            unary_step,
                        ]
                    )
                return cls(
                    steps=[
                        unary_step,
                        SelectorChainStep(
                            SelectorType.RELEVANCE, 1.0, SelectorParameters.from_selection_options(ml_task, options)
                        ),
                    ]
                )
            elif set(options.relevancyMetrics) <= {SelectionMetric.NONE}:
                return cls(
                    steps=[
                        unary_step,
                        SelectorChainStep(
                            SelectorType.REDUNDANCE, 1.0, SelectorParameters.from_selection_options(ml_task, options)
                        ),
                    ]
                )
            elif options.filterOptions.redundanceFirst:
                w = options.filterOptions.redundancyWeight
                return cls(
                    steps=[
                        unary_step,
                        SelectorChainStep(
                            SelectorType.REDUNDANCE, w, SelectorParameters.from_selection_options(ml_task, options)
                        ),
                        SelectorChainStep(
                            SelectorType.RELEVANCE, 1.0 - w, SelectorParameters.from_selection_options(ml_task, options)
                        ),
                    ]
                )
            else:
                w = options.filterOptions.redundancyWeight
                return cls(
                    steps=[
                        unary_step,
                        SelectorChainStep(
                            SelectorType.RELEVANCE, 1.0 - w, SelectorParameters.from_selection_options(ml_task, options)
                        ),
                        SelectorChainStep(
                            SelectorType.REDUNDANCE, w, SelectorParameters.from_selection_options(ml_task, options)
                        ),
                    ]
                )

        if options.selectionMethod == SelectionMethod.MRMR:
            return cls(
                steps=[
                    unary_step,
                    SelectorChainStep(
                        SelectorType.MRMR, 1.0, SelectorParameters.from_selection_options(ml_task, options)
                    ),
                ]
            )
        if options.selectionMethod == SelectionMethod.LINEAR:
            return cls(
                steps=[
                    unary_step,
                    SelectorChainStep(
                        SelectorType.LINEAR, 1.0, SelectorParameters.from_selection_options(ml_task, options)
                    ),
                ]
            )
        if options.selectionMethod == SelectionMethod.RANDOM:
            return cls(
                steps=[
                    unary_step,
                    SelectorChainStep(
                        SelectorType.RANDOM, 1.0, SelectorParameters.from_selection_options(ml_task, options)
                    ),
                ]
            )
        if options.selectionMethod == SelectionMethod.MRMR_IMPORTANCE:
            w = options.mrmrOptions.importanceWeight
            return cls(
                steps=[
                    unary_step,
                    SelectorChainStep(
                        SelectorType.MRMR, 1.0 - w, SelectorParameters.from_selection_options(ml_task, options)
                    ),
                    SelectorChainStep(
                        SelectorType.RELEVANCE,
                        w,
                        SelectorParameters.from_importance_options(ml_task, options.importanceOptions),
                    ),
                ]
            )
        if options.selectionMethod == SelectionMethod.QPFS:
            return cls(
                steps=[
                    unary_step,
                    SelectorChainStep(
                        SelectorType.QPFS, 1.0, SelectorParameters.from_selection_options(ml_task, options)
                    ),
                ]
            )

        raise NotImplementedError


def aggregate(df: pd.DataFrame, mode: Aggregation) -> pd.Series:
    """Aggregate the relevance of the columns in the dataframe.
    Args:
        df (pd.DataFrame):
            The dataframe.
        mode (Aggregation):
            The aggregation mode.
    Returns:
        pd.Series:
            The aggregated relevance.
    """

    if mode == Aggregation.MEAN:
        return df.mean(axis=1)
    if mode == Aggregation.MAX:
        return df.max(axis=1)
    if mode == Aggregation.RANK:
        return (df.max(axis=0) * df.rank(axis=0)).mean(axis=1)
    raise NotImplementedError


def minmax_series(series: pd.Series) -> pd.Series:
    if series.min() == series.max():
        return pd.Series(1.0, index=series.index)
    return (series - series.min()) / (series.max() - series.min())


def calculate_number_features(total_number_feature: int, threshold: int = 40) -> int:
    """
    Calculates the number of features to select based on the number of features
    in the dataset. The function returns the minimum of n_features and a
    square root scaling function tuned to pass through the specified threshold.

    Args:
        total_number_feature (int):
            The number of features being fed into feature selection.
        threshold (int, optional):
            The feature value at which the square root function equals the threshold. Default is 40.

    Returns:
        int:
            The target number of features to generate from mrmr.
    """
    if total_number_feature <= threshold:
        return total_number_feature
    # Square root scaling tuned to pass through the threshold
    sqrt_scale = threshold * math.sqrt(total_number_feature / threshold)
    return min(total_number_feature, round(sqrt_scale))
