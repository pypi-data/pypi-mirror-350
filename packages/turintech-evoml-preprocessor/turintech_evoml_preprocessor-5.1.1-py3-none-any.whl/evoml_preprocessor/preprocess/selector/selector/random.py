import pandas as pd

from evoml_preprocessor.preprocess.models import SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import SelectorParameters


class RandomSelector(Selector):
    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self._report = SelectionMethodReport(method=SelectorType.RANDOM)

    @property
    def name(self) -> str:
        return "random"

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int) -> None:
        """Selects feature as random.

        Not designed to be used in production. This is only for testing
        purposes.

        Args:
            X (pd.DataFrame):
                The features
            y (pd.Series):
                The target
            n (int):
                The number of features to select
        """
        self.init_fit(X, y, n)
        self.selected_features = pd.Index(self.rng.choice(X.columns, n, replace=False).tolist())

        self._generate_report()
