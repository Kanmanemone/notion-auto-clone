import json
import os
import urllib.request as r
from datetime import datetime, timedelta, timezone

import custom_filter
from notion_filters.filter_compiler import to_notion_filter

# 모든 요청에 공통으로 사용할 헤더
HEADERS = {
    "Authorization": "Bearer " + os.environ["NOTION_TOKEN"],
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


# Notion REST API에 HTTP 요청을 보내고 응답으로 JSON을 받는 범용 함수
def api(method, path, body=None):
    req = r.Request("https://api.notion.com/v1" + path,
                    json.dumps(body).encode() if body else None,
                    HEADERS, method=method)
    with r.urlopen(req) as res:
        return json.loads(res.read())


# 사용자 정의 조건을 가져와 source DB에서 복제할 페이지를 조회
filter_body = custom_filter.build_filter()
notion_filter = to_notion_filter(filter_body)
query_body = {"filter": notion_filter} if notion_filter else {}
source_pages = api("POST", f"/databases/{os.environ['SOURCE_DB_ID']}/query", query_body)

# source DB에서 조회한 페이지들을 target DB에 새 페이지로 생성
now = datetime.now(timezone(timedelta(hours=9)))  # astimezone() 대신 KST 명시: GitHub Actions는 UTC 환경이라 OS 타임존에 의존하면 날짜가 달라짐
iso = now.isocalendar()
weekday_str = ["월 (mon)", "화 (tue)", "수 (wed)", "목 (thu)", "금 (fri)", "토 (sat)", "일 (sun)"][now.weekday()]
for page in source_pages["results"]:
    # 페이지 속성 중 title 타입인 것을 추출
    title = next(v for v in page["properties"].values() if v["type"] == "title")
    # target DB에 제목과 실행일을 복사해서 새 페이지 생성
    api("POST", "/pages", {
        "parent": {"database_id": os.environ["TARGET_DB_ID"]},
        "properties": {
            "name": title,
            "extracted_year": {"number": iso.year},
            "extracted_week_of_year": {"number": iso.week},
            "extracted_day_of_week": {"select": {"name": weekday_str}},
        },
    })
    print(title["title"][0]["plain_text"] if title["title"] else "(no title)")
