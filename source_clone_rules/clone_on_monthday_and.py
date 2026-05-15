from datetime import date

def clone_on_monthday_and():
    return {
        "property": "clone_on_monthday_and",
        "multi_select": {"contains": str(date.today().day)},
    }
