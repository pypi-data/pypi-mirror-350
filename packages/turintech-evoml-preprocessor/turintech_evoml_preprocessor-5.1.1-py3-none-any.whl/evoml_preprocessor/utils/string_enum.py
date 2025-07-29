from enum import Enum


class StrEnum(str, Enum):
    """
    A string-based Enum class that ensures correct string formatting when used in f-strings
    or other string operations, providing compatibility across Python versions (3.9 to 3.11).

    In standard `Enum` classes from python 3.11 onwards, referencing an enum instance in an
    f-string (e.g., `f"{enum_instance}"`) may return `ClassName.VALUE` instead of just the
    value. This subclass ensures that the value of the enum is returned as a string.

    This class can be replaced with the StrEnum class from the standard library when support
    for python versions below 3.11 is dropped.

    Example:
        >>> from enum import auto
        >>> class Color(StrEnum):
        ...     RED = "red"
        ...     BLUE = "blue"
        ...
        >>> color = Color.RED
        >>> print(color)
        red
        >>> f"{color}"
        'red'

    Without `StrEnum`, using a standard `Enum` might produce:
        >>> class StandardColor(Enum):
        ...     RED = "red"
        ...     BLUE = "blue"
        ...
        >>> standard_color = StandardColor.RED
        >>> f"{standard_color}"
        'StandardColor.RED'

    By subclassing `str` and `Enum`, this implementation ensures that the value behaves
    like a string in all expected contexts.

    Methods:
        __str__(): Returns the enum value as a string.
    """

    def __str__(self):
        """Return the enum value as a string."""
        return str(self.value)
