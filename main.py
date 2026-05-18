import inspect, pkgutil, importlib, os
from notion_api import api
from clone_processor import process

filters = []
for m in pkgutil.iter_modules(["source_clone_rules"]):
    mod = importlib.import_module(f"source_clone_rules.{m.name}")
    for _, f in inspect.getmembers(mod, inspect.isfunction):
        if f.__module__ == mod.__name__:
            filters.append(f())

if len(filters) == 0:
    query_body = {}
elif len(filters) == 1:
    query_body = {"filter": filters[0]}
else:
    query_body = {"filter": {"and": filters}}

source_pages = api("POST", f"/databases/{os.environ['SOURCE_DB_ID']}/query", query_body)

for page in source_pages["results"]:
    process(page)
