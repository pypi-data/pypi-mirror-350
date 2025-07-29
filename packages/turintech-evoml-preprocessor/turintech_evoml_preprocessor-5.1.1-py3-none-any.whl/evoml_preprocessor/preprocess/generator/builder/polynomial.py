import itertools
from typing import Iterator, List

from evoml_preprocessor.preprocess.generator.builder import FeatureBuilder
from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.operations import BinaryOp
from evoml_preprocessor.preprocess.generator.util import FeatureBuilderParameters, FeatureBuilderType


def get_polynomial(features: List[GeneratedFeatureNode]) -> GeneratedFeatureNode:
    assert len(features) > 1
    root = features[0]
    for feature in features[1:]:
        root = GeneratedFeatureNode.from_operation(BinaryOp.prod, [root, feature])
    return root


class PolynomialFeatureBuilder(FeatureBuilder):
    def __init__(self, parameters: FeatureBuilderParameters) -> None:
        super().__init__(parameters)
        self.order = parameters.polynomial_order

    @property
    def type(self) -> FeatureBuilderType:
        return FeatureBuilderType.POLYNOMIAL

    def build(self, features: List[GeneratedFeatureNode]) -> Iterator[GeneratedFeatureNode]:
        """Generates polynomials to a given order

        Generates all possible combinations of features from a set of features
        using only the product operator. Note that this should be run with a
        single epoch.

        Args:
            features: Features to generate new features from.

        Returns:
            Iterator of generated features
        """
        for i in range(2, self.order + 1):
            for combination in itertools.product(features, repeat=i):
                yield get_polynomial(list(combination))
