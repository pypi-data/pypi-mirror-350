# ───────────────────────────────── imports ────────────────────────────────── #
from __future__ import annotations

# Standard Library
import logging
from typing import Any, Dict, List, Optional, Union

# Dependencies
import numpy as np
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from evoml_api_models import DetectedType
from evoml_utils.convertors.detected_types import to_protein_sequence_column
from sklearn.decomposition import TruncatedSVD

# Module
from evoml_preprocessor.nlp.huggingface import HuggingFaceWrapper
from evoml_preprocessor.preprocess.models import Block
from evoml_preprocessor.preprocess.models.config import ColumnInfo, ImputeValue
from evoml_preprocessor.preprocess.models.enum import (
    AllEncoders,
    AllScalers,
    DateOptions,
    EmbeddingTransformer,
    ImputeStrategy,
    ProteinEmbeddingTransformer,
)
from evoml_preprocessor.preprocess.models.report import GenericOption, TransformationBlock
from evoml_preprocessor.preprocess.transformers import Transformer
from evoml_preprocessor.preprocess.transformers.scalers.identity_scaler import IdentityScaler
from evoml_preprocessor.types.numpy import NumericArray

# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# ──────────────────────────────────────────────────────────────────────────── #


class ProteinSequenceTransformer(Transformer):
    """
    Parses protein to create embedding vectors.
    """

    encoder_slug: AllEncoders
    scaler_slug: AllScalers

    def __init__(
        self,
        column_info: Optional[ColumnInfo] = None,
        encoder: Optional[AllEncoders] = None,
        scaler: Optional[AllScalers] = None,
        impute_strategy: ImputeStrategy = ImputeStrategy.AUTO,
        impute_value: Optional[ImputeValue] = None,
        derived_columns: Optional[List[DateOptions]] = None,
        output_size: int = 100,
        device: Optional[str] = None,
    ):
        super().__init__(column_info, encoder, scaler, impute_strategy, impute_value, derived_columns)

        self.output_size = output_size
        self.transformation_block: List[TransformationBlock] = []
        self.impute_setting = DetectedType.protein_sequence
        self.device = device
        self._embedding_model = None
        self.block = Block.PROTEIN_SEQUENCE
        self.scaler = IdentityScaler()

        # ------------------------------------ AUTO settings ---------------------------------- #

        if self.encoder_slug == GenericOption.AUTO or self.encoder_slug is None:
            self.encoder_slug = ProteinEmbeddingTransformer.PROT_BERT

        # -------------------------------------- settings ------------------------------------- #

        # instantiate the model based on the encoder_slug selected
        if self.encoder_slug is not GenericOption.NONE:
            self._embedding_model = self._huggingface_instantiator()

        # The decomposition process model to reduce the dimensionality of the embedding
        # https://scikit-learn.org/stable/modules/decomposition.html
        # only Truncated SVD supported due to performance requirements on medium-large
        # datasets.
        if self._embedding_model is not None:
            self._decomposition_model = self._truncated_svd_instantiator()

    def _convert(self, data: pd.Series[Any]) -> pd.Series[Any]:
        if self.encoder_slug == GenericOption.NONE:
            return data
        return to_protein_sequence_column(data)

    def _encode(self, data: pd.Series[Any], label: Optional[pd.Series[Any]] = None) -> NumericArray:
        if self.encoder_slug == GenericOption.NONE:
            self.columns = [str(data.name)]
            return data.to_frame()
        if self._embedding_model is None:
            # do nothing
            # @TODO handle none cases better
            self.columns = [str(data.name)]
            return data.to_frame()

        if isinstance(data, pd.DataFrame):
            raise ValueError("ProteinSequenceTransformer encoder only supports single columns.")

        if not self.fitted:
            embedding = self._embedding_model.fit_transform(data)

            # Fit and transform the decomposition process
            if embedding.shape[1] > self._decomposition_model.n_components:
                # there is an issue when we try using fit_transform.
                self._decomposition_model.fit(embedding)
                embedding = self._decomposition_model.transform(embedding)

            self.columns = [f"{data.name}_embedding_{i}" for i in range(embedding.shape[1])]
        else:
            embedding = self._embedding_model.transform(data)

            # Transform the embedding with the decomposition process
            if embedding.shape[1] > self._decomposition_model.n_components:
                embedding = self._decomposition_model.transform(embedding)

        if isinstance(embedding, pd.DataFrame):
            return embedding
        raise TypeError(f"Unsupported return type: {type(embedding)}.")

    def _report(self) -> None:
        self.transformation_block.append(
            TransformationBlock(
                block_name=self.block,
                encoder_name=self.encoder_slug,
                scaler_name=self.scaler_slug,
                impute_strategy=self.impute_strategy,
                column_names=self.columns,
                column_dropped=None,
                reason_dropped=None,
            )
        )

    def _truncated_svd_instantiator(self) -> TruncatedSVD:
        """Returns an instantiated truncated SVD model.

        (https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html#sklearn.decomposition.TruncatedSVD)

        Returns:
            TruncatedSVD:
                An instantiated truncated SVD model.
        """

        model = TruncatedSVD(
            n_components=self.output_size,
            n_iter=7,
            random_state=3,
        )
        return model

    def _huggingface_instantiator(self) -> HuggingFaceWrapper:
        if not isinstance(self.encoder_slug, (EmbeddingTransformer, ProteinEmbeddingTransformer)):
            raise ValueError(
                f"The protein sequence tranasformer only supports embedding and protein embedding transformer models. Received: {self.encoder_slug}."
            )
        return HuggingFaceWrapper(self.encoder_slug, self.device)

    def _get_sequence_property(self, protein: str) -> pd.Series[Any]:
        """Get the protein properties of one protein sequence"""

        # Create a ProteinAnalysis object from the protein sequence
        protein_analysis = ProteinAnalysis(protein)

        # Calculate molecular weight
        # the sum of molecular weights of all amino acids.
        # Large proteins tend to have more complex functions than small proteins.
        # small proteins are more likely to be involved in regulatory functions/signalling
        molecular_weight = protein_analysis.molecular_weight()

        # Calculate hydrophobicity
        # positive GRAVY indicated hydrophobic protein and negative GRAVY indicated hydrophilic protein
        # hydrophobic are non-polar amino acids that do not dissolve in water
        # hydrophilic are polar amino acids that dissolve in water
        gravy = protein_analysis.gravy()

        # Calculate isoelectric point
        # the pH at which the protein has no net charge
        isoelectric_point = protein_analysis.isoelectric_point()
        charge_at_ph = protein_analysis.charge_at_pH(isoelectric_point)

        # Calculate hydrophilicity
        # tendency of a protein to undergo denaturation and aggregation
        instability_index = protein_analysis.instability_index()

        # presence if of an aromatic ring in the chain
        aromaticity = protein_analysis.aromaticity()

        # Calculate pK1
        # the charge affects the protein interaction with other molecules
        ph1 = protein_analysis.charge_at_pH(1)

        # Calculate pK2
        ph2 = protein_analysis.charge_at_pH(2)

        # Calculate secondary structure
        # beta sheets, alpha helixes, and turn
        secondary_structure_fraction = protein_analysis.secondary_structure_fraction()

        amino_count = protein_analysis.get_amino_acids_percent()
        single_entries = {
            "molecular_weight": molecular_weight,
            "gravy": gravy,
            "isoelectric_point": isoelectric_point,
            "charge_at_ph": charge_at_ph,
            "instability_index": instability_index,
            "aromaticity": aromaticity,
            "ph1": ph1,
            "ph2": ph2,
        }
        multiple_entries = {
            "beta_sheets": secondary_structure_fraction[0],
            "alpha_helixes": secondary_structure_fraction[1],
            "turn": secondary_structure_fraction[2],
        }
        single_entries_series = pd.Series(single_entries, index=list(single_entries.keys()))
        amino_entries_series = pd.Series(amino_count, index=list(amino_count.keys()))
        multiple_entries_series = pd.Series(multiple_entries, index=list(multiple_entries.keys()))

        combined_entries: pd.Series[Any] = pd.concat(
            [single_entries_series, multiple_entries_series, amino_entries_series], axis=0
        )

        return combined_entries

    def get_sequence_properties(self, protein_sequence: pd.Series[Any]) -> pd.DataFrame:
        """Get the properties of the protein sequences in the DataFrame."""

        INDEX_NAMES = [
            "molecular_weight",
            "gravy",
            "isoelectric_point",
            "charge_at_ph",
            "instability_index",
            "aromaticity",
            "ph1",
            "ph2",
            "beta_sheets",
            "alpha_helixes",
            "turn",
            "A",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "K",
            "L",
            "M",
            "N",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "V",
            "W",
            "Y",
        ]

        properties = protein_sequence.apply(self._get_sequence_property)
        properties.columns = pd.Index(INDEX_NAMES)

        return properties

    # ---------------------------------------------------------------------------------------------#
    # ---- MODEL DUMP MANAGEMENT
    # ---------------------------------------------------------------------------------------------#

    def __getstate__(self) -> Dict[str, Any]:
        values = self.__dict__.copy()
        del values["_embedding_model"]
        return values

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__ = state
        if self.encoder_slug == GenericOption.NONE:
            self._embedding_model = None
        else:
            self._embedding_model = self._huggingface_instantiator()
