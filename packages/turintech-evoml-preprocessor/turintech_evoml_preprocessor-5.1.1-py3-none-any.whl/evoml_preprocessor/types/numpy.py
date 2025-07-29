from typing import Union

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
IntegerArray = npt.NDArray[np.int64]
BooleanArray = npt.NDArray[np.bool_]
NumericArray = Union[FloatArray, IntegerArray, BooleanArray]
StringArray = npt.NDArray[np.str_]
