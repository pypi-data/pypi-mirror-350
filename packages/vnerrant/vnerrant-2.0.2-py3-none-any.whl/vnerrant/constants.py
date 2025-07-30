from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from vnerrant.utils.utils import load_yml_file

# Replace magic strings with constants
@dataclass
class MergeType:
    """
    Merge types.
    """

    RULES: str = "rules"
    ALL_SPLIT: str = "all-split"
    ALL_MERGE: str = "all-merge"
    ALL_EQUAL: str = "all-equal"

KEY_SPELL = "SPELLING"

base_dir = Path(__file__).resolve().parent
# Load the data from the YAML file into the dataclass
MAPPING_TYPE_ERROR = load_yml_file(base_dir / "config" / "mapping_type_error.yaml")
EXPLANATION_PATH = base_dir / "config" / "errant_verbose.json"


@dataclass(frozen=True)
class Operator:
    """
    Error operation types.
    """

    MISSING: str = "M"
    UNNECESSARY: str = "U"
    REPLACE: str = "R"


@dataclass
class SeparatorTypes:
    """
    Separator types.
    """

    HYPHEN: str = "-"
    COMPOUND: str = "+"
    COLON: str = ":"


@dataclass
class TokenizeTypes:
    SPACY: str = "spacy"
    SPLIT: str = "split"
    STRING: str = "string"


TOKENIZING_CHARACTERS = [
    "\u0020\u00A0\u115f\u1160\u1680",
    "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007",
    "\u2008\u2009\u200A\u200B\u200c\u200d\u200e\u200f",
    "\u2028\u2029\u202a\u202b\u202c\u202d\u202e\u202f",
    "\u205F\u2060\u2061\u2062\u2063\u206A\u206b\u206c\u206d",
    "\u206E\u206F\u3000\u3164\ufeff\uffa0\ufff9\ufffa\ufffb",
    "¦‖∣|,.;()[]{}=*#∗+×·÷<>!?:~/\\\"'«»„”“‘’`´‛′›‹…¿¡‼⁇⁈⁉™®\u203d\u00B6\uFFEB\u2E2E",
    "\u2012\u2013\u2014\u2015",  # dashes
    "\u2500\u3161\u2713",  # other dashes
    "\u25CF\u25CB\u25C6\u27A2\u25A0\u25A1\u2605\u274F\u2794\u21B5\u2756\u25AA\u2751\u2022",  # bullet points
    "\u2B9A\u2265\u2192\u21FE\u21C9\u21D2\u21E8\u21DB",  # arrows
    "\u00b9\u00b2\u00b3\u2070\u2071\u2074\u2075\u2076\u2077\u2078\u2079",  # superscripts
    "\t\n\r\u000B",  # tabs, line breaks
]

TOKENIZING_CHARACTERS = "".join(TOKENIZING_CHARACTERS)
ENGLISH_TOKENIZING_CHARACTERS = TOKENIZING_CHARACTERS + "_"
