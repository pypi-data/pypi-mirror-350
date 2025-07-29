from __future__ import annotations

from lcs2 import lcs_length

SHARED_THRESHOLD = 0.61


class FuzzyWord:
    _normalized: str

    def __init__(self, word: str) -> None:
        self._normalized = word.lower()

    @staticmethod
    def compare(a: FuzzyWord, b: FuzzyWord) -> float:
        """
        Return the similarity score between two FuzzyWord instances.
        Two words are considered more similar if, when lowercased, they share a greater number
        of characters and have a higher ratio of shared characters.
        """
        if not a._normalized and not b._normalized:
            return 1.0
        shared_count = lcs_length(a._normalized, b._normalized)
        shared_ratio = 2 * shared_count / (len(a._normalized) + len(b._normalized))
        return shared_count * shared_ratio if shared_ratio >= SHARED_THRESHOLD else 0.0
