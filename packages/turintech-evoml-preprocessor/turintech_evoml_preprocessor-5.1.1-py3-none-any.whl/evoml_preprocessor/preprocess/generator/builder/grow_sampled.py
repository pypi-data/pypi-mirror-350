from typing import Iterator, List

from evoml_preprocessor.preprocess.generator.builder import FeatureBuilder
from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.operations import BinaryOp, UnaryOp
from evoml_preprocessor.preprocess.generator.util import FeatureBuilderType


class GrowSampledFeatureBuilder(FeatureBuilder):
    """Generate features by getting all combinations of features and operations."""

    @property
    def type(self) -> FeatureBuilderType:
        return FeatureBuilderType.GROW_SAMPLED

    def build(self, features: List[GeneratedFeatureNode]) -> Iterator[GeneratedFeatureNode]:
        """Sampled approach of generating new features.

        Generates features from each feature by appending a random subset of
        unary operators. Generates features from each pair of features, by
        appending a random subset each possible binary operator, thus connecting
        each pair of features by their roots to the new operator.

        Args:
            features: Features to generate new features from.

        Returns:
            Iterator of generated features
        """
        n_target = 100
        n_total = len(features) * len(self.unary_ops) + len(features) * (len(features) - 1) // 2 * len(self.binary_ops)
        p_skip = 0.0 if n_total < n_target else 1 - (n_target / n_total) ** 0.5
        for op in self.unary_ops + self.binary_ops:
            if isinstance(op, UnaryOp):
                for feature in features:
                    rand = self.rng.random()
                    if rand > p_skip:
                        yield GeneratedFeatureNode.from_operation(op, [feature])
            elif isinstance(op, BinaryOp):
                for i, feature in enumerate(features[:-1]):
                    for other_feature in features[i + 1 :]:
                        if self.rng.random() > p_skip:
                            yield GeneratedFeatureNode.from_operation(op, [feature, other_feature])
            else:
                raise ValueError(f"Unknown operation {op}")
