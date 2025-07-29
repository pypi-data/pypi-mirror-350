from abc import ABC, abstractmethod

import pandas as pd

from evoml_preprocessor.preprocess.models import PreprocessConfig


class PostProcessingHandler(ABC):
    def __init__(self, config: PreprocessConfig):
        self.seed = config.seed
        self.dimensionality_reduction_options = config.featureDimensionalityReductionOptions
        self.model = None

    @abstractmethod
    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame: ...

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame: ...
