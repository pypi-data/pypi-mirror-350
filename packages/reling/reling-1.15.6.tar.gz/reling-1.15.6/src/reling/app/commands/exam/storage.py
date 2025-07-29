from datetime import datetime, timedelta

from reling.db import single_session
from reling.db.models import Dialogue, DialogueExam, DialogueExamResult, Language, Text, TextExam, TextExamResult
from reling.utils.ids import generate_id
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'save_exam',
]


def save_exam(
        content: Text | Dialogue,
        source_language: Language,
        target_language: Language,
        read_source: bool,
        read_target: bool,
        listened: bool,
        scanned: bool,
        started_at: datetime,
        finished_at: datetime,
        total_pause_time: timedelta,
        items: list[SentenceWithTranslation | ExchangeWithTranslation],
        results: list[ScoreWithSuggestion | None],
) -> TextExam | DialogueExam:
    """Save the results of a text or dialogue exam."""
    is_text = isinstance(content, Text)
    with single_session() as session:
        exam = (TextExam if is_text else DialogueExam)(
            id=generate_id(),
            content_id=content.id,
            source_language_id=source_language.id,
            target_language_id=target_language.id,
            read_source=read_source,
            read_target=read_target,
            listened=listened,
            scanned=scanned,
            started_at=started_at,
            finished_at=finished_at,
            total_pause_time=total_pause_time,
        )
        session.add(exam)
        for index, (item, result) in enumerate(zip(items, results)):
            if result is not None:
                session.add((TextExamResult if is_text else DialogueExamResult)(
                    exam_id=exam.id,
                    index=index,
                    answer=item.input.text,
                    suggested_answer=result.suggestion,
                    score=result.score,
                ))
        session.commit()
        return exam
