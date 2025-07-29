from typing import Optional

from evoml_api_models.builder import get_builder  # type: ignore

from evoml_preprocessor.preprocess.generator.models import FeatureGenerationReport, GeneratedFeature


class FeatureGenerationReportBuilder:
    """
    building the feature generator report
    """

    builder: FeatureGenerationReport  # Actually Builder[...]
    built: Optional[FeatureGenerationReport] = None

    @property
    def report(self) -> FeatureGenerationReport:
        # Temporary code being backward compatible while using a builder
        # @TODO: fix when evoml-models #326 is released ans used
        if self.built is None:
            self.built = self.builder.build()  # type: ignore

        return self.built

    def __init__(self) -> None:
        self.builder = get_builder(FeatureGenerationReport)
        self.builder.featuresGenerated = []

    def set_total_original_columns(self, total_original_columns: int) -> None:
        self.builder.totalOriginalColumns = total_original_columns

    def append_generated_feature_info(self, generated_feature_info: GeneratedFeature) -> None:
        self.builder.featuresGenerated.append(generated_feature_info)
