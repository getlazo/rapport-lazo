# ✅ notion_utils.py — clean version
import os
from notion_client import Client
from datetime import datetime

notion = Client(auth=os.getenv("NOTION_TOKEN"))

def send_to_notion(database_id: str, title: str, children: list):
    """
    Crée une nouvelle page dans une base de données Notion, avec contenu structuré.
    """
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {
                "title": [
                    {"text": {"content": title}}
                ]
            },
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            }
        },
        children=children
    )