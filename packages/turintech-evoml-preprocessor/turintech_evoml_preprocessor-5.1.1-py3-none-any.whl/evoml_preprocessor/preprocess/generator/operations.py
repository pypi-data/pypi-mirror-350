# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from __future__ import annotations

from enum import Enum, auto
from functools import partial
from typing import Any, Callable, List, Optional, Type, Union

# Dependencies
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from typing_extensions import Self

# Module
from evoml_preprocessor.utils.string_enum import StrEnum

# ──────────────────────────────────────────────────────────────────────────── #


class Priority(int, Enum):
    """Enumeration of cases for priorities. There's 4 fundamental cases (add,
    mul, exp, func) and some potential corner-cases.

    Based on https://qr.ae/pvYGD1
    """

    # Low priorities
    ADD = auto()  # {} + {}, {} - {}
    MUL = auto()  # {} × {}, {} / {}
    # Edge cases
    SCALAR = auto()  # 2 × {}
    # High priorities
    EXP = auto()  # {}², √{}
    FUNCTION = auto()  # sin({}), log({}), ...


OperationFunction = Callable[..., NDArray[np.float64]]


class Operation(Enum):
    """Enum accepting functions and their string representation as values. Makes
    enum values callable (e.g. Functions.add(0, 1)) and provides a lookup (see
    _missing_) for instantiating enum members from functions.

    Notes:
        When adding functions as enum members, please check their type. The
        primitive type <class 'function'> (default type for any function) is
        confused for a method of the class, and thus doesn't show up in the enum
        members.
        A workaround is to wrap them in 'functools.partial'.

        For string template please add appropriate character(s) that represent
        that mathematical operation. If 'None' is set, the default display
        option will be used (code like rather than math like).

        For priority please refer to the order of operations explained in the
        comments below, and assign an integer that corresponds with that table.
    """

    # Why we need to wrap function instances of <class 'function'> in
    # functools.partial in order for them to show up:
    # https://stackoverflow.com/a/40339397
    #
    # > [...]
    # >
    # > However the issue with functions is that they are considered to be
    # > method definitions instead of attributes!
    # >
    # > [...]
    # >
    # > You can work around this by using a wrapper class or just
    # > functools.partial

    function: OperationFunction
    template: Optional[str]
    # @TODO(mypy): mypy says 'cannot assign to final name "priority"', sounds
    # like a bug
    priority: Priority  # type: ignore
    associative: bool

    def __init__(
        self,
        function: OperationFunction,
        template: Optional[str] = None,
        priority: Priority = Priority.FUNCTION,
        is_associative: bool = True,
    ):
        """Creates an enum member using:
        - function: a callable for this operation.
        - template: a string template to represent this operation applied to
          a variable
        """
        self.function = function
        self.template = template
        # @TODO(mypy): mypy says 'cannot assign to final name "priority"', sounds
        # like a bug
        self.priority = priority  # type: ignore
        self.associative = is_associative

    @classmethod
    def _missing_(cls: Type[Self], value: object) -> Optional[Self]:
        """Overrides the behaviour of the Enum class when creating instance by
        value fails. This method is then used to lookup for a matching enum
        member for the provided value.

        Note:
            Our use of `partial` creates situations where we're trying to create
            a new enum instance with a partial(f). The enum class will compare
            this partial(f) to all existing enum values. Our problem is that
            partial(f) != partial(f) : the comparison will be False even if we
            have a partial of the same function.
        """
        if not isinstance(value, tuple) or len(value) == 0:  # empty tuple guard
            return None

        func: Union[OperationFunction, partial[OperationFunction]] = value[0]

        # Reference to the _missing_ function:
        # https://docs.python.org/3/library/enum.html#supported-sunder-names
        if isinstance(func, partial):
            # For partial functions, we can do a lookup with the function being
            # wrapped (partial.func)

            # For more information, see:
            # https://docs.python.org/3.8/library/functools.html#partial-objects

            # Iterate over all defined enum members in the current enum class
            for operator in [op for op in cls if isinstance(op.function, partial)]:
                op_function: partial[OperationFunction] = operator.function  # type: ignore
                if func.func == op_function.func:
                    return operator
        return None

    # Note: we can't use 'Self' here for 'child' as it can be any of the
    # children implementation
    def bracket_child(self, child: Operation, is_left: bool) -> bool:
        """Compares two operations based on priority to figure out bracketing
        of the child.

        This function utilises different checks to compare priorities of an
        operation and its child operation to determine whether brackets
        around current operation's template are required.

        Note that an operation might have multiple children, but we're deciding
        bracketing on one child at a time, knowing if it's the first element
        (is_left) or the second (we only deal with unary and binary operations).

        Args:
            self (Operation):
                The parent operation.
            child (Operation):
                Child operation, the one that might need to be surrounded by
                brackets to maintain correct priority of evaluation.
            is_left (bool):
                Boolean denoting whether our operation is 'on the left' side of
                the equation. E.g. if our operation is subtraction and child
                operation is squaring it could either be 'A² - B' or 'B - A²'.
                In the first case, 'is_left' would be True, in the second case
                it would be False.

        Returns:
            brackets_needed (bool):
                Boolean to denote whether we need brackets around this
                operation and it's inputs or not.

        Implementation Details:
        -----------------------
        This order of operation is very tricky, as we need to consider multiple
        edge cases. Here are some insight on those cases, and our current
        algorithm.

        Table 1: cases with unary as a parent
        ┌─────────────┬───┬───────────┬───┬────────┬───┬────────┐
        │             │ 3 │  2 × {}   │ 4 │   {}²  │ 5 │ f({})  │
        ├───┬─────────┼───┴───────────┼───┴────────┼───┴────────┤
        │ 5 │ f({}):  │ 2 × f({})     │ f({})²     │ f(f({}))   │
        ├───┼─────────┼───────────────┼────────────┼────────────┤
        │ 4 │ {}²     │ 2 × {}²       │ ({}²)²     │ f({}²)     │
        ├───┼─────────┼───────────────┼────────────┼────────────┤
        │ 3 │ 2 × {}  │ 2 × 2 × {}    │ (2 × {})²  │ f(2 × {})  │
        ├───┼─────────┼───────────────┼────────────┼────────────┤
        │ 2 │ {} × {} │ 2 × ({} × {}) │ ({} × {})² │ f({} × {}) │
        ├───┼─────────┼───────────────┼────────────┼────────────┤
        │ 1 │ {} + {} │ 2 × ({} + {}) │ ({} + {})² │ f({} + {}) │
        ├───┼─────────┼───────────────┼────────────┼────────────┤
        │ 1 │ {} - {} │ 2 × ({} - {}) │ ({} - {})² │ f({} - {}) │
        └───┴─────────┴───────────────┴────────────┴────────────┘

        Table 2: cases with unary as a parent, boolean (add bracket)
        ┌─────────────┬───┬───────────┬───┬───────┬───┬───────┐
        │             │ 3 │  2 × {}   │ 4 │  {}²  │ 5 │ f({}) │
        ├───┬─────────┼───┴───────────┼───┴───────┼───┴───────┤
        │ 5 │ f({}):  │       ✗       │     ✗     │     ✗     │
        ├───┼─────────┼───────────────╋━━━━━━━━━━━╋───────────┤
        │ 4 │ {}²     │       ✗       ┃     ✓     ┃     ✗     │
        ├───┼─────────╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋───────────┤
        │ 3 │ 2 × {}  ┃       ✗       ┃     ✓     │     ✗     │
        ├───┼─────────╋━━━━━━━━━━━━━━━╋───────────┼───────────┤
        │ 2 │ {} × {} │       ✓       │     ✓     │     ✗     │
        ├───┼─────────┼───────────────┼───────────┼───────────┤
        │ 1 │ {} + {} │       ✓       │     ✓     │     ✗     │
        ├───┼─────────┼───────────────┼───────────┼───────────┤
        │ 1 │ {} - {} │       ✓       │     ✓     │     ✗     │
        └───┴─────────┴───────────────┴───────────┴───────────┘

        Table 3: cases with binary as a parent, boolean (add bracket)
        ┌──────────────────┬───┬─────────┬───┬─────────┬───┬─────────┐
        │                  │ 2 │ {} × {} │ 1 │ {} + {} │ 1 │ {} - {} │
        ├───┬────┬─────────┼───┴─────────┼───┴─────────┼───┴─────────┤
        │ L │ 3+ │ Unary   │      ✗      │      ✗      │      ✗      │
        │ R │ 3+ │ Unary   │      ✗      │      ✗      │      ✗      │
        ├───┼────┼─────────╋━━━━━━━━━━━━━╋─────────────┼─────────────┤
        │ L │ 2  │ {} × {} ┃      ✗      ┃      ✗      │      ✗      │
        │ R │ 2  │ {} × {} ┃      ✗      ┃      ✗      │      ✗      │
        ├───┼────┼─────────╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━┫
        │ L │ 1  │ {} + {} │      ✓      ┃      ✗      ┃      ✗      ┃
        │ R │ 1  │ {} + {} │      ✓      ┃      ✗      ┃      ✓      ┃
        ├───┼────┼─────────┼─────────────╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━┫
        │ L │ 1  │ {} - {} │      ✓      ┃      ✗      ┃      ✗      ┃
        │ R │ 1  │ {} - {} │      ✓      ┃      ✗      ┃      ✓      ┃
        └───┴────┴─────────┴─────────────┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━┛

        Logic to implement
        ------------------
        Looking at all above cases, we have the following logic:

            parent = function (5) ⇒ ✗ (no brackets)
            child > parent ⇒ ✗ (no brackets)
            child < parent ⇒ ✓ (add brackets)
            child == parent ⇒ complicated

        For the complicated case, tables 2 and 3 highlight in bold what happens when
        priorities of parent and child are the same.

            unary
            -----
            priority 4 ⇒ ✓ (add brackets)
            priority 3 ⇒ ✗ (no brackets)

        For binary priorities (1 & 2), it depends on the parent's commutativity.

            binary
            ------
            parent is associative
                ⇒ ✗ (no brackets)
            parent is not associative
                Left ⇒ ✗ (no brackets)
                Right ⇒ ✓ (add brackets)
        """
        if self.priority == Priority.FUNCTION:
            return False

        if self.priority != child.priority:
            return child.priority < self.priority

        priority = self.priority  # priority for both parent & child (==)
        if priority == Priority.SCALAR:
            return False
        if priority == Priority.EXP:
            return True
        if priority in (Priority.ADD, Priority.MUL):
            if self.associative:
                return False
            return not is_left

        raise ValueError(f"Unsupported priority {priority}")


