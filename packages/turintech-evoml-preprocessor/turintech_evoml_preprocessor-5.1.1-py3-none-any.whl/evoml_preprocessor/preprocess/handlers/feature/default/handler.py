# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import concurrent.futures
import logging
from typing import Dict, List, NamedTuple, Optional, Type

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType

from evoml_preprocessor.preprocess.handlers.feature._base import FeatureHandler
from evoml_preprocessor.preprocess.models import ColumnInfo, ReasonDropped
from evoml_preprocessor.preprocess.transformers import (
    CategoricalTransformer,
    CurrencyTransformer,
    DateTransformer,
    EmailTransformer,
    FloatTransformer,
    FractionTransformer,
    IntTransformer,
    LabelEncodingTransformer,
    PercentageTransformer,
    Transformer,
    UnitTransformer,
    UrlTransformer,
)

#  Module
from evoml_preprocessor.search.encoder_selector import EncoderSelector
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr
from evoml_preprocessor.preprocess.handlers.feature.default.config import DefaultFeatureHandlerConfig


# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")

CONF = conf_mgr.preprocess_conf  # Alias for readability


# ──────────────────────────────────────────────────────────────────────────── #


class EncoderGroups(NamedTuple):
    parallel: Dict[str, Transformer]
    serial: Dict[str, Transformer]


def sort_encoders(encoders: Dict[str, Transformer]) -> EncoderGroups:
    """Divides encoders into groups which can be applied in parallel and serially based on their expected memory
    usage"""

    # A conservative list of low memory encoder types. Most other encoders could likely be added to this list; but text
    # and protein transformers are known to have a high VRAM footprint and should be applied serially.
    encoder_classes_parallel = (IntTransformer, FloatTransformer, CategoricalTransformer)

    encoders_parallel: Dict[str, Transformer] = {}
    encoders_serial: Dict[str, Transformer] = {}

    for name, encoder in encoders.items():
        if isinstance(encoder, encoder_classes_parallel):
            encoders_parallel[name] = encoder
        else:
            encoders_serial[name] = encoder

    return EncoderGroups(encoders_parallel, encoders_serial)


class FitTransformResult(NamedTuple):
    """A named tuple to track the results of the fit_transform method of an encoder."""

    column_name: str
    encoder: Transformer
    transformed_column: pd.DataFrame


def distribute_encoder_fit_transforms(
    encoders: Dict[str, Transformer], data: pd.DataFrame, encoded_label: pd.Series
) -> List[FitTransformResult]:
    """A function to distribute the application of the fit_transform methods of encoders across multiple processes.
    Most encoders are lightweight and can be parallelized, while others have a high memory footprint and should be
    applied serially."""

    encoders_parallel, encoders_serial = sort_encoders(encoders)

    with concurrent.futures.ProcessPoolExecutor(max_workers=CONF.THREADS) as executor:
        # Apply the low memory encoders in parallel
        encoder_fit_transform_tasks = [
            executor.submit(apply_encoder_fit_transform, encoder, data[col_name], encoded_label)
            for col_name, encoder in encoders_parallel.items()
        ]
        results = [task.result() for task in encoder_fit_transform_tasks]

    # Apply the high memory encoders serially
    for col_name, encoder in encoders_serial.items():
        results.append(apply_encoder_fit_transform(encoder, data[col_name], encoded_label))

    return results


def apply_encoder_fit_transform(
    encoder: Transformer, column: pd.Series, encoded_label: pd.Series
) -> FitTransformResult:
    """A function to apply the fit_transform method of an encoder and return fitted encoder along with the transformed
    column. Can be used to parallelize the application of fit_transform."""
    encoded_column = encoder.fit_transform(column, encoded_label)
    return FitTransformResult(str(column.name), encoder, encoded_column)


