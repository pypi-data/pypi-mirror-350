from typing import Dict, Type

from evoml_preprocessor.preprocess.models.enum import SelectorType
from evoml_preprocessor.preprocess.selector.util import SelectorParameters

from ._base import Selector, SelectorScores
from .linear import LinearSelector
from .mrmr import MrmrSelector
from .qpfs import QPFSelector
from .random import RandomSelector
from .redundance import RedundanceSelector
from .relevance import RelevanceSelector
from .unary import UnarySelector


def build_selector(selector_type: SelectorType, parameters: SelectorParameters) -> Selector:
    """Get the selector class for a given selector type

    Args:
        selector_type (SelectorType): The selector type
        parameters (SelectorParameters): The selector parameters

    Returns:
        Type[Selector]: The selector class
    """
    selector: Dict[SelectorType, Type[Selector]] = {
        SelectorType.LINEAR: LinearSelector,
        SelectorType.MRMR: MrmrSelector,
        SelectorType.QPFS: QPFSelector,
        SelectorType.RANDOM: RandomSelector,
        SelectorType.REDUNDANCE: RedundanceSelector,
        SelectorType.RELEVANCE: RelevanceSelector,
        SelectorType.UNARY: UnarySelector,
    }
    return selector[selector_type](parameters)


__all__ = [
    "SelectorScores",
    "Selector",
    "MrmrSelector",
    "QPFSelector",
    "LinearSelector",
    "RandomSelector",
    "RelevanceSelector",
    "RedundanceSelector",
    "UnarySelector",
    "build_selector",
]
