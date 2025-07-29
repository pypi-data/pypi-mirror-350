from typing import Iterator, List

from evoml_preprocessor.preprocess.generator.builder import FeatureBuilder
from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.operations import BinaryOp, UnaryOp
from evoml_preprocessor.preprocess.generator.util import FeatureBuilderType


class GrowAllFeatureBuilder(FeatureBuilder):
    """Generate features by getting all combinations of features and operations."""

    @property
    def type(self) -> FeatureBuilderType:
        return FeatureBuilderType.GROW_ALL

    def build(self, features: List[GeneratedFeatureNode]) -> Iterator[GeneratedFeatureNode]:
        """Brute force approach to generating new features.

        Generates features from each feature by appending each possible unary
        operator. Generates features from each pair of features, by appending
        each possible binary operator, thus connecting each pair of features
        by their roots to the new operator.

        Args:
            features: Features to generate new features from.

        Returns:
            Iterator of generated features
        """
        for op in self.unary_ops + self.binary_ops:
            if isinstance(op, UnaryOp):
                for feature in features:
                    yield GeneratedFeatureNode.from_operation(op, [feature])
            elif isinstance(op, BinaryOp):
                for i, feature in enumerate(features[:-1]):
                    for other_feature in features[i + 1 :]:
                        yield GeneratedFeatureNode.from_operation(op, [feature, other_feature])
            else:
                raise ValueError(f"Unknown operation {op}")
