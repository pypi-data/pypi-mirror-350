# encoding: utf-8
"""
Single module gathering all the preprocessing logic. By design, this module
is meant to be standalone (this python file can be extracted from its context
and work).

It contains one main class, :class:`DataPreprocessor`, providing the public
interface for users as well as the top-level logic, and several classes
subclassing :class:`Transformer` providing the specific logic of preprocessing
different types of data.
"""
# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from __future__ import annotations
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Dependencies
import joblib
import numpy as np
import pandas as pd
import json
import pickle
import zipfile
from evoml_api_models import MlTask
from pydantic import BaseModel

# Private Dependencies
from evoml_api_models.builder import get_builder, Builder  # type: ignore

# Module
from evoml_preprocessor.preprocess.handlers.data_preparation import DataPreparationHandler
from evoml_preprocessor.preprocess.handlers.feature import FeatureHandler
from evoml_preprocessor.preprocess.handlers.feature_generation import FeatureGenerationHandler
from evoml_preprocessor.preprocess.handlers.feature_selection import FeatureSelectionHandler
from evoml_preprocessor.preprocess.handlers.index import IndexHandler
from evoml_preprocessor.preprocess.handlers.label import LabelHandler
from evoml_preprocessor.preprocess.handlers.post_processing._base import PostProcessingHandler
from evoml_preprocessor.preprocess.models import ColumnInfo, PreprocessConfig, TransformationOptions
from evoml_preprocessor.preprocess.models.report import PreprocessingReport
from evoml_preprocessor.utils.anomaly_detection import get_rows_with_duplicate_index
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr
from evoml_preprocessor.preprocess.handlers.factory import handler_factory


# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class FittedConfig(BaseModel):
    original_columns: List[str] = []
    required_columns: List[str] = []
    row_index_name: str = "thor-index"
    drop_missing_labels: bool = False
    dropped_imbalanced_classes: Optional[List] = None
    output_feature_order: List[str] = []


class InitialConfig(BaseModel):
    label_column: str
    index_column: Optional[str] = None
    ml_task: MlTask = None
    is_time_series: bool
    transformation_options: List[TransformationOptions] = []
    info_map: Dict[str, ColumnInfo]


