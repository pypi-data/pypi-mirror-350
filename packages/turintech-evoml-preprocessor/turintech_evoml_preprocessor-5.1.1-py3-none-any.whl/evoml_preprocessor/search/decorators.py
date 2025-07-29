from typing import Any, Callable, TypeVar

import numpy as np
import pandas as pd

T = TypeVar("T")


def normalize(func: Callable) -> Callable:
    def wrapper(cls: T, X: pd.DataFrame, y: pd.Series, **kwargs: Any) -> pd.Series:
        """Normalize the scores to be between 0 and 1.

        Replaces np.inf with the maximum real number of
        the computed scores times 5.

        Args:
            cls (object):
                The class object.
            X (pd.DataFrame):
                The data.
            y (pd.Series):
                The labels.
        Returns:
            pd.Series:
                The normalized scores.

        """

        score = func(cls, X, y, **kwargs)
        score[score == np.inf] = score[score != np.inf].max() * 5
        top = score - score.min()
        bottom = score.max() - score.min()
        return np.true_divide(top, bottom, where=bottom != 0)

    return wrapper
