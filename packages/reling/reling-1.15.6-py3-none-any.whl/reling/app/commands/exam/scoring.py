from typing import Generator

from lcs2 import lcs_indices
from tqdm import tqdm

from reling.app.exceptions import AlgorithmException
from reling.config import MAX_SCORE
from reling.db.enums import ContentCategory
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.helpers.scoring import calculate_diff_score
from reling.types import DialogueExchangeData, Promise
from reling.utils.english import pluralize
from reling.utils.iterables import extract_items, group_items, intersperse, strict_zip
from reling.utils.transformers import add_numbering, apply, get_number, omit_empty, remove_numbering, strip
from reling.utils.values import wrap_in_list
from .types import ExchangeWithTranslation, PreScoreWithSuggestion, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'score_translations',
]

NA = 'N/A'


def build_prompt_translation(
        category: ContentCategory,
        source_language: Language,
        target_language: Language,
        blocks: list[str],
        translations: list[str | None],
) -> str:
    """Build a prompt for scoring translations."""
    # Speaker turns in dialogues are "graded" as well so that the model appreciates the context.
    total = len(blocks)
    numbers = [get_number(index) for index, translation in enumerate(translations) if translation is not None]
    n = len(numbers)
    return '\n'.join([
        f'Below {'is' if total == 1 else 'are'} {total} {pluralize('sentence', total)} from a {category.value} '
        f'in {source_language.name}, along with {'a ' if n == 1 else ''}{pluralize('translation', n)} '
        f'of {n} of them into {target_language.name} made by a language learner.',

        f'Score {'the' if n == 1 else 'each'} translation on a scale from 0 to {MAX_SCORE}. '
        f'If {'the' if n == 1 else 'a'} translation is empty, very short, or poor, assign a low score. ',
        f'If {'the' if n == 1 else 'a'} translation is less than perfect, suggest a minimally modified version that '
        f'would deserve a {MAX_SCORE}.',

        f'{'Provide' if n == 1 else 'For each translation, provide'} your feedback on exactly five lines '
        f'(without adding bullet points or dashes in front of them):',
        f'- number of the sentence being evaluated on the first line (one of {', '.join(numbers)});',
        f'- original sentence on the second line;',  # The first three lines help improve the model's performance
        f'- learner\'s translation on the third line;',
        f'- score (just the number) on the fourth line;',
        f'- suggested modified translation (or "{NA}") on the fifth line.',

        *([f'Provide this feedback for each of the {n} translations, on exactly {n * 5} lines.'] if n > 1 else []),
        f'Say nothing else.',
        f'',
        f'The original {category.value} is:',
        *apply(add_numbering, blocks),
        f'',
        f'The translations are:',
        *(add_numbering(translation, index)
          for index, translation in enumerate(translations)
          if translation is not None),
    ])


def parse_scoring(string_score: str, suggestion: str) -> PreScoreWithSuggestion:
    """
    Parse the score and suggestion from the model output.
    :raises AlgorithmException: If there is an issue with the output of the model.
    """
    try:
        score = int(string_score)
    except ValueError:
        raise AlgorithmException(f'Could not parse the score as an integer from the model output: {string_score}.')
    if score < 0 or score > MAX_SCORE:
        raise AlgorithmException(f'The score {score} given by the model is not in the range from 0 to {MAX_SCORE}.')
    return PreScoreWithSuggestion(
        score=score,
        suggestion=(suggestion or None) if suggestion != NA else None,
    )


def ask_and_parse_translation(gpt: GPTClient, prompt: str) -> Generator[PreScoreWithSuggestion, None, None]:
    """
    Ask the model to score translations and parse the output.
    :raises AlgorithmException: If there is an issue with the output of the model.
    """
    for _, _, _, string_score, suggestion in group_items(gpt.ask(
        prompt,
        creative=False,
        transformers=[strip, omit_empty, remove_numbering],
    ), 5):
        yield parse_scoring(string_score, suggestion)


