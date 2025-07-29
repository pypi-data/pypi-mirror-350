"""Module providing utils functions for cleaning users text data.

The functions are grouped in the following order:
- Utility Functions
    - Checker Functions
    - Stopwords Functions
    - Language Functions
    - Tokenization Function
- Mandatory Functions
- Optional Functions
    - HTML Functions
    - Emoji/Emoticon Functions
    - Lexical Functions
    - Dataset specific Functions (Twitter, Reddit, etc.)
    - Regex Validation Functions

Note: functions that are used in the preprocessing pipeline are Mandatory Functions.
These functions are specific to the text transformer.
"""

# region────────────────────────────────── Imports ────────────────────────────────── #
# Standard Library
from typing import List, Optional, Set, Tuple, Union
import re
from collections import Counter
import pandas as pd

# Dependencies
# import nltk
# from nltk.corpus import stopwords as nltk_sw
# from nltk.corpus import wordnet
# from nltk.stem import WordNetLemmatizer
# from gensim import utils
from emot.emo_unicode import UNICODE_EMOJI

# from langdetect import detect, detect_langs
import logging

# Private Dependencies

# Module
from evoml_preprocessor.nlp.enum import UsernameStyle, NLPFuncRepresentation
from evoml_preprocessor.nlp.patterns import (
    EMAIL_PATTERN,
    HASHTAG_PATTERN,
    URL_PATTERN,
    TWITTER_USERNAME_PATTERN,
    XML_PATTERN,
    NUMBER_PATTERN,
    CHAR_PATTERN,
    CONS_DUPLICATION_PATTERN,
    SPACE_PATTERN,
    ANY_USERNAME_PATTERN,
    EMOJI_PATTERN,
    EMOTICON_DICT,
    BLANK_PATTERN,
    EMOTICON_PATTERN,
    PUNCTUATION_PATTERN,
    SAMPLE_TYPOS_SLANG_PATTERN,
    SAMPLE_TYPOS_SLANG,
    SAMPLE_ACRONYMS,
    SAMPLE_ACRONYMS_PATTERN,
    SAMPLE_ABBR_PATTERN,
    SAMPLE_ABBR,
    CONTRACTIONS_DIC,
    CONTRACTIONS_PATTERN,
)

# endregion ───────────────────────────────────────────────────────────────────────── #

# region────────────────────────────── NLTK Functions ─────────────────────────────── #
# nltk.data.clear_cache()
# nltk.download("wordnet")
# try:
#     nltk.data.find("corpora/stopwords")
# except LookupError:
#     nltk.download("stopwords")
#
# try:
#     nltk.data.find("corpora/averaged_perceptron_tagger")
# except LookupError:
#     nltk.download("averaged_perceptron_tagger")

# endregion ───────────────────────────────────────────────────────────────────────── #

# region───────────────────────────── Utility Functions ───────────────────────────── #

logger = logging.getLogger("preprocessor")


def run_utils_functions(text: str, utils_functions: List[NLPFuncRepresentation]) -> str:
    nlp_utils_map = {
        NLPFuncRepresentation.STRIP: strip,
        NLPFuncRepresentation.TO_LOWER: to_lower,
        NLPFuncRepresentation.REMOVE_STOPWORDS: remove_stopwords,
        NLPFuncRepresentation.REMOVE_NUMBERS: remove_numbers,
        NLPFuncRepresentation.REMOVE_PUNCTUATION: remove_punctuation,
        NLPFuncRepresentation.REMOVE_CHARS: remove_chars,
        NLPFuncRepresentation.REMOVE_CONSECUTIVE_SPACES: remove_consecutive_spaces,
        NLPFuncRepresentation.ABBREVIATION_CONVERTER: abbreviation_converter,
        NLPFuncRepresentation.EXPAND_CONTRACTIONS: expand_contractions,
        NLPFuncRepresentation.LEMMATIZE: lemmatize,
        NLPFuncRepresentation.REMOVE_URL: remove_url,
        NLPFuncRepresentation.REMOVE_DUPLICATION: remove_duplication,
        NLPFuncRepresentation.REMOVE_EMAIL: remove_email,
        NLPFuncRepresentation.REMOVE_XML: remove_xml,
        NLPFuncRepresentation.REMOVE_EMOJI: remove_emoji,
        NLPFuncRepresentation.REMOVE_EMOTICON: remove_emoticon,
        NLPFuncRepresentation.REMOVE_USERNAME: remove_username,
        NLPFuncRepresentation.REMOVE_HASHTAG: remove_hashtag,
    }
    try:
        # if the text is valid
        if is_valid_string(text):
            # run the utils functions
            for method in utils_functions:
                text = nlp_utils_map[method](text)
    except Exception as e:
        logger.error(f"Error cleaning text: {e}")
    return text


