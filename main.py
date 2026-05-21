import json
import os
import urllib.request as r
from datetime import datetime, timedelta, timezone

import custom_filter
import custom_patch
import custom_property
from notion_filters.filter_compiler import to_notion_filter
from notion_filters.filter_logic import and_
from notion_filters.notion_filter import NotionFilter as f

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


today = datetime.now(timezone(timedelta(hours=9)))
today_str = today.date().isoformat()

# 사용자 정의 조건을 가져와 source DB에서 복제할 페이지를 조회
notion_filter = to_notion_filter(custom_filter.build_filter())
query_body = {"filter": notion_filter} if notion_filter else {}
source_pages = api("POST", f"/databases/{os.environ['SOURCE_DB_ID']}/query", query_body)

for source_page in source_pages["results"]:
    # source DB에서 조회한 페이지를 target DB에 새 페이지로 생성
    minimum_interval_days = source_page["properties"]["minimum_interval_days"]["number"]

    if minimum_interval_days not in (None, 0):
        source_title = source_page["properties"]["name"]["title"]
        source_title = source_title[0]["plain_text"] if source_title else ""
        # minimum_interval_days=7이면 14일에 clone 후 21일, 28일에 재복제 (예: 14 -> 21 -> 28)
        # on_or_after(≥) 사용 시 경계일 당일 제외되므로 +1일 보정
        interval_start_str = (today.date() - timedelta(days=minimum_interval_days) + timedelta(days=1)).isoformat()

        notion_filter_2 = to_notion_filter(
            and_(
                f.title(
                    name="name",
                    value=source_title
                ),
                f.status(
                    name="progress",
                    value="완료",
                    operator="does_not_equal"
                ),
                f.date(
                    name="calculated_date",
                    value=interval_start_str,
                    date_operator="on_or_after"
                ),
                f.date(
                    name="calculated_date",
                    value=today_str,
                    date_operator="on_or_before"
                ),
            )
        )
        query_body_2 = {"filter": notion_filter_2} if notion_filter_2 else {}
        query_page_2 = api("POST", f"/databases/{os.environ['TARGET_DB_ID']}/query", {**query_body_2, "page_size": 1})
        query_page_2_exists = len(query_page_2.get("results", [])) > 0
        if query_page_2_exists:
            title = query_page_2["results"][0]["properties"]["name"]["title"]
            print("(존재 확인) " + title[0]["plain_text"] if title else "(no title)")
            print("(존재 확인) " + query_page_2["results"][0]["properties"]["calculated_date"]["formula"]["date"]["start"])
            continue

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

