from typing import Literal

from notion_filter import NotionFilter

Value = Literal[True, False]


def auto_clone():
    value: Value = True

    return NotionFilter.checkbox(
        name="auto_clone",
        value=value,
    )
