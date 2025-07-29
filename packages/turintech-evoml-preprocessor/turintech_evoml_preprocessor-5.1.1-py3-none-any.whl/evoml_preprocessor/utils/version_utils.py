"""Module providing utils to get library version and requirements."""

from pathlib import Path

EVOML_PREPROCESSOR_ROOT_PATH = Path(__file__).parents[1]
SETUP_FOLDER = EVOML_PREPROCESSOR_ROOT_PATH / "setup"
VERSION_PATH = SETUP_FOLDER / ".version"


def _py_version() -> str:
    """Get the current version of the `evoml_preprocessor` library (this
    repository)
    """
    # There are two ways to get the version:
    # - src/evoml_preprocessor/setup/.version
    # - importlib.metadata.version
    return VERSION_PATH.read_text().strip()
