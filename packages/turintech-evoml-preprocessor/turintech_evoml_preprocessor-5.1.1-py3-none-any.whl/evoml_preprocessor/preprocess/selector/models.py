# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Dict, List, Optional

# Dependencies
from pydantic import BaseModel

# Module
from evoml_preprocessor.preprocess.models import Aggregation, ModelOption

# Private Dependencies


# ──────────────────────────────────────────────────────────────────────────── #


class SelectionScoresReport(BaseModel):
    # @TODO we might want to combine multiple relevancy / redundancy scores

    relevancy: Optional[List[float]] = None
    redundancy: Optional[List[List[float]]] = None
    redundancy_agg: Optional[List[float]] = None
    combined: Optional[List[float]] = None
    index: Optional[List[str]] = None

    class Config:
        arbitrary_types_allowed = True


class MetricReport(BaseModel):
    """Report describing the metric choices made during the feature selection process"""

    name: str = ""
    draw: bool = False
    scores: Dict[str, float] = {}
    wrapper_model: Optional[ModelOption] = None


class SelectionMethodReport(BaseModel):
    """Report describing the selection method used during the feature selection process

    TODO: the redundancyMetricReport is currently deprecated, but we might want to add it back in
    """

    # necessary
    method: str = ""
    nColumnsTarget: Optional[int] = None
    nColumnsSelected: int = 0
    nColumnsRemoved: int = 0
    featuresSelected: List[str] = []
    featuresRemoved: List[str] = []
    finalScores: Dict[str, float] = {}

    # optional
    relevancyMetricReports: List[MetricReport] = []
    relevancyAggregation: Optional[Aggregation] = None
    redundancyMetricReport: Optional[MetricReport] = None
    redundancyAggregation: Optional[Aggregation] = None


class FeatureSelectionReport(BaseModel):
    """Report describing the choices made during the feature selection process"""

    featuresOriginal: List[str] = []
    featuresSelected: List[str] = []
    selectionMethods: List[SelectionMethodReport] = []

    @property
    def noOriginalColumns(self) -> int:
        return len(self.featuresOriginal)

    @property
    def noSelectedColumns(self) -> int:
        return len(self.featuresSelected)
