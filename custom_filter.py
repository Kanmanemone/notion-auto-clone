from calendar import monthrange
from datetime import datetime, timedelta, timezone
from typing import Any

from notion.filter import NotionFilter as f
from notion.filter_logic import and_, or_


def already_cloned_filter(source_page: dict[str, Any]) -> dict[str, Any] | None:
    minimum_interval_days = source_page["properties"]["minimum_interval_days"]["number"]
    if minimum_interval_days is None:
        minimum_interval_days = 0

    today = datetime.now(timezone(timedelta(hours=9)))
    search_range_end_str = today.date().isoformat()

    # minimum_interval_days=7이면 14일에 clone 후 21일, 28일에 재복제 (예: 14 -> 21 -> 28)
    # on_or_after(≥) 사용 시 경계일 당일 제외되므로 +1일 보정
    search_range_start_str = (today.date() - timedelta(days=minimum_interval_days) + timedelta(days=1)).isoformat()

    return and_(
        f.relation(name="schedule", page_id=source_page["id"]),
        f.formula_date(name="date", value=search_range_start_str, date_operator="on_or_after"),
        f.formula_date(name="date", value=search_range_end_str, date_operator="on_or_before"),
    )


def pages_to_clone_filter() -> dict[str, Any] | None:
    today = datetime.now(
        timezone(timedelta(hours=9)))  # astimezone() 대신 KST 명시: GitHub Actions는 UTC 환경이라 OS 타임존에 의존하면 날짜가 달라짐
    today_str = today.date().isoformat()  # "2026-05-17" 형태. 시간 무시하고 날짜로만 비교
    # today_str = today.isoformat(timespec="seconds")  # "2026-05-17T21:25:25+09:00" 형태. 시각까지 비교

    month = today.month
    monthday = today.day
    last_monthday = monthrange(today.year, month)[1]
    week_of_month = (monthday - 1) // 7 + 1
    last_week_of_month = (last_monthday - 1) // 7 + 1
    weekday_value = ["월 (mon)", "화 (tue)", "수 (wed)", "목 (thu)", "금 (fri)", "토 (sat)", "일 (sun)"][today.weekday()]

    return and_(
        f.checkbox(
            name="auto_clone",
            value=True,
        ),
        or_(
            and_(
                # 날짜 범위: 시작일은 오늘 이전/당일이고, 종료일은 오늘 이후/당일인 항목
                f.date(name="date", value=today_str, date_operator="on_or_before"),
                f.date(name="_end_date", value=today_str, date_operator="on_or_after"),
            ),
            f.date(name="date", value=None),
        ),
        or_(
            # or로 적용되는 특수 조건
            # TODO f.multi_select(name="clone_on_before_or", values=None),
            and_(
                # and로 적용되는 특수 조건
                # TODO f.multi_select(name="clone_on_before_and", values=None),

                # 달 (1 ~ 12), 비어 있으면 매월 반복
                or_(
                    f.multi_select(name="clone_on_month_and", values=[str(month)]),
                    f.multi_select(name="clone_on_month_and", values=None),
                ),

                # 일 (1 ~ 31), 비어 있으면 매일 반복
                or_(
                    f.multi_select(name="clone_on_monthday_and", values=[str(monthday)]),
                    f.multi_select(
                        name="clone_on_monthday_and",
                        values=["last_date"],
                    ) if monthday == last_monthday else None,
                    f.multi_select(name="clone_on_monthday_and", values=None),
                ),

                # 주차 (1 ~ 5), 비어 있으면 매주 반복
                or_(
                    f.multi_select(name="clone_on_week_of_month_and", values=[str(week_of_month)]),
                    f.multi_select(
                        name="clone_on_week_of_month_and",
                        values=["last_week"],
                    ) if week_of_month == last_week_of_month else None,
                    f.multi_select(name="clone_on_week_of_month_and", values=None),
                ),

                # 요일 (월 ~ 일), 비어 있으면 매일 반복
                or_(
                    f.multi_select(name="clone_on_weekday_and", values=[weekday_value]),
                    f.multi_select(name="clone_on_weekday_and", values=None),
                ),
            ),
        ),
    )
