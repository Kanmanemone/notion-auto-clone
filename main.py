# 외부 라이브러리 없이 stdlib만으로 HTTP 요청 처리
import urllib.request as r, json, os

r.urlopen(r.Request(
    # Notion REST API: 페이지 생성 엔드포인트
    "https://api.notion.com/v1/pages",
    # 요청 바디: JSON 직렬화 후 bytes로 인코딩
    json.dumps({
        "parent": {"database_id": os.environ["TARGET_DB_ID"]},  # 생성될 위치 (데이터베이스)
        "properties": {"title": [{"text": {"content": "Hello Notion"}}]}  # 페이지 제목
    }).encode(),
    # 요청 헤더
    {
        "Authorization": "Bearer " + os.environ["NOTION_TOKEN"],  # Integration 토큰
        "Notion-Version": "2022-06-28",  # Notion API 버전 고정
        "Content-Type": "application/json"
    }
))
