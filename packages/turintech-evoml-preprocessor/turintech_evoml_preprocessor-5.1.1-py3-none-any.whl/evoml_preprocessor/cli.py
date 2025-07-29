#!/usr/bin/env python3
# encoding: utf-8
# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
import os
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import List, Optional

from evoml_preprocessor.preprocess.models.config import ColumnInfoList
from evoml_preprocessor.reports.display_generator import make_feature_generation_table
from evoml_preprocessor.reports.display_selector import create_feature_aggregation_graph
from evoml_preprocessor.reports.display_transformation import summarise_column_tags
from evoml_preprocessor.reports.timeline import summarise_preprocess_report
from evoml_preprocessor.utils.log import memory_logger
from evoml_preprocessor_internal.__main__ import OutputFlags, preprocess
from evoml_preprocessor_internal.utils.io_structure import Outputs


def set_num_threads(thread_number: int) -> None:
    """Sets env variables for number of threads for some widely used
    libraries"""
    VARS = [
        "OPENBLAS_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
    ]
    for var in VARS:
        if var in os.environ:
            logger.warning("Overwriting %s env var (value: %s)", var, os.environ[var])
        os.environ[var] = str(thread_number)


# Making sure that the number of threads is set before anything else is imported
if __name__ == "__main__":
    cpu_count = os.cpu_count()
    assert cpu_count is not None

    threads = int(os.environ.get("PREPROCESS_THREADS", cpu_count * 0.5))
    set_num_threads(threads)

    from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

    conf_mgr.preprocess_conf.THREADS = threads

from evoml_preprocessor.utils.validation import validate_data
from evoml_preprocessor.utils.sort import sort_datasets_index
from evoml_preprocessor.utils.exceptions import silence_errors

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import MlTask, DetectedType
from evoml_utils.data import load_dataset, first_valid_extension
from evoml_utils.logger import add_ttm_handler  # type: ignore

# Module
from evoml_preprocessor.preprocess.models import (
    PreprocessConfig,
    ColumnInfo,
    DatasetConfig,
)
from evoml_preprocessor_internal.preprocess.preprocessor import EvomlDataPreprocessor
from evoml_preprocessor.splitting import splitting_factory
from evoml_preprocessor.utils import (
    save_data,
    save_json,
)

logger = logging.getLogger("preprocessor")


# ──────────────────────────────────────────────────────────────────────────── #
#                            Main for preprocessing                            #
# ──────────────────────────────────────────────────────────────────────────── #
@dataclass
class OutputPaths:
    appendix: Path


def preprocessing_main(
    reports_directory: Path,
    config: PreprocessConfig,
    data: pd.DataFrame,
    types: List[ColumnInfo],
    data_test: Optional[pd.DataFrame] = None,
    dev: bool = True,
) -> None:
    """Saves the main outputs of the preprocessor:
    - preprocessed data (train & test)
    - graphs & tables
    - the internal json report
    """
    output_paths = Outputs(reports_directory, parquet=True)

    # ───────────────────────── Run the preprocessor ───────────────────────── #
    # The preprocess method needs to save the following outputs:
    # - split original data (train, test, dropped)
    # - appendix code
    preprocess_output = preprocess(
        config=config,
        types=types,
        dataset=data,
        dataset_test=data_test,
        output_flags=OutputFlags(
            appendix=dev,
            graphs=dev,
            internal_report=dev,
            original_split=dev,
        ),
    )

    # alias for readability
    preprocessed_train = preprocess_output.train
    preprocessed_test = preprocess_output.test
    report = preprocess_output.report

    if dev:
        output_paths.appendix.preprocessor_meta.write_text(report.json(indent=2, allow_nan=False))

        # Save the output to different formats depending on the flags
        to_save = [
            (preprocessed_train, output_paths.data.train),
            (preprocessed_test, output_paths.data.test),
        ]

        for source, path in to_save:
            save_data(source, path)

        # Preprocessor Report
        # • this is not an 'official' output, only serves for debugging purpose
        #   for developers (& internal use)
        output_paths.graphs.report.write_text(report.json(indent=2, allow_nan=False))

        # Preprocessing Timeline → required
        #
        #     step A                          step C
        #        ▲                              ▲
        #        │                              │
        # ┌──────┴───────┬───────────────┬──────┴──────┬───────────────┐
        # │              │               │             │               │
        # └──────────────┴───────┬───────┴─────────────┴───────┬───────┘
        #                        │                             │
        #                        ▼                             ▼
        #                      step B                        step D
        summarised_report = summarise_preprocess_report(config, report, types)
        save_json(summarised_report.dict(), output_paths.graphs.timeline)

        # Summarise Table → optional
        #
        # ┌────┬─────┬───────────┬───────────┬─────┬─────┐
        # │ id │ ... │    ...    │    ...    │ ... │ ... │
        # ├────┼─────┼───────────┼───────────┼─────┼─────┤
        # │    │     │           │           │     │     │
        # └────┴─────┴───────────┴───────────┴─────┴─────┘
        with silence_errors("Failed to generate Summarised Report:\n{}", logger):
            column_tags = summarise_column_tags(report, config, types, data)
            save_json(column_tags.dict(), output_paths.graphs.tags)

        # Feature Generation Table → optional
        #
        # ┌─────────┬─────┬───────────┬───────────┬─────┬─────┐
        # │ feature │ ... │    ...    │    ...    │ ... │ ... │
        # ├─────────┼─────┼───────────┼───────────┼─────┼─────┤
        # │         │     │           │           │     │     │
        # └─────────┴─────┴───────────┴───────────┴─────┴─────┘
        with silence_errors("Failed to generate Feature Generation Table:\n{}", logger):
            feature_generation_table = make_feature_generation_table(report)
            save_json(feature_generation_table.dict(), output_paths.graphs.feature_generation_table)

        # Feature Aggregation → optional
        #                                       ┌──┐
        #                                  ┌──┐ │  │
        #                        ┌──┐ ┌──┐ │  │ │  │
        #                   ┌──┐ │  │ │  │ │  │ │  │
        #              ┌──┐ │  │ │  │ │  │ │  │ │  │
        #              ┴──┴─┴──┴─┴──┴─┴──┴─┴──┴─┴──┴
        with silence_errors("Failed to generate Feature Aggregation Graph:\n{}", logger):
            feature_aggregation_graph = create_feature_aggregation_graph(report)
            feature_aggregation_path = output_paths.graphs.feature_importance_aggregation
            # @TODO: make sure that we return None if and only if not having
            # this graph is intended. Otherwise (i.e. wrong data, any kind of
            # unexpected behaviour), we should raise explicit exceptions
            if feature_aggregation_graph is not None:
                save_json(feature_aggregation_graph.dict(), feature_aggregation_path)