# This is used for feature generator (UnaryOp)
def double(col: NDArray[np.float64]) -> NDArray[np.float64]:
    """Custom function to replace np.add(col, col)"""
    return col * 2


class UnaryOp(Operation):
    """Enum of unary operators.

    Unary operators are those that take a single argument.

    The format is as follows:
        The name is an actual name of a mathematical function.
        The value is a tuple of three elements:
            1. Callable function
            2. Template string representation
            3. Priority

    Examples:
        sin = np.sin, None, 3
        square = np.square, "{}²", 5

    Notes:
        Please read the documentation of `Operation` enum before
        adding new members.
    """

    sin = np.sin
    cos = np.cos
    square = np.square, "{} ** 2", Priority.EXP
    # double = partial(double), "2 ⋅ {}", Priority.SCALAR

    def __init__(
        self,
        function: OperationFunction,
        template: Optional[str] = None,
        priority: Priority = Priority.FUNCTION,
        is_associative: bool = True,
    ):
        """Applies validation for the template of this operation (we know we're
        templating a single parameter)
        """
        super().__init__(function, template, priority, is_associative)
        if self.template is not None:
            assert self.template.count("{}") == 1

    @classmethod
    def from_literal(cls, name: UnaryOpLiteral) -> UnaryOp:
        """Instantiate an enum member from its name (UnaryOpLiteral)"""
        for op in list(cls):
            if name == op.name:
                return op
        raise ValueError(f"name '{name}' not one of {[op.name for op in cls]}")

    def display(self, value: str) -> str:
        """Uses this operation's template to provide a representation of this
        operation applied to a (string) variable
        """
        if self.template is None:
            return f"{self.name}({value})"
        return self.template.format(value)

    def __call__(self, column: List[pd.Series[float]]) -> pd.Series[float]:
        # Support for custom functions put in a tuple
        result = self.function(*column)

        if isinstance(result, pd.Series):
            return result
        return pd.Series(result)