class DataPreprocessor:
    """The DataPreprocessor class provides the interface for preprocessing data. Preprocessing is divided into steps
    encapsulated in the handlers.
    """

    config: InitialConfig
    label_handler: LabelHandler
    index_handler: IndexHandler
    feature_handler: FeatureHandler
    fs_handler: FeatureSelectionHandler
    fg_handler: FeatureGenerationHandler
    data_preparation_handler: DataPreparationHandler
    post_processing_handler: PostProcessingHandler
    fitted_config: FittedConfig

    def __init__(
        self,
        config: InitialConfig,
        label_handler: LabelHandler,
        index_handler: IndexHandler,
        feature_handler: FeatureHandler,
        fs_handler: FeatureSelectionHandler,
        fg_handler: FeatureGenerationHandler,
        data_preparation_handler: DataPreparationHandler,
        post_processing_handler: PostProcessingHandler,
        fitted_config: FittedConfig,
    ):
        """Initializes the DataPreprocessor object.

        Args:
            config (InitialConfig): Model containing generic information about the dataset and the
            preprocessing task.
            label_handler (LabelHandler): Responsible for cleaning and transforming the target.
            index_handler (IndexHandler): Responsible for cleaning and transforming the index of the dataset.
            feature_handler (FeatureHandler): Responsible for cleaning and transforming the features.
            fs_handler (FeatureSelectionHandler): Responsible for selecting the most relevant features for inference.
            fg_handler (FeatureGenerationHandler): Responsible for generating new features useful for inference.
            post_processing_handler (PostProcessingHandler): Responsible for dimensionality reduction.
            fitted_config (FittedConfig): Model information obtained while fitting the preprocessor to the dataset.

        """
        # -------------------------------------------------------------------- #
        # Attributes used for reporting
        self._report_builder: Optional[Builder] = get_builder(PreprocessingReport)

        # Information obtained during fitting which will be used to transform unseen data
        # Will be updated when calling fit_transform.
        self.fitted_config = fitted_config

        # Attributes from init arguments
        self.config = config

        self.data_preparation_handler = data_preparation_handler
        self.index_handler = index_handler
        self.feature_handler = feature_handler
        self.fs_handler = fs_handler
        self.fg_handler = fg_handler
        self.post_processing_handler = post_processing_handler
        self.label_handler = label_handler

    @classmethod
    def from_config(cls, config: PreprocessConfig, info_map: Dict[str, ColumnInfo]) -> DataPreprocessor:

        fitted_config = FittedConfig()

        (
            data_preparation_handler,
            index_handler,
            feature_handler,
            fg_handler,
            fs_handler,
            post_processing_handler,
            label_handler,
        ) = handler_factory(config, info_map)

        initial_config = InitialConfig(
            label_column=config.labelColumn,
            index_column=config.indexColumn,
            ml_task=config.mlTask,
            is_time_series=config.isTimeseries,
            transformation_options=config.transformationOptions,
            info_map=info_map,
        )

        return cls(
            config=initial_config,
            data_preparation_handler=data_preparation_handler,
            label_handler=label_handler,
            index_handler=index_handler,
            feature_handler=feature_handler,
            fs_handler=fs_handler,
            fg_handler=fg_handler,
            post_processing_handler=post_processing_handler,
            fitted_config=fitted_config,
        )

    def transform(self, data: pd.DataFrame, include_label_column: bool = False) -> pd.DataFrame:
        """Transforms a dataframe that has already been fitted in fit_transform.

        NOTE: This function directly modifies the input dataframe.

        Args:
            data (pd.DataFrame): Dataframe to transform.
            include_label_column (bool): Whether to include the label column
                in the transformed dataframe.

        Returns:
            pd.Dataframe: Transformed dataframe.

        """

        # -------------------------- safety checks --------------------------- #
        original_cols = set(self.fitted_config.original_columns) - {self.config.label_column}
        received_cols = set(data.columns) - {self.config.label_column}
        if not received_cols.issubset(original_cols):
            unexpected_cols = received_cols - original_cols
            logger.info(f"Some columns have not been seen during training and will be ignored: {unexpected_cols}")
            data = data.drop(columns=list(unexpected_cols))
        if not set(self.fitted_config.original_columns).issubset(received_cols):
            difference = set(self.fitted_config.original_columns) - received_cols

            logger.info(f"Some used during original training are missing in the new dataset: {difference}.")

        # ensure that the index is named
        if data.index.name is None:
            data.index.name = self.fitted_config.row_index_name
        if data.index.name != self.fitted_config.row_index_name:
            logger.warning(
                f"Index name mismatch. Expected {self.fitted_config.row_index_name} but found {data.index.name}"
            )

        # ------------------------ drop missing rows ------------------------- #
        # Drop the missing labels if that's been done in fit_transform
        if has_label := self.config.label_column in data.columns:
            data = self._drop_rows(data)

        # ---------------- processing the index column first ----------------- #
        # Transforming the index column (add it first to the dataset)
        if self.config.index_column in data.columns:
            duplicates = get_rows_with_duplicate_index(data, self.config.index_column)
            if duplicates:
                data.drop(duplicates, inplace=True)
            index_col = self.index_handler.transform(data[self.config.index_column])
        else:
            if self.config.index_column is not None:
                logger.warning(f"Index column {self.config.index_column} not found in the dataset. ")

            index_col = self.index_handler.transform(None, index_size=data.shape[0])

        # -------------------- create and index encoded dataset --------------------- #
        # Create encoded dataset
        data_encoded = pd.DataFrame(index=data.index)
        if index_col is not None:
            # Add index column to the original train dataset
            data.loc[:, index_col.name] = index_col

            # add index to encoded dataframe - it is needed for some feature handlers
            data_encoded[index_col.name] = index_col

        # ---------------- processing the label column ----------------------- #
        extra_label_features = None

        # Encode label column if exists
        if has_label:
            data_label = data[self.config.label_column]

            if index_col is not None:
                data_label.index = pd.Index(index_col, name=self.fitted_config.row_index_name)

            encoded_label, extra_label_features = self.label_handler.transform(data_label)

            # Set index of encoded_label and extra_label_features to data.index
            encoded_label.index = data.index

            # Add encoded label column to data as needed for some feature handlers
            data.loc[:, self.config.label_column] = encoded_label

        # Time Series task with no label given
        elif self.config.is_time_series:
            data_label = pd.Series(index=index_col, name=self.config.label_column)
            data_label.index.name = self.fitted_config.row_index_name
            _, extra_label_features = self.label_handler.transform(data_label)

        # ------------------------ data preparation ------------------------ #
        # Execute data preparation handler
        data = self.data_preparation_handler.transform(data)

        # ------------ Add encoded features using Feature Handler ------------ #
        # add encoded features - inner is used as some transformers reduce number of lines
        data_encoded = data_encoded.join(self.feature_handler.transform(data), how="inner")

        # --------------------- Add extra label features --------------------- #

        if extra_label_features is not None:

            # Set index of extra label features
            extra_label_features.index = data.index[-extra_label_features.shape[0] :] if has_label else data.index[:1]
            extra_label_features.index.name = data.index.name

            # Add extra label features
            data_encoded = data_encoded.join(extra_label_features, how="inner")

        # ------------------------ Feature Selection ------------------------ #
        data_encoded = self.fs_handler.transform(data_encoded)

        # ------------------------ Feature Generation ------------------------ #
        data_encoded = self.fg_handler.transform(data_encoded)

        # --------------------- Dimensionality Reduction --------------------- #
        data_encoded = self.post_processing_handler.transform(data_encoded)

        # --------------------- Order Features --------------------- #
        # Features should appear in the same order as produced by fit_transform
        filtered_column_order = [col for col in self.fitted_config.output_feature_order if col in data_encoded.columns]
        missing_transformed_features = set(self.fitted_config.output_feature_order) - set(filtered_column_order)
        if missing_transformed_features:
            logger.info(
                f"Some features produced during fit_transform are not present in the newly transformed dataset: {missing_transformed_features}"
            )
        data_encoded = data_encoded[filtered_column_order]

        # ----------------- Add the label column at the end ----------------- #
        # Add transformed label column to the dataset as last column
        if has_label and include_label_column:

            # Add label column at the end
            data_encoded = data_encoded.join(encoded_label, how="inner")

        return data_encoded

    def _drop_rows(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.fitted_config.drop_missing_labels:
            missing_labels_index = data[data[self.config.label_column].isnull()].index
            data.drop(missing_labels_index, inplace=True)

        if self.fitted_config.dropped_imbalanced_classes is not None:
            # identify the classes that have been dropped
            index_to_drop = data.loc[
                data[self.config.label_column].isin(self.fitted_config.dropped_imbalanced_classes),
                self.config.label_column,
            ].index

            # drop rows for dropped imbalanced classes found in the test set
            data.drop(index_to_drop, inplace=True)

            # warn users that some classes have been dropped
            logger.warning(f"Dropped imbalanced classes: {self.fitted_config.dropped_imbalanced_classes}")

        return data

    def inverse_label_transform(self, transformed_label_column: np.ndarray) -> np.ndarray:
        """Inverse transforms a label column (already preprocessed) back to
        original labels.

        Args:
            transformed_label_column (np.ndarray): (N,) The column that
                has been preprocessed. For classification, it is
                preprocessed using label encoder.

        Returns:
            np.ndarray: (N,) Inverse transformed label column.

        """

        label_col = self.label_handler.inverse_transform(pd.Series(transformed_label_column))
        return label_col.to_numpy()

    def label_transform(self, label_column: pd.Series) -> pd.Series:
        """This function transforms the test label using the same encoder trained using train label.

        Args:
            label_column (pd.Series): The label column in the test data.

        Returns:
            pd.Series: Transformed label column in the test data.

        """

        label_col, _ = self.label_handler.transform(label_column)
        return label_col

    def update(self, data: pd.DataFrame) -> None:
        """Updates the fitted label data with the given unseen label values on the
        corresponding index positions.

        Args:
            data (pd.DataFrame): Includes the unseen label values and
                the corresponding index column.

        """

        if self.config.label_column not in data:
            raise ValueError("No target values were given.")
        if self.config.index_column is not None and self.config.index_column not in data:
            raise ValueError("No index values were given.")

        # transform index column
        if self.config.index_column:
            index_col = self.index_handler.transform(data[self.config.index_column])
        else:
            index_col = self.index_handler.transform(None, index_size=data.shape[0])

        # transform label column
        data_label = data[self.config.label_column]
        if index_col is not None:
            data_label.index = pd.Index(index_col, name=self.fitted_config.row_index_name)
        encoded_label, _ = self.label_handler.transform(data_label)

        # update label handler
        self.label_handler.update(encoded_label)
        encoded_label.index = data.index

        # update feature handler
        self.feature_handler.update(encoded_label, index_col)

    # ----------------------------- save methods ----------------------------- #
    # The preprocessor's fit_transform "generates" some auxiliary data that we
    # might need to save. In order to keep responsibilities clean, we want to
    # avoid the 'fit_transform' method from dealing with the filesystem/saving
    # stuff.
    # Thus, we're providing save methods that allow the user to save the
    # auxiliary outputs if needed after 'fit_transform'
    def save_joblib(self, path: Path) -> None:
        """Saves this object to the file-system"""

        joblib.dump(self, path)

    def remove_nonpickled_attributes(self) -> None:
        """Removes attributes incompatible with the conversion to joblib
        (pickling) and not needed for the `transform` method.
        """

        # Set report builders to None as they are not used in transform they cause an error with dump/load
        self._report_builder = None
        if self.fs_handler.feature_selector is not None:
            self.fs_handler.feature_selector.report_builder = None
        self.label_handler.block_builder = None
        self.label_handler.feature_builder = None
        self.index_handler.feature_builder = None
        self.fg_handler.report_builder = None

    @property
    def metadata(self) -> Dict:
        """Preprocessor's metadata, required to use the train/test outputs"""
        # Note: these future covariates are used by the pipeline handler
        return {
            "labelMappings": self.label_handler.get_label_mappings(),
            "futureCovariates": sorted(self.feature_handler.future_covariates_names),
        }

    @property
    def report_builder(self) -> Builder:
        if self._report_builder is None:
            raise AttributeError("The report builder is not set.")
        return self._report_builder

    def save_requirements(self, path: Path) -> None:
        """Save all the preprocessed model requirements in one file

        Args:
            path (Path): The path to save the requirements file.

        """

        requirements = {
            conf_mgr.requirements_map.get(col_info.detectedType) for col_info in self.config.info_map.values()
        }
        nl = "\n"
        with path.open(mode="w") as f:
            f.write(conf_mgr.setup_path.joinpath("requirements.txt").read_text() + nl)
            for file_path in requirements:
                if file_path:
                    f.write(file_path.read_text() + nl)

    def save(self, filepath: str):
        """
        Save the DataPreprocessor configuration and handlers to a zip archive.

        Args:
            filepath (str): Path where the zip archive will be saved.
        """
        save_path = Path(filepath)
        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(save_path, "w") as archive:
            # Save InitialConfig to a JSON file
            initial_config_json_path = "initial_config.json"
            with archive.open(initial_config_json_path, "w") as f:
                f.write(json.dumps(self.config.dict()).encode("utf-8"))

            # Save FittedConfig to a JSON file
            fitted_config_json_path = "fitted_config.json"
            with archive.open(fitted_config_json_path, "w") as f:
                f.write(json.dumps(self.fitted_config.dict()).encode("utf-8"))

            # Save each handler as a pickle file
            handlers = {
                "label_handler": self.label_handler,
                "index_handler": self.index_handler,
                "feature_handler": self.feature_handler,
                "fs_handler": self.fs_handler,
                "fg_handler": self.fg_handler,
                "data_preparation_handler": self.data_preparation_handler,
                "post_processing_handler": self.post_processing_handler,
            }

            for handler_name, handler in handlers.items():
                handler_path = f"{handler_name}.pkl"
                with archive.open(handler_path, "w") as f:
                    pickle.dump(handler, f)

    @classmethod
    def load(cls, filepath: str) -> DataPreprocessor:
        """
        Load a DataPreprocessor instance from a zip archive.

        Args:
            filepath (str): Path to the zip archive containing the saved DataPreprocessor.

        Returns:
            DataPreprocessor: An instance of DataPreprocessor loaded with the saved configuration and handlers.
        """
        load_path = Path(filepath)

        with zipfile.ZipFile(load_path, "r") as archive:
            # Load InitialConfig
            with archive.open("initial_config.json") as f:
                initial_config_data = json.loads(f.read().decode("utf-8"))
                config = InitialConfig(**initial_config_data)

            # Load FittedConfig
            with archive.open("fitted_config.json") as f:
                fitted_config_data = json.loads(f.read().decode("utf-8"))
                fitted_config = FittedConfig(**fitted_config_data)

            # Load handlers
            handlers = {}
            handler_names = [
                "label_handler",
                "index_handler",
                "feature_handler",
                "fs_handler",
                "fg_handler",
                "data_preparation_handler",
                "post_processing_handler",
            ]

            for handler_name in handler_names:
                handler_path = f"{handler_name}.pkl"
                with archive.open(handler_path) as f:
                    handlers[handler_name] = pickle.load(f)

        # Instantiate the DataPreprocessor with the loaded configuration and handlers
        return cls(
            config=config,
            label_handler=handlers["label_handler"],
            index_handler=handlers["index_handler"],
            feature_handler=handlers["feature_handler"],
            fs_handler=handlers["fs_handler"],
            fg_handler=handlers["fg_handler"],
            data_preparation_handler=handlers["data_preparation_handler"],
            post_processing_handler=handlers["post_processing_handler"],
            fitted_config=fitted_config,
        )

    @property
    def original_columns(self) -> List[str]:
        return self.fitted_config.original_columns

    @property
    def future_covariates_names(self) -> List[str]:
        return list(self.feature_handler.future_covariates_names)
