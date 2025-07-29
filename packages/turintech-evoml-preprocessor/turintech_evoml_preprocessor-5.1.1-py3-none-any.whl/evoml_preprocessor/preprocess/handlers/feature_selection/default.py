# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Dict, Optional, Tuple

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.feature_selection._base import FeatureSelectionHandler
from evoml_preprocessor.preprocess.handlers.feature_selection.config import FeatureSelectionConfig
from evoml_preprocessor.preprocess.selector.selector_chain import SelectorChain
from evoml_preprocessor.preprocess.selector.util import calculate_number_features
from evoml_preprocessor.utils.sample import get_sample

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class DefaultFeatureSelectionHandler(FeatureSelectionHandler):
    """Handles the default algorithm for feature selection (for non-timeseries
    tasks)
    """

    # @TODO: it seems that a lot of the functionalities here are report-related.
    # The best way to implement that is probably to add common methods for
    # reporting, to ensure consistency in the reports between the different
    # implementations (default & timeseries for now)

    def __init__(self, config: FeatureSelectionConfig):
        super().__init__(config)

    def fit_transform_report(
        self, data: pd.DataFrame, encoded_label: pd.Series
    ) -> Tuple[pd.DataFrame, Optional[Dict[str, float]]]:
        """Fit the feature selector and return the transformed data and the"""

        if self.is_timeseries or not self.options.enable or data.shape[1] <= 1:
            # Early exit conditions (skipping feature selection altogether)
            transformed_data = data
        else:
            transformed_data = self.fit_transform(data, encoded_label)

        scores: Optional[Dict[str, float]] = None

        if self.feature_selector is not None:
            scores = self.feature_selector.selectors[-1].scores.combined.to_dict()

        # Save the final scores
        return transformed_data, scores

    def _feature_selection(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        self.original_columns = set(data.columns)
        self.feature_selector = SelectorChain.from_selection_options(
            ml_task=self.ml_task, selection_options=self.options
        )
        logger.info(" Feature Selection ".center(60, "-"))

        nfeatures_to_select = (
            self.options.noOfFeatures
            if self.options.noOfFeatures is not None
            else calculate_number_features(data.shape[1])
        )

        # Perform sampling if the data is large, fit on the sample
        sample_size = 100_000
        if data.shape[0] > sample_size:
            sampled_index = get_sample(label_column=encoded_label, sample_size=sample_size, task=self.ml_task)
            self.feature_selector.fit(data.loc[sampled_index], encoded_label.loc[sampled_index], nfeatures_to_select)
        else:
            self.feature_selector.fit(data, encoded_label, nfeatures_to_select)

        self.feature_selector.transform(data, inplace=True)

        return data
