import json
import os
import urllib.request as r

import custom_filter
import custom_patch
import custom_property
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
notion_filter = to_notion_filter(custom_filter.build_filter())
query_body = {"filter": notion_filter} if notion_filter else {}
source_pages = api("POST", f"/databases/{os.environ['SOURCE_DB_ID']}/query", query_body)

for source_page in source_pages["results"]:
    # source DB에서 조회한 페이지를 target DB에 새 페이지로 생성
    notion_properties = custom_property.build_properties(source_page)
    target_page_body = {"parent": {"database_id": os.environ["TARGET_DB_ID"]}, "properties": notion_properties}
    target_page = api("POST", "/pages", target_page_body)

    # 후처리 (post process)
    source_patch_body = {"properties": custom_patch.build_source_patch(source_page, target_page)}
    target_patch_body = {"properties": custom_patch.build_target_patch(source_page, target_page)}
    api("PATCH", f"/pages/{source_page['id']}", source_patch_body)
    api("PATCH", f"/pages/{target_page['id']}", target_patch_body)

    # 콘솔창 로그
    title = target_page["properties"]["name"]["title"]
    print(title[0]["plain_text"] if title else "(no title)")
