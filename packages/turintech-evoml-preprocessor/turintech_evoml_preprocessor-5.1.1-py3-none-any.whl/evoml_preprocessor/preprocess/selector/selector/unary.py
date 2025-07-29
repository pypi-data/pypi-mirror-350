import pandas as pd

from evoml_preprocessor.preprocess.models import SelectorType
from evoml_preprocessor.preprocess.selector.models import SelectionMethodReport
from evoml_preprocessor.preprocess.selector.selector import Selector
from evoml_preprocessor.preprocess.selector.util import SelectorParameters


def is_unary(series: pd.Series) -> bool:
    """Check if a Pandas Series is unary (all elements are the same) by iterating over the first 1000 elements and
    searching for any differences from the first non-NaN element. If no differences are found, we then check the entire
    series for the number of unique values.

    This strategy is very fast on most non-unary series, since differences are usually found in first ~2 elements. In
    the worst case we have a large unary series which would take a very long time to iterate over. In this case we fall
    back to the nunique() for better performance.

    Args:
        series (pd.Series): The series to check.

    Returns:
        bool: True if the series is unary, False otherwise.
    """
    first_valid_element = None

    # Limit the iteration to the first 1000 elements
    for element in series.head(1000):
        if not pd.isna(element):
            if first_valid_element is None:
                first_valid_element = element
            elif element != first_valid_element:
                return False

    # If the function hasn't returned False yet, fall back to nunique()
    return series.nunique(dropna=True) == 1


class UnarySelector(Selector):
    def __init__(self, parameters: SelectorParameters):
        super().__init__(parameters)
        self._report = SelectionMethodReport(method=SelectorType.UNARY)

    @property
    def name(self) -> str:
        return "unary"

    def fit(self, X: pd.DataFrame, y: pd.Series, n: int = 0) -> None:
        """Iterates over columns in the dataframe to check whether there
        are unary features. Unary features are removed. If there are more unary
        features than `n`, not all unary features are removed (useful for
        benchmarking to ensure consistent number of target features).

        Args:
            X (pd.DataFrame): The original data.
            y (pd.Series): The target data.
            n (int): The lower limit for number of features to keep.

        Returns:
            pd.DataFrame: The data with unary features removed.

        """

        self.init_fit(X, y, n)
        n_remove = max(0, len(X.columns) - n)
        to_remove = pd.Index([col for col in X.columns if is_unary(X[col])][:n_remove])
        self.selected_features = self.fitted_features.difference(to_remove)

        self._generate_report()
