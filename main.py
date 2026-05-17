import urllib.request as r, json, os
import custom_filter
from notion_filter import NotionFilter

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

# 특정 페이지를 복제할지 말지를 정하는, 사용자 정의 조건 가져오기
and_filters = custom_filter.and_filters(NotionFilter()).filters
or_filters = custom_filter.or_filters(NotionFilter()).filters

# 아래와 같은 형태로 and 조건과 or 조건을 조합하여, query_body 만들기 → source DB에서 복제할 페이지 가져오기
# {
#     "filter": {
#         "or": [
#             {
#                 "and": [
#                     aaa,
#                     bbb,
#                     ccc
#                 ]
#             },
#             ddd,
#             eee
#         ]
#     }
# }
if and_filters and or_filters:
    query_body = {"filter": {"or": [{"and": and_filters}, *or_filters]}}
elif and_filters:
    query_body = {"filter": {"and": and_filters}}
elif or_filters:
    query_body = {"filter": {"or": or_filters}}
else:
    query_body = {}
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