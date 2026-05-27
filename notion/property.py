class NotionProperties(dict):
    """
    Notion property dict builder with method chaining.
    Subclasses dict so instances can be passed directly to NotionApi.create/update.

    Usage:
        props = (
            NotionProperties()
            .title("name", "홍길동")
            .checkbox("is_in_guild", True)
            .relation("config", config_page_id)
            .number("level", 260)
            .rich_text("ocid", ocid)
            .date("last_api_sync_date", "2025-01-01")
            .select("character_relation_type", "bossㆍdrop")
        )
        notion_api.update(page_id=..., properties=props)
    """

    def title(self, name: str, content: str) -> "NotionProperties":
        self[name] = {"title": [{"type": "text", "text": {"content": content}}]}
        return self

    def title_mention(self, name: str, page_id: str) -> "NotionProperties":
        self[name] = {"title": [{"type": "mention", "mention": {"type": "page", "page": {"id": page_id}}}]}
        return self

    def rich_text(self, name: str, content: str) -> "NotionProperties":
        self[name] = {"rich_text": [{"type": "text", "text": {"content": content}}]}
        return self

    def number(self, name: str, value: int | float | None) -> "NotionProperties":
        self[name] = {"number": value}
        return self

    def checkbox(self, name: str, value: bool) -> "NotionProperties":
        self[name] = {"checkbox": value}
        return self

    def select(self, name: str, value: str | None) -> "NotionProperties":
        self[name] = {"select": {"name": value} if value is not None else None}
        return self

    def relation(self, name: str, *ids: str) -> "NotionProperties":
        self[name] = {"relation": [{"id": id_} for id_ in ids]}
        return self

    def url(self, name: str, value: str | None) -> "NotionProperties":
        self[name] = {"url": value}
        return self

    def date(self, name: str, start: str | None, end: str | None = None) -> "NotionProperties":
        if start is not None:
            self[name] = {"date": {"start": start, "end": end}}
        return self
