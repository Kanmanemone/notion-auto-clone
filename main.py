import urllib.request as r, json, os, glob

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

# source_clone_rules 디렉토리의 필터 파일을 읽어 source DB 페이지 조회
filters = [json.load(open(f)) for f in glob.glob("source_clone_rules/*.json")]
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
    # [콘솔 출력] api로 복제 의뢰(요청)한 페이지의 제목
    print(title["title"][0]["plain_text"] if title["title"] else "(no title)")