def is_valid_string(text: str) -> bool:
    """
    Checks if the given string is valid or not

    Args:
        text (str): a text to be checked

    Returns:
        bool: True if the text is valid, otherwise False
    """
    # Input checking
    return not pd.isnull(text) or not isinstance(text, str)


def blank_checker(text: str) -> bool:
    """
    Checks the given text is composed space, \t, \r, and \n.

    Args:
        text (str): a text can be empty

    Returns:
        bool: a boolean value that shows whether the given text is empty or not.
    """
    if BLANK_PATTERN.search(text):
        return True
    return False


def regex_validation_checker(regex: str) -> bool:
    """
    Checks if the given regular expression is valid.

    Args:
        regex (str): a regular expression

    Returns:
        bool: True if the given regular expression is valid, False otherwise
    """
    # Input checking
    if pd.isnull(regex) or not isinstance(regex, str):
        return False

    try:
        re.compile(regex)
        return True
    except re.error:
        return False


def add_word_to_stopwords_set(stop_words: Optional[set], word: Union[list, set, str]) -> Optional[set]:
    """
    Adds a word to the stop words set.

    Args:
        stop_words (Optional[set]): a stop words set
        word (Union[list, str]): a word or a list of words that will be added to the stop words set

    Returns:
        Optional[set]: a stop words set that does not contain the given word
    """
    # Input checking
    if pd.isnull(stop_words) or not isinstance(stop_words, set):
        return None

    # Check the empty set
    if len(stop_words) == 0:
        return None

    if isinstance(pd.isnull(word), bool):
        if pd.isnull(word):
            return stop_words
    else:
        if pd.isnull(word).all():
            return stop_words

    if not isinstance(word, (list, set, str)):
        return stop_words

    # Check the empty set, set
    if len(word) == 0:
        return stop_words

    # The add function, adds a single element to the existing set or
    # original set, so we create a new instance of that
    stop_words = set(stop_words)

    if isinstance(word, str):
        stop_words.add(word)
    elif isinstance(word, (list, set)):
        for w in word:
            stop_words.add(w)

    return stop_words


# def stopwords(pref_lang_lst: Union[List[str], Set[str], str, None]) -> Optional[Set[str]]:
#     """
#     Returns a set that contains all stop words in NLTK based on the given language list.
#     If the given language list is empty, or None, then it assumes English as the default language.
#
#     Args:
#         pref_lang_lst (Optional[List[str]]): a list of languages
#
#     Returns:
#         Optional[Set[str]]: a set of all stop words w.r.t the given languages
#     """
#     # Input checking
#     if isinstance(pref_lang_lst, str):
#         # The input is in string format, instead of list or set
#         pref_lang_lst = [pref_lang_lst]
#     elif pd.isnull(pref_lang_lst) or not isinstance(pref_lang_lst, (Set, List)):
#         pref_lang_lst = ["English"]
#     if len(pref_lang_lst) == 0:
#         pref_lang_lst = ["English"]
#
#     NLTK_sup_lang = set(nltk_sw.fileids())
#     pref_lang_lst_lower_case = [lang.lower().strip() for lang in pref_lang_lst]
#     pref_lang_set = set(pref_lang_lst_lower_case)
#
#     # Check the intersection between two sets: NLTK_sup_lang and pref_lang_set
#     if pref_lang_set.issubset(NLTK_sup_lang):
#         total_lang = pref_lang_set
#     elif pref_lang_set.intersection(NLTK_sup_lang):
#         # we found some languages that are supported by NLTK
#         total_lang = pref_lang_set.intersection(NLTK_sup_lang)
#     else:
#         # There is no intersection between sets and Nltk does not support any of the given languages
#         return None
#     try:
#         stop_words = set()
#         stop_words = nltk_sw.words("english")
#     except LookupError:
#         nltk.download("stopwords")
#     finally:
#         stop_words = set()
#         for language in total_lang:
#             stop_words = stop_words.union(set(nltk_sw.words(language)))
#
#     full_stopwords_set = set.union(set(CUSTOM_EXTENDED_STOPWORDS), set(stop_words))
#
#     return full_stopwords_set


