from typing import Dict, Type

from evoml_preprocessor.preprocess.generator.builder._base import FeatureBuilder
from evoml_preprocessor.preprocess.generator.builder.genetic import GeneticFeatureBuilder
from evoml_preprocessor.preprocess.generator.builder.grow_all import GrowAllFeatureBuilder
from evoml_preprocessor.preprocess.generator.builder.grow_sampled import GrowSampledFeatureBuilder
from evoml_preprocessor.preprocess.generator.builder.polynomial import PolynomialFeatureBuilder
from evoml_preprocessor.preprocess.generator.util import FeatureBuilderParameters, FeatureBuilderType


def feature_builder_factory(builder_type: FeatureBuilderType, parameters: FeatureBuilderParameters) -> FeatureBuilder:
    """Builds a feature builder based on the given type"""
    implementation_map: Dict[FeatureBuilderType, Type[FeatureBuilder]] = {
        FeatureBuilderType.GROW_ALL: GrowAllFeatureBuilder,
        FeatureBuilderType.GROW_SAMPLED: GrowSampledFeatureBuilder,
        FeatureBuilderType.GENETIC: GeneticFeatureBuilder,
        FeatureBuilderType.POLYNOMIAL: PolynomialFeatureBuilder,
    }

    builder_class = implementation_map.get(builder_type)
    if builder_class is None:
        raise ValueError(f"Unsupported builder type: {builder_type}")
    return builder_class(parameters)
