import pandas as pd

from evoml_preprocessor.preprocess.handlers.post_processing._base import PostProcessingHandler
from evoml_preprocessor.preprocess.models import PreprocessConfig


class TimeseriesPostProcessingHandler(PostProcessingHandler):
    """
    Default dimensionality reduction handler. Does not perform any dimensionality reduction.
    """

    def __init__(self, config: PreprocessConfig):
        super().__init__(config)

    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
