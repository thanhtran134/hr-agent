import json

from fastapi import FastAPI
import uvicorn
from autogen_agentchat.messages import ThoughtEvent
from exceptions.exceptions import InvalidToolCallException
from orchestrator.orchestrator import run_agent_with_validation, run_stream_agent_with_validation
from orchestrator.models import ImportExecutionResult
from orchestrator.orchestrator_agent import create_orchestrator_agent_with_context
from orchestrator_agentchat.base import TaskResult, TaskResultList
from orchestrator_agentchat.messages_loader import messages_loader
from orchestrator_agentchat.schemas import ChatResponseMemory, get_current_datetime

app = FastAPI(title="HR Agent Autogen")


@app.get("/")
async def root():
    return {"message": "Chatbot is running"}


@app.post("/autogen_chat", response_model=ChatResponseMemory)
async def autogen_chat(item: ChatRequestMemory):
    print("=========== item ===========")
    print(item)

    messages = messages_loader(item.history)

    agent = await create_orchestrator_agent_with_context(messages)

    # task = (f"Current datetime: {get_current_datetime()}\n"
    #         f"User ID: {item.knox_id}\n"
    #         f"Query: {item.query.strip()}")
    task = (f"현재 날짜 및 시간: {get_current_datetime()}\n"
            f"사용자 ID: {item.knox_id}\n"
            f"질문: {item.query.strip()}")

    try:
        # result = await run_agent_with_validation(agent, task)
        # answer = result.messages[-1].content
        # except InvalidToolCallException as e:
        #     result = e.detail
        #     answer = "Please try again with the similar question."

        result = await run_stream_agent_with_validation(agent, task)
        answer = result.messages[-1].content
    except InvalidToolCallException as e:
        result = e.detail
        answer = "Please try again with the similar question."

    # debug info
    context = ""
    for msg in result.messages:
        if isinstance(msg.content, list) and all(isinstance(item, FunctionExecutionResult) for item in msg.content):
            context += f"type = {msg.type}, content = {msg.content}\n"
            for tool_result in msg.content:
                context += f"tool_result: {tool_result}\n"
                context += f"VAL: {tool_result.result}\n"
                context += f"content_val = {tool_result.content}\n"
                context += f"content_type = {tool_result.content_type}\n"
                list_val = json.loads(content_val)
                context += f"list_val: {list_val}\n"
                context += f"VAL: {(list_val)}\n"
                context += f"Tool = {tool_result.name}\n"
        elif isinstance(msg, ThoughtEvent):
            continue
        else:
            context += f"type = {msg.type}, content = {msg.content}\n"
            context += "___________\n"
            print("DEBUG INFO")
            print(context)

    return ChatResponseMemory(
        answer=answer,
        messages=result.messages,
        debug_info={
            "context": context
        } if item.isDebugOn else None
    )

if __name__ == "__main__":
    uvicorn.run_app("router:app", host="127.0.0.1", port=8005)
