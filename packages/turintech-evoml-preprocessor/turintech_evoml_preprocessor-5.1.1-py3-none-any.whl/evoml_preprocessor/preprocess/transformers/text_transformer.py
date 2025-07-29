"""
This module contains the TextTransformer class,
which parses strings to create embedding vectors.

Each TextTransformer uses an embedding process, and a decomposition algorithm.

There are two embedding processes:
- tfidf (https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- huggingface sentence transformers (https://huggingface.co/sentence-transformers)

The only decomposition algorithm available is:
- truncated SVD (https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html#sklearn.decomposition.TruncatedSVD)
- kernel PCA was previously offered however due to the algorithms inherent scaling
 as input size increases (in the worst case O(N^3)) it had to be disabled as medium
 row count interesting datasets were just hanging when it came to dimensionality reduction
 with default settings.

Further information on decomposition: (https://scikit-learn.org/stable/modules/decomposition.html)

Typical usage example:
    > data = pd.read_csv(csv_filepath)
    > text_transformer = TextTransformer(column_infos=infos, encoder=encoder)
    > embedding = text_transformer.fit_transform(data)

Contact the NLP team for help.
"""

# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, Dict, List, Optional

# Dependencies
import numpy as np
import pandas as pd

# Private Dependencies
from evoml_api_models import DetectedType
from scipy.sparse import spmatrix
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

# Module
from evoml_preprocessor.nlp.huggingface import HuggingFaceWrapper
from evoml_preprocessor.nlp.nlp_preprocessing import preprocess_text
from evoml_preprocessor.preprocess.models import Block, EmbeddingTransformer
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import AllEncoders, AllScalers, DateOptions, ImputeStrategy
from evoml_preprocessor.preprocess.models.report import GenericOption, TransformationBlock
from evoml_preprocessor.preprocess.transformers import Transformer
from evoml_preprocessor.preprocess.transformers.scalers.identity_scaler import IdentityScaler
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #

# TODO: test performance on non-DL ML models in evoml development frontend once this code is pushed
# run on 5-10 datasets with current text embedding and then push code to develop and run with new


