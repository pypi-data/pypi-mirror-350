"""Defines types used by the interface and implementations of the MlTask
specific preprocessors
"""

from typing import Union, List, Callable
import pandas as pd


LabelMapping = Union[List[str], List[int], List[float], None]
Converter = Callable[[pd.Series], pd.Series]  # @TODO: [pd.Series] → None
