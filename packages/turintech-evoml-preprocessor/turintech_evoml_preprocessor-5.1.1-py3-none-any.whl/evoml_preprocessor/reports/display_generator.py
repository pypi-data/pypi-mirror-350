# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
import re
from typing import Dict, List

# Private Dependencies
from evoml_api_models import DataTableGraph

# Module
from evoml_preprocessor.preprocess.models import GenericOption
from evoml_preprocessor.preprocess.models.report import PreprocessingReport, TableColumn
from evoml_preprocessor.reports import _to_data_table_format

# Dependencies


# ------------------------- Feature Generation Table ------------------------- #
#             ┌─────────┬─────┬───────────┬───────────┬─────┬─────┐
#             │ feature │ ... │    ...    │    ...    │ ... │ ... │
#             ├─────────┼─────┼───────────┼───────────┼─────┼─────┤
#             │         │     │           │           │     │     │
#             └─────────┴─────┴───────────┴───────────┴─────┴─────┘
def split_name(string: str) -> List[str]:
    """Splits a name into a list of the words composing it, as lowercase
    strings. Supports `snake_case`, `kebab-case`, `camelCase`, `PascalCase`.
    Args:
        string (str):
            The string to split.
    Returns:
        List[str]:
            The list of words composing the string.
    """

    # remove white spaces
    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    string = _RE_COMBINE_WHITESPACE.sub(" ", string).strip()

    for sep in ("_", "-", " "):  # 'snake_case' and 'kebab-case'
        if sep in string:
            # Exclude empty strings for cases like leading/trailing '_'/'-'
            return [word for word in string.split(sep) if len(word) > 0]

    if string == string.lower():  # single word (note that '-'.lower() == '-')
        return [string]

    # We're camelCase or PascalCase here. We'll add '_' before every capital
    # letter, then proceed as for a snake case (we lower separated words anyway)
    sep_string = re.sub(r"([A-Z])", r"_\1", string)
    words = [word for word in sep_string.split("_") if len(word) > 0]
    if len(words) > 0:
        words[0] = words[0].capitalize()
    return words


def build_shorthand_name(full_name: str) -> str:
    """Creates a 3 letters shorthand for a name, trying to use word separation
    in different casing to produce meaningful acronyms.
    Args:
        full_name (str):
            The full name to create a shorthand for
    Returns:
        str:
            The shorthand name
    """

    words = split_name(full_name)
    # Single word (e.g. 'gender')
    if len(words) == 1:
        # Take first 3 letters of a word, e.g, 'gen'
        name = words[0]

        # Full_name length is less than or equal to 5, return complete name
        if len(name) <= 5:
            return name
        return name[:3]

    if len(words) == 2:
        # Use the first letters
        return words[0][0] + words[1][0]

    # Use the first letter of the first 3 words
    return "".join([word[0] for word in words][:3])


def make_feature_generation_table(report: PreprocessingReport) -> DataTableGraph:
    """Builds a table describing the output of the feature selection
    process. This table shows how each new feature relates to existing features
    (using the formula to obtain the one from the others).

    This table also operates a replacement on feature names to provide
    colour-based (using css) aliases. The main goal of the backend is to keep
    track of the relation between an alias and its reference (full name).

    1. Original table row
    ┌─────────────────┬──────────┐
    │ cos(one) + two² │ one, two │
    └─────────────────┴──────────┘
    2. Table row replacement
      formula alias    reference
    ┌─────────────────┬──────────┐
    │ cos(1) + T²     │ [1], [T] │
    └─────────────────┴──────────┘
    """

    if report.multiColumnStatistics.featureGenerationReport is None:
        raise ValueError("Feature generation report is not set.")

    features_info = report.multiColumnStatistics.featureGenerationReport.featuresGenerated
    encoded_to_original_map = report.multiColumnStatistics.encodedToOriginalMapping

    # Create columns to be filled
    feature_name = TableColumn(name="Generated Feature")
    features_used = TableColumn(name="Features Used")
    formula = TableColumn(name="Feature Formula")
    correlation = TableColumn(name="Correlation With Target")

    name_to_index: Dict[str, int] = {}

    tag_class = "tue-tag"

    transformations = [col for col in report.singleColumnStatistics]
    # Iterate over every feature in the report (table row)
    for feature in features_info:
        feature_name.add(feature.generatedFeatureName)
        reference_names: List[str] = []

        aliased_formula = feature.formula
        for encoded_name in feature.featuresUsed:
            # Create an alias entry if needed
            if encoded_name not in name_to_index:
                name_to_index[encoded_name] = len(name_to_index)
            index = name_to_index[encoded_name]

            if encoded_name in encoded_to_original_map:
                original_name = encoded_to_original_map[encoded_name]
            else:
                original_name = encoded_name

            colour_class = f"tue-tag-{index}"
            # We're trying to avoid a feature being a subset of another feature,
            # so we use a regex with non-identifier chars before and after for
            # the replacement
            identifier = "a-zA-Z0-9_"
            regex = re.compile(f"([^{identifier}]|^){encoded_name}([^{identifier}]|$)")

            short_name = build_shorthand_name(encoded_name)

            # identify transformation used using the original_name - this is needed for the tooltip
            transformation = ""
            transform = [c for c in transformations if c.column_name == original_name]
            if len(transform) > 0:
                if transform[0].transformation_block is not None:
                    block = transform[0].transformation_block[0]
                    # extract string form of names from enums if available
                    encoder = block.encoder_name
                    if encoder is not None and encoder != GenericOption.NONE:
                        transformation = "-[" + encoder.name + "]-"

            # Replacements on the left column (formula)
            alias = (
                f"<span class='{tag_class} {colour_class}'"
                f" title='{original_name}-{transformation}->{encoded_name} ({short_name})'>{short_name}</span>"
            )
            aliased_formula = regex.sub(f"\\1{alias}\\2", aliased_formula)

            # Replacements on the right column (reference names)
            reference_names.append(
                f"<span class='{tag_class} {colour_class}' title='{original_name}-{transformation}->{encoded_name} ("
                f"{short_name})'"
                f">{encoded_name}</span>"
            )

        operator_tags = []
        for operator in feature.basicFunctions:
            operator_tags.append(f"<span class='{tag_class}'>{operator}</span>")

        # Deals with the reference names markup
        features_used.add(" ".join(reference_names))
        formula.add(aliased_formula)
        correlation.add(str(round(feature.correlationWithTarget, 3)))

    # Validate the table
    return DataTableGraph(
        type="dataTable",
        data=_to_data_table_format(feature_name, formula, features_used, correlation),
        description=None,
        graphFields=None,
        context=None,
    )
