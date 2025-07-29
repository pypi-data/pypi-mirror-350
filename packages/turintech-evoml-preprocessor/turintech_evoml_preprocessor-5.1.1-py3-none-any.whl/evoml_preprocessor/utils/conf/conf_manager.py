"""
This module implements and instantiates the common configuration class used in the project.
"""

# pylint: disable=C0415
#       C0415: Import outside toplevel (torch) (import-outside-toplevel)
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
import contextlib
import logging
from pathlib import Path
from typing import Any, Optional, Union

from evoml_api_models import DetectedType

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["conf_mgr"]

from evoml_preprocessor.utils.conf.conf_factory import PreprocessSettings, preprocess_conf_factory

# ────────────────────────────────────────────────────────────────────────────────────────────── #
#                                             Logger                                             #
# ────────────────────────────────────────────────────────────────────────────────────────────── #

logger = logging.getLogger(__name__)


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                     Configuration Manager                                     #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


class ConfManager:
    """Configuration Manager class"""

    # APP paths
    conf_path: Path = Path(__file__).parent.resolve()  # conf package
    util_path: Path = conf_path.parent.resolve()  # util package
    preprocess_path: Path = util_path.parent.resolve()  # evoml_preprocessor package
    src_path: Path = preprocess_path.parent  # src package
    root_path: Path = src_path.parent  # project
    setup_path: Path = preprocess_path.joinpath("setup")  # setup folder

    # APP environment file
    _path_env_file: Optional[Path] = None
    _env_file: Optional[str] = None

    # The Data Configurations object
    _preprocess_conf: PreprocessSettings = PreprocessSettings()

    python_version: str = "3.8"

    requirements_map = {
        DetectedType.text: setup_path.joinpath("requirements_embedding.txt"),
        DetectedType.bank_code: setup_path.joinpath("requirements_bank_code.txt"),
        DetectedType.barcode: setup_path.joinpath("requirements_bar_code.txt"),
        DetectedType.protein_sequence: setup_path.joinpath("requirements_protein_sequence.txt"),
    }

    def __init__(self, env_file: Optional[Union[str, Path]] = None):
        self.update_conf_mgr(env_file=env_file)

    # -------------------------------------------------------------------------------------------------

    @property
    def env_file(self) -> Optional[str]:
        """Environment configuration file used in the current configuration.
        Returns:
            str:
                The environment configuration file
        """
        return self._env_file

    def update_conf_mgr(self, env_file: Optional[Union[str, Path]] = None, **kwargs: Any) -> None:
        """
        Update all the configuration by loading the environment variables from the indicated file.
        """

        if env_file:
            self._path_env_file = Path(env_file)
            self._env_file = str(self._path_env_file) if self._path_env_file.exists() else None

        self._preprocess_conf = preprocess_conf_factory(_env_file=self.env_file, defaults=kwargs)

        self._set_num_threads(self._preprocess_conf.THREADS)

    # -------------------------------------------------------------------------------------------------

    @property
    def preprocess_conf(self) -> PreprocessSettings:
        """The Preprocess Configurations object.
        Returns:
            PreprocessSettings: the Preprocess Configurations object.
        """

        return self._preprocess_conf

    # -------------------------------------------------------------------------------------------------
    @staticmethod
    def _set_num_threads(n: int) -> None:
        """
        Limit the number of threads the process can use.  There are certain
        libraries for which this can be set globally (i.e. pytorch). This is
        done here. For other libraries (i.e. joblib), this must be done where they
        are done where they are used. In this case they use
        PrerprocessConfig.THREADS property.
        """

        with contextlib.suppress(ModuleNotFoundError):  # "Couldn't set the number of threads. `torch` is not installed"
            import torch

            torch.set_num_threads(n)


# ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ─── ConfManager instance
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

conf_mgr = ConfManager()
