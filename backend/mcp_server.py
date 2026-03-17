from mcp.server.fastmcp import FastMCP
from sqlalchemy.orm import Session
from database import SessionLocal, Meeting
import os

# Initialize FastMCP
mcp = FastMCP("MeetingSummaryManager")

@mcp.tool()
def get_meeting_summary():
    """
    SQLite DB에서 가장 최근에 저장된 회의록 원문과 제목을 불러옵니다.
    """
    db = SessionLocal()
    try:
        latest_meeting = db.query(Meeting).order_by(Meeting.created_at.desc()).first()
        if not latest_meeting:
            return "저장된 회의록이 없습니다."
        
        return {
            "title": latest_meeting.title,
            "raw_text": latest_meeting.raw_text,
            "created_at": latest_meeting.created_at.isoformat()
        }
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
