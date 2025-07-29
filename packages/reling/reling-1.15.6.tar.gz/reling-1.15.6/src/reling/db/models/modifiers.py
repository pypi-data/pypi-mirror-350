from sqlalchemy.orm import Mapped, mapped_column

from reling.db.base import Base
from reling.db.enums import Level

__all__ = [
    'Speaker',
    'Style',
    'Topic',
]


class Topic(Base):
    __tablename__ = 'topics'

    name: Mapped[str] = mapped_column(primary_key=True)
    level: Mapped[Level]


class Style(Base):
    __tablename__ = 'styles'

    name: Mapped[str] = mapped_column(primary_key=True)
    level: Mapped[Level]


class Speaker(Base):
    __tablename__ = 'speakers'

    name: Mapped[str] = mapped_column(primary_key=True)
    level: Mapped[Level]
