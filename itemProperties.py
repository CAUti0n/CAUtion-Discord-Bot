from datetime import datetime, timedelta, timezone

# Period of item use
periodOfUse = {
    "Book": ["1 week", 7],
    "Lecture": ["1 day", 1],
    "Account": ["1 day", 1],
}


# For request item
def return_request_item_properties(id, item_type, item_name, user):
    start_date = datetime.now(timezone(timedelta(hours=9)))
    end_date = start_date + timedelta(days=periodOfUse[item_type][1])

    print(id, item_type, item_name, user)

    request_item = {
        "Book": {
            "Type": {
                "type": "select",
                "select": {"name": " Book"}
            },
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": item_name}}]
            },
            "Status": {
                "type": "status",
                "status": {"name": "이용 중"}
            },
            "Period": {
                "type": "multi_select",
                "multi_select": [{"name": periodOfUse["Book"][0]}]
            },
            "ID": {
                "type": "number",
                "number": id
            },
            "User": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": user
                        }
                    }
                ]
            },
            "Date of Use": {
                "type": "date",
                "date": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                }
            }
        },
        "Lecture": {
            "Type": {
                "type": "select",
                "select": {"name": " Lecture"}
            },
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": item_name}}]
            },
            "Status": {
                "type": "status",
                "status": {"name": "이용 중"}
            },
            "Period": {
                "type": "multi_select",
                "multi_select": [{"name": periodOfUse["Lecture"][0]}]
            },
            "ID": {
                "type": "number",
                "number": id
            }
        },
        "Account": {
            "Type": {
                "type": "select",
                "select": {"name": " Account"}
            },
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": item_name}}]
            },
            "Status": {
                "type": "status",
                "status": {"name": "이용 중"}
            },
            "Period": {
                "type": "multi_select",
                "multi_select": [{"name": periodOfUse["Account"][0]}]
            },
            "ID": {
                "type": "number",
                "number": id
            }
        },
    }

    return request_item[item_type]


# For add available item
def return_available_item_properties(id, type, item_name):
    available_item = {
        "Book": {
            "Type": {
                "type": "select",
                "select": {"name": " Book"}
            },
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": item_name}}]
            },
            "Status": {
                "type": "status",
                "status": {"name": "이용 가능"}
            },
            "Period": {
                "type": "multi_select",
                "multi_select": [{"name": periodOfUse["Book"][0]}]
            },
            "ID": {
                "type": "number",
                "number": 0
            }
        },
        "Lecture": {
            "Type": {
                "type": "select",
                "select": {"name": " Lecture"}
            },
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": item_name}}]
            },
            "Status": {
                "type": "status",
                "status": {"name": "이용 가능"}
            },
            "Period": {
                "type": "multi_select",
                "multi_select": [{"name": periodOfUse["Lecture"][0]}]
            },
            "ID": {
                "type": "number",
                "number": 0
            }
        },
        "Account": {
            "Type": {
                "type": "select",
                "select": {"name": " Account"}
            },
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": item_name}}]
            },
            "Status": {
                "type": "status",
                "status": {"name": "이용 가능"}
            },
            "Period": {
                "type": "multi_select",
                "multi_select": [{"name": periodOfUse["Account"][0]}]
            },
            "ID": {
                "type": "number",
                "number": 0
            }
        },
    }

    return available_item[type]
