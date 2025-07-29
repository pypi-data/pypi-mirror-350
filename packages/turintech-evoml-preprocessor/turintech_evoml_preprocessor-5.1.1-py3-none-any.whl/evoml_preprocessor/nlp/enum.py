from enum import Enum

from evoml_preprocessor.utils.string_enum import StrEnum


class NLPFuncRepresentation(StrEnum):
    """
    A class to represent the function name
    """

    # Mandatory Functions
    STRIP = "strip"
    TO_LOWER = "to_lower"
    REMOVE_STOPWORDS = "remove_stopwords"
    REMOVE_NUMBERS = "remove_numbers"
    REMOVE_PUNCTUATION = "remove_punctuation"
    REMOVE_CHARS = "remove_chars"
    REMOVE_CONSECUTIVE_SPACES = "remove_consecutive_spaces"

    # Optional Functions
    ABBREVIATION_CONVERTER = "abbreviation_converter"
    EXPAND_CONTRACTIONS = "expand_contractions"
    LEMMATIZE = "lemmatize"
    REMOVE_URL = "remove_url"
    REMOVE_DUPLICATION = "remove_duplication"

    # Optional Functions / HTML Functions
    REMOVE_EMAIL = "remove_email"
    REMOVE_XML = "remove_xml"

    # Optional Functions / Emoji and Emoticon Functions
    REMOVE_EMOJI = "remove_emoji"
    REMOVE_EMOTICON = "remove_emoticon"

    # Optional Functions / Dataset Specific Functions
    REMOVE_USERNAME = "remove_username"
    REMOVE_HASHTAG = "remove_hashtag"

    # FOR FUTURE USE
    # language
    LANGUAGE_DETECTION = "language_detection"
    LANGUAGE_PROB_DETECTION = "language_prob_detection"
    # tokenization
    TOKENIZE = "tokenize"
    # applied to whole dataset
    REMOVE_COMMON_WORDS = "remove_common_words"
    REMOVE_RARE_WORDS = "remove_rare_words"
    CONVERT_TO_UNICODE = "convert_to_unicode"


class UsernameStyle(StrEnum):
    GENERAL = "general"
    TWITTER = "twitter"
