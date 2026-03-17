from notion_client import AsyncClient
import os
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

class NotionService:
    def __init__(self):
        self.notion = AsyncClient(auth=os.getenv("NOTION_API_KEY"))
        self.database_id = os.getenv("NOTION_DB_ID")
        self.logger = logging.getLogger("notion_service")

    async def create_kanban_card(self, title: str, content: str, assignee: str, deadline: str):
        try:
            properties = {
                "이름": {"title": [{"text": {"content": title}}]},
                "상태": {"status": {"name": "시작 전"}},
            }
            
            if assignee and assignee != "None":
                properties["담당자"] = {"rich_text": [{"text": {"content": assignee}}]}
            
            if deadline and deadline != "None":
                # Basic YYYY-MM-DD validation/fallback could be added here
                properties["마감일"] = {"date": {"start": deadline}}

            children = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📝 상세 업무 내용"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}
                }
            ]

            response = await self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )
            return response
        except Exception as e:
            self.logger.error(f"Failed to create Notion card: {str(e)}")
            raise e

# Singleton instance
notion_service = NotionService()
