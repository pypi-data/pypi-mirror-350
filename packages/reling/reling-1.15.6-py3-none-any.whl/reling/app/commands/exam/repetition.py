from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from math import floor, log2

from reling.db import single_session
from reling.db.models import Dialogue, Language, Text
from reling.utils.tables import build_table, print_table
from reling.utils.time import now
from .streaks import compute_streaks, LanguagePair, Streak

__all__ = [
    'compute_repetition_data',
    'print_repetition_statistics',
    'RepetitionData',
    'RepetitionCategoryStatistics',
    'RepetitionStatistics',
]

MIN_WAIT_PERIOD = timedelta(hours=1)

SESSION_SUMMARY_TITLE = 'Session Summary'
CUMULATIVE_REVIEWS_TITLE = 'Estimated Cumulative Sentence Reviews'

METRIC = 'Metric'
TEXTS = 'Texts'
DIALOGUES = 'Dialogues'
TOTAL = 'Total'

EXAMS = 'Exams to take'
SENTENCES = 'Sentences to review'

PERIOD = 'Period'

PERIODS: dict[int, str] = {
    1: 'day',
    7: 'week',
    30: 'month',
    365: 'year',
}

COLUMN_WIDTH = max(len(METRIC), len(PERIOD), len(TEXTS), len(DIALOGUES), len(TOTAL))


@dataclass
class RepetitionCategoryStatistics:
    exams: int = 0
    sentences: int = 0
    cumulative_reviews: dict[int, int] = field(default_factory=lambda: {period: 0 for period in PERIODS})


@dataclass
class RepetitionStatistics:
    texts: RepetitionCategoryStatistics = field(default_factory=RepetitionCategoryStatistics)
    dialogues: RepetitionCategoryStatistics = field(default_factory=RepetitionCategoryStatistics)


@dataclass
class ExamInfo:
    content: Text | Dialogue
    source_language: Language
    target_language: Language
    skipped_indices: set[int]

    @property
    def sentences_to_review(self) -> int:
        return self.content.size - len(self.skipped_indices)

    def __gt__(self, other: ExamInfo) -> bool:
        return self.sentences_to_review > other.sentences_to_review or (
            self.sentences_to_review == other.sentences_to_review and
            self.content.created_at < other.content.created_at
        )


@dataclass
class RepetitionData:
    statistics: RepetitionStatistics = field(default_factory=RepetitionStatistics)
    next_exam: ExamInfo | None = None


def get_next_review_times(streak: Streak, reference_time: datetime) -> tuple[datetime, timedelta, timedelta]:
    """
    Compute the next scheduled review time and wait periods for subsequent reviews,
    assuming all reviews are successful and occur on time.
    """
    if streak.timeline:
        wait_period = max(streak.timeline.last - streak.timeline.first, MIN_WAIT_PERIOD)
        next_review_time = max(streak.timeline.last + wait_period, reference_time)
        next_review_wait = next_review_time - streak.timeline.first
        return next_review_time, next_review_wait, 2 * next_review_wait
    else:
        return reference_time, MIN_WAIT_PERIOD, MIN_WAIT_PERIOD


