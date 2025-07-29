from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, cast

from rich.console import Console
from rich.text import Text

from reling.tts import TTSVoiceClient
from reling.types import Reader, Speed
from reling.utils.console import clear_current_line, input_and_erase
from reling.utils.prompts import ENTER, Prompt, PromptOption
from reling.utils.values import coalesce, ensure_not_none
from .colors import fade

__all__ = [
    'output',
    'SentenceData',
]

NA = fade('N/A')

PLAY_PROMPT_TITLE = 'Play'
NORMAL_SPEED = 'normal speed'
SLOWLY = 'slowly'
REPLAY = 'replay'

INTERRUPTED = f'INTERRUPTED ({ENTER} to continue)'


@dataclass
class SentenceData:
    print_text: str | Text | None = None
    print_prefix: str | Text | None = None
    reader: Reader | None = None
    reader_id: str | None = None

    @staticmethod
    def from_tts(
            text: str | None,
            client: TTSVoiceClient | None,
            *,
            print_text: str | Text | None = None,
            print_prefix: str | Text | None = None,
            reader_id: str | None = None,
    ) -> SentenceData:
        return SentenceData(
            print_text=coalesce(print_text, text),
            print_prefix=print_prefix,
            reader=client.get_reader(text) if client and (text is not None) else None,
            reader_id=reader_id,
        )


@dataclass
class ReaderWithSpeed:
    reader: Reader
    speed: Speed


@dataclass
class ReaderWithId:
    reader: Reader
    id: str


type OutputPromptOption = ReaderWithSpeed | Callable[[], None]
type OutputPrompt = Prompt[OutputPromptOption]


def add_single_sentence_options(prompt: OutputPrompt, reader: Reader) -> None:
    """Attach the options for a single sentence to the prompt: '[n]ormal speed | [s]lowly'."""
    prompt.add_option(PromptOption(
        description=NORMAL_SPEED,
        action=ReaderWithSpeed(reader, Speed.NORMAL),
    ))
    prompt.add_option(PromptOption(
        description=SLOWLY,
        action=ReaderWithSpeed(reader, Speed.SLOW),
    ))


def add_multi_sentence_options(prompt: OutputPrompt, readers: list[ReaderWithId]) -> None:
    """Attach the options for multiple sentences to the prompt: '[i]mproved | [is] | [o]riginal | [os]'."""
    for reader in readers:
        prompt.add_option(PromptOption(
            description=reader.id,
            action=ReaderWithSpeed(reader.reader, Speed.NORMAL),
            modifiers={
                SLOWLY: ReaderWithSpeed(reader.reader, Speed.SLOW),
            },
        ))


def add_extra_options(prompt: OutputPrompt, extra_options: list[PromptOption[Callable[[], None]]]) -> None:
    """Attach the extra options to the prompt."""
    for option in extra_options:
        prompt.add_option(option)


def construct_play_prompt(
        sentences_with_readers: list[SentenceData],
        current: ReaderWithSpeed | None,
        multi_sentence: bool,
        extra_options: list[PromptOption[Callable[[], None]]],
) -> OutputPrompt:
    """
    Construct a prompt for the user to choose the next sentence to read and the speed of the reading.
    :raises ValueError: If reader_id is not provided for a sentence with a reader in a multi-sentence output.
    """
    prompt: OutputPrompt = Prompt(PLAY_PROMPT_TITLE)
    if multi_sentence:
        add_multi_sentence_options(prompt, [
            ReaderWithId(
                reader=ensure_not_none(sentence.reader),
                id=ensure_not_none(sentence.reader_id),
            )
            for sentence in sentences_with_readers
        ])
    else:
        add_single_sentence_options(prompt, sentences_with_readers[0].reader)
    if current:
        prompt.add_option(PromptOption(
            description=REPLAY,
            action=current,
        ))
    add_extra_options(prompt, extra_options)
    return prompt


def do_prompt(prompt: OutputPrompt) -> OutputPromptOption | None:
    """Prompt the user and return the chosen option."""
    while True:
        try:
            return prompt.prompt()
        except KeyboardInterrupt:
            input_and_erase(INTERRUPTED)


def invoke(option: OutputPromptOption) -> None:
    """Invoke the reader or the function."""
    try:
        if isinstance(option, ReaderWithSpeed):
            option.reader(option.speed)
        else:
            option()
    except KeyboardInterrupt:
        pass
    clear_current_line()  # Otherwise the input made during the operation will get displayed twice


def output(*sentences: SentenceData, extra_options: list[PromptOption[Callable[[], None]]] | None = None) -> None:
    """
    Output the sentences, reading them if a reader is provided.
    If multiple readers are provided, the user can choose which sentence to read next.
    The user can also choose the speed of the reading.

    :raises ValueError: If reader_id is not provided for a sentence with a reader in a multi-sentence output.
    """
    extra_options = extra_options or []
    console = Console(highlight=False)
    for sentence in sentences:
        console.print(sentence.print_prefix or '', end='')
        console.print(coalesce(sentence.print_text, cast(str | Text, NA)))
    multi_sentence = len(sentences) > 1
    if sentences_with_readers := [sentence for sentence in sentences if sentence.reader]:
        current = ReaderWithSpeed(sentences_with_readers[0].reader, Speed.NORMAL) if len(sentences) == 1 else None
        while True:
            if current:
                invoke(current)
            current = do_prompt(construct_play_prompt(sentences_with_readers, current, multi_sentence, extra_options))
            if not current:
                break
    elif multi_sentence or extra_options:
        prompt: OutputPrompt = Prompt()
        add_extra_options(prompt, extra_options)
        while True:
            if current := do_prompt(prompt):
                invoke(current)
            else:
                break
