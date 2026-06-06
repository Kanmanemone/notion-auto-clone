import json
import time
import urllib.error
import urllib.request as r
from typing import Any

from notion.filter_compiler import to_notion_filter


class NotionApi:
    _BASE_URL = "https://api.notion.com/v1"

    def __init__(self, token: str):
        # 모든 요청에 공통으로 사용할 헤더
        self._headers = {
            "Authorization": "Bearer " + token,
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    # Notion REST API에 HTTP 요청을 보내고 응답으로 JSON을 받는 범용 함수
    def _api(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        req = r.Request(
            self._BASE_URL + path,
            json.dumps(body).encode() if body else None,
            self._headers,
            method=method,
        )

        time.sleep(0.4)  # Notion API 초당 3건 제한 → 0.4초 간격 유지

        wait = 1
        for attempt in range(1, 6):  # 최대 5회 시도
            try:
                with r.urlopen(req) as res:
                    return json.loads(res.read())

            except urllib.error.HTTPError as e:
                is_rate_limit = (e.code == 429)
                is_last_attempt = (attempt == 5)

                if not is_rate_limit or is_last_attempt:
                    raise  # 429 외 에러거나 5회 모두 실패 시 그냥 던짐

                # Retry-After 헤더가 있으면 그 값, 없으면 지수 백오프(1→2→4...최대 60초)
                wait = int(e.headers.get("Retry-After", wait))
                print(f"Rate limited. {attempt}회 시도 실패, {wait}초 후 재시도...")
                time.sleep(wait)
                wait = min(wait * 2, 60)

    # noinspection PyShadowingBuiltins
    def read(
        self,
        db_id: str,
        filter: dict[str, Any] | None = None,
        page_size: int | None = None,
        sorts: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        compiled = to_notion_filter(filter)
        if compiled:
            body["filter"] = compiled
        if page_size is not None:
            body["page_size"] = page_size
        if sorts:
            body["sorts"] = sorts
        return self._api("POST", f"/databases/{db_id}/query", body or None)

    def create(self, db_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        return self._api("POST", "/pages", {"parent": {"database_id": db_id}, "properties": properties})

    def update(self, page_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        return self._api("PATCH", f"/pages/{page_id}", {"properties": properties})
