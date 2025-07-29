"""Defines the feature selection's config for FeatureSelectionHandler"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Dict, Any

# Dependencies
from evoml_api_models import MlTask
from pydantic import BaseModel, root_validator

# Module
from evoml_preprocessor.preprocess.models import FeatureSelectionOptions

# ──────────────────────────────────────────────────────────────────────────── #


class FeatureSelectionConfig(BaseModel):
    """Main config for the handler selecting different features."""

    mlTask: MlTask
    isTimeseries: bool = False
    featureSelectionOptions: FeatureSelectionOptions = FeatureSelectionOptions()

    @root_validator(allow_reuse=True)
    def forecasting_is_timeseries(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Overwrite `isTimeseries` when mlTask is forecasting."""

        ml_task = values["mlTask"]
        if ml_task == MlTask.forecasting:
            values["isTimeseries"] = True  # previous value does not matter

        return values
