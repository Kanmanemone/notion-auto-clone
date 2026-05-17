import json
from typing import Any

from sympy import And, Or, Symbol
from sympy.logic.boolalg import BooleanFalse, BooleanTrue, to_dnf

from .filter_logic import and_, or_


# custom_filter.py에서는 사람이 읽기 쉬운 중첩 and/or 조건을 작성한다.
# Notion API는 compound filter 안에 다시 compound filter가 깊게 들어가면
# validation_error를 반환할 수 있으므로, API 요청 직전에 DNF 형태로 펼친다.
# 예를 들어, A AND (B OR C)를 Notion이 받기 쉬운 형태인
# (A AND B) OR (A AND C)로 변환한다.


def to_notion_filter(filter_body: dict[str, Any] | None) -> dict[str, Any] | None:
    if not filter_body:
        return None

    symbol_to_filter: dict[Symbol, dict[str, Any]] = {}
    filter_to_symbol: dict[str, Symbol] = {}

    def to_expr(item: dict[str, Any]):
        if "and" in item:
            return And(*(to_expr(child) for child in item["and"]))
        if "or" in item:
            return Or(*(to_expr(child) for child in item["or"]))

        key = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if key not in filter_to_symbol:
            symbol = Symbol(f"f{len(filter_to_symbol)}")
            filter_to_symbol[key] = symbol
            symbol_to_filter[symbol] = item
        return filter_to_symbol[key]

    def from_expr(expr):
        if isinstance(expr, BooleanTrue):
            return None
        if isinstance(expr, BooleanFalse):
            return None
        if isinstance(expr, Symbol):
            return symbol_to_filter[expr]
        if isinstance(expr, Or):
            return or_(*(from_expr(arg) for arg in expr.args))
        if isinstance(expr, And):
            return and_(*(from_expr(arg) for arg in expr.args))
        raise TypeError(f"Unsupported filter expression: {expr!r}")

    return from_expr(to_dnf(to_expr(filter_body), simplify=False))
