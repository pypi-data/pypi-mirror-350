from typing import Iterable, Iterator, List, Set, Tuple, Union

import numpy as np

from evoml_preprocessor.preprocess.generator.builder import FeatureBuilder
from evoml_preprocessor.preprocess.generator.node import GeneratedFeatureNode
from evoml_preprocessor.preprocess.generator.operations import BinaryOp, UnaryOp
from evoml_preprocessor.preprocess.generator.util import FeatureBuilderType


class GeneticFeatureBuilder(FeatureBuilder):
    @property
    def type(self) -> FeatureBuilderType:
        return FeatureBuilderType.GENETIC

    def random_tree(self, primitives: Set[GeneratedFeatureNode], depth: int = 1) -> GeneratedFeatureNode:
        if depth < 1:
            # mutate into leaf
            new_node: GeneratedFeatureNode = self.rng.choice(list(primitives))  # type: ignore
        else:
            # mutate into operation
            new_node: Union[UnaryOp, BinaryOp] = self.rng.choice(self.unary_ops + self.binary_ops)  # type: ignore

        if isinstance(new_node, GeneratedFeatureNode):
            return new_node
        if isinstance(new_node, UnaryOp):
            return GeneratedFeatureNode.from_operation(new_node, [self.random_tree(primitives, depth - 1)])
        if isinstance(new_node, BinaryOp):
            return GeneratedFeatureNode.from_operation(
                new_node, [self.random_tree(primitives, depth - 1), self.random_tree(primitives, depth - 1)]
            )

        raise ValueError(f"Unknown node type {new_node} ({type(new_node)})")

    def mate_pair(
        self, feature: GeneratedFeatureNode, other_feature_: GeneratedFeatureNode
    ) -> Tuple[GeneratedFeatureNode, GeneratedFeatureNode]:
        new_feature = feature.clone_empty()
        new_other_feature = other_feature_.clone_empty()

        descendants = np.array(new_feature.descendants)
        other_descendants = np.array(new_other_feature.descendants)

        node: GeneratedFeatureNode = self.rng.choice(descendants)
        other_node: GeneratedFeatureNode = self.rng.choice(other_descendants)
        node.parent, other_node.parent = other_node.parent, node.parent
        return new_feature, new_other_feature

    def mutate_feature(
        self, feature: GeneratedFeatureNode, primitives: Set[GeneratedFeatureNode]
    ) -> GeneratedFeatureNode:
        new_feature = feature.clone_empty()

        node: GeneratedFeatureNode
        if new_feature.is_leaf:
            # we've already tried all leaves, so mutate into operation
            node = new_feature
        else:
            node = self.rng.choice(np.array(new_feature.descendants))

        new_node = self.random_tree(primitives, self.rng.integers(2, 3))
        if new_feature.is_leaf:
            return new_node

        node.parent, new_node.parent = new_node.parent, node.parent
        return new_feature

    def build(self, features: List[GeneratedFeatureNode]) -> Iterator[GeneratedFeatureNode]:
        """Builds new features with a genetic programming inspired algorithm

        This builder generates a set of features that scales with the number of
        input features squared. Each feature gets randomly mutated (a part of
        the expression tree is replaced by a randomly generated expression tree).
        Each feature pair gets randomly mated (a part of expression tree `A` is
        swapped with a part of expression tree `B`. Parts are chosen at random.)

        Relies on a tree-based method of expressing generated features.

        Args:
            features: Features to generate new features from.

        Returns:
            Iterator of generated features
        """
        generated_features = []
        primitives = {feature for feature in features if feature.is_leaf}

        # mate each feature with each other feature
        for i, feature in enumerate(features[:-1]):
            for other_feature in features[i + 1 :]:
                if not feature.is_leaf and not other_feature.is_leaf:
                    new_feature, new_other_feature = self.mate_pair(feature, other_feature)
                    generated_features += [new_feature, new_other_feature]

        # mutate each feature once, on average
        chosen_features: Iterable[GeneratedFeatureNode] = self.rng.choice(
            features, size=max(10, len(features))  # type: ignore
        )  # type: ignore
        for feature in chosen_features:
            new_feature = self.mutate_feature(feature, primitives)
            generated_features.append(new_feature)

        return iter(generated_features)
