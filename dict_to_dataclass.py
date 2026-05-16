#!/usr/bin/env python3
"""Converts a nested Python dict into @dataclass definitions."""
from __future__ import annotations
import re
from collections import OrderedDict
from typing import Any

_registry: OrderedDict[str, dict[str, str]] = OrderedDict()
_anon_counter = 0


def _pascal(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name)
    return "".join(p.capitalize() if p.isascii() else p for p in parts if p)


def _safe_field(name: str) -> str:
    # 숫자로 시작하면 _ 접두사, 하이픐·공백만 제거
    s = re.sub(r"[\-\s]", "_", name)
    return ("_" + s) if s and s[0].isdigit() else (s or "_field")


def _infer(value: Any, hint: str) -> str:
    if value is None:
        return "Any"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        if not value:
            return "list[Any]"
        return f"list[{_infer(value[0], hint + 'Item')}]"
    if isinstance(value, dict):
        _analyze(hint, value)
        return hint
    return "Any"


def _analyze(class_name: str, d: dict) -> None:
    if class_name in _registry:
        return
    _registry[class_name] = {}  # 재귀 방지용 선점
    _registry[class_name] = {
        _safe_field(k): _infer(v, _pascal(k)) for k, v in d.items()
    }


def to_dataclasses(data: dict, root: str = "Root") -> str:
    _registry.clear()
    _analyze(root, data)
    lines = [
        "from __future__ import annotations",
        "from dataclasses import dataclass",
        "from typing import Any",
        "",
    ]
    # 자식 클래스가 먼저 오도록 역순 출력
    for cls, fields in reversed(list(_registry.items())):
        lines.append("@dataclass")
        lines.append(f"class {cls}:")
        if fields:
            for fname, ftype in fields.items():
                lines.append(f"    {fname}: {ftype}")
        else:
            lines.append("    pass")
        lines.append("")
    return "\n".join(lines)


# ── 예시: Notion DB 스키마 dict ──────────────────────────────────────────────
notion_db = {
    "object": "database",
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "created_time": "2024-01-01T00:00:00.000Z",
    "last_edited_time": "2024-05-01T12:00:00.000Z",
    "title": [
        {
            "type": "text",
            "text": {"content": "내 데이터베이스", "link": None},
            "plain_text": "내 데이터베이스",
            "annotations": {"bold": False, "italic": False, "color": "default"},
        }
    ],
    "properties": {
        "이름": {
            "id": "title",
            "name": "이름",
            "type": "title",
            "title": {},
        },
        "auto_clone": {
            "id": "abc1",
            "name": "auto_clone",
            "type": "checkbox",
            "checkbox": {},
        },
        "clone_on_monthday_and": {
            "id": "abc2",
            "name": "clone_on_monthday_and",
            "type": "multi_select",
            "multi_select": {
                "options": [
                    {"id": "opt1", "name": "1",  "color": "blue"},
                    {"id": "opt2", "name": "15", "color": "green"},
                    {"id": "opt3", "name": "31", "color": "red"},
                ]
            },
        },
        "상태": {
            "id": "abc3",
            "name": "상태",
            "type": "select",
            "select": {
                "options": [
                    {"id": "s1", "name": "진행중", "color": "yellow"},
                    {"id": "s2", "name": "완료",  "color": "green"},
                ]
            },
        },
        "날짜": {
            "id": "abc4",
            "name": "날짜",
            "type": "date",
            "date": {},
        },
        "수량": {
            "id": "abc5",
            "name": "수량",
            "type": "number",
            "number": {"format": "number"},
        },
    },
    "parent": {
        "type": "page_id",
        "page_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    },
    "url": "https://www.notion.so/a1b2c3d4e5f67890abcdef1234567890",
    "archived": False,
    "is_inline": False,
}

if __name__ == "__main__":
    print(to_dataclasses(notion_db, root="NotionDatabase"))
