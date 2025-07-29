from typing import Dict, Type

import numpy as np
from evoml_api_models import MlTask

from evoml_preprocessor.preprocess.generator.scorer._base import FeatureScorer
from evoml_preprocessor.preprocess.generator.scorer.lasso import LassoScorer
from evoml_preprocessor.preprocess.generator.scorer.lightgbm import LgbmScorer
from evoml_preprocessor.preprocess.generator.scorer.mrmr import MrmrScorer
from evoml_preprocessor.preprocess.generator.scorer.mrmr_fast import MrmrFastScorer
from evoml_preprocessor.preprocess.generator.scorer.qpfs import QpfsScorer
from evoml_preprocessor.preprocess.generator.util import FeatureScorerType


def feature_scorer_factory(scorer_type: FeatureScorerType, ml_task: MlTask, rng: np.random.Generator) -> FeatureScorer:
    """Builds a feature scorer based on the given type."""
    implementation_map: Dict[FeatureScorerType, Type[FeatureScorer]] = {
        FeatureScorerType.MRMR: MrmrScorer,
        FeatureScorerType.MRMR_FAST: MrmrFastScorer,
        FeatureScorerType.LASSO: LassoScorer,
        FeatureScorerType.LIGHTGBM: LgbmScorer,
        FeatureScorerType.QPFS: QpfsScorer,
    }
    scorer_class = implementation_map.get(scorer_type)
    if scorer_class is None:
        raise ValueError(f"Unsupported scorer type: {scorer_type}")
    return scorer_class(ml_task, rng)
