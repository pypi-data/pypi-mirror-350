from reling.app.default_content import get_default_content_id
from reling.db import single_session
from reling.db.models import Dialogue, Text
from reling.helpers.typer import typer_raise

__all__ = [
    'find_content',
]


def find_content[T](
        content_id: str,
        last_content_marker: str,
        extra_options: dict[str, T] | None = None,
) -> Text | Dialogue | T | None:
    """Find a text or dialogue by its ID."""
    if extra_options and content_id in extra_options:
        return extra_options[content_id]
    if content_id == last_content_marker:
        content_id = get_default_content_id()
        if content_id is None:
            typer_raise('No content has been interacted with yet')
    with single_session() as session:
        return session.get(Text, content_id) or session.get(Dialogue, content_id)
