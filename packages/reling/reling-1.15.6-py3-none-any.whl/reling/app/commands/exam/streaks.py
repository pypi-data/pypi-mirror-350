from dataclasses import dataclass
from datetime import datetime
from typing import cast

from reling.config import MAX_SCORE
from reling.db.models import Dialogue, DialogueExam, DialogueExamResult, Language, Text, TextExam, TextExamResult

__all__ = [
    'compute_pair_streaks',
    'compute_streaks',
    'LanguagePair',
    'Streak',
    'StreakTimeline',
]


@dataclass(frozen=True)
class LanguagePair:
    source_language: Language
    target_language: Language


@dataclass
class StreakTimeline:
    first: datetime
    last: datetime


@dataclass
class Streak:
    timeline: StreakTimeline | None = None
    count: int = 0
    ever_failed: bool = False


def update(streak: Streak, result: TextExamResult | DialogueExamResult, exam: TextExam | DialogueExam) -> None:
    """Update the streaks list with the given result."""
    if streak.ever_failed:
        return
    is_perfect = result.score == MAX_SCORE
    if not is_perfect:
        streak.ever_failed = True
        return
    streak.count += 1
    time = cast(datetime, exam.finished_at)
    if streak.timeline:
        streak.timeline.first = time
    else:
        streak.timeline = StreakTimeline(time, time)


def get_default_streaks(content: Text | Dialogue) -> list[Streak]:
    """Get the default streaks list."""
    return [Streak() for _ in range(content.size)]


def compute_streaks(
        content: Text | Dialogue,
        source_language: Language | None,
        target_language: Language | None,
) -> dict[LanguagePair, list[Streak]]:
    """Compute the sentence streaks for the given content and language pair."""
    streaks: dict[LanguagePair, list[Streak]] = {}
    for exam in cast(list[TextExam] | list[DialogueExam], content.exams):
        pair = LanguagePair(exam.source_language, exam.target_language)
        if pair != LanguagePair(source_language or exam.source_language,
                                target_language or exam.target_language):
            continue
        if pair not in streaks:
            streaks[pair] = get_default_streaks(content)
        for result in exam.results:
            update(streaks[pair][result.index], result, exam)
    return streaks


def compute_pair_streaks(
        content: Text | Dialogue,
        source_language: Language,
        target_language: Language,
) -> list[Streak]:
    """Compute the sentence streaks for the given content and language pair."""
    streaks = compute_streaks(content, source_language, target_language)
    pair = LanguagePair(source_language, target_language)
    return streaks[pair] if pair in streaks else get_default_streaks(content)