class DefaultFeatureHandler(FeatureHandler):
    label_name: str

    def __init__(self, config: DefaultFeatureHandlerConfig):
        self.config = config
        super().__init__()

    def fit_transform(self, data: pd.DataFrame, encoded_label: pd.Series) -> pd.DataFrame:
        """Transform columns in the dataset based on their DetectedType and
        return a dataframe with all the transformed columns.

        Note: the following code expects all the features in config to be there as it loops by config

        Arguments:
            data: dataset including the encoded label column.
            encoded_label: label column name

        Returns:
            data_encoded: dataframe with transformed columns
        """
        # /!\ The label column is already encoded, and the index column should
        # be skipped by this method.
        # ┌───┬───┬───┬───┬───┬───┬───┐
        # │ I │ L │ A │ B │ C │ D │ E │
        # ├───┼───┼───┼───┼───┼───┼───┤
        # │   │   │   │   │   │   │   │
        # │   │ e │ . │ . │ . │ . │ . │  # e → encoded
        # │   │   │   │   │   │   │   │
        # └───┴───┴───┴───┴───┴───┴───┘
        #           │   │   │   │   ├────┐
        #           ▼   ▼   ▼   ▼   ▼    ▼
        # ┌───┬───┬───┬───┬───┬───┬────┬────┐
        # │ I │ L │ A │ B │ C │ D │ E1 │ E2 │
        # ├───┼───┼───┼───┼───┼───┼────┼────┤
        # │   │   │   │   │   │   │    │    │
        # │   │ e │ e │ e │ d │ d │ e  │  e │  # e → encoded
        # │   │   │   │   │   │   │    │    │  # d → dropped
        # └───┴───┴───┴───┴───┴───┴────┴────┘

        self.config.label_name = str(encoded_label.name)

        # We operate on samples of the dataset instead of the whole dataset
        encoder_selector = EncoderSelector(
            self.config.transformation_options,
            encoded_label,
            self.config.ml_task,
            self.config.model_names,
        )

        # max number of features that can be dropped other than the ignored features
        # num of features - ignored_features - 1
        max_dropped = len(data.columns) - len(self.config.ignored_features) - 2

        # ----------------------- process each column ------------------------ #
        # In this loop encoders are set for all columns expect float and
        # categorical. We update the search space for float and categorical columns.

        # For some features we do not search for the optimal encoder. For these features we now prepare a mapping of
        # feature names to their respective encoders.
        preset_encoders = self.get_preset_encoders(data, max_dropped, encoder_selector)

        logger.info("→ fitting preset encoders")

        results = distribute_encoder_fit_transforms(preset_encoders, data, encoded_label)

        # Update the state of the handler with the fitted encoders
        self.save_encoders(results, data)

        # Concatenate the encoded columns or create an empty dataframe if there are no encoded columns
        if results:
            data_encoded = pd.concat([result[2] for result in results], axis=1)
        else:
            data_encoded = pd.DataFrame(index=data.index)

        # Find the optimal encoders for the remaining columns
        optimal_encoders = encoder_selector.get_optimised_encoders(encoded_label, data_encoded)

        logger.info("→ fitting optimised encoders")
        results = distribute_encoder_fit_transforms(optimal_encoders, data, encoded_label)

        # Update the state of the handler with the fitted encoders
        self.save_encoders(results, data)

        # pd.concat is more memory-efficient compared to data_encoded.join
        # especially when dealing with a large number of columns
        data_encoded = pd.concat([data_encoded] + [result[2] for result in results], axis=1)

        # check if data_encoded has positive number of features
        if data_encoded.shape[1] == 0:
            logger.error("No encoded features.")
            raise ValueError(f"No appropriate features were provided.")

        logger.info("→ column transformation successful")
        # return encoded dataset
        return data_encoded

    def get_preset_encoders(
        self,
        data: pd.DataFrame,
        max_dropped: int,
        encoder_selector: EncoderSelector,
    ) -> Dict[str, Transformer]:
        """Many features already have an encoder set by the user. Or it may be necessary to drop the feature based on
        some rule-based conditions. This method has responsibility for both dropping features and return a mapping of
        feature names to preset encoders."""

        preset_encoders = {}
        for col_info in self.config.info_map.values():
            # Aliases for code readability
            col_name = col_info.name

            if col_name in self.removed_cols:
                continue

            col_index = col_info.columnIndex

            # Label and index columns have been done already
            if col_name == self.config.label_name:
                # These columns have already been transformed
                continue

            # Columns filtered out by user input
            if col_info.columnIndex in self.config.ignored_features:
                self.drop_column(col_info, ReasonDropped.DROPPED_BY_USER)
                continue

            # drop columns detected as unary by type detector
            if col_info.detectedType == DetectedType.unary:
                self.drop_column(col_info, ReasonDropped.CONSTANT_VALUE)
                continue

            # Early conditions to drop columns
            is_not_required = col_info.columnIndex not in self.config.required_features
            can_drop = is_not_required and self.dropped_count < max_dropped

            if col_info.isDeleted:  # Duplicate detection in the column infos
                if not can_drop:
                    logger.warning(
                        f"Unable to drop duplicate column {col_name} (index {col_info.columnIndex}): column is "
                        f"required by the user."
                    )
                else:
                    self.drop_column(col_info, ReasonDropped.DUPLICATE_COLUMN)
                    continue

            # Drop columns if there are too many missing values
            if data[col_name].isnull().mean() > CONF.DROP_MISS_VALUE_RATE:
                self.drop_column(col_info, ReasonDropped.HIGH_MISSING_RATE)
                continue

            encoder_class = self.find_encoder(data, col_info, encoder_selector)

            # Apply the encoder found - if any for all columns except float and
            # categorical
            if encoder_class is not None:
                if col_index in self.config.transformation_options:
                    options = self.config.transformation_options[col_index]
                    encoder = encoder_class(
                        column_info=col_info,
                        encoder=options.encoder,
                        scaler=options.scaler,
                        impute_strategy=options.imputeStrategy,
                        impute_value=options.imputeValue,
                        derived_columns=options.derivedColumns,
                    )
                else:
                    encoder = encoder_class(column_info=col_info)

                preset_encoders[col_name] = encoder

        return preset_encoders

    def find_encoder(
        self, data: pd.DataFrame, col_info: ColumnInfo, encoder_selector: EncoderSelector
    ) -> Optional[Type[Transformer]]:
        """Finds an encoder for a column (or adds it to the search space to find
        if later) or drops it.

        This method does one of the following for the given column:
        - drop the column
        - add the column to a search space (for finding the encoder later)
        - return an encoder class

        Args:
            data:
                The dataset to encode.
            col_info:
                The columnInfo model
            encoder_selector:
                The search space to find encoder combinations
        Returns:
            transformer object
        """
        # Aliases
        _type = col_info.detectedType
        col = col_info.name

        # max number of features that can be dropped other than the ignored features
        # num of features - ignored_features - 1
        max_dropped = len(data.columns) - len(self.config.ignored_features) - 2
        is_not_required = col_info.columnIndex not in self.config.required_features
        can_drop = is_not_required and self.dropped_count < max_dropped

        if _type == DetectedType.unary:
            if not can_drop:
                logger.warning(f"We are removing the required column {col} since all values are identical.")
            # Drop unary columns as they do not provide information
            self.drop_column(col_info, ReasonDropped.CONSTANT_VALUE)
            return None

        if _type == DetectedType.binary:
            return LabelEncodingTransformer

        if _type == DetectedType.sample_id:
            if can_drop:
                self.drop_column(col_info, ReasonDropped.ID)
                return None
            #  if base_type str we treat as categorical
            if col_info.baseType == "string":
                return CategoricalTransformer
            # if base type int we treat as integer
            return IntTransformer

        if _type == DetectedType.integer:
            return IntTransformer

        if _type == DetectedType.fraction:
            return FractionTransformer

        if _type == DetectedType.percentage:
            return PercentageTransformer

        if _type == DetectedType.unit_number:
            return UnitTransformer

        if _type == DetectedType.datetime:
            return DateTransformer

        if _type == DetectedType.url:
            return UrlTransformer

        elif _type == DetectedType.text:
            from evoml_preprocessor.preprocess.transformers.text_transformer import TextTransformer

            return TextTransformer

        if _type == DetectedType.currency:
            return CurrencyTransformer

        if _type == DetectedType.email:
            return EmailTransformer

        if _type == DetectedType.categorical:
            # remove categorical column if there are too many missing values
            if col_info.statsUniqueValuesRatio >= CONF.DROP_UNIQUE_VALUE_RATIO and can_drop:
                self.drop_column(col_info, ReasonDropped.HIGH_UNIQUE_VALUES)
            elif col_info.metadata and col_info.metadata.get("is_special_categorical", False):
                return CategoricalTransformer
            else:
                encoder_selector.include_categorical_feature(data[col], col_info)
            return None

        if _type == DetectedType.float:
            encoder_selector.include_float_feature(data[col], col_info)
            return None

        if _type == DetectedType.protein_sequence:
            from evoml_preprocessor.preprocess.transformers.protein_transformer import ProteinSequenceTransformer

            return ProteinSequenceTransformer

        if _type == DetectedType.unsupported:
            self.drop_column(col_info, ReasonDropped.UNSUPPORTED_TYPE)
            return None

        self.drop_column(col_info, ReasonDropped.DEPRECATED)
        return None

    def save_encoders(self, encoder_fit_transform_results: List[FitTransformResult], data: pd.DataFrame) -> None:
        """Save the encoders found during the fitting stage.

        Args:
            encoder_fit_transform_results: A list of tuples, each containing (col_name, encoder, transformed_col)

        """
        for col_name, encoder, transformed_col in encoder_fit_transform_results:
            col_info = self.config.info_map[col_name]

            # Save the encoder for future transformations
            self.encoders[col_name] = encoder

            # Report the selected encoder
            self.report_encoder(
                data[col_name], col_info, encoder, col_info.columnIndex in self.config.required_features
            )

            # Track the origin of each encoded column
            self.update_encoded_to_original_map(list(transformed_col.columns), col_info.name)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform the columns of a dataset using the encoders found during the fitting stage. Transformations are
        performed in parallel where possible to improve performance.

        Args:
            data (pd.DataFrame): The dataset to transform using the fitted encoders.

        Returns:
            pd.DataFrame: The transformed dataset.

        """
        # Sort the encoders into groups which can be applied in parallel and serially based on their expected memory
        # usage
        parallel_encoders, serial_encoders = sort_encoders(self.encoders)

        # Apply the low memory encoders in parallel
        with concurrent.futures.ProcessPoolExecutor(max_workers=CONF.THREADS) as executor:
            encoding_tasks = [
                executor.submit(encoder.transform, data[col_name])
                for col_name, encoder in parallel_encoders.items()
                if col_name in data.columns  # The user may not supply some columns if they were dropped during fitting
            ]
            # Wait for the completion of all transformations and concatenate the results
            data_encoded: List[pd.DataFrame] = [task.result() for task in encoding_tasks]

        # Apply the high memory encoders serially
        for col_name, encoder in serial_encoders.items():
            if col_name in data.columns:  # The user may not supply some columns if they were dropped during fitting
                data_encoded.append(encoder.transform(data[col_name]))

        return pd.concat(data_encoded, axis=1)