# def language_detection(text: str) -> str:
#     """
#     To detect the language of the text. The method returns a single language
#     name which has the highest probability.
#
#     Note:
#         Language detection algorithm is non-deterministic, which means that if
#         we try to run it on a text which is either too short or too ambiguous, we
#         might get different results everytime you run it.
#
#     See more:
#         https://code.google.com/archive/p/language-detection/wikis/Tools.wiki
#         https://github.com/Mimino666/langdetect
#
#     Args:
#         text (Optional[str]): a given that that can be in any language
#
#     Returns:
#         Optional[str]: a single language abbreviation which has the highest probability.
#     """
#     return detect(text)


# def language_prob_detection(text: str) -> List[Tuple[str, float]]:
#     """
#     To find out the probabilities for the top languages.
#
#     Note:
#         Language detection algorithm is non-deterministic, which means that if
#         we try to run it on a text which is either too short or too ambiguous, we
#         might get different results everytime you run it.
#
#     See more:
#         https://code.google.com/archive/p/language-detection/wikis/Tools.wiki
#         https://github.com/Mimino666/langdetect
#
#     Args:
#         text (str): a given that that can be in any language
#
#     Returns:
#         List[Tuple[str, float]]: a list of multiple languages and their probabilities.
#     """
#     return detect_langs(text)


# def tokenize(text: str) -> List[str]:
#     """
#     Tokenize the given text.
#
#     Args:
#         text (Optional[str]): a text that may contain multiple words
#
#     Returns:
#         Optional[List[str]]: a list of tokens
#     """
#
#     try:
#         output = nltk.word_tokenize(text)
#     except LookupError:
#
#         nltk.download("punkt")
#         output = nltk.word_tokenize(text)
#
#     return output


# endregion ────────────────────────────────────────────────────────────────────── #

# region──────────────────────────── Mandatory Functions ──────────────────────────── #
# These functions should be applied to any text data, because they are generic to all text data.


def strip(text: str) -> str:
    """
    Removes all whitespaces at the beginning and end of the string.
    Also, it eliminates multiple spaces between words.

    Args:
        text (str): a string may contain multiple spaces

    Returns:
        str: a purified string that does not have whitespaces at the beginning and end of the string
    """
    return " ".join([c for c in text.split()])


def abbreviation_converter(text: str) -> str:
    """
    Converts abbreviation forms of the input text into the normal shape.

    Args:
        text (str): a text with abbreviation forms of words

    Returns:
        str: a converted text without any abbreviation
    """
    text = SAMPLE_TYPOS_SLANG_PATTERN.sub(lambda x: SAMPLE_TYPOS_SLANG[x.group()], text)
    text = SAMPLE_ACRONYMS_PATTERN.sub(lambda x: SAMPLE_ACRONYMS[x.group()], text)
    text = SAMPLE_ABBR_PATTERN.sub(lambda x: SAMPLE_ABBR[x.group()], text)

    return text


def expand_contractions(text: str) -> str:
    """
    Contractions are words or combinations of words that are shortened by dropping letters and replacing them with an apostrophe.
    With this function, we are going to convert the text into the standard form.

    See more:
        TODO: We can use the Contraction library to expand our coverage (https://github.com/kootenpv/contractions)
        contractions.add('mychange', 'my change') to add our contractions to the contractions library
        contractions.fix(expanded_text)
    Args:
        text (str): a text that may contain shortened forms of words
    Returns:
        str: A converted text in which shortened words are transferred to a standard shape.
    """

    def expand_match(contraction: re.Match) -> str:
        match = contraction.group(0)
        expanded_contraction = (
            CONTRACTIONS_DIC.get(match) if CONTRACTIONS_DIC.get(match) else CONTRACTIONS_DIC.get(match.lower())
        )

        return expanded_contraction

    expanded_text = CONTRACTIONS_PATTERN.sub(expand_match, text)

    # In a case that we could not find the contraction in the dictionary we remove the apostrophe sign
    expanded_text = re.sub("'", " ", expanded_text)

    return expanded_text


