import aiohttp
from itemProperties import ip
import dotenv
import os
import requests
import json


# Set Token
dotenv.load_dotenv()
token = str(os.getenv("NOTION_TOKEN"))
database_id = str(os.getenv("DATABASE_ID"))


# # Get Item List
# def get_item_list():
#     url = f'https://api.notion.com/v1/databases/{database_id}/query'
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "accept": "application/json",
#         "Notion-Version": "2022-06-28",
#         "content-type": "application/json"
#     }
#     payload = {
#         "page_size": 100,
#         "sorts": [
#             {
#                 "property": "Name",
#                 "direction": "ascending"
#             }
#         ]
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     objects = json.loads(response.text)['results']

#     items = []
#     for o in objects:
#         item = {
#             'id': o['properties']['ID']['number'],
#             'name': o['properties']['Name']['title'][0]['plain_text'],
#             'type': o['properties']['Type']['select']['name'].strip(),
#             'status': o['properties']['Status']['status']['name'],
#         }
#         items.append(item)

#     # 출력
#     # print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))

#     return items


async def get_item_list():
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
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            objects = (await response.json())['results']

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


# Request Item
def request_item():

    # Call Notion API
    url = 'https://api.notion.com/v1/pages'
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
        "properties": ip['Lecture']
    }

    response = requests.post(url, json=payload, headers=headers)
    # print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))


# request_item()
# get_item_list()
