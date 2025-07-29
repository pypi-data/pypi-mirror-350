from typing import Callable, Generator

from reling.config import MAX_SCORE
from reling.db.enums import ContentCategory
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogueExchangeData, Promise
from reling.utils.feeders import CharFeeder
from reling.utils.values import coalesce
from .types import ExchangeWithTranslation, ExplanationRequest, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'build_explainer',
]

MISTAKE_THRESHOLD_RATIO = 0.5


def if_not(text: str | None, until_equals: str) -> str | None:
    """Return the text if it does not equal the specified value, otherwise return None."""
    return text if text != until_equals else None


def explain_structure(sentence: str, language: Language) -> list[str]:
    """Generate a prompt section for explaining the structure of a translation in the specified language."""
    return [
        f'The last line is translated into {language.name} as follows:',
        f'"""{sentence}"""',
        f'Explain the structure of this translation to a learner of {language.name}.',
    ]


def explain_mistakes(sentence: str, corrected: str, language: Language, source_language: Language) -> list[str]:
    """Generate a prompt section explaining why a corrected translation is preferred over the provided one."""
    return [
        f'A learner of {language.name} translated the last line as follows:',
        f'"""{sentence}"""',
        f'',
        f'Compare it to the following reference translation:',
        f'"""{corrected}"""',
        f'',
        f'Enumerate the individual differences between the two versions. For each difference:',
        f'- Determine whether it is a mistake.',
        f'- If it is a mistake, specify its type:',
        f'  • **Grammatical error** – the learner’s translation is ungrammatical.',
        f'  • **Unidiomatic phrasing** – the translation is unnatural or awkward.',
        f'  • **Deviation from the original meaning** – the translation alters the intended message.',
        f'- If the mistake is a deviation from the original meaning, translate the learner’s version '
        f'(or relevant parts of it) back into {source_language.name} to clarify the difference.',
    ]


def explain_difference(sentence: str, alternative: str, language: Language) -> list[str]:
    """Generate a prompt section for explaining differences between a provided and an alternative translation."""
    return [
        f'A learner of {language.name} translated the last line as follows:',
        f'"""{sentence}"""',
        f'',
        f'Compare it to the following alternative translation:',
        f'"""{alternative}"""',
        f'',
        f'Enumerate the individual differences between the two versions. For each difference:',
        f'- Explain whether it affects meaning, grammar, or naturalness.',
        f'- Indicate which version is more appropriate and why.',
        f'- If both versions are acceptable, clarify the nuances in their usage and context.',
    ]


def explain_source_structure(sentence: str) -> list[str]:
    """Generate a prompt section for explaining the structure of a sentence in the source language."""
    return [
        f'Explain the grammatical and structural elements of the last line ("""{sentence}""") to a language learner.',
    ]


def do_explain(
        category: ContentCategory,
        gpt: Promise[GPTClient],
        initial_sentences: list[str],
        provided: str,
        original: str,
        result: ScoreWithSuggestion,
        source_language: Language,
        target_language: Language,
        explain_source: bool,
) -> Generator[str, None, None]:
    """Generate an explanation for translations based on user-provided and corrected data."""
    return gpt().ask(
        prompt='\n'.join([
            f'Here is the beginning of a {category.value} in {source_language.name}:',
            f'',
            *initial_sentences,
            f'',
            *(
                explain_source_structure(initial_sentences[-1])
                if explain_source else
                explain_difference(
                    sentence=provided,
                    alternative=alternative,
                    language=target_language,
                )
                if result.score == MAX_SCORE and (alternative := coalesce(
                    if_not(result.suggestion, provided),
                    if_not(original, provided),
                )) else
                explain_mistakes(
                    sentence=provided,
                    corrected=result.suggestion or original,
                    language=target_language,
                    source_language=source_language,
                )
                if MISTAKE_THRESHOLD_RATIO * MAX_SCORE < result.score < MAX_SCORE else
                explain_structure(
                    sentence=result.suggestion or original,
                    language=target_language,
                )
            ),
        ]),
        creative=False,
        feeder_type=CharFeeder,
        auto_normalize=False,
    )


def build_explainer(
        category: ContentCategory,
        gpt: Promise[GPTClient],
        items: list[SentenceWithTranslation | ExchangeWithTranslation],
        original_translations: list[str | DialogueExchangeData],
        results: list[ScoreWithSuggestion | None],
        source_language: Language,
        target_language: Language,
) -> Callable[[ExplanationRequest], Generator[str, None, None]]:
    """Create a function to generate explanations for text or dialogue translations."""
    is_text = category == ContentCategory.TEXT

    def explain(request: ExplanationRequest) -> Generator[str, None, None]:
        index = request.sentence_index
        assert results[index] is not None
        return do_explain(
            category=category,
            gpt=gpt,
            initial_sentences=(
                [item.sentence for item in items[:index + 1]]
                if is_text
                else [turn for item in items[:index + 1] for turn in item.exchange.all()]
            ),
            provided=items[index].input.text,
            original=original_translations[index] if is_text else original_translations[index].user,
            result=results[index],
            source_language=source_language,
            target_language=target_language,
            explain_source=request.source,
        )

    return explain
