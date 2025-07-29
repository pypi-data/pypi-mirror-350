from enum import StrEnum
from typing import Any, Callable

from lcs2 import lcs_indices
from rich.text import Text

from reling.utils.strings import tokenize
from .colors import default, green, red
from .fuzzy_word import FuzzyWord

__all__ = [
    'DiffType',
    'highlight_diff',
]


class DiffType(StrEnum):
    CHAR = 'char'
    TOKEN = 'token'

    def get_tokenizer(self) -> Callable[[str], list[str]]:
        match self:
            case DiffType.CHAR:
                return lambda section: list(section)
            case DiffType.TOKEN:
                return lambda section: tokenize(section)
            case _:
                raise NotImplementedError

    def get_normalizer(self) -> Callable[[str], Any]:
        match self:
            case DiffType.CHAR:
                return lambda section: section
            case DiffType.TOKEN:
                return lambda section: FuzzyWord(section)
            case _:
                raise NotImplementedError

    def get_weight[T](self) -> Callable[[T, T], float] | None:
        match self:
            case DiffType.CHAR:
                return None
            case DiffType.TOKEN:
                return FuzzyWord.compare
            case _:
                raise NotImplementedError


def highlight_diff(worse: str, better: str, diff_type: DiffType = DiffType.TOKEN) -> tuple[Text, Text]:
    """Return the formatted pair of strings, highlighting the difference between the two."""
    tokenizer, normalizer, weight = diff_type.get_tokenizer(), diff_type.get_normalizer(), diff_type.get_weight()
    worse_tokens, better_tokens = tokenizer(worse), tokenizer(better)
    lcs = lcs_indices(
        *([normalizer(token) for token in tokens] for tokens in (worse_tokens, better_tokens)),
        weight=weight,
    )
    worse_segments: list[Text] = []
    better_segments: list[Text] = []

    worse_cursor = better_cursor = 0
    for worse_index, better_index in lcs + [(len(worse_tokens), len(better_tokens))]:
        worse_segments.append(red(''.join(worse_tokens[worse_cursor:worse_index])))
        better_segments.append(green(''.join(better_tokens[better_cursor:better_index])))
        if (worse_index, better_index) == (len(worse_tokens), len(better_tokens)):
            break
        match diff_type:
            case DiffType.CHAR:
                worse_segments.append(default(worse_tokens[worse_index]))
                better_segments.append(default(better_tokens[better_index]))
            case DiffType.TOKEN:
                worse_segment, better_segment = highlight_diff(
                    worse_tokens[worse_index],
                    better_tokens[better_index],
                    DiffType.CHAR,
                )
                worse_segments.append(worse_segment)
                better_segments.append(better_segment)
        worse_cursor = worse_index + 1
        better_cursor = better_index + 1

    return sum(worse_segments, Text('')), sum(better_segments, Text(''))
