import os
from datetime import datetime, timedelta, timezone

import custom_filter
import custom_patch
import custom_property
from notion.api import NotionApi
from notion.filter_logic import and_
from notion.filter import NotionFilter as f

notion_api = NotionApi(os.environ["NOTION_TOKEN"])
source_db_id = os.environ["SOURCE_DB_ID"]
target_db_id = os.environ["TARGET_DB_ID"]

today = datetime.now(timezone(timedelta(hours=9)))
today_str = today.date().isoformat()

# 사용자 정의 조건을 가져와 source DB에서 복제할 페이지를 조회
source_pages = notion_api.read(db_id=source_db_id, filter=custom_filter.build_filter())

for source_page in source_pages["results"]:
    # source DB에서 조회한 페이지를 target DB에 새 페이지로 생성
    minimum_interval_days = source_page["properties"]["minimum_interval_days"]["number"]

    if minimum_interval_days not in (None, 0):
        source_title = source_page["properties"]["name"]["title"]
        source_title = source_title[0]["plain_text"] if source_title else ""
        # minimum_interval_days=7이면 14일에 clone 후 21일, 28일에 재복제 (예: 14 -> 21 -> 28)
        # on_or_after(≥) 사용 시 경계일 당일 제외되므로 +1일 보정
        interval_start_str = (today.date() - timedelta(days=minimum_interval_days) + timedelta(days=1)).isoformat()

        query_page_2 = notion_api.read(
            db_id=target_db_id,
            filter=and_(
                f.title(name="name", value=source_title),
                f.status(name="progress", value="완료", operator="does_not_equal"),
                f.date(name="calculated_date", value=interval_start_str, date_operator="on_or_after"),
                f.date(name="calculated_date", value=today_str, date_operator="on_or_before"),
            ),
            page_size=1,
        )
        if query_page_2.get("results"):
            title = query_page_2["results"][0]["properties"]["name"]["title"]
            print("(존재 확인) " + title[0]["plain_text"] if title else "(no title)")
            print("(존재 확인) " + query_page_2["results"][0]["properties"]["calculated_date"]["formula"]["date"]["start"])
            continue

    notion_properties = custom_property.build_properties(source_page)
    target_page = notion_api.create(db_id=target_db_id, properties=notion_properties)

    # 후처리 (post process)
    notion_api.update(page_id=source_page["id"], properties=custom_patch.build_source_patch(source_page, target_page))
    notion_api.update(page_id=target_page["id"], properties=custom_patch.build_target_patch(source_page, target_page))

    # 콘솔창 로그
    title = target_page["properties"]["name"]["title"]
    print(title[0]["plain_text"] if title else "(no title)")
