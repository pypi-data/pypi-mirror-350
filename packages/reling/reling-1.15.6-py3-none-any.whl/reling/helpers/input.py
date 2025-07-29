from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from tempfile import mkstemp
from typing import Callable, Generator

from reling.db.models import Language
from reling.scanner import Scanner
from reling.types import Input, Transcriber
from reling.utils.console import input_and_erase, interruptible_input, print_and_erase, print_and_maybe_erase
from reling.utils.prompts import ENTER, format_shortcut, Prompt
from .wave import FILE_EXTENSION, play, record

__all__ = [
    'get_input',
    'ScannerParams',
    'TranscriberParams',
]


class AudioAction(StrEnum):
    RE_RECORD = 're-record'
    LISTEN = 'listen'
    MANUAL_INPUT = 'manual input'


class ImageAction(StrEnum):
    RETAKE = 'retake'
    MANUAL_INPUT = 'manual input'


MANUAL_SHORTCUT = 'm'
assert MANUAL_SHORTCUT == AudioAction.MANUAL_INPUT.value[0] == ImageAction.MANUAL_INPUT.value[0]
SKIP_SHORTCUT = 's'

MULTIMEDIA_PROMPT = (f'({ENTER} to {{action}},'
                     f' {format_shortcut(MANUAL_SHORTCUT)} to input manually,'
                     f' {format_shortcut(SKIP_SHORTCUT)} to skip)')

START_RECORDING = 'start recording'
RECORDING_REDO_SHORTCUT = AudioAction.RE_RECORD.value[0]
RECORDING_UNTIL_ENTER = f'(recording... {ENTER} to stop, {format_shortcut(RECORDING_REDO_SHORTCUT)} to redo)'
TRANSCRIBING = '(transcribing...)'

CAPTURE_IMAGE = 'capture image'
CAPTURING = '(capturing...)'
PROCESSING = '(processing...)'

PAUSED = f'PAUSED ({ENTER} to resume)'


@dataclass
class TranscriberParams:
    transcribe: Transcriber
    storage: Path


@dataclass
class ScannerParams:
    scanner: Scanner
    language: Language


@dataclass
class ResultToReturn:
    result: Input | None


def prompt_multimedia(prefix: str, action: str) -> ResultToReturn | None:
    """Prompt the user for an action related to multimedia input."""
    response = input_and_erase(prefix + MULTIMEDIA_PROMPT.format(action=action)).strip().lower()
    if response == MANUAL_SHORTCUT.lower():
        return ResultToReturn(None)
    elif response == SKIP_SHORTCUT.lower():
        return ResultToReturn(Input(''))
    else:
        return None


@contextmanager
def pausing(on_pause: Callable[[], None], on_resume: Callable[[], None]) -> Generator[None, None, None]:
    """Pause and then resume once the context is exited."""
    on_pause()
    yield
    on_resume()


def get_manual_input(prompt: str, suggestions: list[str]) -> Input:
    """Prompt the user for manual input."""
    return Input(interruptible_input(prompt, suggestions, mouse_support=True))


def get_temp_file(storage: Path) -> Path:
    """Generate a temporary file in the given storage directory."""
    return Path(mkstemp(dir=storage, suffix=FILE_EXTENSION)[1])


def do_record(prompt: str, file: Path) -> bool:
    """Record audio and return whether the user is satisfied with the recording."""
    with record(file):
        return input_and_erase(prompt + RECORDING_UNTIL_ENTER).strip().lower() != RECORDING_REDO_SHORTCUT.lower()


def do_transcribe(prompt: str, transcribe: Transcriber, file: Path) -> str:
    """Transcribe the audio file and return the transcription."""
    with print_and_erase(prompt + TRANSCRIBING):
        try:
            return transcribe(file)
        except KeyboardInterrupt:
            return ''


def get_audio_input(
        prompt: str,
        params: TranscriberParams,
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
        dynamic_suggestions: list[str],
) -> Input | None:
    """
    Get input from the user via audio recording, with options for re-recording, listening, and manual input.
    :return: The user's input, or None if the user has chosen to manually input the text.
    """
    if result := prompt_multimedia(prompt, START_RECORDING):
        return result.result
    file = get_temp_file(params.storage)
    while True:
        if not do_record(prompt, file):
            continue
        with pausing(on_pause, on_resume):
            transcription = do_transcribe(prompt, params.transcribe, file)
            dynamic_suggestions.append(transcription)
        with print_and_maybe_erase(prompt + transcription) as do_erase:
            try:
                while True:
                    match Prompt.from_enum(AudioAction).prompt():
                        case AudioAction.RE_RECORD:
                            do_erase()
                            break
                        case AudioAction.LISTEN:
                            try:
                                play(file)
                            except KeyboardInterrupt:
                                pass
                        case AudioAction.MANUAL_INPUT:
                            do_erase()
                            return None
                        case None:
                            return Input(transcription, audio=file)
                        case _:
                            assert False
            except KeyboardInterrupt:
                do_erase()
                raise


def do_scan(prompt: str, scanner: Scanner, language: Language) -> str:
    """Capture an image and return the extracted text."""
    with print_and_erase(prompt + CAPTURING):
        try:
            image = scanner.capture()
        except KeyboardInterrupt:
            return ''
    with print_and_erase(prompt + PROCESSING):
        try:
            return scanner.process(image, language)
        except KeyboardInterrupt:
            return ''


def get_image_input(
        prompt: str,
        params: ScannerParams,
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
        dynamic_suggestions: list[str],
) -> Input | None:
    """
    Get input from the user via image capture, with options for retaking or manual input.
    :return: The user's input, or None if the user has chosen to manually input the text.
    """
    if result := prompt_multimedia(prompt, CAPTURE_IMAGE):
        return result.result
    while True:
        with pausing(on_pause, on_resume):
            text = do_scan(prompt, params.scanner, params.language)
            dynamic_suggestions.append(text)
        with print_and_maybe_erase(prompt + text) as do_erase:
            try:
                while True:
                    match Prompt.from_enum(ImageAction).prompt():
                        case ImageAction.RETAKE:
                            do_erase()
                            break
                        case ImageAction.MANUAL_INPUT:
                            do_erase()
                            return None
                        case None:
                            return Input(text)
                        case _:
                            assert False
            except KeyboardInterrupt:
                do_erase()
                raise


def get_input(
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
        prompt: str = '',
        input_suggestions: list[str] | None = None,
        transcriber_params: TranscriberParams | None = None,
        scanner_params: ScannerParams | None = None,
) -> Input:
    """Get user input, optionally via audio recording or image capture."""
    if transcriber_params and scanner_params:
        raise ValueError('Cannot use both transcriber and scanner.')
    dynamic_suggestions = [*(input_suggestions or [])]
    while True:
        try:
            return (
                (transcriber_params and get_audio_input(
                    prompt,
                    transcriber_params,
                    on_pause,
                    on_resume,
                    dynamic_suggestions,
                ))
                or
                (scanner_params and get_image_input(
                    prompt,
                    scanner_params,
                    on_pause,
                    on_resume,
                    dynamic_suggestions,
                ))
                or
                get_manual_input(prompt, dynamic_suggestions)
            )
        except KeyboardInterrupt:
            with pausing(on_pause, on_resume):
                input_and_erase(PAUSED)
