# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging

# Dependencies
import pandas as pd


# Private Dependencies

# Module
from evoml_preprocessor.nlp.enum import NLPFuncRepresentation
from evoml_preprocessor.nlp.nlp_utils import run_utils_functions

# ──────────────────────────────────────────────────────────────────────────── #

# Logger
logger = logging.getLogger("preprocessor")

# ──────────────────────────────────────────────────────────────────────────── #


def preprocess_text(text: pd.Series) -> pd.Series:
    """
    Preprocess text data in place using a chain of utils functions.
    :param text: text data
    :return: preprocessed text data
    """

    text_copy = text.copy()

    utils_functions = [
        NLPFuncRepresentation.STRIP,
        NLPFuncRepresentation.TO_LOWER,
        # NLPFuncRepresentation.REMOVE_STOPWORDS,
        NLPFuncRepresentation.REMOVE_NUMBERS,
        NLPFuncRepresentation.REMOVE_PUNCTUATION,
        NLPFuncRepresentation.REMOVE_CHARS,
        NLPFuncRepresentation.REMOVE_CONSECUTIVE_SPACES,
    ]

    clean_text = text_copy.apply(lambda x: run_utils_functions(x, utils_functions))
    return clean_text