class UnaryOpLiteral(StrEnum):
    """String enumeration of the supported unary operations. Used to reference
    those operations in a json-serializable context.
    """

    # Note: we use to implement this as a dynamic enum to scale with the content
    # of `UnaryOp`. However, this created problems with type checking tools.
    sin = "sin"
    cos = "cos"
    square = "square"


# Runtime check that both enums are in sync.
# @TODO: maybe move to unit tests
if set(UnaryOpLiteral) != {op.name for op in UnaryOp}:
    raise RuntimeError("UnaryOpLiteral is out of sync with UnaryOp")


class BinaryOp(Operation):
    """Enum of binary operators.

    Binary operators are those that take two arguments.

    The format is as follows:
        The name is an actual name of a mathematical function.
        The value is a tuple of four elements:
            1. Callable function
            2. Template string representation
            3. Priority
            4. Associativity
        For function please wrap in 'partial' and specify the axis parameter

    Example:
        prod = partial(np.prod, axis=0), "{} × {}", 2
        subtract = partial(np.subtract), "{} - {}", 0

    Notes:
        Please use partial as a wrapper and specify axis if necessary.
        The function should be able to accept a list of inputs or
        be a binary function to accept two separate parameters.

        Please read the documentation of `Operation` enum before
        adding new members.
    """

    prod = partial(np.multiply), "{} * {}", Priority.MUL
    add = partial(np.add), "{} + {}", Priority.ADD
    # Subtraction is the only non-associative operation we implement for now
    subtract = partial(np.subtract), "{} - {}", Priority.ADD, False

    def __init__(self, *args: Any, **kwargs: Any):
        """Applies validation for the template of this operation (we know we're
        templating two parameters)
        """
        super().__init__(*args, **kwargs)
        if self.template is not None:
            assert self.template.count("{}") == 2

    @classmethod
    def from_literal(cls, name: BinaryOpLiteral) -> BinaryOp:
        for op in list(cls):
            if name == op.name:
                return op
        raise ValueError(f"name '{name}' not one of {[op.name for op in cls]}")

    def display(self, a: str, b: str) -> str:
        """Uses this operation's template to provide a representation of this
        operation applied to a (string) variable
        """
        if self.template is None:
            return f"{self.name}({a}, {b})"
        return self.template.format(a, b)

    def __call__(self, column: List[pd.Series[float]]) -> pd.Series[float]:
        try:
            # Support of a single argument being a list of operands
            # e.g. f([a, b, c, d])
            result = self.function(column)

        # Note: for some numpy functions, when the argument format is not valid,
        # numpy<1.21 raises ValueError, numpy>=1.21 raises TypeError
        except (ValueError, TypeError):
            # Support for operands as individual positional arguments
            # e.g. f(a, b, c, d)
            result = self.function(*column)

        if isinstance(result, pd.Series):
            return result
        return pd.Series(result)


# Note: this implementation scales with BinaryOp but is less LSP friendly. That's
# okay as this is only used for loading from json (in generic functions)
class BinaryOpLiteral(StrEnum):
    """String enumeration of the supported binary operations. Used to reference
    those operations in a json-serializable context.
    """

    # Note: we use to implement this as a dynamic enum to scale with the content
    # of `BinaryOp`. However, this created problems with type checking tools.
    prod = "prod"
    add = "add"
    # Subtraction is the only non-associative operation we implement for now
    subtract = "subtract"


# Runtime check that both enums are in sync.
# @TODO: maybe move to unit tests
if set(BinaryOpLiteral) != {op.name for op in BinaryOp}:
    raise RuntimeError("BinaryOpLiteral is out of sync with UnaryOp")