# ──────────────────────────────────────────────────────────────────────────── #
#               Simple CLI to run preprocessor or visualisation                #
# ──────────────────────────────────────────────────────────────────────────── #


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Main entrypoint to run the preprocessor and the visualisation of columns"
    )

    # ----------------------- add the different flags ------------------------ #
    # Development flag to create files outside the expected options
    parser.add_argument(
        "--dev",
        dest="dev",
        default=False,
        action="store_true",
        help="Create development files as well",
    )

    parser.add_argument(
        "-j",
        "--joblib",
        dest="joblib",
        default=False,
        action="store_true",
        help="Create a joblib file. Implied by --dev",
    )

    # Flag to generate summarised preprocess report or not.
    # Could potentially grow to be computationally expensive
    # Or take a lot of storage (not so much for now) so I set
    # flag that can be used to not generate them if not needed
    parser.add_argument(
        "-s",
        "--summarise",
        dest="summarise",
        default=False,
        action="store_true",
        help="summarise logs of the preprocessor",
    )

    # -- Main options
    # Inputs directory
    parser.add_argument(
        "-i",
        "--inputs",
        dest="input_dir",
        type=Path,
        default="inputs",
        help=dedent(
            """\
                        Path to the input directory, that should contain the following files:
                        - data.csv
                        - config.json
                        - columns-info.json\
                    """
        ),
    )

    # Outputs directory
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        type=Path,
        default="outputs",
        help=dedent(
            """\
                        Path to the output directory, that will contain the following files:
                        - train.csv
                        - test.csv
                        - original_train.csv
                        - original_test.csv
                        - dropped.csv
                        - metadata.json
                        - ...\
                    """
        ),
    )

    # Strict Mode -- read inputs in a strict way, making everything required
    parser.add_argument(
        "--strict",
        dest="strict_mode",
        default=False,
        action="store_true",
        help=dedent(
            """\
                        Strict mode: disable default values for fields, and rejects
                        unexpected fields. Useful to check if your current config is up to
                        date with the preprocessor.
                    """
        ),
    )

    # Mutually exclusive flags for file-types (preprocessor only)
    filetype = parser.add_mutually_exclusive_group()

    filetype.add_argument(
        "--parquet",
        action="store_true",
        help="Use parquet for the train and test output files. Default is csv.",
    )

    # --------------------- process the parsed arguments --------------------- #
    args = parser.parse_args()

    # Setting up the logger here because we need to know the output directory (for frontend logs)

    # Add a console handler to print clean logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)5s] %(message)s", datefmt="%H:%M:%S"))

    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    memory_logger.addHandler(console_handler)
    memory_logger.setLevel(logging.ERROR)

    # This is a fix for enigmaopt's current invasive behaviour of setting the
    # root logger's config. We disable propagation to make sure the root logger
    # won't be used.
    logger.propagate = False
    memory_logger.propagate = False

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    add_ttm_handler(logger, args.output_dir)  # frontend logs

    # Catch ground breaking errors
    # @TODO: replace this try/except with a more elegant context manager
    try:
        logger.info(" Start Feature Preprocessing ".center(60, "-"))

        # Find paths for input files
        data_path = first_valid_extension(args.input_dir / "data", [".parquet", ".csv"])  # → parquet > csv
        data_test_path = first_valid_extension(args.input_dir / "test", [".parquet", ".csv"])
        if data_path is None:
            raise ValueError("No valid data file found")
        config_path = args.input_dir / "config.json"
        columns_path = args.input_dir / "columns-info.json"

        # Load the column infos
        columns = ColumnInfoList.parse_file(columns_path).__root__

        # Load the config
        config = PreprocessConfig.parse_file(config_path)

        # Load the data
        dataset_config = DatasetConfig.parse_obj(config)
        data, _ = load_dataset(dataset_config.dict(), str(data_path))

        # validate loaded data - ensuring the base types = loaded datatypes
        # this validation code was added as there was a bug due to loading or parque files
        data = validate_data(data, columns)
        data_test = None
        if data_test_path is not None:
            data_test, _ = load_dataset(dataset_config.dict(), str(data_test_path))
            data_test = validate_data(data_test, columns)

        # Convert the index column's index to name if given
        index_column_index = dataset_config.indexColumnIndex
        if index_column_index is not None and dataset_config.indexColumn is None:
            config.indexColumn = data.columns.values[index_column_index]

        # Preprocessor call
        preprocessing_main(
            args.output_dir,
            config,
            data,
            columns,
            data_test=data_test,
            dev=args.dev,
        )
    except BaseException as e:
        logger.error(traceback.format_exc())
        raise e

    logger.info(" Feature Preprocessing Successful  ".center(60, "-"))


if __name__ == "__main__":
    main()
