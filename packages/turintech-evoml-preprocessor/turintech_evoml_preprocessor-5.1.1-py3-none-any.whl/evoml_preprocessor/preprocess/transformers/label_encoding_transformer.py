# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, List, Optional, Set, Union

# Dependencies
import numpy as np
import pandas as pd
from evoml_api_models import BaseTypes, DetectedType
from sklearn.preprocessing import LabelEncoder

# Module
from evoml_preprocessor.preprocess.models import Block, GenericOption, ImputeStrategy
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions
from evoml_preprocessor.preprocess.models.report import TransformationBlock
from evoml_preprocessor.preprocess.transformers._base import Transformer
from evoml_preprocessor.preprocess.transformers.scalers.identity_scaler import IdentityScaler
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class LabelEncodingTransformer(Transformer):
    """
    The missing data is first imputed then an 'unseen' type label is added
    to handle the unseen data in the test data set, followed by the label
    encoding scheme from sklearn API.
    """

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
    ):
        super().__init__(column_info, encoder, scaler, impute_strategy, impute_value, derived_columns)

        self._encoder: Optional[LabelEncoder] = None
        self.scaler = IdentityScaler()
        self.train_unique: Set[str] = set()
        self.unseen = "~unseen"
        self.impute_setting = DetectedType.categorical
        self.base_type = BaseTypes.string
        self.na_replacement: Optional[int] = None

        if self.impute_strategy in [None, ImputeStrategy.AUTO]:
            self.impute_strategy = ImputeStrategy.CONSTANT

    def inverse_transform(self, transformed_data: pd.Series[Any]) -> pd.Series[Any]:
        """Decodes an encoded label column into the original label space."""
        assert self.encoder is not None, "Call `fit_transform` before calling this method"
        np_data = transformed_data.to_numpy().astype(np.int64)

        np_inverse_transformed: np.ndarray = self.encoder.inverse_transform(np_data)  # type: ignore

        # There is always an `unseen` label which forced the type of original
        # space to string. We'd like to keep the original type when `unseen` is
        # not present.
        has_unseen = self.unseen in np_inverse_transformed
        if not has_unseen and self.base_type == BaseTypes.integer:
            np_inverse_transformed = np_inverse_transformed.astype(np.int64)
        elif not has_unseen and self.base_type == BaseTypes.float:
            np_inverse_transformed = np_inverse_transformed.astype(np.float64)

        return pd.Series(
            np_inverse_transformed,
            name=transformed_data.name,
            index=transformed_data.index,
        )

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if data.dtype is not str:
            if self.encoder_slug != GenericOption.NONE and self.base_type == BaseTypes.integer and data.dtype != int:
                # ensures 1.0 and 1 are converted to 1; if there are nans in data
                # this assumes that `_convert` is called in `fit` ONCE and then `transform` `n` many times
                if self.na_replacement is None:
                    self.na_replacement = max(data.loc[~data.isna()].unique()) + 1
                data.replace(np.nan, self.na_replacement, inplace=True)
                data = data.astype(np.int64)

            data = data.astype(str)
        return data

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:
        """Encoder for label encoding

        Encode data such that the transformed data is of the form [0, 1, 2, ...]

        `LabelEncoder` expects data to be of shape (n)

        We also want to handle
        - unseen data in the test data set
        - None values in the data set

        Both of these ought to be encoded differently

        `LabelEncoder` can handle everything except for unseen values

        The order of encoded values is [0, 1, 2, ..., enc('unseen'), enc(None)]
        where enc('unseen') would be `n-1` and enc(None) would be `n`, and
        `n` is the unique number of encoded values in the training data set

        @TODO: output here is a numpy array, ought to be shape (n, 1) in line
        with the other transformers but is currently (n,) to pass unit tests

        Args:
            data: The data to be encoded
            label: The label to be encoded

        Returns:
            np.ndarray: The encoded data
        """

        if isinstance(data, pd.DataFrame):
            raise NotImplementedError(
                "This method is not yet implemented for DataFrame input, since unique is not defined for DataFrames."
            )

        if self.encoder_slug == GenericOption.NONE:
            return data.to_frame()

        if not self.fitted:
            self._encoder = LabelEncoder()
            data_np = self.encoder.fit_transform(data.to_numpy())

            # add unseen values, this won't work in the case where one of the classes happens
            # overlap with our internal unseen label
            classes_ = self.encoder.classes_
            if not isinstance(classes_, np.ndarray):
                classes_np = np.array(classes_)
            else:
                classes_np = classes_
            self.train_unique = set(classes_np)

            if self.unseen in classes_np:
                logger.warning(
                    f"{self.unseen} is in the target, but we use this as a catch-all case, this may produce unexpected"
                    " results!"
                )

            updated_values = np.append(classes_np, self.unseen)
            self.encoder.classes_ = np.unique(updated_values)

            return pd.Series(data_np, name=str(data.name), index=data.index).to_frame()
        else:
            test_unique = set(data.unique())
            unseen_category = test_unique - self.train_unique
            if unseen_category:
                data[data.isin(list(unseen_category))] = self.unseen

            data_np = self.encoder.transform(data.to_numpy())

        return pd.Series(data_np, name=str(data.name), index=data.index, dtype=np.int64).to_frame()

    def _report(self) -> None:
        self.transformation_block.append(
            TransformationBlock(
                block_name=Block.LABEL_ENCODING,
                encoder_name=self.encoder_slug,
                scaler_name=None,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )

    @property
    def encoder(self) -> LabelEncoder:
        if self._encoder is None:
            raise AttributeError("The encoder must be set during fitting.")
        return self._encoder