def get_num_reviews_before(
        first_review: datetime,
        first_wait: timedelta,
        second_wait: timedelta,
        before: datetime,
) -> int:
    """
    Return the total number of on-time, successful reviews that occur strictly before a given time;
    starting from the third review, the wait time doubles after each successful review.
    """
    if first_review >= before:
        return 0
    second_review = first_review + first_wait
    if second_review >= before:
        return 1
    return floor(log2((before - second_review) // second_wait + 1)) + 2


def update(
        data: RepetitionData,
        content: Text | Dialogue,
        streaks: list[Streak],
        languages: LanguagePair,
        reference_time: datetime,
) -> None:
    """Update the repetition data given the streaks for a content."""
    stats = data.statistics.texts if isinstance(content, Text) else data.statistics.dialogues
    skipped_indices: set[int] = set()
    for index, streak in enumerate(streaks):
        first_review, first_wait, second_wait = get_next_review_times(streak, reference_time)
        if first_review == reference_time:
            stats.sentences += 1
        else:
            skipped_indices.add(index)
        for period in PERIODS:
            stats.cumulative_reviews[period] += get_num_reviews_before(
                first_review,
                first_wait,
                second_wait,
                reference_time + timedelta(days=period),
            )
    candidate = ExamInfo(content, languages.source_language, languages.target_language, skipped_indices)
    if candidate.sentences_to_review > 0:
        stats.exams += 1
        if data.next_exam is None or candidate > data.next_exam:
            data.next_exam = candidate


def compute_repetition_data(source_language: Language | None, target_language: Language | None) -> RepetitionData:
    """Compute spaced repetition mode data."""
    reference_time = now()
    data = RepetitionData()
    with single_session() as session:
        for model in [Text, Dialogue]:
            for content in session.query(model).filter(model.archived_at.is_not(None)):
                for languages, streaks in compute_streaks(content, source_language, target_language).items():
                    update(data, content, streaks, languages, reference_time)
    return data


def print_session_summary_statistics(statistics: RepetitionStatistics) -> None:
    """Display current session statistics."""
    table = build_table(
        title=SESSION_SUMMARY_TITLE,
        headers=[
            METRIC,
            TEXTS,
            DIALOGUES,
            TOTAL,
        ],
        justify={
            METRIC: 'left',
            TEXTS: 'right',
            DIALOGUES: 'right',
            TOTAL: 'right',
        },
        widths={
            METRIC: COLUMN_WIDTH,
            TEXTS: COLUMN_WIDTH,
            DIALOGUES: COLUMN_WIDTH,
            TOTAL: COLUMN_WIDTH,
        },
        data=[
            {
                METRIC: EXAMS,
                TEXTS: str(statistics.texts.exams),
                DIALOGUES: str(statistics.dialogues.exams),
                TOTAL: str(statistics.texts.exams + statistics.dialogues.exams),
            },
            {
                METRIC: SENTENCES,
                TEXTS: str(statistics.texts.sentences),
                DIALOGUES: str(statistics.dialogues.sentences),
                TOTAL: str(statistics.texts.sentences + statistics.dialogues.sentences),
            },
        ],
        group_by=[
            METRIC,
        ],
    )
    print_table(table)


def print_cumulative_reviews_statistics(statistics: RepetitionStatistics) -> None:
    """Display total reviews statistics."""
    metric_column_width = max(len(TEXTS), len(DIALOGUES), len(TOTAL))
    table = build_table(
        title=CUMULATIVE_REVIEWS_TITLE,
        headers=[
            PERIOD,
            TEXTS,
            DIALOGUES,
            TOTAL,
        ],
        justify={
            PERIOD: 'left',
            TEXTS: 'right',
            DIALOGUES: 'right',
            TOTAL: 'right',
        },
        widths={
            PERIOD: COLUMN_WIDTH,
            TEXTS: metric_column_width,
            DIALOGUES: metric_column_width,
            TOTAL: metric_column_width,
        },
        data=[{
            PERIOD: period_title.capitalize(),
            TEXTS: str(statistics.texts.cumulative_reviews[period]),
            DIALOGUES: str(statistics.dialogues.cumulative_reviews[period]),
            TOTAL: str(statistics.texts.cumulative_reviews[period] + statistics.dialogues.cumulative_reviews[period]),
        } for period, period_title in PERIODS.items()],
        group_by=[
            PERIOD,
        ],
    )
    print_table(table)


def print_repetition_statistics(statistics: RepetitionStatistics) -> None:
    """Display spaced repetition statistics."""
    print()
    print_session_summary_statistics(statistics)
    print()
    print_cumulative_reviews_statistics(statistics)
