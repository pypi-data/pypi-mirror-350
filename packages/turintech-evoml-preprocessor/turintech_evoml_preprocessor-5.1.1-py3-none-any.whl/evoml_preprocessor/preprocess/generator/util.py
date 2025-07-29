from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.operations import BinaryOp, UnaryOp
from evoml_preprocessor.preprocess.models import FeatureGenerationOptions
from evoml_preprocessor.utils.string_enum import StrEnum


class FeatureBuilderType(StrEnum):
    GROW_ALL = "grow_all"
    GROW_SAMPLED = "grow_sampled"
    GENETIC = "genetic"
    POLYNOMIAL = "polynomial"


class FeatureScorerType(StrEnum):
    MRMR = "mrmr"
    MRMR_FAST = "mrmr_fast"
    LASSO = "lasso"
    LIGHTGBM = "lightgbm"
    QPFS = "qpfs"


@dataclass
class FeatureBuilderParameters:
    unary_ops: List[UnaryOp]
    binary_ops: List[BinaryOp]
    rng: np.random.Generator = np.random.default_rng(42)
    polynomial_order: int = 2


@dataclass
class GeneratorParameters:
    ml_task: MlTask
    rng: np.random.Generator = np.random.default_rng(42)
    batch_size: int = 100
    n_epochs: int = 5
    n_new_features: int = 5
    builder_type: FeatureBuilderType = FeatureBuilderType.GROW_ALL
    builder_parameters: FeatureBuilderParameters = field(default_factory=lambda: FeatureBuilderParameters)
    scorer_type: FeatureScorerType = FeatureScorerType.LASSO

    @classmethod
    def from_generation_options(cls, ml_task: MlTask, options: FeatureGenerationOptions) -> GeneratorParameters:
        parameters = cls(
            ml_task=ml_task,
            n_epochs=options.epochs,
            n_new_features=options.noOfNewFeatures,
        )
        if options.unaryOps is not None:
            parameters.builder_parameters.unary_ops = [UnaryOp.from_literal(op) for op in options.unaryOps]
        if options.binaryOps is not None:
            parameters.builder_parameters.binary_ops = [BinaryOp.from_literal(op) for op in options.binaryOps]
        return parameters


def is_invalid_feature(feature: GeneratedFeatureNode) -> bool:
    return True if feature.values is None else is_invalid(feature.values)


def is_invalid(values: pd.Series[float]) -> bool:
    # @TODO: should we have a function performing a check (is_xxx) mutate its
    # input?
    # @TODO: could use a docstring explaining what it means to be invalid for
    # the current context.
    values.replace([np.inf, -np.inf], np.nan, inplace=True)
    return values.isnull().any() or values.nunique(dropna=False) == 1
