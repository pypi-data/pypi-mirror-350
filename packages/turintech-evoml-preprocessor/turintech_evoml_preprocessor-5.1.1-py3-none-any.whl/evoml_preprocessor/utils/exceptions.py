import contextlib
import logging
from types import FrameType
from typing import Iterator, Optional

logger = logging.getLogger(__name__)
memory_logger = logging.getLogger("memory")


@contextlib.contextmanager
def silence_errors(message: str = "{}", _logger: Optional[logging.Logger] = None) -> Iterator[None]:
    """Small context manager silencing the first exception occurring inside the
    with statement, then quiting. Make sure when using it that no code outside
    the statement depends on code inside the statement.
    Args:
        message (str):
            A python3's format template string. It must include a '{}'
            placeholder that will be replaced by the error silenced.
            By default, the error is logged as is.

        _logger (logging.Logger):
            The logger used to log the silenced error. A global variable named
            logger will be used by default, and if it doesn't exist, the root
            logger will be used.
    """

    # Note: this is similar to contextlib.suppress, but it logs systematically.
    local_logger = _logger or globals().get("logger", logging.getLogger())

    try:
        yield
    except BaseException as exception:  # pylint: disable=W0703
        local_logger.error("%s", message.format(exception))


class UserInputError(Exception):
    """Exception used for errors caused by the user"""


class NotInitializedError(Exception):
    """Exception used for uninitialized variables"""


class InvalidScalerError(Exception):
    """Exception used for errors caused by the user"""


def signal_handler(signum: int, frame: Optional[FrameType]) -> None:
    raise TimeoutError("Timeout occurred: unable to simplify generated feature formula")
