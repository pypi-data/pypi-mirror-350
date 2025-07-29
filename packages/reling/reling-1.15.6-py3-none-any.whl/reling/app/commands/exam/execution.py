from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from reling.app.exceptions import AlgorithmException
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.asr import ASRClient
from reling.config import MAX_SCORE
from reling.db.enums import ContentCategory, Gender
from reling.db.models import Dialogue, DialogueExam, Language, Text, TextExam
from reling.gpt import GPTClient
from reling.helpers.typer import typer_raise
from reling.helpers.voices import pick_voices
from reling.scanner import Scanner, ScannerManager
from reling.tts import TTSClient, TTSVoiceClient
from reling.types import DialogueExchangeData, Promise
from reling.utils.timetracker import TimeTracker
from .explanation import build_explainer
from .input import collect_translations
from .presentation import present_results
from .scoring import score_translations
from .storage import save_exam
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'perform_exam',
]


def collect_perfect(content: Text | Dialogue, target_language: Language) -> list[set[str]]:
    """
    Collect the suggestions and correct answers from previous exams in the same target language, indexed by sentence.
    """
    suggestions = [set() for _ in range(content.size)]
    for exam in cast(list[TextExam] | list[DialogueExam], content.exams):
        if exam.target_language == target_language:
            for result in exam.results:
                if result.suggested_answer:
                    suggestions[result.index].add(result.suggested_answer)
                if result.score == MAX_SCORE:
                    suggestions[result.index].add(result.answer)
    return suggestions


def get_voices(
        content: Text | Dialogue,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
) -> tuple[TTSVoiceClient | None, TTSVoiceClient | None, TTSVoiceClient | None]:
    """
    Pick TTS voices based on the content type (text or dialogue):
    - For a Text, return (source_voice, target_voice, None).
    - For a Dialogue, return (source_user_voice, target_user_voice, target_speaker_voice).
    """
    if isinstance(content, Text):
        source_voice, target_voice = pick_voices(None, None)
        return (
            source_tts.with_voice(source_voice) if source_tts else None,
            target_tts.with_voice(target_voice) if target_tts else None,
            None,
        )
    else:
        speaker_voice, user_voice = pick_voices(
            cast(Gender, content.speaker_gender),
            cast(Gender, content.user_gender),
        )
        return (
            source_tts.with_voice(user_voice) if source_tts else None,
            target_tts.with_voice(user_voice) if target_tts else None,
            target_tts.with_voice(speaker_voice) if target_tts else None,
        )


def perform_exam_round(
        gpt: Promise[GPTClient],
        content: Text | Dialogue,
        items: list[str | DialogueExchangeData],
        original_translations: list[str | DialogueExchangeData],
        skipped_indices: set[int],
        source_language: Language,
        target_language: Language,
        source_tts: TTSVoiceClient | None,
        target_speaker_tts: TTSVoiceClient | None,
        asr: ASRClient | None,
        scanner_manager: ScannerManager,
        hide_prompts: bool,
        offline_scoring: bool,
        previous_attempts: list[list[SentenceWithTranslation | ExchangeWithTranslation]],
        previous_scores: list[list[ScoreWithSuggestion]],
        storage: Path,
        tracker: TimeTracker,
) -> tuple[
    list[SentenceWithTranslation | ExchangeWithTranslation],
    list[ScoreWithSuggestion | None],
    Scanner | None,
]:
    """Collect user translations of the text or dialogue, score them, and return the results, all in a single round."""
    with scanner_manager.get_scanner() as scanner:
        tracker.resume()
        translated = list(collect_translations(
            category=ContentCategory.TEXT if isinstance(content, Text) else ContentCategory.DIALOGUE,
            items=items,
            original_translations=original_translations,
            skipped_indices=skipped_indices,
            target_language=target_language,
            source_tts=source_tts,
            target_speaker_tts=target_speaker_tts,
            asr=asr,
            scanner=scanner,
            hide_prompts=hide_prompts,
            previous_attempts=previous_attempts,
            previous_scores=previous_scores,
            storage=storage,
            on_pause=tracker.pause,
            on_resume=tracker.resume,
        ))
        tracker.pause()

    try:
        results = list(score_translations(
            category=ContentCategory.TEXT if isinstance(content, Text) else ContentCategory.DIALOGUE,
            gpt=gpt,
            items=translated,
            original_translations=original_translations,
            previous_perfect=collect_perfect(content, target_language),
            source_language=source_language,
            target_language=target_language,
            offline=offline_scoring,
        ))
    except AlgorithmException as e:
        typer_raise(e.msg)

    return translated, results, scanner