def build_prompt_averaging(language: Language, sentence: str, a: str, b: str) -> str:
    """Build a prompt for scoring an "averaged" translation."""
    return '\n'.join([
        f'Below are two nearly identical sentences in {language.name}:',

        add_numbering(a, 0),
        add_numbering(b, 1),

        f'A learner of {language.name} briefly viewed both sentences and was then asked to reproduce a similar '
        f'sentence from memory. The learner\'s response is provided below:',

        f'"""{sentence}"""',

        f'Score the learner\'s response on a scale from 0 to {MAX_SCORE}. Deduct points if the response contains '
        f'grammatical errors or does not convey the same meaning as the original sentences.',

        f'If the response is less than perfect, suggest a minimally modified version of it that would deserve a score '
        f'of {MAX_SCORE}.',

        f'Provide your feedback on exactly two lines (without adding bullet points or dashes in front of them):',
        f'- the score (just the number) on the first line;',
        f'- the suggested improved response (or "{NA}") on the second line (do not enclose it in quotes).',
    ])


def ask_and_parse_averaging(gpt: GPTClient, prompt: str) -> PreScoreWithSuggestion:
    """
    Ask the model to score an "averaged" translation and parse the output.
    :raises AlgorithmException: If there is an issue with the output of the model.
    """
    for string_score, suggestion in group_items(gpt.ask(
            prompt,
            creative=False,
            transformers=[strip, omit_empty, remove_numbering],
    ), 2):
        return parse_scoring(string_score, suggestion)
    raise AlgorithmException('The model did not provide a response.')


def lcs_indices_a(a: str, b: str) -> set[int | tuple[int, int]]:
    """
    Return a set of indices and consecutive index pairs in `a` that are part of the longest common subsequence with `b`.
    Consecutive index pairs are included only if the corresponding indices in `b` are also consecutive.
    """
    result: set[int | tuple[int, int]] = set()
    last_a_index = last_b_index = None
    for a_index, b_index in lcs_indices(a, b):
        result.add(a_index)
        if last_a_index == a_index - 1 and last_b_index == b_index - 1:
            result.add((last_a_index, a_index))
        last_a_index, last_b_index = a_index, b_index
    return result


def finalize_scoring(
        provided_translation: str,
        default_score: int | None = None,
        default_suggestion: str | None | None = None,
        perfect_options: set[str] | None = None,
) -> ScoreWithSuggestion:
    """
    Finalize the scoring by comparing the provided translation with the default suggestion and the perfect options
    and returning the best score and suggestion.
    """
    if default_score is None and default_suggestion is None and perfect_options is None:
        raise ValueError('At least one of the optional arguments must be provided.')

    if not provided_translation:
        return ScoreWithSuggestion(0, None)

    options = wrap_in_list(default_suggestion) + sorted(perfect_options - set(wrap_in_list(default_suggestion)))
    option_scores = [calculate_diff_score(provided_translation, option) for option in options]
    best_option_index = option_scores.index(max(option_scores)) if option_scores else None

    score, suggestion = (
        (option_scores[best_option_index], options[best_option_index])
        if option_scores and (default_score is None or option_scores[best_option_index] >= default_score)
        else (default_score, default_suggestion)
    )

    return ScoreWithSuggestion(
        score=score,
        suggestion=suggestion if suggestion != provided_translation and score > 0 else None,
    )


def fix_scoring(
        gpt: GPTClient,
        language: Language,
        provided_translation: str,
        original_translation: str,
        perfect_options: set[str],
        score: PreScoreWithSuggestion,
) -> ScoreWithSuggestion:
    """
    Fix the scoring by comparing the provided translation with the original translation and the suggested translation,
    as well as the perfect options, and returning the best score and suggestion.
    """
    default = (
        score if (score.suggestion is None
                  # If the provided translation shares as much or more common characters (individual indices)
                  # and omissions (pairs of consecutive indices) with the suggestion as with the original translation,
                  # proceed with the current score; otherwise, recalculate the score using "averaging":
                  or lcs_indices_a(provided_translation, score.suggestion)
                  >= lcs_indices_a(provided_translation, original_translation))
        else ask_and_parse_averaging(
            gpt,
            build_prompt_averaging(language, provided_translation, a=original_translation, b=score.suggestion),
        )
    )
    return finalize_scoring(
        provided_translation,
        default.score,
        default.suggestion,
        perfect_options,
    )


def extract_translation(translation: str | DialogueExchangeData) -> str:
    """Extract the translation from a sentence or a user turn in a dialogue."""
    return translation.user if isinstance(translation, DialogueExchangeData) else translation


