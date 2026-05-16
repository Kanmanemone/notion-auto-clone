from typing import Literal


class NotionFilter:
    @staticmethod
    def multi_select(name: str, values: list[str], logical_operator: Literal["or", "and"] = "or") -> dict | None:
        if len(values) == 0:
            return None
        if len(values) == 1:
            return {"property": name, "multi_select": {"contains": values[0]}}
        return {
            logical_operator: [
                {"property": name, "multi_select": {"contains": v}}
                for v in values
            ]
        }

    @staticmethod
    def checkbox(name: str, value: bool = True) -> dict:
        return {"property": name, "checkbox": {"equals": value}}
