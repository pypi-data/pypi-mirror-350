"""Requirement related utilities"""


def _onnxruntime_installed() -> bool:
    """Checks whether onnxruntime is installed and is of the correct version.
    Returns:
        bool:
            True if onnxruntime is installed, False otherwise.
    """

    try:
        import onnxruntime
    except ImportError:
        return False
    return True


def _optimum_installed() -> bool:
    """Checks whether Optimum is installed.
    Returns:
        bool:
            True if Optimum is installed, False otherwise.
    """

    try:
        import optimum
    except ImportError:
        return False
    return True
