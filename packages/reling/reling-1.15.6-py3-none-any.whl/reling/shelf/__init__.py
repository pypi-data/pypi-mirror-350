from pathlib import Path
import shelve
from typing import Any

__all__ = [
    'delete_value',
    'get_value',
    'init_shelf',
    'set_value',
]

FILENAME: Path | None = None


def init_shelf(filename: Path) -> None:
    global FILENAME
    FILENAME = filename


def get_filename() -> str:
    if FILENAME is None:
        raise RuntimeError('Shelf is not initialized.')
    return str(FILENAME.absolute())


def get_value[T](key: str, default: T | None = None) -> T | None:
    with shelve.open(get_filename()) as db:
        return db.get(key, default)


def set_value(key: str, value: Any) -> None:
    with shelve.open(get_filename()) as db:
        db[key] = value


def delete_value(key: str) -> None:
    with shelve.open(get_filename()) as db:
        if key in db:
            del db[key]
