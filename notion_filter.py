from typing import Literal


class NotionFilter:
    def __init__(self):
        self.filters = []

    def multi_select(self, name: str, values: list[str], logical_operator: Literal["or", "and"] = "or"):
        match len(values):
            case 0:
                return
            case 1:
                # 단일 값일 때는 "or"나 "and"래핑 없이
                self.filters.append(
                    {
                        "property": name,
                        "multi_select": {"contains": values[0]}
                    }
                )
            case _:
                # 여러 값일 때는, "or"나 "and"로 래핑해서
                self.filters.append(
                    {
                        logical_operator: [
                            {
                                "property": name,
                                "multi_select": {"contains": v}
                            }
                            for v in values
                        ]
                    }
                )

    def checkbox(self, name: str, value: bool = True):
        self.filters.append(
            {
                "property": name,
                "checkbox": {"equals": value}
            }
        )
