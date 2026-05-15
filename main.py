import urllib.request as r, json, os, inspect, pkgutil, importlib

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

# source_clone_rules 순회해서 복제할지 말지의 조건(filter) 모으기
filters = []
for m in pkgutil.iter_modules(["source_clone_rules"]):
    mod = importlib.import_module(f"source_clone_rules.{m.name}")
    for _, f in inspect.getmembers(mod, inspect.isfunction):
        if f.__module__ == mod.__name__:  # import한 함수는 제외
            filters.append(f())

# 조건 개수에 따라 query body의 모양 잡고, source DB 조회
if len(filters) == 0:
    query_body = {}
elif len(filters) == 1:
    query_body = {"filter": filters[0]}
else:
    query_body = {"filter": {"and": filters}}
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