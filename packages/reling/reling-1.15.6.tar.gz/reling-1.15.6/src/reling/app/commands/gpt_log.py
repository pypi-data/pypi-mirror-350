from reling.app.app import app
from reling.gpt_log import get_log

__all__ = [
    'gpt_log',
]

ITEM_DIVIDER = '-' * 10


@app.command(hidden=True)
def gpt_log() -> None:
    """Display the GPT log from the last application run."""
    for item_index, item in enumerate(get_log()):
        if item_index > 0:
            print(ITEM_DIVIDER + '\n')
        print(f'Prompt:\n"""\n{item.prompt}\n"""\n')
        print(f'Temperature:\n{item.temperature}\n')
        print(f'Response:\n"""\n{item.response}\n"""\n')
