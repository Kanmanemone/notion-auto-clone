import os

from custom_filter import pages_to_clone_filter, already_cloned_filter
from custom_patch import source_page_patch, target_page_patch
from custom_property import target_page_properties
from notion.api import NotionApi

notion_api = NotionApi(os.environ["NOTION_TOKEN"])
source_db_id = os.environ["SOURCE_DB_ID"]
target_db_id = os.environ["TARGET_DB_ID"]

# 사용자 정의 조건을 가져와 source DB에서 복제할 페이지를 조회
source_pages = notion_api.read(
    db_id=source_db_id,
    filter=pages_to_clone_filter()
)

for source_page in source_pages["results"]:
    # source DB에서 조회한 페이지를 target DB에 새 페이지로 생성
    already_cloned_page = notion_api.read(
        db_id=target_db_id,
        filter=already_cloned_filter(source_page=source_page),
        page_size=1,
    )
    if already_cloned_page["results"]:
        page = already_cloned_page["results"][0]
        title = page["properties"]["name"]["title"]
        date = page["properties"]["date"]["formula"]["date"]["start"]
        print(f"(이미 존재) {title[0]['plain_text'] if title else '(no title)'} | {date}")
        continue

    target_page = notion_api.create(
        db_id=target_db_id,
        properties=target_page_properties(source_page)
    )

    # 후처리 (post process)
    notion_api.update(page_id=source_page["id"], properties=source_page_patch(source_page, target_page))
    notion_api.update(page_id=target_page["id"], properties=target_page_patch(source_page, target_page))

    # 콘솔창 로그
    title = target_page["properties"]["name"]["title"]
    print(title[0]["plain_text"] if title else "(no title)")