def map_to_null_if_not[T](condition: bool, items: list[T]) -> list[T | None]:
    """Map the items to `None` if the condition is not met."""
    return [item if condition else None for item in items]


def score_offline(
        items: list[SentenceWithTranslation] | list[ExchangeWithTranslation],
        original_translations: list[str] | list[DialogueExchangeData],
        previous_perfect: list[set[str]],
) -> Generator[ScoreWithSuggestion | None, None, None]:
    """Score the translations of a text or user turns in a dialogue offline."""
    for item, original_translation, perfect in zip(items, original_translations, previous_perfect):
        yield finalize_scoring(
            provided_translation=item.input.text,
            default_score=None,
            default_suggestion=extract_translation(original_translation),
            perfect_options=perfect,
        ) if item.input else None


def score_with_gpt(
        category: ContentCategory,
        gpt: Promise[GPTClient],
        items: list[SentenceWithTranslation] | list[ExchangeWithTranslation],
        original_translations: list[str] | list[DialogueExchangeData],
        previous_perfect: list[set[str]],
        source_language: Language,
        target_language: Language,
) -> Generator[ScoreWithSuggestion | None, None, None]:
    """
    Score the translations of a text or user turns in a dialogue with the help of a GPT model.
    :raises AlgorithmException: If there is an issue with the output of the model.
    """
    translated_indices_set = {index for index in range(len(items)) if items[index].input}
    empty_translation_indices_set = {
        index for index in range(len(items))
        if index in translated_indices_set and not items[index].input.text
    }
    indices = [
        index for index in range(len(items))
        if index in translated_indices_set and index not in empty_translation_indices_set
        and items[index].input.text not in {extract_translation(original_translations[index])} | previous_perfect[index]
    ]
    indices_set = set(indices)
    client, prompt = (gpt(), build_prompt_translation(
        category=category,
        source_language=source_language,
        target_language=target_language,
        blocks=[block for item in items for block in item.all()],
        translations=[translation for index, item in enumerate(items)
                      for translation in map_to_null_if_not(index in indices_set, item.input_within_all())],
    )) if indices_set else (None, None)
    outer: list[
        tuple[SentenceWithTranslation, str, set[str], PreScoreWithSuggestion] |
        tuple[ExchangeWithTranslation, DialogueExchangeData, set[str], PreScoreWithSuggestion] |
        None
    ] = [None] * (len(items) - len(indices))
    for index, data in enumerate(intersperse(outer, zip(strict_zip(
            AlgorithmException('The model returned an unexpected number of results.'),
            extract_items(items, indices),
            extract_items(original_translations, indices),
            extract_items(previous_perfect, indices),
            tqdm(
                ask_and_parse_translation(client, prompt),
                desc='Scoring translations',
                total=len(indices),
                leave=False,
            ) if client and prompt else [],
    ), indices))):
        if data is None:
            yield (ScoreWithSuggestion(0 if index in empty_translation_indices_set else MAX_SCORE, None)
                   if index in translated_indices_set else None)
        else:
            item, original_translation, perfect, pre_score = data
            assert client is not None
            yield fix_scoring(
                client,
                target_language,
                item.input.text,
                extract_translation(original_translation),
                perfect,
                pre_score,
            )


def score_translations(
        category: ContentCategory,
        gpt: Promise[GPTClient],
        items: list[SentenceWithTranslation] | list[ExchangeWithTranslation],
        original_translations: list[str] | list[DialogueExchangeData],
        previous_perfect: list[set[str]],
        source_language: Language,
        target_language: Language,
        offline: bool,
) -> Generator[ScoreWithSuggestion | None, None, None]:
    """
    Score the translations of a text or user turns in a dialogue and provide suggestions for improvement.
    `None`s are yielded for the sentences or turns that are not translated.
    :raises AlgorithmException: If there is an issue with the scoring algorithm.
    """
    if offline:
        yield from score_offline(
            items=items,
            original_translations=original_translations,
            previous_perfect=previous_perfect,
        )
    else:
        yield from score_with_gpt(
            category=category,
            gpt=gpt,
            items=items,
            original_translations=original_translations,
            previous_perfect=previous_perfect,
            source_language=source_language,
            target_language=target_language,
        )
