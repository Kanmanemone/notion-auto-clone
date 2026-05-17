from calendar import monthrange
from datetime import date

from notion_filter import NotionFilter

def and_filters(f: NotionFilter) -> NotionFilter:
    f.checkbox(
        name="auto_clone",
        value=True,
    )

    today = date.today()
    month = today.month  # 1 ~ 12 반환
    monthday = today.day  # 1 ~ 31 반환
    last_monthday = monthrange(today.year, month)[1]  # 오늘이 속한 달의 마지막 날
    week_of_month = (monthday - 1) // 7 + 1  # "1" ~ "5" 반환
    last_week_of_month = (last_monthday - 1) // 7 + 1  # 오늘이 속한 달의 마지막 주

    # 달 (1 ~ 12)
    f.multi_select(
        name="clone_on_month_and",
        values=[str(month), None]  # "clone_on_monthday_and" 속성이 비어 있는 페이지도 가져오도록 함
    )

    # 일 (1 ~ 31)
    monthday_values: list[str | None] = [str(monthday)]
    if monthday == last_monthday:
        monthday_values.append("last_date")
    monthday_values.append(None)
    f.multi_select(
        name="clone_on_monthday_and",
        values=monthday_values,
    )

    # 주차 (1 ~ 5)
    week_of_month_values: list[str | None] = [str(week_of_month)]
    if week_of_month == last_week_of_month:
        week_of_month_values.append("last_week")
    week_of_month_values.append(None)
    f.multi_select(
        name="clone_on_week_of_month_and",
        values=week_of_month_values,
    )

    # 요일 (월 ~ 일)
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