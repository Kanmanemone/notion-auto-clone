from calendar import monthrange
from datetime import date

from notion_filter import NotionFilter

def and_filters(f: NotionFilter) -> NotionFilter:
    f.checkbox(
        name="auto_clone",
        value=True,
    )

    today = date.today()
    monthday_values: list[str | None] = [str(today.day)]
    if today.day == monthrange(today.year, today.month)[1]:  # 오늘이 이번 달의 마지막 날이라면, 매달 마지막 날에도 복제하도록 설정
        monthday_values.append("last_date")
    monthday_values.append(None) # "clone_on_monthday_and" 속성이 비어 있는 페이지도 가져오도록 함
    f.multi_select(
        name="clone_on_monthday_and",
        values=monthday_values,
    )

    weekday = today.weekday()
    if weekday == 0:
        weekday_value = "월 (mon)"
    elif weekday == 1:
        weekday_value = "화 (tue)"
    elif weekday == 2:
        weekday_value = "수 (wed)"
    elif weekday == 3:
        weekday_value = "목 (thu)"
    elif weekday == 4:
        weekday_value = "금 (fri)"
    elif weekday == 5:
        weekday_value = "토 (sat)"
    else:
        weekday_value = "일 (sun)"
    f.multi_select(
        name="clone_on_weekday_and",
        values=[weekday_value, None],
    )

    return f

def or_filters(f: NotionFilter) -> NotionFilter:
    # TODO

    return f