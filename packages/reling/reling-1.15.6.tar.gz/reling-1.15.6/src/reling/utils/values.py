__all__ = [
    'coalesce',
    'ensure_not_none',
    'wrap_in_list',
]


def ensure_not_none[T](value: T | None) -> T:
    """Raise a ValueError if the value is None."""
    if value is None:
        raise ValueError('Value cannot be None.')
    return value


def coalesce[T](*values: T | None) -> T | None:
    """Return the first non-null value, if any."""
    return next((value for value in values if value is not None), None)


def wrap_in_list[T](value: T | None) -> list[T]:
    """Wrap the value in a list if it is not None."""
    return [value] if value is not None else []
