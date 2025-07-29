from __future__ import annotations

from typing import Iterator, List

from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.operations import BinaryOp, UnaryOp
from evoml_preprocessor.preprocess.generator.util import FeatureBuilderParameters, FeatureBuilderType


class FeatureBuilder:
    """'abstract' base class for building new features

    Defines a set of methods that all builders must have:
    - `type`: the builder type is used in certain checks
    - `build`: generates a set of new features from a set of features
    """

    unary_ops: List[UnaryOp]
    binary_ops: List[BinaryOp]

    def __init__(self, parameters: FeatureBuilderParameters) -> None:
        if parameters.unary_ops is None:
            self.unary_ops = list(UnaryOp)
        else:
            self.unary_ops = parameters.unary_ops

        if parameters.binary_ops is None:
            self.binary_ops = list(BinaryOp)
        else:
            self.binary_ops = parameters.binary_ops
        self.rng = parameters.rng

    @property
    def type(self) -> FeatureBuilderType:
        raise NotImplementedError("Not implemented")

    def build(self, features: List[GeneratedFeatureNode]) -> Iterator[GeneratedFeatureNode]:
        raise NotImplementedError("Not implemented")
