from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class Parent:
    type: str
    page_id: str

@dataclass
class Number:
    format: str

@dataclass
class 수량:
    id: str
    name: str
    type: str
    number: Number

@dataclass
class Date:
    pass

@dataclass
class 날짜:
    id: str
    name: str
    type: str
    date: Date

@dataclass
class Select:
    options: list[OptionsItem]

@dataclass
class 상태:
    id: str
    name: str
    type: str
    select: Select

@dataclass
class OptionsItem:
    id: str
    name: str
    color: str

@dataclass
class MultiSelect:
    options: list[OptionsItem]

@dataclass
class CloneOnMonthdayAnd:
    id: str
    name: str
    type: str
    multi_select: MultiSelect

@dataclass
class Checkbox:
    pass

@dataclass
class AutoClone:
    id: str
    name: str
    type: str
    checkbox: Checkbox

@dataclass
class Title:
    pass

@dataclass
class 이름:
    id: str
    name: str
    type: str
    title: Title

@dataclass
class Properties:
    이름: 이름
    auto_clone: AutoClone
    clone_on_monthday_and: CloneOnMonthdayAnd
    상태: 상태
    날짜: 날짜
    수량: 수량

@dataclass
class Annotations:
    bold: bool
    italic: bool
    color: str

@dataclass
class Text:
    content: str
    link: Any

@dataclass
class TitleItem:
    type: str
    text: Text
    plain_text: str
    annotations: Annotations

@dataclass
class NotionDatabase:
    object: str
    id: str
    created_time: str
    last_edited_time: str
    title: list[TitleItem]
    properties: Properties
    parent: Parent
    url: str
    archived: bool
    is_inline: bool
