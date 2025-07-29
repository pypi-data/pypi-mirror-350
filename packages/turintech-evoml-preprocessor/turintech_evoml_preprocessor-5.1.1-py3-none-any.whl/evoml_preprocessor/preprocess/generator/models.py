from __future__ import annotations
from typing import List, Dict
import re
from pydantic import BaseModel, PrivateAttr


class FeatureFormula(BaseModel):
    """Report describing the feature formula"""

    # Fields
    formula: str
    functions: List[str]
    features: List[str]

    # Private attributes (not to serialize)
    _remapped_formula: str = PrivateAttr()
    _feature_mapping: Dict[str, str] = PrivateAttr()  # feat1, feat2 ... feat30

    def __init__(self, formula: str, features: List[str], functions: List[str]):
        # Dataclasses can be instantiated with positional arguments, but not
        # pydantic models. This temporary code makes this pydantic model behave
        # like a dataclass while waiting for a move to python 3.8 AST in code
        # generation
        super().__init__(formula=formula, features=features, functions=functions)
        # sort the features and functions to make sure that the order is always the same
        self.features.sort()
        # map the features to feat1, feat2 ... feat30
        self._feature_mapping = {elem: f"feat{idx}" for idx, elem in enumerate(self.features)}

    @property
    def get_mapped_formula(self) -> str:
        pattern = re.compile("|".join(re.escape(key) for key in self._feature_mapping.keys()))
        self._remapped_formula = pattern.sub(lambda x: self._feature_mapping[x.group()], self.formula)
        return self._remapped_formula

    def get_remapped_formula(self, formula: str) -> str:
        reverse_dict = {value: key for key, value in self._feature_mapping.items()}
        pattern = re.compile("|".join(re.escape(value) for value in reverse_dict.keys()))
        return pattern.sub(lambda x: reverse_dict[x.group()], formula)


class GeneratedFeature(BaseModel):
    """The generated feature."""

    generatedFeatureName: str
    formula: str
    ast: str
    featuresUsed: List[str]
    basicFunctions: List[str]
    correlationWithTarget: float

    def __repr__(self) -> str:
        return f"<{self.generatedFeatureName} - {self.formula}>"

    @classmethod
    def from_feature_formula(
        cls,
        simplified_formula: str,
        formula: FeatureFormula,
        generated_feature_name: str,
        ast: str,
        correlation_with_target: float,
    ) -> GeneratedFeature:
        return GeneratedFeature(
            generatedFeatureName=generated_feature_name,
            formula=simplified_formula,
            ast=ast,
            featuresUsed=list(formula.features),
            basicFunctions=list(formula.functions),
            correlationWithTarget=correlation_with_target,
        )


class FeatureGenerationReport(BaseModel):
    """Report describing the choices made during the feature generation process"""

    featuresGenerated: List[GeneratedFeature] = []
    totalOriginalColumns: int = 0
