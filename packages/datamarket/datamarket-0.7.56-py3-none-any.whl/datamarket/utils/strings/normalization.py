########################################################################################################################
# IMPORTS

import unicodedata
from enum import Enum, auto
from typing import Any

import numpy as np
from inflection import camelize, parameterize, titleize, underscore
from string_utils import prettify, strip_html
from unidecode import unidecode

########################################################################################################################
# CLASSES


class NormalizationMode(Enum):
    NONE = auto()
    BASIC = auto()  # removes accents and converts punctuation to spaces
    SYMBOLS = auto()  # translates only symbols to Unicode name
    FULL = auto()  # BASIC + SYMBOLS


class NamingConvention(Enum):
    NONE = auto()  # no style change
    CONSTANT = auto()  # CONSTANT_CASE (uppercase, underscores)
    SNAKE = auto()  # snake_case (lowercase, underscores)
    CAMEL = auto()  # camelCase (capitalize words except first one, no spaces)
    PASCAL = auto()  # PascalCase (capitalize words including first one, no spaces)
    PARAM = auto()  # parameterize (hyphens)
    TITLE = auto()  # titleize (capitalize words)


########################################################################################################################
# FUNCTIONS


def transliterate_symbols(s: str) -> str:
    """
    Translates Unicode symbols (category S*) in the input string to their lowercase Unicode names,
    with spaces replaced by underscores. Other characters remain unchanged.

    Args:
        s: The input string.

    Returns:
        The string with symbols transliterated.
    """
    out: list[str] = []
    for c in s:
        if unicodedata.category(c).startswith("S"):
            name = unicodedata.name(c, "")
            if name:
                out.append(name.lower().replace(" ", "_"))
        else:
            out.append(c)
    return "".join(out)


def normalize(
    s: Any, mode: NormalizationMode = NormalizationMode.BASIC, naming: NamingConvention = NamingConvention.NONE
) -> str:
    """
    Normalizes and applies a naming convention to the input.

    Handles None and NaN values by returning an empty string. Converts non-string inputs to strings.

    Normalization is applied according to `mode`:
    - NONE: Returns the input as a string without any normalization.
    - BASIC: Removes accents, converts punctuation and spaces to single spaces, and preserves alphanumeric characters.
    - SYMBOLS: Translates only Unicode symbols (category S*) to their lowercase Unicode names with underscores.
    - FULL: Applies both BASIC and SYMBOLS normalization.

    After normalization, a naming convention is applied according to `naming`:
    - NONE: Returns the normalized text.
    - CONSTANT: Converts to CONSTANT_CASE (uppercase with underscores).
    - SNAKE: Converts to snake_case (lowercase with underscores).
    - CAMEL: Converts to camelCase (lowercase first word, capitalize subsequent words, no spaces).
    - PASCAL: Converts to PascalCase (capitalize all words, no spaces).
    - PARAM: Converts to parameterize (lowercase with hyphens).
    - TITLE: Converts to Title Case (capitalize each word).

    Args:
        s: The input value to normalize and format. Can be any type.
        mode: The normalization mode to apply. Defaults to NormalizationMode.BASIC.
        naming: The naming convention to apply. Defaults to NamingConvention.NONE.

    Returns:
        The normalized and formatted string.
    """
    # Parameter mapping
    if isinstance(mode, str):
        mode = NormalizationMode[mode]
    if isinstance(naming, str):
        naming = NamingConvention[naming]

    # Handling null values
    if s is None or (isinstance(s, float) and np.isnan(s)):
        normalized = ""
    elif not isinstance(s, str):
        return str(s)
    else:
        text = prettify(strip_html(str(s), True))
        if mode is NormalizationMode.NONE:
            normalized = text
        elif mode is NormalizationMode.SYMBOLS:
            normalized = transliterate_symbols(text)
        else:
            # BASIC and FULL: remove accents and lowercase
            normalized = unidecode(text).lower()
            tokens: list[str] = []
            current: list[str] = []

            def flush_current():
                nonlocal current
                if current:
                    tokens.append("".join(current))
                    current.clear()

            for c in normalized:
                cat = unicodedata.category(c)
                if c.isalnum():
                    current.append(c)
                elif mode is NormalizationMode.FULL and cat.startswith("S"):
                    flush_current()
                    name = unicodedata.name(c, "")
                    if name:
                        tokens.append(name.lower().replace(" ", "_"))
                elif cat.startswith("P") or c.isspace():
                    flush_current()
                # other characters ignored

            flush_current()
            normalized = " ".join(tokens)

    # Apply naming convention
    if naming is NamingConvention.NONE:
        return normalized
    if naming is NamingConvention.PARAM:
        return parameterize(normalized)
    if naming is NamingConvention.TITLE:
        return titleize(normalized)

    underscored = underscore(parameterize(normalized))
    if naming is NamingConvention.CONSTANT:
        return underscored.upper()
    if naming is NamingConvention.CAMEL:
        return camelize(underscored, False)
    if naming is NamingConvention.PASCAL:
        return camelize(underscored)

    return underscored
