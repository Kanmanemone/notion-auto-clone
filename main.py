import json
import os
import urllib.request as r

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

for page in source_pages["results"]:
    # 페이지 속성 중 title 타입인 것을 추출
    title = next(v for v in page["properties"].values() if v["type"] == "title")
    # target DB에 Notion 기본 제목 속성(title)만 복사해서 새 페이지 생성
    api("POST", "/pages", {
        "parent": {"database_id": os.environ["TARGET_DB_ID"]},
        "properties": {"name": title},
    })
    print(title["title"][0]["plain_text"] if title["title"] else "(no title)")
