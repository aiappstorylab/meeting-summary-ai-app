from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class TaskItem(BaseModel):
    title: str = Field(description="할 일 제목")
    content: str = Field(description="업무에 대한 구체적인 설명/지침 (1-2문장 요약)")
    assignee: str = Field(description="담당자 이름 (없으면 'None')")
    deadline: str = Field(description="마감일 (YYYY-MM-DD 형식, 자연어 날짜 변환 필수)")

class TaskList(BaseModel):
    tasks: List[TaskItem]

class AgentService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.parser = JsonOutputParser(pydantic_object=TaskList)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "너는 회의록 내용을 분석하여 수행해야 할 업무(Action Items)를 추출하는 전문가야. "
                       "반드시 한국어로 답변하고, 출력 형식은 아래 제공된 JSON 스키마를 엄격히 따라야 해.\n\n"
                       "{format_instructions}"),
            ("user", "다음 회의록 내용을 분석해서 할 일 목록을 추출해 줘:\n\n{meeting_text}")
        ])
        
        self.chain = self.prompt | self.llm | self.parser

    async def extract_tasks(self, meeting_text: str) -> List[dict]:
        response = await self.chain.ainvoke({
            "meeting_text": meeting_text,
            "format_instructions": self.parser.get_format_instructions()
        })
        return response.get("tasks", [])

# Singleton instance
agent_service = AgentService()
