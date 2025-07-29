import typing

import numpy

if typing.TYPE_CHECKING:
    Int64 = numpy.dtype[numpy.int64]
    Int16 = numpy.dtype[numpy.int16]
    Int8 = numpy.dtype[numpy.int8]
    Uint8 = numpy.dtype[numpy.uint8]
    Float64 = numpy.dtype[numpy.float64]
    Bool = numpy.dtype[numpy.bool_]
    String = numpy.dtype[numpy.str_]
    DateTime64 = numpy.dtype[numpy.datetime64]
else:
    Int64 = numpy.int64
    Int16 = numpy.int16
    Int8 = numpy.int8
    Uint8 = numpy.uint8
    Float64 = numpy.float64
    Bool = numpy.bool_
    String = numpy.str_
    DateTime64 = numpy.datetime64

# current supported dtypes for numeric values
Numeric = typing.Union[Float64, Int64, Int8, Int16, Uint8, Bool]

# current supported dtypes for a categorical feature
Categorical = String

# current supported dtypes for a target feature
Target = typing.Union[Int64, Float64]

# all current supported dtypes for a feature
Any = typing.Union[Int64, Int8, Int16, Uint8, Float64, Bool, String, DateTime64]
