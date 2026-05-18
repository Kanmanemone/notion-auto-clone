from datetime import datetime, timedelta, timezone
from typing import Any

_now = datetime.now(
    timezone(timedelta(hours=9)))  # astimezone() 대신 KST 명시: GitHub Actions는 UTC 환경이라 OS 타임존에 의존하면 날짜가 달라짐
_iso = _now.isocalendar()
_weekday_str = ["월 (mon)", "화 (tue)", "수 (wed)", "목 (thu)", "금 (fri)", "토 (sat)", "일 (sun)"][_now.weekday()]


def build_properties(page: dict[str, Any]) -> dict[str, Any]:
    title = next(v for v in page["properties"].values() if v["type"] == "title")
    return {
        "name": title,
        "extracted_year": {"number": _iso.year},
        "extracted_week_of_year": {"number": _iso.week},
        "extracted_day_of_week": {"select": {"name": _weekday_str}},
    }