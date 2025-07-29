from dataclasses import dataclass

from reling.types import DialogueExchangeData, Input

__all__ = [
    'ExchangeWithTranslation',
    'ExplanationRequest',
    'PreScoreWithSuggestion',
    'ScoreWithSuggestion',
    'SentenceWithTranslation',
]


@dataclass
class SentenceWithTranslation:
    sentence: str
    translation: Input | None

    @property
    def input(self) -> Input | None:
        return self.translation

    def all(self) -> list[str]:
        return [self.sentence]

    def input_within_all(self) -> list[str | None]:
        return [self.translation.text if self.translation else None]


@dataclass
class ExchangeWithTranslation:
    exchange: DialogueExchangeData
    user_translation: Input | None

    @property
    def input(self) -> Input | None:
        return self.user_translation

    def all(self) -> list[str]:
        return list(self.exchange.all())

    def input_within_all(self) -> list[str | None]:
        self.exchange.assert_speaker_comes_first()
        return [None, self.user_translation.text if self.user_translation else None]


@dataclass
class PreScoreWithSuggestion:
    score: int
    suggestion: str | None


@dataclass
class ScoreWithSuggestion:
    score: int
    suggestion: str | None


@dataclass
class ExplanationRequest:
    sentence_index: int
    source: bool
