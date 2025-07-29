from reling.db.models import Dialogue, Language, Text
from .streaks import compute_pair_streaks

__all__ = [
    'get_skipped_indices',
]


def get_skipped_indices(
        content: Text | Dialogue,
        source_language: Language,
        target_language: Language,
        skip_after: int,
) -> set[int]:
    """Get the indices of sentences that should be skipped for a specified language pair."""
    streaks = compute_pair_streaks(content, source_language, target_language)
    return {index for index, streak in enumerate(streaks) if streak.count >= skip_after}
