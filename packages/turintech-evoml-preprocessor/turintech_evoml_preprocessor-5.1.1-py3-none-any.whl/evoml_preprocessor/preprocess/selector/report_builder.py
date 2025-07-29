from __future__ import annotations

import pandas as pd
from evoml_api_models.builder import get_builder, Builder

from evoml_preprocessor.preprocess.selector.models import FeatureSelectionReport, SelectionMethodReport


class FeatureSelectionReportBuilder:
    builder: Builder[FeatureSelectionReport]

    @property
    def report(self) -> FeatureSelectionReport:
        # Temporary code being backward compatible while using a builder
        # @TODO: fix when evoml-models #326 is released ans used
        return self.builder.build()  # type: ignore

    def __init__(self) -> None:
        """Creates a FeatureReport object and adds it as an attribute to
        it with all the information related to the feature selection available
        from the beginning.
        @TODO:
            1) add pipeline to replace hardcoded selection steps
            ```
            def add_to_pipeline(self, selection_step: SelectionMethodReport):
                self.builder.selectionPipelineInfo.append(selection_step)
            ```
        Returns:
             feature_report(FeatureReport):
                Object containing feature selection related fields.
        """

        self.builder = get_builder(FeatureSelectionReport)

    def add_original_data(self, columns: pd.Index[str]) -> None:
        """Adds the original data to the report"""
        self.builder.featuresOriginal = list(set(columns))

    def add_selected_data(self, columns: pd.Index[str]) -> None:
        self.builder.featuresSelected = list(set(columns))

    def add_selector(self, info: SelectionMethodReport) -> None:
        self.builder.selectionMethods.append(info)
