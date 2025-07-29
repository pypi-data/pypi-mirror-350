"""Implements the generic split data interface using an algorithm splitting by
subset
"""

import logging
from functools import partial

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from typing import Optional

# Dependencies
import pandas as pd

# Private Dependencies
from evoml_api_models import ColumnInfo, DetectedType, MlTask
from evoml_utils.convertors.detected_types import to_datetime_column

# Module
from evoml_preprocessor.preprocess.models import SplitMethod
from evoml_preprocessor.splitting.interface import DataSplitting, SplitData, splitting_factory

# ──────────────────────────────────────────────────────────────────────────── #


logger = logging.getLogger("preprocessor")


class SubsetSplit(DataSplitting):
    """Splitting factory for the subset splitting method
    TODO: this option was removed from the UI, but we still need to re-evaluate and enable it
    """

    def split(
        self,
        data: pd.DataFrame,
        label_name: str,
        ml_task: MlTask,
        ref_column: Optional[ColumnInfo],
        keep_order: bool = False,
        test_data: Optional[pd.DataFrame] = None,
        index_name: Optional[str] = None,
    ) -> SplitData:
        """splitting dataset train/test files based on a reference column"""
        assert ref_column is not None
        assert ref_column.name == self.options.subsetColumnName

        # Renaming options for convenience
        train_from = self.options.trainRangeFrom
        train_to = self.options.trainRangeTo
        test_from = self.options.testRangeFrom
        test_to = self.options.testRangeTo

        logger.info("Splitting using train/test range on reference column %s", ref_column.name)
        logger.info("→ train dataset from indices %s to %s", train_from, train_to)
        logger.info("→ test dataset from indices %s to %s", test_from, test_to)

        if ref_column.detectedType == DetectedType.datetime:
            converted_col_name = f"{ref_column.name}_converted"
            if ref_column.metadata is None:
                raise ValueError("Conversion metadata is required if the reference column is of datetime type.")

            # For backwards compatibility with datasets analysed using evoml-type-detector<=1.8.1 we must check the contents
            # of the column metadata and call the conversion function correctly.
            if "dateTimeOrder" in ref_column.metadata:
                # The old format is present. This is deprecated but still supported.
                converted_col = to_datetime_column(
                    data[ref_column.name], datetime_order=ref_column.metadata["dateTimeOrder"]
                )
            else:
                # The new format is present.
                converted_col = to_datetime_column(data[ref_column.name], **ref_column.metadata["to_datetime_kwargs"])

            # Figure out train/test ranges
            min_time = data[converted_col_name].min()
            max_time = data[converted_col_name].max()

            from dateutil import parser

            parse = partial(parser.parse, ignoretz=True)  # shortcut

            # Handle special ranges (MIN/MAX)
            # @TODO: improve the validation of the models to indicate that we
            # expect a parsable date (str?) or some specific litterals MIN/MAX
            train_from = min_time if train_from == "MIN" else parse(train_from)
            train_to = max_time if train_to == "MAX" else parse(train_to)
            test_from = min_time if test_from == "MIN" else parse(test_from)
            test_to = max_time if test_to == "MAX" else parse(test_to)

            data_train = data.loc[(converted_col >= train_from) & (converted_col <= train_to)]
            data_test = data.loc[(converted_col >= test_from) & (converted_col <= test_to)]

            # Add the converted column after selection to make sure we don't
            # have it in the test/train data
            # @TODO: do we really need to have the converted column in the
            # dataset 'data'?
            data[converted_col_name] = converted_col

        else:
            # Figure out train/test ranges
            min_value = data[ref_column.name].min()
            max_value = data[ref_column.name].max()

            # Handle special ranges (MIN/MAX)
            train_from = min_value if train_from == "MIN" else float(train_from)
            train_to = max_value if train_to == "MAX" else float(train_to)
            test_from = min_value if test_from == "MIN" else float(test_from)
            test_to = max_value if test_to == "MAX" else float(test_to)

            data_train = data.loc[(data[ref_column.name] >= train_from) & (data[ref_column.name] <= train_to)]
            data_test = data.loc[(data[ref_column.name] >= test_from) & (data[ref_column.name] <= test_to)]

        return SplitData(train=data_train, test=data_test)


splitting_factory.register(SplitMethod.subset, SubsetSplit)