def perform_exam(
        gpt: Promise[GPTClient],
        content: Text | Dialogue,
        skipped_indices: set[int],
        source_language: Language,
        target_language: Language,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
        asr: ASRClient | None,
        scanner_manager: ScannerManager,
        hide_prompts: bool,
        offline_scoring: bool,
        retry: bool,
) -> None:
    """
    Collect user translations of the text or dialogue, score them, save and present the results to the user,
    optionally reading the source and/or target language out loud.
    """
    with TemporaryDirectory() as file_storage:
        is_text = isinstance(content, Text)

        voice_source_tts, voice_target_tts, voice_target_speaker_tts = get_voices(content, source_tts, target_tts)
        items, original_translations = (
            (get_text_sentences if is_text else get_dialogue_exchanges)(content, language, gpt)
            for language in (source_language, target_language)
        )

        updated_skipped_indices = {*skipped_indices}

        translated: list[SentenceWithTranslation | ExchangeWithTranslation] | None = None
        results: list[ScoreWithSuggestion] | None = None

        previous_attempts: list[list[SentenceWithTranslation | ExchangeWithTranslation]] = []
        previous_scores: list[list[ScoreWithSuggestion]] = []

        tracker = TimeTracker()
        tracker.pause()
        while True:
            current_translated, current_results, scanner = perform_exam_round(
                gpt=gpt,
                content=content,
                items=items,
                original_translations=original_translations,
                skipped_indices=updated_skipped_indices,
                source_language=source_language,
                target_language=target_language,
                source_tts=voice_source_tts,
                target_speaker_tts=voice_target_speaker_tts,
                asr=asr,
                scanner_manager=scanner_manager,
                hide_prompts=hide_prompts,
                offline_scoring=offline_scoring,
                previous_attempts=previous_attempts,
                previous_scores=previous_scores,
                storage=Path(file_storage),
                tracker=tracker,
            )

            if translated is None:
                translated = [*current_translated]
                results = [*current_results]
            else:
                for index, (attempt, score) in enumerate(zip(current_translated, current_results)):
                    if attempt.input and attempt.input.text and score and score.score >= results[index].score:
                        translated[index] = attempt
                        results[index] = score

            for index, (attempt, score) in enumerate(zip(current_translated, current_results)):
                if (score and score.score == MAX_SCORE) or (attempt.input and attempt.input.text == ''):
                    updated_skipped_indices.add(index)

            if not retry or len(updated_skipped_indices) == content.size:
                break

            previous_attempts.append(current_translated)
            previous_scores.append(current_results)
        tracker.stop()

        exam = save_exam(
            content=content,
            source_language=source_language,
            target_language=target_language,
            read_source=source_tts is not None,
            read_target=target_tts is not None,
            listened=asr is not None,
            scanned=scanner is not None,
            started_at=tracker.started_at,
            finished_at=tracker.finished_at,
            total_pause_time=tracker.total_pause_time,
            items=translated,
            results=results,
        )

        present_results(
            items=translated,
            original_translations=original_translations,
            exam=exam,
            source_tts=voice_source_tts,
            target_tts=voice_target_tts,
            target_speaker_tts=voice_target_speaker_tts,
            explain=build_explainer(
                category=ContentCategory.TEXT if is_text else ContentCategory.DIALOGUE,
                gpt=gpt,
                items=translated,
                original_translations=original_translations,
                results=results,
                source_language=source_language,
                target_language=target_language,
            ),
        )
