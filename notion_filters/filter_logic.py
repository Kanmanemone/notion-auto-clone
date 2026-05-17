from typing import Any

def and_(*items: dict[str, Any] | None) -> dict[str, Any] | None:
    items = [x for x in items if x]

    if len(items) == 0:
        return None

    if len(items) == 1:
        return items[0]

    return {"and": items}


def or_(*items: dict[str, Any] | None) -> dict[str, Any] | None:
    items = [x for x in items if x]

    if len(items) == 0:
        return None

    if len(items) == 1:
        return items[0]

    return {"or": items}
