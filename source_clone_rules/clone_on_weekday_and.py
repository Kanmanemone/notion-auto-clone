from datetime import date
from typing import Literal

from notion_filter import NotionFilter

FilterValue = Literal[
    "월 (mon)", "화 (tue)", "수 (wed)", "목 (thu)", "금 (fri)", "토 (sat)", "일 (sun)"
]


def clone_on_weekday_and():
    values: list[FilterValue] = []

    today = date.today()
    weekday = today.weekday()

    if weekday == 0:
        values.append("월 (mon)")
    elif weekday == 1:
        values.append("화 (tue)")
    elif weekday == 2:
        values.append("수 (wed)")
    elif weekday == 3:
        values.append("목 (thu)")
    elif weekday == 4:
        values.append("금 (fri)")
    elif weekday == 5:
        values.append("토 (sat)")
    elif weekday == 6:
        values.append("일 (sun)")

    return NotionFilter.multi_select(
        name="clone_on_weekday_and",
        values=values,
    )
