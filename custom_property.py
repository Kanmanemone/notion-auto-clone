from datetime import datetime, timedelta, timezone
from typing import Any

from notion.property import NotionProperties

_now = datetime.now(
    timezone(timedelta(hours=9)))  # astimezone() 대신 KST 명시: GitHub Actions는 UTC 환경이라 OS 타임존에 의존하면 날짜가 달라짐
_iso = _now.isocalendar()
_weekday_str = ["월 (mon)", "화 (tue)", "수 (wed)", "목 (thu)", "금 (fri)", "토 (sat)", "일 (sun)"][_now.weekday()]


def target_page_properties(source_page: dict[str, Any]) -> NotionProperties:
    props = (
        NotionProperties()
        .relation("schedule", source_page["id"])
        .title_mention("name", source_page["id"])
        .rich_text("memo", source_page["properties"]["memo"]["rich_text"])
        .relation("people", *[p["id"] for p in source_page["properties"]["people"]["relation"]])
        .select("type", (source_page["properties"]["type"]["select"] or {}).get("name"))
        .select("area", (source_page["properties"]["area"]["select"] or {}).get("name"))
        .multi_select("tags", source_page["properties"]["tags"]["multi_select"])
        .number("duration_hour", 0)
        .number("_source_year", _iso.year)
        .number("_source_week_of_year", _iso.week)
        .select("_source_day_of_week", _weekday_str)
    )
    return props
