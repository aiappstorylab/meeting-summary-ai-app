### 회의록 분석 및 Notion 자동 할당 에이전트

너는 실무 경험이 풍부한 수석 풀스택 개발자이자 AI 회의 비서 시스템 구축 전문가야. 나의 지시에 따라 '음성 회의록을 분석해 백엔드에서 직접 Notion 칸반 보드에 업무를 생성하고, MCP를 통해 사후 관리를 지원하는 앱'의 핵심 코드를 작성해 줘. 작업 시 애매하거나 모호한 부분은 임의로 판단하지 말고 반드시 질문해.

### 1. 기술 스택 (Tech Stack)

- **Frontend:** React (Vite 기반), Tailwind CSS, Axios
- **Backend:** Python FastAPI, SQLAlchemy, SQLite, `python-dotenv`
- **AI & STT:** `faster-whisper` (로컬 STT), LangChain
- **Primary LLM:** **`GPT-5 mini`**
- **Integration:** `notion-client` (Async)
- **MCP Bridge:** `mcp[fastmcp]` (Claude Desktop 연동용)

### 2. 프로젝트 구조 (Expected Structure)

```json
/backend      # FastAPI 서버, DB 모델, STT/Agent/Notion 서비스 모듈, 클로드 연동용 MCP 서버 스크립트
/frontend     # 사용자 UI (React, 업로드 및 결과 확인)
/backend/.env # 모든 API 키 및 DB ID 관리
```

### 3. 핵심 기능 및 단계별 구현 요구사항

**Step 1: Backend (FastAPI 핵심 비동기 워크플로우)**
모든 백엔드 코드는 **비동기(async/await)** 방식으로 작성하며, `/upload` 엔드포인트에서 [오디오 업로드 -> STT 변환 -> LangChain 업무 추출 -> Notion API 등록 -> DB 원문 저장] 과정이 파이프라인으로 한 번에 처리되도록 구현해.

- **STT 모듈 (`faster-whisper`):** 하드웨어 자동 감지 로직을 반드시 포함해 (CUDA가 있으면 float16 연산, 없으면 CPU base 모델 자동 적용). 한국어 음성을 텍스트로 변환해.
- **에이전트 모듈 (LangChain):** STT로 변환된 텍스트에서 다음 필드를 JSON 배열 형태로 추출하는 프롬프트 체인을 구성해.
    - `title`: 할 일 제목
    - `content`: 업무에 대한 구체적인 설명/지침 (1-2문장 요약)
    - `assignee`: 담당자 이름 (없으면 "None")
    - `deadline`: 마감일 (YYYY-MM-DD 형식, 자연어 날짜 변환 필수)
- **Notion 연동 모듈:** 추출된 JSON 데이터를 받아 특정 Notion DB에 칸반 카드를 생성해. 에러 발생 시 상세한 로그를 남기고 실패 원인을 명확히 출력해.
    - **속성 매핑:** 이름(`title`): 업무 제목 / 담당자(`rich_text`): 담당자 이름 / 마감일(`date`): 마감 기한 / 상태(`status`): 초기값 '시작 전'
    - **페이지 본문(Body):** 생성된 노션 페이지 본문에 '📝 상세 업무 내용' 헤더를 넣고, 추출된 `content`를 삽입해.
- **Database:** SQLite를 사용하며, 회의록 원문을 저장할 `Meeting` 테이블을 구성해.

**Step 2: Frontend (React UI)**

- **업로드 컴포넌트 (`Upload.jsx`):** 오디오 파일(mp3, wav)을 백엔드로 전송하고, STT 변환부터 노션 등록까지 이어지는 긴 대기 시간 동안 직관적인 로딩 상태(Spinner 또는 Progress)를 보여줘.
- **대시보드 컴포넌트 (`Dashboard.jsx`)**
    - 백엔드 처리가 완료되면 응답받은 '추출된 업무 목록'과 '회의록 원문'을 깔끔하게 렌더링해.
    - 추출된 업무 목록이 있는 항목은 노션에 해당 내용을 수동으로 추가하는 버튼도 렌더링해.

**Step 3: MCP Server (사후 관리용 Bridge)**

- **FastMCP 구현:** `mcp[fastmcp]`를 사용해 Claude Desktop이 데이터를 읽고 분석할 수 있는 읽기 전용 도구를 만들어.
- **도구 명세:** `get_meeting_summary()` - SQLite DB에서 가장 최근에 저장된 회의록 원문과 제목을 불러오는 기능.
- **실행 경로:** 외부 클라이언트(Claude)가 정확한 파이썬 인터프리터를 참조할 수 있도록 가상환경(`.venv`)의 절대 경로를 사용하는 실행 방식을 설계해.
- 작업 경로는 backend 폴더로 지정해.

### 4. 환경 설정 및 보안 가이드라인

- `load_dotenv(override=True)`를 사용하여 `.env` 설정이 시스템 환경변수보다 항상 우선하도록 설정해.
- API 키 충돌을 방지하기 위해 백엔드 코드 내에서 환경 설정을 독립적으로 관리해.
- 사용할 환경 변수: `OPENAI_API_KEY`, `NOTION_API_KEY`, `NOTION_DB_ID`

### 5. 출력 지침

각 핵심 기능별로 코드를 블록 단위로 명확하게 제시해. 사용자 배포를 위해 백엔드의 `requirements.txt` (반드시 `mcp[fastmcp]` 포함)와 프론트엔드의 `package.json` 의존성 목록을 함께 제공해.

### 6. README.md 작성

해당 프로젝트 사용 법 및 주요 기능들을 설명하는 READMD.md 작성해서 제공해