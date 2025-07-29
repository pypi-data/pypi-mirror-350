"""Module providing functions to generate a static copy of the preprocessor's
codebase for a given dataset
"""

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Appendix:
    """Structure of the appendix directory containing the preprocessing code"""

    directory: Path

    # ------------------------------- folders -------------------------------- #
    @property
    def data(self) -> Path:
        return self.directory / "data"

    @property
    def setup(self) -> Path:
        return self.directory / "setup"

    # -------------------------------- files --------------------------------- #
    @property
    def preprocessor_meta(self) -> Path:
        return self.data / "preprocessor_meta.json"

    @property
    def joblib(self) -> Path:
        return self.data / "prepro.joblib"

    @property
    def requirements(self) -> Path:
        return self.setup / "requirements_prepro.txt"

    # ------------------------------- methods -------------------------------- #
    def mkdir(self) -> None:
        """Create the path directories"""
        self.data.mkdir(exist_ok=True, parents=True)
        # self.sources.mkdir(exist_ok=True, parents=True)
        self.setup.mkdir(exist_ok=True, parents=True)


class CodeGenerator:
    """Static class providing functions to generate static code for preprocessing specific datasets.

    This static class exposes different constants to modify the behaviour of the methods.
    """

    GLOBS_TO_SCAN = [
        "models/config/*.py",
        "preprocess/**/*.py",
        "preprocess/feature/metric/*.py",
        "utils/conf/**/*.py",
        "utils/reports/models.py",
        "utils/representative_models.py",
        "utils/misc.py",
        "utils/utils.py",
        "utils/requirements.py",
        "utils/huggingface.py",
        "utils/opt_heuristic.py",
        "utils/aggregation.py",
    ]
    EXCLUDED_FUNC_NAMES = ["__save", "check_task", "check_consecutive", "save_requirements"]
    PKG_FOLDER = "evoml_preprocessor"

    @classmethod
    def transform_only(cls, path: Path) -> None:
        """Generates the code for running the transform only (removes all fit
        & fit_transform methods).
        """
        # Isolated imports as this class will not always be used
        import inspect
        from datetime import datetime

        from evoml_preprocessor.preprocess import preprocessor

        prepro_file_path = inspect.getfile(preprocessor)
        pkg_folder_idx = prepro_file_path.rfind(cls.PKG_FOLDER) + len(cls.PKG_FOLDER) + 1
        if pkg_folder_idx < 0:
            return
        pkg_root_path = Path(prepro_file_path[:pkg_folder_idx])

        # Don't overwrite source files
        if path.absolute() == pkg_root_path.absolute() or path.absolute() == Path().absolute():
            return

        path.mkdir(exist_ok=True)
        for python_file in [path for glob in cls.GLOBS_TO_SCAN for path in pkg_root_path.glob(glob)]:
            file_lines = python_file.open().readlines()
            lines_to_delete = []

            file_ast = ast.parse("".join(file_lines))
            for node in ast.walk(file_ast):
                if not isinstance(node, ast.FunctionDef):
                    continue
                fit_transform = "fit_transform" in node.name
                excluded = node.name in cls.EXCLUDED_FUNC_NAMES
                if fit_transform or excluded:
                    assert node.end_lineno is not None
                    lines_to_delete += list(range(node.lineno, node.end_lineno + 1))

            # Finally, only keep the lines that is not in a fit_transform function
            source_transform_only = [datetime.now().strftime("# Generated at %Y-%m-%d %H:%M:%S\n")]
            for i, line in enumerate(file_lines, start=1):
                if i not in lines_to_delete:
                    source_transform_only.append(line)

            transform_path = path / python_file.relative_to(pkg_root_path.parent)
            transform_path.parent.mkdir(exist_ok=True, parents=True)
            with transform_path.open("w") as fp:
                fp.writelines(source_transform_only)

        # Create init file if it does not exist
        for module in path.glob("**/*/"):
            init_path = module / "__init__.py"
            if module.is_dir() and not init_path.exists():
                init_path.touch()
