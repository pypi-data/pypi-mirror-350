from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import (
    API_KEY,
    ASR_MODEL,
    EXAM_CONTENT_ARG,
    ExamExtraContentOptions,
    HIDE_PROMPTS_OPT,
    LANGUAGE_OPT,
    LANGUAGE_OPT_FROM,
    LISTEN_OPT,
    MODEL,
    OFFLINE_SCORING_OPT,
    READ_LANGUAGE_OPT,
    RETRY_OPT,
    SCAN_OPT,
    SKIP_OPT,
    TTS_MODEL,
)
from reling.asr import ASRClient
from reling.db.models import Dialogue, Language, Text
from reling.gpt import GPTClient
from reling.helpers.audio import ensure_audio
from reling.helpers.typer import typer_raise
from reling.scanner import ScannerManager, ScannerParams
from reling.tts import get_tts_client
from reling.utils.prompts import enter_to_continue
from .execution import perform_exam
from .repetition import compute_repetition_data, print_repetition_statistics, RepetitionData
from .skips import get_skipped_indices

__all__ = [
    'exam',
]


def adjust_exam_params(
        content: Text | Dialogue | ExamExtraContentOptions,
        from_: Language | None,
        to: Language | None,
        skip: int | None,
        read: list[Language] | None,
        listen: bool,
        scan: int | None,
) -> tuple[
        tuple[
            Text | Dialogue,
            Language,
            Language,
            set[int],
            list[Language],
            bool,
            int | None,
        ] | None,
        RepetitionData | None,
]:
    """Validate and adjust exam parameters; handle spaced repetition mode if requested."""
    read = read or []
    if listen and scan is not None:
        typer_raise('Choose either listen or scan, not both.')
    if read or listen:
        ensure_audio()

    if content == ExamExtraContentOptions.SPACED_REPETITION:
        if skip is not None:
            typer_raise('Cannot skip sentences in spaced repetition mode.')
        repetition_data = compute_repetition_data(source_language=from_, target_language=to)
        if next_exam := repetition_data.next_exam:
            content = next_exam.content
            from_ = next_exam.source_language
            to = next_exam.target_language
            skipped_indices = next_exam.skipped_indices
        else:
            return None, repetition_data
    else:
        if from_ is None and to is None:
            typer_raise('You must specify at least one language.')
        from_ = from_ or content.language
        to = to or content.language
        if from_ == to:
            typer_raise('Source and target languages must be different.')
        repetition_data = None
        skipped_indices = (get_skipped_indices(content, source_language=from_, target_language=to, skip_after=skip)
                           if skip is not None else set())

    for language in read:
        if language not in [from_, to]:
            typer_raise(f'Cannot read in {language.name} as the exam is from {from_.name} to {to.name}.')

    return (content, from_, to, skipped_indices, read, listen, scan), repetition_data


@app.command()
def exam(
        api_key: API_KEY,
        model: MODEL,
        tts_model: TTS_MODEL,
        asr_model: ASR_MODEL,
        content: EXAM_CONTENT_ARG,
        from_: LANGUAGE_OPT_FROM = None,
        to: LANGUAGE_OPT = None,
        skip: SKIP_OPT = None,
        read: READ_LANGUAGE_OPT = None,
        listen: LISTEN_OPT = False,
        scan: SCAN_OPT = None,
        hide_prompts: HIDE_PROMPTS_OPT = False,
        offline_scoring: OFFLINE_SCORING_OPT = False,
        retry: RETRY_OPT = False,
) -> None:
    """
    Test the user's ability to translate content from one language to another.
    If only one language is specified, the content's original language is assumed for the unspecified direction.
    """
    params, repetition_data = adjust_exam_params(content, from_, to, skip, read, listen, scan)

    if repetition_data:
        print_repetition_statistics(repetition_data.statistics)
        print()

    if not params:
        typer_raise('No content to review, exiting.', is_error=False)

    content, from_, to, skipped_indices, read, listen, scan = params

    if repetition_data:
        print(f'Continuing with "{content.id}"...')
        print()
        enter_to_continue()

    set_default_content(content)

    if len(skipped_indices) == content.size:
        typer_raise('All sentences are skipped, exiting.', is_error=False)

    def get_gpt() -> GPTClient:
        return GPTClient(api_key=api_key.get(), model=model.get())

    perform_exam(
        get_gpt,
        content,
        skipped_indices=skipped_indices,
        source_language=from_,
        target_language=to,
        source_tts=(get_tts_client(model=tts_model.get(), api_key=api_key.promise(), language=from_)
                    if from_ in read else None),
        target_tts=(get_tts_client(model=tts_model.get(), api_key=api_key.promise(), language=to)
                    if to in read else None),
        asr=ASRClient(api_key=api_key.get(), model=asr_model.get()) if listen else None,
        scanner_manager=ScannerManager(ScannerParams(
            camera_index=scan,
            gpt=get_gpt(),
        ) if scan is not None else None),
        hide_prompts=hide_prompts,
        offline_scoring=offline_scoring,
        retry=retry,
    )
