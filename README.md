# Meeting Summary & Notion Assignment Agent 🎙️📝

음성 회의록을 분석하여 자동으로 Notion 칸반 보드에 업무를 생성하고, Claude Desktop(MCP)을 통해 사후 관리를 지원하는 AI 에이전트 시스템입니다.

## 🌟 주요 기능

- **STT (Speech-to-Text):** `faster-whisper`를 활용한 로컬 음성 전사 (GPU 자동 감지).
- **AI 업무 추출:** GPT-4o mini 모델을 통해 회의 맥락에서 할 일(Title, Content, Assignee, Deadline)을 추출.
- **Notion 자동 연동:** 추출된 업무를 지정된 Notion 데이터베이스에 칸반 카드로 자동 등록.
- **MCP 브릿지:** Claude Desktop에서 `get_meeting_summary` 도구를 통해 최신 회의 내용을 즉시 조회.
- **Premium UI:** React, Tailwind CSS 기반의 세련된 글래스모피즘 디자인.

## 🛠️ 기술 스택

- **Frontend:** React (Vite), Tailwind CSS, Axios, Lucide React
- **Backend:** Python FastAPI, SQLAlchemy, SQLite, faster-whisper, LangChain
- **AI:** OpenAI GPT-4o mini, faster-whisper (Base model)
- **Integration:** Notion API (Async), mcp[fastmcp]

## 🚀 시작하기

### 1. 환경 변수 설정

`backend/.env.example` 파일을 복사하여 `backend/.env`를 생성하고 API 키를 입력하세요.

```env
OPENAI_API_KEY=your_openai_api_key
NOTION_API_KEY=your_notion_api_key
NOTION_DB_ID=your_notion_database_id
```

### 2. 백엔드 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

### 4. MCP 서버 설정 (Claude Desktop)

`~/Library/Application Support/Claude/claude_desktop_config.json`에 다음 설정을 추가하세요.

```json
{
  "mcpServers": {
    "meeting-agent": {
      "command": "/path/to/backend/.venv/bin/python",
      "args": ["/path/to/backend/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your_api_key",
        "NOTION_API_KEY": "your_notion_key",
        "NOTION_DB_ID": "your_db_id"
      }
    }
  }
}
```

## 🏗️ 프로젝트 구조

- `/backend`: FastAPI 서버, DB 모델, STT/Agent/Notion 서비스, MCP 서버
- `/frontend`: React 기반 사용자 UI
- `/backend/meeting_data.db`: SQLite 데이터베이스 파일 (자동 생성)
