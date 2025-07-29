"""This module implements a class providing methods to construct and find
a solution in a search space for categorical and float encoders.
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from itertools import product
from typing import Dict, List, Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import ColumnInfo, DetectedType, MlTask
from evoml_utils.convertors.detected_types import to_float_column

from evoml_preprocessor.preprocess.models import (
    CategoricalEncoder,
    ColumnOptions,
    ImputeStrategy,
    ImputeValue,
    NumericEncoder,
    ScalerEncoder,
)
from evoml_preprocessor.preprocess.models.report import Encoder, GenericOption, Scaler
from evoml_preprocessor.preprocess.transformers import CategoricalTransformer, FloatTransformer, Transformer

# Module
from evoml_preprocessor.search.encoder_space import EncoderSpace
from evoml_preprocessor.search.opt_heuristic import heuristic_selector_categorical, heuristic_selector_numeric
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr
from evoml_preprocessor.utils.sample import get_sample

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")

CONF = conf_mgr.preprocess_conf  # Alias for readability

DEFAULT_CATEGORICAL_ENCODERS = {
    CategoricalEncoder.ONE_HOT_ENCODER,
    CategoricalEncoder.HASH_ENCODER,
    CategoricalEncoder.HELMERT_ENCODER,
    CategoricalEncoder.BACKWARD_DIFFERENCE_ENCODER,
    CategoricalEncoder.TARGET_ENCODER,
    CategoricalEncoder.CAT_BOOST_ENCODER,
}

DEFAULT_NUMERIC_ENCODERS = {
    NumericEncoder.POWER_ENCODER,
    NumericEncoder.QUANTILE_TRANSFORM_ENCODER,
    GenericOption.NONE,
}

DEFAULT_SCALERS = {
    ScalerEncoder.STANDARD_SCALER,
    ScalerEncoder.MIN_MAX_SCALER,
    ScalerEncoder.ROBUST_SCALER,
    ScalerEncoder.MAX_ABS_SCALER,
}

CATEGORICAL_CHECK_1 = {
    CategoricalEncoder.CAT_BOOST_ENCODER,
    CategoricalEncoder.TARGET_ENCODER,
}

CATEGORICAL_CHECK_2 = {
    CategoricalEncoder.ONE_HOT_ENCODER,
    CategoricalEncoder.HELMERT_ENCODER,
    CategoricalEncoder.BACKWARD_DIFFERENCE_ENCODER,
}

# ──────────────────────────────────────────────────────────────────────────── #


class EncoderSelector:
    """EncoderSelector builds a search space of combinations of encoders and scalers
    for categorical and float columns, and search for the optimal combinations for the
    whole dataset using either Genetic Algorithm or rule-based selection.
    """

    def __init__(
        self,
        column_options: Dict[int, ColumnOptions],
        label: pd.Series,
        ml_task: MlTask,
        config_models: List[str],
    ):
        self.column_options = column_options
        self.ml_task = ml_task
        self.config_models = config_models
        self.search_space: Dict[str, Dict[str, dict]] = {}
        self.data_label: pd.Series = label
        self.data_to_search: List[pd.Series] = []

        # dictionary that maps a column to an EncoderSpace, so that we can
        # either populate a search space, or determine which columns need
        # heuristic selection
        self.numerical_columns: Dict[str, EncoderSpace] = {}
        self.categorical_columns: Dict[str, EncoderSpace] = {}

    # --------------------------- static methods for building search space ---------------------------- #

    @staticmethod
    def _build_search_space(
        numerical_columns: dict, categorical_columns: dict, data_to_search: pd.DataFrame, label: pd.Series
    ) -> Dict[str, Dict[str, dict]]:
        """Utility function to build the search space from column info."""

        search_space: Dict[str, Dict[str, dict]] = {}

        for col_name, col_info in {**numerical_columns, **categorical_columns}.items():
            search_space[col_name] = {}
            scalers_to_use = col_info.scalers if col_info.scalers is not None else [None]

            for encoder, scaler in product(col_info.encoders, scalers_to_use):
                EncoderSelector._join_feature_space(
                    col_info=col_info.col_info,
                    encoder=encoder,
                    scaler=scaler,
                    impute_strategy=col_info.impute_strategy,
                    impute_value=col_info.impute_value,
                    data_to_search=data_to_search,
                    label=label,
                    search_space=search_space,
                )
        return search_space

    @staticmethod
    def _join_feature_space(
        col_info: ColumnInfo,
        encoder: Encoder,
        data_to_search: pd.DataFrame,
        label: pd.Series,
        search_space: Dict[str, Dict[str, dict]],
        impute_strategy: ImputeStrategy,
        scaler: Optional[Scaler] = None,
        impute_value: Optional[ImputeValue] = None,
    ) -> None:
        """Helper function to transform a column using specified encoder and scaler, and
        add the result with all the information to the search space.
        Args:
            col_info:
                Information for the column.
            encoder:
                The encoder to use.
            scaler:
                The scaler to use.
            impute_strategy:
                The imputation strategy to use.
            impute_value:
                The imputation value to use.
            sample:
                The sample data.
            search_space:
                The search space to add the transformed data to.
        Returns:
            None
        """
        if col_info.detectedType == DetectedType.categorical:
            transformer = CategoricalTransformer(
                encoder=encoder,
                scaler=scaler,
                impute_strategy=impute_strategy,
                impute_value=impute_value,
            )
        elif col_info.detectedType == DetectedType.float:
            transformer = FloatTransformer(
                encoder=encoder,
                scaler=scaler,
                impute_strategy=impute_strategy,
                impute_value=impute_value,
            )
        else:
            raise ValueError(f"Column type {col_info.detectedType} is not supported by search space!")

        method = f"{encoder}:{scaler}"

        transformed_col = transformer.fit_transform(data_to_search.loc[:, col_info.name], label)
        search_space[col_info.name][method] = {
            "transformer": transformer,
            "transformed_col": transformed_col,
        }

    # --------------------------- adding features ---------------------------- #
    def include_float_feature(self, col_data: pd.Series, col_info: ColumnInfo) -> None:
        """A helper function to include a float column of data for which the encoder/scaler
        need to be optimised. It first determines which transformations are illegible for
        the data, then adds all combinations to the search space for search later.

        Args:
            col_data: data of the column
            col_info: information for the column
        Returns:
            None
        """
        # append data to our search
        self.data_to_search.append(col_data)

        # retrieve user selected options, if no options provided we use default column options
        options = self.column_options.get(col_info.columnIndex, ColumnOptions())
        encoders = options.encoder if options.encoder is not None else [GenericOption.AUTO]
        scalers = options.scaler if options.scaler is not None else [GenericOption.AUTO]

        temp = col_data

        # select encoders used in the search
        if encoders[0] == GenericOption.AUTO:

            # TODO: temp encoding - workaround as we need numeric values to calc stats
            if col_info.baseType.name == "string" and col_data.dtype != float:
                temp = to_float_column(temp)

            # consider all default encoders
            encoders = list(DEFAULT_NUMERIC_ENCODERS)
            # add log encoder is all_positive
            if (temp >= 0).all():
                encoders.append(NumericEncoder.LOG_ENCODER)
            # add reciprocal encoder if there are no zeros
            if not (temp == 0).any():
                encoders.append(NumericEncoder.RECIPROCAL_ENCODER)
        else:
            # TODO: temp encoding - workaround as we need numeric values to calc stats
            if col_info.baseType.name == "string" and col_data.dtype != float:
                temp = to_float_column(temp)

            # verify check user selected options are valid
            if NumericEncoder.LOG_ENCODER in encoders:
                # ensure all_positive
                if not (temp >= 0).all():
                    encoders.remove(NumericEncoder.LOG_ENCODER)
                    logger.warning(
                        f"{col_info.name} column - user defined invalid (numeric) encoder(s). "
                        f"{str(NumericEncoder.LOG_ENCODER)} have been removed from further processing",
                    )
            if NumericEncoder.RECIPROCAL_ENCODER in encoders:
                # ensure there are no zeros
                if (temp == 0).any():
                    encoders.remove(NumericEncoder.RECIPROCAL_ENCODER)
                    logger.warning(
                        f"{col_info.name} column - user defined invalid (numeric) encoder(s). "
                        f"{str(NumericEncoder.RECIPROCAL_ENCODER)} have been removed from further processing",
                    )

        # consider all default encoders
        if scalers[0] == GenericOption.AUTO:
            scalers = list(DEFAULT_SCALERS)

        if not isinstance(encoders, list):
            encoders = [encoders]

        if not isinstance(scalers, list):
            scalers = [scalers]

        # append data to our search
        self.data_to_search.append(col_data)

        # build the search space
        self.numerical_columns[col_info.name] = EncoderSpace(
            col_info=col_info,
            encoders=encoders,
            scalers=scalers,
            impute_strategy=options.imputeStrategy,
            impute_value=options.imputeValue,
        )

    def include_categorical_feature(self, col_data: pd.Series, col_info: ColumnInfo):
        """A helper function to include a categorical column of data for which the encoder/scaler
        need to be optimised. It first determines which transformations are illegible for
        the data, then adds all combinations to the search space for search later.

        Args:
            col_data: data of the column
            col_info: information for the column
        Returns:
            None
        """
        # retrieve user selected encoders
        options = self.column_options.get(col_info.columnIndex, ColumnOptions())
        encoders = options.encoder

        if not isinstance(encoders, list):
            encoders = [encoders]

        user_selected_encoder = encoders

        # select all encoders if auto was selected
        if encoders is None or encoders and encoders[0] == GenericOption.AUTO:
            encoders = list(DEFAULT_CATEGORICAL_ENCODERS)

        # filter encoders to ensure we only select valid encoders
        encoders = self._get_valid_categorical_encoders(encoders, col_info, user_selected_encoder)

        # append data to our search
        self.data_to_search.append(col_data)

        # build the search space
        self.categorical_columns[col_info.name] = EncoderSpace(
            col_info=col_info,
            encoders=encoders,
            scalers=None,
            impute_strategy=options.imputeStrategy,
            impute_value=options.imputeValue,
        )

    def _get_valid_categorical_encoders(
        self,
        encoders: List[CategoricalEncoder],
        col_info: ColumnInfo,
        user_selected_encoder: List[CategoricalEncoder],
    ) -> List[CategoricalEncoder]:
        """A helper function to determine which encoders are valid.
        Args:
            encoders:
                The list of encoders to validate.
            col_info:
                Allows us to check whether the column has too many unique values.
        Returns:
            List[CategoricalEncoder]:
                A list of valid encoders.
        """
        too_many_unique = col_info.statsUniqueValuesCount > CONF.ONE_HOT_ENCODING_THRESHOLD

        modified_encoder_list = [
            encoder
            for encoder in encoders
            if not (
                (encoder in CATEGORICAL_CHECK_1 and self.ml_task == MlTask.classification)
                or (encoder in CATEGORICAL_CHECK_2 and too_many_unique)
            )
        ]

        # If no valid encoder is selected, use HASH_ENCODER if too many unique values else ONE_HOT_ENCODER
        if not modified_encoder_list:
            modified_encoder_list = [
                CategoricalEncoder.HASH_ENCODER if too_many_unique else CategoricalEncoder.ONE_HOT_ENCODER
            ]

        # log warning if user selected encoders have not been selected
        if user_selected_encoder is not None and user_selected_encoder != [GenericOption.AUTO]:
            difference = set(user_selected_encoder) - set(modified_encoder_list)
            if len(difference) > 0:
                raise ValueError(
                    "Invalid encoders have been detected in your selection. \n"
                    f"Invalid encoders: {', '.join(user_selected_encoder)}\n"
                )

        return modified_encoder_list

    # --------------------------- specifying optimiser ---------------------------- #

    def create_sample_data(self, encoded_label):
        sampled_index = get_sample(encoded_label, task=self.ml_task)
        sample_label = encoded_label.loc[sampled_index]
        sample_data_to_search = pd.DataFrame({str(data.name): data.loc[sampled_index] for data in self.data_to_search})
        return sampled_index, sample_label, sample_data_to_search

    def get_optimised_encoders(
        self, encoded_label: pd.Series, data_encoded: Optional[pd.DataFrame] = None
    ) -> Dict[str, Transformer]:
        """Main function of this class to run the selection and get the results.
        It uses self.optimise_selection unless there are too many columns, in which case
        it falls back to a rule-based system.
        Args:
            encoded_label:
                The encoded label column
            data_encoded:
                The encoded dataset (all other column types not considered in the search e.g. integer)
        Returns:
            Dict[str, Transformer]:
                A dictionary of the best Transformer class for each column.
        """

        if not self.data_to_search:
            return {}

        sampled_index, sample_label, sample_data_to_search = self.create_sample_data(encoded_label)

        if len(self.numerical_columns) + len(self.categorical_columns) > CONF.MAX_SEARCH_FEATURES:
            return self.heuristic_selection(sample_label, sample_data_to_search)

        sample_data_encoded = data_encoded.loc[sampled_index]

        return self.optimise_selection(sample_label, sample_data_to_search, sample_data_encoded)

    def optimise_selection(
        self, label: pd.Series, data_to_search: pd.DataFrame, data: pd.DataFrame
    ) -> Dict[str, Transformer]:
        """Using Genetic Algorithm (EncoderSearchEngine) to find the optimal encoders for
        float and categorical columns.
        Args:
            label:
                The encoded label column
            data_to_search:
                The base dataset that will be joined with the data under search.
            data:
                Encoded columns forming this rest of the dataset, this is useful so we can search for the best encoder using all encoded columns
        Returns:
            Dict[str, Transformer]:
                A dictionary of the best Transformer class for each column.
        """

        self.search_space = EncoderSelector._build_search_space(
            self.numerical_columns, self.categorical_columns, data_to_search, label
        )

        # Will only search for optimal encoders if there is at least one column
        # with a non-empty search space
        search_sizes = [len(space) for space in self.search_space.values()]

        logger.info("→ start search-based encoder selection")

        # edge case, if there's only one choice, don't run the optimizer and
        # just set the transformers accordingly
        optimal_encoders = {}
        search_sizes = list(filter(lambda x: x > 1, search_sizes))  # remove ones
        if not search_sizes:
            for col, encodings in self.search_space.items():
                for transformer in encodings.values():
                    optimal_encoders[col] = transformer["transformer"]
            logger.info("→ complete encoder selection - no search required")
            return optimal_encoders

        # Optuna start
        from evoml_preprocessor.search.opt_optuna import EncoderSearchOptuna

        # Run search to find optimal encoders for float and categorical
        optuna_search = EncoderSearchOptuna(
            self.search_space,
            data,
            label,
            self.ml_task,
            self.config_models,
        )
        optimal_encoders = optuna_search.search()

        logger.info("→ complete search-based encoder selection")

        return optimal_encoders

    def heuristic_selection(self, label: pd.Series, sample_data_to_search: pd.DataFrame) -> Dict[str, Transformer]:
        """A heuristic to select the optimal encoders for float and categorical
        columns. This is used when the number of columns is greater than
        CONF.MAX_SEARCH_FEATURES.
        Returns:
            Dict[str, Transformer]:
                A dictionary of the best Transformer class for each column.
        """

        optimal_encoders = {}

        logger.info("→ start rule-based encoder selection")

        numeric_data = sample_data_to_search.loc[:, self.numerical_columns.keys()]
        categorical_data = sample_data_to_search.loc[:, self.categorical_columns.keys()]

        optimal_encoders.update(
            heuristic_selector_numeric(
                numeric_data,
                self.numerical_columns,
                label,
            )
        )
        optimal_encoders.update(
            heuristic_selector_categorical(
                categorical_data,
                self.categorical_columns,
            )
        )

        logger.info("→ complete rule-based encoder selection")

        return optimal_encoders
