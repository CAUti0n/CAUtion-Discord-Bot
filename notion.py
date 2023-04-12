import dotenv
import os
import requests
import json

# Set Token
dotenv.load_dotenv()
token = str(os.getenv("NOTION_TOKEN"))
database_id = str(os.getenv("DATABASE_ID"))


# Get Items Info
def get_items_info():
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    payload = {
        "page_size": 100,
        "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    objects = json.loads(response.text)['results']

    items = []
    for o in objects:
        item = {
            'id': o['properties']['ID']['number'],
            'name': o['properties']['Name']['title'][0]['plain_text'],
            'type': o['properties']['Type']['select']['name'],
            'status': o['properties']['Status']['status']['name'],
        }
        items.append(item)

    return items

# 출력
# print(json.dumps(json.loads(response.text), indent=2, ensure_ascii=False))
