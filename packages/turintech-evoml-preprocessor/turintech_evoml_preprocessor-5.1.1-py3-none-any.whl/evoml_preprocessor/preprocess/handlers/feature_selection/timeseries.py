# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from typing import Dict, Optional, Tuple

import numpy as np

# Dependencies
import pandas as pd

# Module
from evoml_preprocessor.preprocess.handlers.feature_selection._base import FeatureSelectionHandler
from evoml_preprocessor.preprocess.handlers.feature_selection.config import FeatureSelectionConfig
from evoml_preprocessor.preprocess.models import (
    FeatureSelectionOptions,
    SelectionMethod,
    SelectionMetric,
)
from evoml_preprocessor.preprocess.selector.selector_chain import SelectorChain
from evoml_preprocessor.preprocess.selector.util import calculate_number_features
from evoml_preprocessor.utils.sample import get_sample

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #

# The correlation after which we consider a variable as a potential
# data leakage and exclude it from feature selection.
# And for two features to be considered multicorrelated.
CORRELATION_THRESHOLD = 0.99


class TimeseriesFeatureSelectionHandler(FeatureSelectionHandler):
    """The feature selection handler for timeseries data.

    This handler is responsible for handling the feature selection process
    for timeseries data.

    It uses the QPFS algorithm to select the features. Please note that QPFS
    requires some additional preparation to ensure the stability of the results.
    For instance, we have to make sure that highly correlated features are not
    included in the feature selection process (> 0.99 pearson correlation).

    """

    def __init__(self, config: FeatureSelectionConfig):
        super().__init__(config)

    def fit_transform_report(
        self, data: pd.DataFrame, encoded_label: pd.Series
    ) -> Tuple[pd.DataFrame, Optional[Dict[str, float]]]:

        if not self.options.enable or data.shape[1] <= 1:
            # Early exit conditions (skipping feature selection altogether)
            transformed_data = data
        else:
            transformed_data = self.fit_transform(data, encoded_label.loc[data.index])

        scores: Optional[Dict[str, float]] = None

        if self.feature_selector is not None:
            scores = self.feature_selector.selectors[-1].scores.combined.to_dict()

        # Save the final scores
        return transformed_data, scores

    def _feature_selection(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:

        # ------------------------- QPFS preparation ------------------------- #

        # QPFS breaks with data containing perfect correlation between features
        # or between features and target.

        # Unary columns will be dropped during the first step of the feature selection SelectorChain.

        # save columns with abs correlation > 0.99
        corr_matrix = data.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop_features = [column for column in upper.columns if any(upper[column] > CORRELATION_THRESHOLD)]

        # save columns with abs correlation with target > 0.99
        corr_vector = data.corrwith(encoded_label).abs()
        to_drop_with_target = corr_vector[corr_vector > CORRELATION_THRESHOLD].index.tolist()

        # drop columns with abs correlation > 0.99 or with abs correlation with target > 0.99
        data_to_drop = data[to_drop_features + to_drop_with_target]
        data = data.drop(data_to_drop.columns, axis=1)

        if data.shape[1] == 0:
            logger.warning("Skipping feature selection as all the remaining columns are perfectly correlated.")
            return data_to_drop

        # -------------------------- QPFS selection -------------------------- #

        self.options = FeatureSelectionOptions(
            relevancyMetrics=[SelectionMetric.PEARSON],
            selectionMethod=SelectionMethod.QPFS,
        )
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
        if data.shape[0] > 100_000:
            sample_size = max(100_000, int(data.shape[0] * 0.1))
            sampled_index = get_sample(encoded_label, sample_size, self.ml_task)
            sample_x = data.loc[sampled_index]
            sample_y = encoded_label.loc[sampled_index]

            self.feature_selector.fit(sample_x, sample_y, nfeatures_to_select)
        else:
            self.feature_selector.fit(data, encoded_label, nfeatures_to_select)

        self.feature_selector.transform(data, inplace=True)

        return data
