import dotenv
import os
import requests
import json
from itemProperties import return_request_item_properties

# Set Token
dotenv.load_dotenv()
token = str(os.getenv("NOTION_TOKEN"))
database_id = str(os.getenv("DATABASE_ID"))


# Get Item List
def get_item_list():
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }
    payload = {
        "page_size": 100,
        "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    objects = json.loads(response.text)['results']

    items = []
    for o in objects:
        item = {
            'id': o['properties']['ID']['number'],
            'name': o['properties']['Name']['title'][0]['plain_text'],
            'type': o['properties']['Type']['select']['name'].strip(),
            'status': o['properties']['Status']['status']['name'],
        }
        items.append(item)

    return items


# Get Item info by ID
def get_item_info_by_id(item_id):
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }
    payload = {
        "filter": {
            "and": [
                {
                    "property": "ID",
                    "number": {
                        "equals": item_id
                    }
                },
                {
                    "property": "Status",
                    "status": {
                        "equals": "이용 가능"
                    }
                }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    item = json.loads(response.text)

    if len(item['results']) > 1:
        return 'Error'

    item_info = []
    item_info.append(item['results'][0]['id'])  # Page id
    item_info.append(item['results'][0]['properties']['Type']['select']['name'].strip())    # Item Type
    item_info.append(item['results'][0]['properties']['Name']['title'][0]['plain_text'].strip())    # Item Name

    return item_info


# Item 이용 신청
def request_item(item_id, user):

    # Get Item info
    item = get_item_info_by_id(item_id)

    # Call Notion API
    url = f'https://api.notion.com/v1/pages/{item[0]}'
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": database_id
        },
        "properties": return_request_item_properties(item_id, item[1], item[2], user)
    }

    response = requests.patch(url, json=payload, headers=headers)



# 사용자가 이용 중인 item 목록 반환
def get_user_item_list(user):

    # Item 반납
    # 사용자가 이용 중인 item 목록 반환
    get_user_item_list(user)


# get_item_list()
# request_item(1, '이승현')

