from math import ceil, floor
from statistics import mean

from lcs2 import diff, lcs_indices, lcs_length

from reling.config import MAX_SCORE
from reling.db.models import DialogueExam, TextExam
from reling.utils.strings import tokenize
from .fuzzy_word import FuzzyWord

__all__ = [
    'calculate_diff_score',
    'format_average_score',
    'get_average_score',
]


def calculate_mistake_score(mistakes: int) -> int:
    """Return the score based on the number of mistakes."""
    return floor(MAX_SCORE * ((1 - 1 / MAX_SCORE) ** mistakes))


def calculate_lcs_score(lcs_len: int, a_len: int, b_len: int) -> int:
    """Return the score based on the length of the longest common subsequence of two sequences."""
    if lcs_len == a_len == b_len:
        return MAX_SCORE
    else:
        return ceil(lcs_len / max(a_len, b_len) * (MAX_SCORE - 1))


def calculate_char_diff_score(a: str, b: str) -> int:
    """Return the score based on the longest common subsequence of two strings."""
    return calculate_lcs_score(lcs_length(a, b), len(a), len(b))


def calculate_fuzzy_word_diff_score(a: str, b: str, cj: bool) -> int:
    """
    Calculate the score based on the total length of the longest common subsequences of characters
    within fuzzily aligned words from two strings.
    """
    a_words, b_words = (tokenize(sentence, punctuation=False, whitespace=False, cj=cj) for sentence in (a, b))
    a_len, b_len = (sum(map(len, words)) for words in (a_words, b_words))
    lcs_len = 0
    for a_index, b_index in lcs_indices(map(FuzzyWord, a_words), map(FuzzyWord, b_words), FuzzyWord.compare):
        lcs_len += lcs_length(a_words[a_index], b_words[b_index])
    return calculate_lcs_score(lcs_len, a_len, b_len)


def calculate_word_mistake_diff_score(a: str, b: str, cj: bool) -> int:
    """Return the score based on the number of mistakes computed from a word-level diff between two strings."""
    a_words, b_words = ([word.lower() for word in tokenize(sentence, punctuation=False, whitespace=False, cj=cj)]
                        for sentence in (a, b))
    a_diff: list[str] = []
    b_diff: list[str] = []
    mistakes = 0
    for a_tokens, b_tokens in diff(a_words, b_words):
        mistakes += max(len(a_tokens), len(b_tokens))
        a_diff.extend(a_tokens)
        b_diff.extend(b_tokens)
    mistakes -= lcs_length(a_diff, b_diff)
    return calculate_mistake_score(mistakes)


def calculate_diff_score(a: str, b: str) -> int:
    """Return the score based on the diff between two strings."""
    return min(
        calculate_char_diff_score(a, b),
        calculate_fuzzy_word_diff_score(a, b, cj=True),
        calculate_word_mistake_diff_score(a, b, cj=False),
    )


def get_average_score(exam: TextExam | DialogueExam) -> float:
    """Return the average score of the exam."""
    return mean(result.score for result in exam.results)


def format_average_score(exam: TextExam | DialogueExam) -> str:
    return f'{get_average_score(exam):.1f}'
