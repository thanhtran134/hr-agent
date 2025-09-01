import json
from fastapi import FastAPI
import uvicorn
from autogen.agentchat import ThoughtEvent
from exceptions.exceptions import InvalidToolCallException
from exceptions.utils import run_agent_with_validation, run_stream_agent_with_validation
from autogen.core.models import FunctionExecutionResult
from orchestrator.agent_builder import create_orchestrator_agent_with_context
from orchestrator.messages_loader import messages_loader
from schemas import ChatResponseMemory, ChatRequestMemory, get_current_datetime

app = FastAPI(title="HR Agent: Autogen")

@app.get("/")
async def root():
    return {"message": "Chatbot is running"}

@app.post("/autogen_chat", response_model=ChatResponseMemory)
async def autogen_chat(item: ChatRequestMemory):
    print(json.dumps(item.__dict__, indent=2))
    print(item.query.strip())

    messages = messages_loader(item.history)
    agent = await create_orchestrator_agent_with_context(messages)

    # task = {"Current datetime": get_current_datetime()} #n
    # f'User ID: {item.knox_id}'n
    # f'Query: {item.query.strip()}'n
    # task = {"현재 날짜 및 시간": get_current_datetime()} #n
    # f'사용자 ID: {item.knox_id}'n
    # f'쿼리: {item.query.strip()}'n
    # try:
    result = await run_agent_with_validation(agent, task)
    # answer = result.messages[-1].content
    # except InvalidToolCallException as e:
    #     result = e.detail
    #     answer = "Please try again with the similar question."
    # try:
    result = await run_stream_agent_with_validation(agent, task)
    # answer = result.messages[-1].content
    # except InvalidToolCallException as e:
    #     result = e.detail