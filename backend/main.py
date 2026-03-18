from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from database import engine, init_db, get_db, Meeting
from stt_service import stt_service
from agent_service import agent_service
from notion_service import notion_service
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Meeting Summary AI")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB is initialized
init_db()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TaskResponse(BaseModel):
    title: str
    content: str
    assignee: str
    deadline: str

class UploadResponse(BaseModel):
    meeting_id: int
    raw_text: str
    tasks: List[TaskResponse]

@app.post("/upload", response_model=UploadResponse)
async def upload_meeting(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save File Temporarily
    file_ext = file.filename.split(".")[-1]
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{file_ext}")
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    from datetime import datetime
    upload_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # 2. STT Transformation
        raw_text = await stt_service.transcribe(temp_path)
        
        # 3. Save Meeting to DB
        new_meeting = Meeting(title=file.filename, raw_text=raw_text)
        db.add(new_meeting)
        db.commit()
        db.refresh(new_meeting)
        
        # 4. Extract Tasks via LLM
        tasks = await agent_service.extract_tasks(raw_text, upload_date)
        
        # 5. Automatically create Notion cards
        for task in tasks:
            await notion_service.create_kanban_card(
                title=task['title'],
                content=task['content'],
                assignee=task['assignee'],
                deadline=task['deadline']
            )
            
        return {
            "meeting_id": new_meeting.id,
            "raw_text": raw_text,
            "tasks": tasks
        }
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/meetings")
async def list_meetings(db: Session = Depends(get_db)):
    return db.query(Meeting).order_by(Meeting.created_at.desc()).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