class TextTransformer(Transformer):
    """
    Parses strings to create embedding vectors.
    """

    encoder_slug: AllEncoders
    scaler_slug: AllScalers

    # TODO: save unfitted pre-trained models in class, and when fitting make copy & save in instance

    # TODO: look at: max sequence length, dimensions of embedding vector,
    # dimensionality reduction, training data
    # Models have method get_max_seq_length()

    # TODO: make all transformers accessible through huggingface API,

    # TODO: implement domain-specific pre-trained transformers

    # ---------------------------------------------------------------------------------------------#
    # --- INHERITANCE METHODS
    # ---------------------------------------------------------------------------------------------#

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
        output_size: Optional[int] = None,
        device: Optional[str] = None,
    ):
        super().__init__(column_info, encoder, scaler, impute_strategy, impute_value, derived_columns)

        self.output_size = output_size
        self.impute_setting = DetectedType.text
        self.device = device
        self._decomposition_model = None
        self.block = Block.TEXT
        self.scaler = IdentityScaler()
        # ------------------------------------ AUTO settings ---------------------------------- #

        if self.encoder_slug == GenericOption.AUTO or self.encoder_slug is None:
            self.encoder_slug = EmbeddingTransformer.ALL_MINI_LM_L6_V2

        # -------------------------------------- settings ------------------------------------- #

        # TODO: should autodetect languages, text length,
        # domain (medical, law, finance, etc.), optimal transformer

        # TODO: should recommend best transformer(s)

        # instantiate the model based on the encoder_slug selected
        if self.encoder_slug == GenericOption.NONE:
            self._embedding_model = None
        elif self.encoder_slug == EmbeddingTransformer.TFIDF:
            # https: // scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
            self._embedding_model = self._tfidf_instantiator()
        else:
            self._embedding_model = self._huggingface_instantiator()

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series] = None) -> NumericArray:
        if self.encoder_slug == GenericOption.NONE:
            self.columns = [str(data.name)]
            return data.to_frame()
        if self._embedding_model is None:
            # do nothing
            # @TODO handle none cases better
            self.columns = [str(data.name)]
            return data.to_frame()

        if isinstance(data, pd.DataFrame):
            raise ValueError("TextTransformer encoder does not support multi-column data.")

        # preprocess the text data before embedding in place
        data = preprocess_text(data)

        if not self.fitted:
            # Fit and transform the data using the embedding model
            embedding = self._embedding_model.fit_transform(data)
            if self.output_size is not None and embedding.shape[1] > self.output_size > 0:
                # Reduce the dimensionality using TruncatedSVD if necessary
                self._decomposition_model = self._truncated_svd_instantiator(output_size=self.output_size)
                self._decomposition_model.fit(embedding)
                embedding = self._decomposition_model.transform(embedding)
        else:
            # Transform the data using the fitted embedding model
            embedding = self._embedding_model.transform(data)

            if self._decomposition_model is not None:
                # Reduce the dimensionality using the fitted decomposition model
                embedding = self._decomposition_model.transform(embedding)

        # tfidf returns a sparse matrix, not of type np.ndarray. TruncatedSVD fixes this,
        # however it might not be called if embedding dimensionality < output_size dimensionality
        # therefore, we must force it here to avoid problems when creating the dataframe
        if self.encoder_slug == EmbeddingTransformer.TFIDF and isinstance(embedding, spmatrix):
            # @pyright: doesn't understand that after calling issparse we are sure that the embedding has a todense method.
            embedding = pd.DataFrame(np.asarray(embedding.todense().tolist()), index=data.index)  # type: ignore
            self.columns = [f"{data.name}_embedding_{i}" for i in range(embedding.shape[1])]
            embedding.columns = self.columns
        else:
            embedding = pd.DataFrame(embedding, index=data.index)
            self.columns = [f"{data.name}_embedding_{i}" for i in range(embedding.shape[1])]
            embedding.columns = self.columns

        return embedding

    def _report(self) -> None:
        self.transformation_block.append(
            TransformationBlock(
                block_name=self.block,
                encoder_name=self.encoder_slug,
                scaler_name=None,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )

    def _truncated_svd_instantiator(self, output_size: int) -> TruncatedSVD:
        """Returns an instantiated truncated SVD model.

           The decomposition process model to reduce the dimensionality of the embedding
           https://scikit-learn.org/stable/modules/decomposition.html
           only Truncated SVD supported due to performance requirements on medium-large
           datasets.

           (https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html#sklearn.decomposition.TruncatedSVD)

        Returns:
            TruncatedSVD:
                An instantiated truncated SVD model.
        """
        model = TruncatedSVD(
            n_components=output_size,
            n_iter=7,
            random_state=3,
        )
        return model

    # ---------------------------------------------------------------------------------------------#
    # ---- TFIDF EMBEDDING PROCESS INSTANTIATORS
    # ---------------------------------------------------------------------------------------------#
    def _tfidf_instantiator(self) -> TfidfVectorizer:
        """
        Instantiates a TfidVectorizer.

        (https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)

        Returns:
            TfidfVectorizer:
                The TfidVectorizer used for the embedding process.
        """
        return TfidfVectorizer()

    def _huggingface_instantiator(self) -> HuggingFaceWrapper:

        if self.encoder_slug not in list(EmbeddingTransformer):
            raise ValueError(f"Encoder {self.encoder_slug} is invalid.")

        return HuggingFaceWrapper(self.encoder_slug, self.device)

    # ---------------------------------------------------------------------------------------------#
    # ---- MODEL DUMP MANAGEMENT
    # ---------------------------------------------------------------------------------------------#

    def __getstate__(self) -> Dict[str, Any]:
        values = self.__dict__.copy()
        if self.encoder_slug != EmbeddingTransformer.TFIDF:
            del values["_embedding_model"]
        return values

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__ = state
        if self.encoder_slug == GenericOption.NONE:
            self._embedding_model = None
        elif self.encoder_slug == EmbeddingTransformer.TFIDF:
            self._embedding_model = state["_embedding_model"]
        else:
            self._embedding_model = self._huggingface_instantiator()
