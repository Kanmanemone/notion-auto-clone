from datetime import datetime, timedelta, timezone
from typing import Any

from notion.property import NotionProperties

_now = datetime.now(
    timezone(timedelta(hours=9)))  # astimezone() 대신 KST 명시: GitHub Actions는 UTC 환경이라 OS 타임존에 의존하면 날짜가 달라짐
_iso = _now.isocalendar()
_weekday_str = ["월 (mon)", "화 (tue)", "수 (wed)", "목 (thu)", "금 (fri)", "토 (sat)", "일 (sun)"][_now.weekday()]


def target_page_properties(source_page: dict[str, Any]) -> NotionProperties:
    title = next(v for v in source_page["properties"].values() if v["type"] == "title")  # title 속성명은 DB마다 달라서 이름 대신 타입으로 탐색
    props = (
        NotionProperties()
        .number("duration_hour", 0)
        .number("extracted_year", _iso.year)
        .number("extracted_week_of_year", _iso.week)
        .select("extracted_day_of_week", _weekday_str)
        .url("source", source_page["url"])
    )
    props["name"] = title
    props["memo"] = {"rich_text": source_page["properties"]["memo"]["rich_text"]}
    if source_page["properties"]["date"]["date"] is None:
        props.select("type", "무한 반복")
    return props
