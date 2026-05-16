from typing import Literal

from notion_filter import NotionFilter

FilterValue = Literal[True, False]


def auto_clone():
    value: FilterValue = True

    return NotionFilter.checkbox(
        name="auto_clone",
        value=value,
    )
