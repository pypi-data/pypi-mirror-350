from __future__ import annotations
from enum import StrEnum

__all__ = [
    'ContentCategory',
    'Gender',
    'Level',
]


class ContentCategory(StrEnum):
    TEXT = 'text'
    DIALOGUE = 'dialogue'


class Level(StrEnum):
    BASIC = 'basic'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

    def get_included_levels(self) -> list[Level]:
        match self:
            case Level.BASIC:
                return [Level.BASIC]
            case Level.INTERMEDIATE:
                return [Level.BASIC, Level.INTERMEDIATE]
            case Level.ADVANCED:
                return [Level.BASIC, Level.INTERMEDIATE, Level.ADVANCED]
            case _:
                raise NotImplementedError


class Gender(StrEnum):
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'

    def describe(self) -> str:
        match self:
            case Gender.MALE:
                return 'a male'
            case Gender.FEMALE:
                return 'a female'
            case Gender.NONBINARY:
                return 'a nonbinary person'
            case _:
                raise NotImplementedError
