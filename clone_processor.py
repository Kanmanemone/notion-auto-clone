import inspect, pkgutil, importlib, os
from notion_api import api

def _load_hooks():
    hooks = []
    for m in pkgutil.iter_modules(["post_clone_hooks"]):
        mod = importlib.import_module(f"post_clone_hooks.{m.name}")
        for _, f in inspect.getmembers(mod, inspect.isfunction):
            if f.__module__ == mod.__name__:
                hooks.append(f)
    return hooks

_hooks = _load_hooks()

def process(page):
    title = next(v for v in page["properties"].values() if v["type"] == "title")
    api("POST", "/pages", {
        "parent": {"database_id": os.environ["TARGET_DB_ID"]},
        "properties": {"name": title},
    })
    print(title["title"][0]["plain_text"] if title["title"] else "(no title)")
    for hook in _hooks:
        hook(page)
