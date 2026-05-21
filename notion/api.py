import json
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
        with r.urlopen(req) as res:
            return json.loads(res.read())

    # noinspection PyShadowingBuiltins
    def read(self, db_id: str, filter: dict[str, Any] | None = None, page_size: int | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {}
        compiled = to_notion_filter(filter)
        if compiled:
            body["filter"] = compiled
        if page_size is not None:
            body["page_size"] = page_size
        return self._api("POST", f"/databases/{db_id}/query", body or None)

    def create(self, db_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        return self._api("POST", "/pages", {"parent": {"database_id": db_id}, "properties": properties})

    def update(self, page_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        return self._api("PATCH", f"/pages/{page_id}", {"properties": properties})
