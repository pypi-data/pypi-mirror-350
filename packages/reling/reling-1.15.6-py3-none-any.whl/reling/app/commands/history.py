from datetime import datetime
from typing import cast

from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import ANSWERS_OPT, CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM
from reling.db.models import DialogueExam, DialogueExamResult, Language, TextExam, TextExamResult
from reling.helpers.colors import fade
from reling.helpers.scoring import format_average_score
from reling.helpers.typer import typer_raise
from reling.utils.tables import build_table, print_table, Table
from reling.utils.time import format_time, format_time_delta
from reling.utils.transformers import get_number

__all__ = [
    'history',
]

FROM = 'From'
TO = 'To'
TAKEN_AT = 'Taken at'
DURATION = 'Duration'
SENTENCES = 'Sents'
SCORE = 'Score'

SENTENCE_NUM = '#'
ANSWER = 'Answer'
EMPTY_ANSWER = fade('N/A')

AUDIO_OUTPUT = '🔈'
AUDIO_INPUT = '🎤'
IMAGE_INPUT = '📷'


def match(exam: TextExam | DialogueExam, from_: Language | None, to: Language | None) -> bool:
    return ((from_ is None or cast(Language, exam.source_language).id == from_.id)
            and (to is None or cast(Language, exam.target_language).id == to.id))


def get_sort_key(exam: TextExam | DialogueExam) -> tuple:
    return (
        cast(Language, exam.source_language).name,
        cast(Language, exam.target_language).name,
    )


def get_taken_at(exam: TextExam | DialogueExam) -> str:
    return format_time(cast(datetime, exam.started_at))


def get_default_table(exams: list[TextExam] | list[DialogueExam]) -> Table:
    """Generate a summary table for exam history."""
    return build_table(
        headers=[
            FROM,
            TO,
            TAKEN_AT,
            DURATION,
            SENTENCES,
            SCORE,
        ],
        justify={
            FROM: 'left',
            TO: 'left',
            TAKEN_AT: 'left',
            DURATION: 'right',
            SENTENCES: 'right',
            SCORE: 'right',
        },
        data=[{
            FROM: ' '.join([
                cast(Language, exam.source_language).name,
                *([AUDIO_OUTPUT] if exam.read_source else []),
            ]),
            TO: ' '.join([
                cast(Language, exam.target_language).name,
                *([AUDIO_OUTPUT] if exam.read_target else []),
                *([AUDIO_INPUT] if exam.listened else []),
                *([IMAGE_INPUT] if exam.scanned else []),
            ]),
            TAKEN_AT: get_taken_at(exam),
            DURATION: format_time_delta(exam.duration),
            SENTENCES: str(len(cast(list, exam.results))),
            SCORE: format_average_score(exam),
        } for exam in exams],
        group_by=[
            FROM,
            TO,
        ],
    )


def get_answers_table(exams: list[TextExam] | list[DialogueExam], include_from: bool, include_to: bool) -> Table:
    """Generate a detailed table showing answers for each exam."""
    if not exams:
        raise ValueError('No exams provided.')
    size = exams[0].content.size
    by_langs_and_index: dict[
        tuple[Language, Language],
        list[list[tuple[TextExamResult | DialogueExamResult, TextExam | DialogueExam]]],
    ] = {}
    for exam in exams:
        for result in exam.results:
            by_langs_and_index.setdefault(
                (exam.source_language, exam.target_language),
                [[] for _ in range(size)],
            )[result.index].append((result, exam))
    return build_table(
        headers=[
            *([FROM] if include_from else []),
            *([TO] if include_to else []),
            SENTENCE_NUM,
            TAKEN_AT,
            SCORE,
            ANSWER,
        ],
        justify={
            **({FROM: 'left'} if include_from else {}),
            **({TO: 'left'} if include_to else {}),
            SENTENCE_NUM: 'right',
            TAKEN_AT: 'left',
            SCORE: 'right',
            ANSWER: 'left',
        },
        data=[
            {
                **({FROM: source_language.name} if include_from else {}),
                **({TO: target_language.name} if include_to else {}),
                SENTENCE_NUM: get_number(sentence_index),
                TAKEN_AT: get_taken_at(exam),
                SCORE: str(result.score),
                ANSWER: result.answer or EMPTY_ANSWER,
            }
            for (source_language, target_language), items in by_langs_and_index.items()
            for sentence_index, results in enumerate(items)
            for result, exam in results
        ],
        group_by=[
            *([FROM] if include_from else []),
            *([TO] if include_to else []),
            SENTENCE_NUM,
        ],
    )


@app.command()
def history(
        content: CONTENT_ARG,
        from_: LANGUAGE_OPT_FROM = None,
        to: LANGUAGE_OPT = None,
        answers: ANSWERS_OPT = False,
) -> None:
    """Display exam history, optionally filtered by source or target language."""
    set_default_content(content)
    exams = sorted(
        filter(lambda e: match(e, from_, to), content.exams),
        key=get_sort_key,
    )
    if exams:
        table = get_answers_table(
            exams,
            include_from=from_ is None,
            include_to=to is None,
        ) if answers else get_default_table(exams)
        print_table(table)
    else:
        typer_raise('No exams found.', is_error=False)
