import re
from typing import Generator
from unicodedata import category, normalize

__all__ = [
    'capitalize_first_char',
    'char_range',
    'is_cj',
    'is_punctuation',
    'is_whitespace',
    'replace_prefix_casing',
    'tokenize',
    'universal_normalize',
]

CJ = re.compile(r'[\u4E00-\u9FFF\u3040-\u30FF]')


def universal_normalize(string: str) -> str:
    """Normalize a string using Unicode NFC and replace specific characters."""
    return normalize('NFC', string).replace('’', "'")


def capitalize_first_char(string: str) -> str:
    """Capitalize the first character of a string."""
    return string[:1].upper() + string[1:]


def replace_prefix_casing(string: str, prefix: str) -> str:
    """Replace the prefix of a string with the casing of the given prefix."""
    return prefix + string[len(prefix):] if string.lower().startswith(prefix.lower()) else string


def is_whitespace(char: str, _before: str | None = None, _after: str | None = None) -> bool:
    """Return whether the character is a whitespace character."""
    return category(char).startswith('Z')


def is_punctuation(char: str, before: str | None = None, after: str | None = None) -> bool:
    """Return whether the character is a punctuation symbol."""
    if char in ["'", '’'] and before and not is_whitespace(before) and after and not is_whitespace(after):
        return False
    return category(char).startswith('P')


def is_cj(char: str, _before: str | None = None, _after: str | None = None) -> bool:
    """Return whether the character is a Chinese or Japanese character."""
    return CJ.fullmatch(char) is not None


def tokenize(string: str, *, punctuation: bool = True, whitespace: bool = True, cj: bool = True) -> list[str]:
    """Tokenize a string into words, punctuation, whitespace, and individual CJ characters."""
    tokens: list[str] = []
    current: list[str] = []
    for index, char in enumerate(string):
        for (checker, should_include) in [
            (is_punctuation, punctuation),
            (is_whitespace, whitespace),
            (is_cj, cj),
        ]:
            if checker(
                    char,
                    string[index - 1] if index > 0 else None,
                    string[index + 1] if index + 1 < len(string) else None,
            ):
                if current:
                    tokens.append(''.join(current))
                    current.clear()
                if should_include:
                    tokens.append(char)
                break
        else:
            current.append(char)
    if current:
        tokens.append(''.join(current))
    return tokens


def char_range(from_char: str, to_char: str) -> Generator[str, None, None]:
    """Generate characters from the given range, inclusive."""
    direction = 1 if from_char <= to_char else -1
    for char_code in range(ord(from_char), ord(to_char) + direction, direction):
        yield chr(char_code)
