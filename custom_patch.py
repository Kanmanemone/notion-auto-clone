from typing import Any


def build_source_patch(source_page: dict[str, Any], target_page: dict[str, Any]) -> dict[str, Any]:
    # TODO 테스트 코드
    title = next(v for v in source_page["properties"].values() if v["type"] == "title")
    title_text = title["title"][0]["plain_text"] if title["title"] else ""
    if title_text == "test":
        return {"memo": {"rich_text": [{"text": {"content": "a"}}]}}

    return {}


def build_target_patch(source_page: dict[str, Any], target_page: dict[str, Any]) -> dict[str, Any]:
    #TODO

    return {}
