from __future__ import annotations

import logging
from copy import copy
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import anytree
import pandas as pd
import xxhash
from sympy import simplify
from typing_extensions import Self

from evoml_preprocessor.preprocess.generator.models import FeatureFormula
from evoml_preprocessor.preprocess.generator.operations import BinaryOp, UnaryOp
from evoml_preprocessor.utils.exceptions import signal_handler

logger = logging.getLogger("preprocessor")


@dataclass
class GeneratedFeatureNode(anytree.Node):  # type: ignore
    name: str
    values: Optional[pd.Series[float]]
    operation: Union[UnaryOp, BinaryOp, None]
    children: List[Self]

    # Adding typing where the parent class is missing
    @property
    def descendants(self) -> Tuple[Self, ...]:
        # @mypy: we can trust the return type of descendants to match the type
        # of `children`
        return super().descendants  # type: ignore

    # CONSTRUCTORS

    @classmethod
    def from_operation(cls, op: Union[UnaryOp, BinaryOp], features: List[GeneratedFeatureNode]) -> GeneratedFeatureNode:
        # the data should not be generated here because it can be expensive and
        # we want to check whether the feature is already in the cache
        return cls(name=op.name, operation=op, children=[copy(f) for f in features], values=None)

    @classmethod
    def from_feature(cls, feature: pd.Series[float]) -> GeneratedFeatureNode:
        return cls(name=str(feature.name), operation=None, children=[], values=feature)

    # REPRESENTATION

    def __str__(self) -> str:
        return f"{self.formula.formula}"

    def __repr__(self) -> str:  # type: ignore
        return self.preorder

    # COMPARISON

    def __hash__(self) -> int:
        if self.values is None:
            logger.warning("Hashing a node without data")
            return xxhash.xxh128(self.preorder).intdigest()

        np_values = self.values.to_numpy()
        return xxhash.xxh128(np_values.round(4)).intdigest()  # type: ignore

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, GeneratedFeatureNode)
        return hash(self) == hash(other)

    def __len__(self) -> int:
        return len(self.descendants) + 1

    # Define less than operator for comparison during sorting
    def __lt__(self, other: object) -> bool:
        assert isinstance(other, GeneratedFeatureNode)
        return self.name < other.name

    # ──────────────────────────────────────────────────────────────────────── #

    def call_operation(self, column: List[pd.Series[float]]) -> pd.Series[float]:
        """Calls the unary or binary operation of this node with the given
        features. Provides a unified interface to simplify typing.
        """
        assert self.operation is not None
        return self.operation(column)  # type: ignore

    @property
    def preorder(self) -> str:
        return ", ".join([n.name for n in anytree.PreOrderIter(self)])

    def display(self, *formulas: str) -> str:
        """Delegates the display method to the composed operation."""
        if isinstance(self.operation, UnaryOp):
            assert len(formulas) == 1
            # @TODO(mypy): getting `no-any-return` when LSP says this is OK
            return self.operation.display(formulas[0])  # type: ignore

        assert isinstance(self.operation, BinaryOp)
        assert len(formulas) == 2

        return self.operation.display(formulas[0], formulas[1])  # type: ignore

    @property
    def formula(self) -> FeatureFormula:
        features = set()
        functions = set()

        def _traverse(node: GeneratedFeatureNode) -> str:
            if node.operation is None:
                features.add(node.name)
                return node.name
            functions.add(node.name)

            formulas = list(map(_traverse, node.children))

            for i, child in enumerate(node.children):
                if child.operation is not None and node.operation.bracket_child(child.operation, i == 0):
                    formulas[i] = f"({formulas[i]})"

            return node.display(*formulas)

        formula = _traverse(self)
        return FeatureFormula(formula, list(features), list(functions))

    @classmethod
    def get_simplified_formula(cls, formula: str) -> str:
        # call sympy simplify function
        # This function was separated out to allow for easier testing
        # @TODO(mypy): getting `operator` [Module Not Callable] but it's valid
        return str(simplify(expr=formula))  # type: ignore

    @property
    def simplified_formula(self) -> FeatureFormula:
        # timer used to avoid hanging in symp library
        original_formula = self.formula
        try:
            import signal

            signal.signal(signal.SIGALRM, signal_handler)
            signal.setitimer(signal.ITIMER_REAL, 2)

            # Get mapped formula to simplify
            mapped_formula = self.formula.get_mapped_formula

            # Simplify formula using sympy
            simplified_formula = GeneratedFeatureNode.get_simplified_formula(mapped_formula)
            # Disable the signal timer
            signal.setitimer(signal.ITIMER_REAL, 0)
        except Exception:
            # If simplified formula fails, then go back to original method of
            # forming formula
            logger.warning(f"Unable to simplify generates feature formula: {original_formula.formula}")
            return original_formula

        # get remapped formula
        remapped_formula = self.formula.get_remapped_formula(simplified_formula)

        # generate simplified formula model
        return FeatureFormula(remapped_formula, self.formula.features, self.formula.functions)

    @property
    def depth(self) -> int:
        return len(self.ancestors)

    # @pyright: method overrides a parent method which isn't typed, but the type
    # provided here is correct (see NodeMixin in anytree)
    def height(self) -> int:  # type: ignore
        # @TODO: why is the parent implementation not good enough?
        if not self.descendants:
            return 0
        return max(node.height() for node in self.descendants) + 1

    def generate_data(self) -> None:
        if self.values is not None:
            return
        if self.is_leaf:
            raise ValueError("Leaf nodes should have data already")

        for ch in self.children:
            if ch.values is None:
                ch.generate_data()

        self.values = self.operation([ch.values for ch in self.children])  # type: ignore
        self.values.name = self.preorder

    def reset_data(self) -> None:
        if not self.is_leaf:
            self.values = None
            for ch in self.children:
                ch.reset_data()

    def clone_empty(self) -> GeneratedFeatureNode:
        if self.is_leaf:
            return GeneratedFeatureNode(name=self.name, values=self.values, operation=None, children=[])
        return GeneratedFeatureNode(
            name=self.name,
            values=None,
            operation=self.operation,
            children=[ch.clone_empty() for ch in self.children],
        )

    def get_primitives(self) -> int:
        return hash(frozenset({n.name for n in anytree.PreOrderIter(self) if n.is_leaf}))
