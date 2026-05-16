from calendar import monthrange
from datetime import date
from typing import Literal

from notion_filter import NotionFilter

FilterValue = Literal[
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
    "31", "last_date"
]


def clone_on_monthday_and():
    values: list[FilterValue] = []

    today = date.today()
    values.append(str(today.day))  # type: ignore[list-item]

    last_day = monthrange(today.year, today.month)[1]
    if today.day == last_day:
        values.append("last_date")

    return NotionFilter.multi_select(
        name="clone_on_monthday_and",
        values=values,
    )
