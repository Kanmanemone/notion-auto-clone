from typing import Any, Literal

from .filter_logic import and_, or_


class NotionFilter:
    @staticmethod
    def multi_select(
            name: str,
            values: list[str | None] | None,
            logical_operator: Literal["or", "and"] = "or"
    ) -> dict[str, Any] | None:
        def one(value: str | None) -> dict[str, Any]:
            return {
                "property": name,
                "multi_select": {"contains": value} if value is not None else {"is_empty": True}
            }

        if values is None:
            return one(None)
        else:
            filters = [one(value) for value in values]

            if logical_operator == "and":
                return and_(*filters)
            else:
                return or_(*filters)

    @staticmethod
    def checkbox(name: str, value: bool = True) -> dict[str, Any]:
        return {
            "property": name,
            "checkbox": {"equals": value}
        }

    @staticmethod
    def date(
            name: str,
            value: str | None,
            date_operator: Literal[
                "equals", "before", "after", "on_or_before", "on_or_after",
                "past_week", "this_week", "next_week"
            ] = "equals"
    ) -> dict[str, Any]:
        return {
            "property": name,
            "date": {date_operator: value} if value is not None else {"is_empty": True}
        }

    @staticmethod
    def status(
            name: str,
            value: str | None,
            operator: Literal["equals", "does_not_equal", "is_empty", "is_not_empty"] = "equals"
    ) -> dict[str, Any]:
        return {
            "property": name,
            "status": {operator: value} if value is not None else {"is_empty": True},
        }

    @staticmethod
    def rich_text(
            name: str,
            value: str | None,
            operator: Literal["contains", "does_not_contain", "equals", "does_not_equal", "starts_with", "ends_with", "is_empty", "is_not_empty"] = "equals"
    ) -> dict[str, Any]:
        return {
            "property": name,
            "rich_text": {operator: value} if value is not None else {"is_empty": True},
        }

    @staticmethod
    def title(
            name: str,
            value: str | None,
            operator: Literal["contains", "does_not_contain", "equals", "does_not_equal", "starts_with", "ends_with", "is_empty", "is_not_empty"] = "equals"
    ) -> dict[str, Any]:
        return {
            "property": name,
            "title": {operator: value} if value is not None else {"is_empty": True},
        }

    @staticmethod
    def url(
            name: str,
            value: str | None,
            operator: Literal["contains", "does_not_contain", "equals", "does_not_equal", "starts_with", "ends_with", "is_empty", "is_not_empty"] = "equals"
    ) -> dict[str, Any]:
        return {
            "property": name,
            "url": {operator: value} if value is not None else {"is_empty": True},
        }

    # TODO
    @staticmethod
    def files() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def formula_date(
            # name: str,
            # value: str | None,
            # date_operator: Literal[
            #     "equals", "before", "after", "on_or_before", "on_or_after",
            #     "past_week", "this_week", "next_week"
            # ] = "equals"
    ) -> dict[str, Any]:
        return {
            # "property": name,
            # "formula": {
            #     "date": {date_operator: value} if value is not None else {"is_empty": True}
            # }
        }

    # TODO
    @staticmethod
    def formula() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def number() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def people() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def relation() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def select() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def timestamp() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def unique_id() -> dict[str, Any]:
        return {}

    # TODO
    @staticmethod
    def rollup() -> dict[str, Any] | None:
        return {}
