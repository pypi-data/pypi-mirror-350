from dataclasses import dataclass

from reling.shelf import delete_value, get_value, set_value

__all__ = [
    'get_log',
    'GptLogItem',
    'log',
]

ITEMS_VAR_NAME = 'GPT_LOG_ITEM_{index}'
COUNT_VAR_NAME = 'GPT_LOG_COUNT'

CURRENT_RUN_COUNT = 0


@dataclass
class GptLogItem:
    prompt: str
    temperature: float
    response: str


def clear() -> None:
    """Remove all items from the GPT log."""
    for index in range(get_value(COUNT_VAR_NAME, 0)):
        delete_value(ITEMS_VAR_NAME.format(index=index))


def log(item: GptLogItem) -> None:
    """Append an item to the GPT log; if this is the first item, clear the log from the previous run first."""
    global CURRENT_RUN_COUNT
    if CURRENT_RUN_COUNT == 0:
        clear()
    set_value(ITEMS_VAR_NAME.format(index=CURRENT_RUN_COUNT), item)
    CURRENT_RUN_COUNT += 1
    set_value(COUNT_VAR_NAME, CURRENT_RUN_COUNT)


def get_log() -> list[GptLogItem]:
    """Get the GPT log items."""
    count = get_value(COUNT_VAR_NAME, 0)
    return [
        get_value(ITEMS_VAR_NAME.format(index=index))
        for index in range(count)
    ]
