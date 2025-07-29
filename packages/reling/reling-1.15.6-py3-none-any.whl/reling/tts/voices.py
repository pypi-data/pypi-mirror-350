from enum import StrEnum

from reling.db.enums import Gender

__all__ = [
    'Voice',
]


class Voice(StrEnum):
    ALLOY = 'alloy'
    ASH = 'ash'
    CORAL = 'coral'
    ECHO = 'echo'
    FABLE = 'fable'
    ONYX = 'onyx'
    NOVA = 'nova'
    SAGE = 'sage'
    SHIMMER = 'shimmer'

    @property
    def gender(self) -> Gender:
        match self:
            case Voice.ALLOY:
                return Gender.NONBINARY
            case Voice.ASH:
                return Gender.MALE
            case Voice.CORAL:
                return Gender.FEMALE
            case Voice.ECHO:
                return Gender.MALE
            case Voice.FABLE:
                return Gender.NONBINARY
            case Voice.ONYX:
                return Gender.MALE
            case Voice.NOVA:
                return Gender.FEMALE
            case Voice.SAGE:
                return Gender.FEMALE
            case Voice.SHIMMER:
                return Gender.FEMALE
            case _:
                raise NotImplementedError