def to_lower(text: str) -> str:
    """
    Converts the given text to lower case

    Args:
        text (str): a text to be converted

    Returns:
        str: a lowercase string
    """
    return text.lower()


def remove_stopwords(text: str, stopwords: Optional[Set[str]] = None) -> str:
    """
    Removes all stopwords from the given text

    Args:
        text (Optional[str]): a text may contain stopwords
        stopwords (Set): the desired stopwords set based on a specific language/s

    Returns:
        Optional[str]: a purified text w/o any stopwords
    """

    if stopwords is None or not isinstance(stopwords, Set):
        return text

    return " ".join([word for word in str(text).split() if word not in stopwords])


def remove_numbers(text: str) -> str:
    """
    Removes any digits from the given string

    Args:
        text (str): a text may contain digits

    Returns:
        str: a purified string that does not have any numbers
    """
    # @mypy: thinks that str.sub returns 'Any'
    return NUMBER_PATTERN.sub(r"", text)  # type: ignore


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation from the given text and replace with space.

    Args:
        text (Optional[str]): a text that may contain punctuation

    Returns:
        Optional[str]: a purified string that does not have any punctuation
    """
    # @mypy: thinks that str.sub returns 'Any'
    return PUNCTUATION_PATTERN.sub(r" ", text)  # type: ignore


def lemmatize(text: str) -> str:
    """
    Perform lemmatization for the given text.

    Note:
        Lemmatization is the process of converting a word to its base form. The difference between stemming and lemmatization is,
        lemmatization considers the context and converts the word to its meaningful base form, whereas stemming just removes
        the last few characters, often leading to incorrect meanings and spelling errors.

    More info:
        https://www.machinelearningplus.com/nlp/lemmatization-examples-python/

    Args:
        text (str): a regular text that may contain for example the "ing" form of verbs

    Returns:
        str: a lemmatized text
    """
    # TODO uncomment this part after we have a lemmatization process
    return text
    # # TODO: Ask to Amir: In transformer models do we need to lemmaize the text?
    # # https://stackoverflow.com/questions/63979544/using-trained-bert-model-and-data-preprocessing
    # # For lemmatization, we need to provide the POS tag of the word along with the word.
    # # Depending on the POS, the lemmatizer may return different results.
    # lemmatizer = WordNetLemmatizer()
    # wordnet_map = {
    #     "N": wordnet.NOUN,
    #     "V": wordnet.VERB,
    #     "J": wordnet.ADJ,
    #     "R": wordnet.ADV,
    # }  # Pos tag, used Noun, Verb, Adjective and Adverb
    #
    # pos_tagged_text = nltk.pos_tag(text.split())
    # return " ".join(
    #     [lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text]
    # )


def remove_duplication(text: str, consecutive: bool = True) -> str:
    """
    Removes duplicate words from the given text

    Args:
        text (str): a text may contain the same words

        consecutive (bool, optional): if True, it will remove the consecutive duplicated words.
                                      Otherwise, it will remove all duplicated words. Defaults to True.
    Returns:
        str: the purified text that does not contain consecutive duplicated words
    """
    if consecutive:
        # @mypy: thinks that str.sub returns 'Any'
        return CONS_DUPLICATION_PATTERN.sub(r"\1", text)  # type: ignore
    tokenize_text = text.split()
    return " ".join(sorted(set(tokenize_text), key=tokenize_text.index))


def remove_consecutive_spaces(text: str) -> str:
    """
    Removes continuous whitespaces

    Example:
        >>> remove_consecutive_spaces("Manal                          went to     the gym!")
        ... "Manal went to the gym!"

    Args:
        text (str): a text that may contain multiple spaces sequentially

    Returns:
        str: a text string without any continuous whitespaces
    """
    # @mypy: thinks that str.sub returns 'Any'
    return SPACE_PATTERN.sub(r" ", text)  # type: ignore


# endregion ─────────────────────────────────────────────────────────────────────── #

# region──────────────────── Optional Functions / HTML functions ──────────────────── #


def remove_xml(html_text: str) -> str:
    """
    Eliminates the HTML tags from the given text and returns a tuple
    that contains the purified text and the number of matches.

    Alternatively, you can use the following code:
        from bs4 import BeautifulSoup
        def remove_xml_v2(text):
            return BeautifulSoup(text, "lxml").text

    Args:
        html_text (str): a text that may contain HTML tags

    Returns:
        str : the purified text according to HTML tags
    """
    # @mypy: thinks that str.sub returns 'Any'
    return XML_PATTERN.sub(r"", html_text)  # type: ignore


# endregion ──────────────────────────────────────────────────────────────────────── #

# region─────────── Optional Functions / Emoji and Emoticon Functions ──────────────── #


def remove_emoji(text: str, to_word: bool = False) -> str:
    """
    Removes any emojis in the given text.

    See more:
        http://www.unicode.org/Public/emoji/1.0//emoji-data.txt

    Args:
        text (str): a text that may contain multiple emojis
        to_word (bool, optional): If the to_word is True, it will convert
        the emojis to words. Defaults to False.

    Returns:
        str: a purified string that does not have any emojis
    """

    if to_word is True:
        for emot in UNICODE_EMOJI:
            text = text.replace(
                emot,
                "_".join(UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()) + " ",
            )
        return text

    # @mypy: thinks that str.sub returns 'Any'
    return EMOJI_PATTERN.sub(r" ", text)  # type: ignore


def remove_emoticon(text: str, to_word: bool = False) -> str:
    """
    Removes all emoticons from the given text.

    Args:
        text (str): a text which contains multiple emoticons
        to_word (bool, optional): If the to_word is True, it will convert
        the emoticons into words. Defaults to False.

    Returns:
        str: the purified text does not have any emoticons
    """
    if to_word is True:
        for emot in EMOTICON_DICT:
            text = re.sub(
                "(" + emot + ")",
                "_".join(EMOTICON_DICT[emot].replace(",", "").split()) + " ",
                text,
            )

        return text

    # @mypy: thinks that str.sub returns 'Any'
    return EMOTICON_PATTERN.sub(r" ", text)  # type: ignore


# endregion ───────────────────────────────────────────────────────────────────────── #

# region───────────────── Optional Functions / Lexical Functions ───────────────────── #


def remove_common_words(text_series: pd.Series, n: int) -> pd.Series:
    """
    Removes the common words from the given text set.

    Args:
        text_series (pd.Series):  a text series that may contain the common words
        common_words_num (int): the number of the common words that will be removed

    Returns:
        pd.Series: a purified text set that does not contain the common words
    """
    # Input checking
    counter: Counter = Counter()
    for words in map(str.split, text_series.values):
        counter.update(words)

    # Find the frequent words
    freq = [word for word, _ in counter.most_common()[-(n + 1) : -1]]

    for i, text in enumerate(text_series.values):
        # text here is the new value for the current wor of text
        # figure out how to mutate the current row, preferably without having to re-allocate an entire new series
        filtered_text = " ".join([word for word in str(text).split() if word not in freq])
        text_series.iloc[i] = filtered_text

    return text_series


def remove_rare_words(text_series: pd.Series, n: int) -> pd.Series:
    """
    Removes the rare words from the given text set.

    Args:
        text_series (pd.Series):  a text series that may contain the rare words
        rare_words_num (int): the number of the rare words that will be removed

    Returns:
        pd.Series: a purified text set that does not contain the rare words
    """
    counter: Counter = Counter()
    for words in map(str.split, text_series.values):
        counter.update(words)

    # Find the rare words
    rare = [word for word, _ in counter.most_common()[-(n + 1) : -1]]

    for i, text in enumerate(text_series.values):
        # text here is the new value for the current wor of text
        # figure out how to mutate the current row, preferably without having to re-allocate an entire new series
        filtered_text = " ".join([word for word in str(text).split() if word not in rare])
        text_series.iloc[i] = filtered_text

    return text_series


def remove_chars(text: str, special_char: Optional[List[str]] = None) -> str:
    """
    Removes characters in the given text

    Args:
        text (str): a text may contain multiple types of characters
        special_char (List[str]): a list of characters that will be removed

    Returns:
        str: the purified text does not have the given characters
    """
    if special_char is None:
        # @mypy: thinks that str.sub returns 'Any'
        return CHAR_PATTERN.sub(r" ", text, re.I | re.A)  # type: ignore

    if not isinstance(special_char, List):
        return text

    for char in special_char:
        text = text.replace(char, " ")

    return text


# endregion ───────────────────────────────────────────────────────────────────────── #

# region──────────── Optional Functions / Dataset specific Functions ────────────────── #


def remove_url(text: str) -> str:
    """
    Removes any url in the given text (Example: https://regex101.com/r/RvtAey/1)

    Args:
        text (str): a text that may contain multiple URLS

    Returns:
        str: the purified string that does not have any URLs
    """
    return URL_PATTERN.sub(r" ", text)


def remove_email(text: str) -> str:
    """
    Removes email address/s from the given text

    Args:
        text (str): a text that may contain multiple email addresses

    Returns:
        str: (the purified text  does not have any email addresses, the number of matches)
    """
    # @mypy: thinks that str.sub returns 'Any'
    return EMAIL_PATTERN.sub(r"", text)  # type: ignore


def remove_username(text: str, domain: UsernameStyle = UsernameStyle.GENERAL) -> str:
    """
    Removes username parts that start with the "@" sign.

    Args:
        text (str): a text that may contain multiple usernames

        domain((Optional[str]): a domain name that will be removed from the text.
            - None means that the function will remove all usernames and there is no limitation for the length of the username.

    Returns:
        str: the purified text doesn't have any username
    """
    if domain == UsernameStyle.TWITTER:
        # Removes twitter username from the given text w.r.t Twitter username policies.
        # A maximum of 15 characters (words) are allowed.
        # @mypy: thinks that str.sub returns 'Any'
        return TWITTER_USERNAME_PATTERN.sub(r" ", text)  # type: ignore
    else:
        # @mypy: thinks that str.sub returns 'Any'
        return ANY_USERNAME_PATTERN.sub(r"", text)  # type: ignore


def remove_hashtag(text: str) -> str:
    """
    Removes hashtag from the given text. This function supports multilanguage hashtags.

    Example:
        https://regex101.com/r/SxRara/1

    Args:
        text (str): a text that may contain multiple hashtags

    Returns:
        str: the purified text doesn't have any hashtag
    """
    # @mypy: thinks that str.sub returns 'Any'
    return HASHTAG_PATTERN.sub(r"", text)  # type: ignore


# endregion ────────────────────────────────────────────────────────────────────────────── #

# region────────────── Optional Functions / Regex Validation Functions ─────────────────── #


def remove_regex_match(text: str, regex: Optional[str]) -> Optional[str]:
    """
    Removes the given regular expression from the given text.

    Args:
        text (Optional[str]): a text that may contain the given regular expression
        regex (Optional[str]): a regular expression

    Returns:
        Optional[str]: a purified text that does not contain the given regular expression
    """

    if pd.isnull(regex) or not isinstance(regex, str) or not regex_validation_checker(regex):
        return None

    return re.sub(regex, r"", text)


def substitutes_regex_match(text: str, regex: Optional[str], sub_text: str) -> Optional[str]:
    """
    Substitutes with a string w.r.t the given regular expression.

    Args:
        text (str): a text that may contain the given regular expression
        regex (str): a regular expression
        sub_text: (str): a string that will be substituted

    Returns:
        Optional[str]: a purified text that does substitute with the given string
    """
    # Input checking
    if pd.isnull(regex) or not isinstance(regex, str):
        return None

    if not regex_validation_checker(regex):
        return None

    return re.sub(regex, sub_text, text)


# endregion ────────────────────────────────────────────────────────────────────────────── #
