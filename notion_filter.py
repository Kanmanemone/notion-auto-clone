from typing import Literal


class NotionFilter:
    def __init__(self):
        self.filters = []

    def multi_select(
            self,
            name: str,
            values: list[str | None] | None,
            logical_operator: Literal["or", "and"] = "or"
    ):
        if values is None:
            self.filters.append(
                {
                    "property": name,
                    "multi_select": {"is_empty": True}
                }
            )
        else:
            match len(values):
                case 0:
                    self.filters.append(
                        {
                            "property": name,
                            "multi_select": {"is_empty": True}
                        }
                    )
                case 1:
                    self.filters.append(
                        {
                            "property": name,
                            "multi_select": {"contains": values[0]} if values[0] is not None else {"is_empty": True}
                        }
                    )
                case _:
                    self.filters.append(
                        {
                            logical_operator: [
                                {
                                    "property": name,
                                    "multi_select": {"contains": v} if v is not None else {"is_empty": True}
                                }
                                for v in values
                            ]
                        }
                    )

    # 노션의 체크박스는 반드시 True 또는 False로, 이른바 '빈 값'이 존재할 수 없다
    def checkbox(self, name: str, value: bool = True):
        self.filters.append(
            {
                "property": name,
                "checkbox": {"equals": value}
            }
        )
