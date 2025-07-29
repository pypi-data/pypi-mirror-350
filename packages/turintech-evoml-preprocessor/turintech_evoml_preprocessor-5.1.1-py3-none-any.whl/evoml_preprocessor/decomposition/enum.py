from enum import Enum
from typing import Dict

from evoml_preprocessor.utils.string_enum import StrEnum


class DimReduction(StrEnum):
    """Generic options for all modules."""

    SVD = "svd"
    PCA = "pca"
    ICA = "ica"

    def get_full_name(self) -> str:
        full: Dict[str, str] = {
            DimReduction.SVD: "Singular Value Decomposition",
            DimReduction.PCA: "Principal Component Analysis",
            DimReduction.ICA: "Independent Component Analysis",
        }
        return full[self.value]
