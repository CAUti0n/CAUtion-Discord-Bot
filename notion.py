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

    # 출력
    print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))

    return items


# Get Page ID by ID
def get_page_id_by_id(item_id):
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
    objects = json.loads(response.text)['results']
    page_id = objects[0]['id']

    return page_id

    # print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))


# Item 이용 신청
def request_item(item_id, item_type, user, item_name):

    # Call Notion API
    url = f'https://api.notion.com/v1/pages/{get_page_id_by_id(item_id)}'
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
        "properties": return_request_item_properties(item_id, item_type, user, item_name)
    }

    response = requests.patch(url, json=payload, headers=headers)
    print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))


# Item 반납
# def return_item(item_id, item_type, user, item_name):

    # get_item_list()
request_item(1, 'Book', '이승현', 'C로 배우는 암호학 프로그래밍')
# get_page_id_by_id(4)
