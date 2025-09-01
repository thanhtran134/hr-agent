from orchestrator import agent_builder
import json
from typing import List
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.messages import BaseChatMessage, BaseAgentEvent, ToolCallExecutionEvent, TextMessage
from autogen_agentchat.base import TaskResult
from .llm_connect import get_llm_client

from orchestrator.mcp_tool_loader import load_mcp_tools
from pydantic import BaseModel, Field

class CustomAssistantAgent(AssistantAgent):
    async def run_stream(self, *args, **kwargs):
        output_messages: List[BaseAgentEvent | BaseChatMessage] = []
        async for event in super().run_stream(*args, **kwargs):
            # When the tool is called
            if isinstance(event, ToolCallExecutionEvent):
                for function_result in event.content:
                    if function_result.name == "search_knowledge":
                        # 1. yield ToolCallExecutionEvent
                        yield event
                        output_messages.append(event)

                        # 2. Yield TextMessage custom content
                        content_val = function_result.content
                        list_val = json.loads(content_val)
                        result = "\n\n".join([item["text"] for item in list_val])
                        msg = TextMessage(
                            role="assistant",
                            content=result,
                            source=event.source,
                        )
                        yield msg
                        output_messages.append(msg)
                        yield TaskResult(messages=output_messages)

            # If not search_knowledge tool -> yield normal
            if isinstance(event, (BaseChatMessage, BaseAgentEvent)):
                output_messages.append(event)
                yield event

        # yield TaskResult(messages=output_messages)
# yield TaskResult(messages=output_messages)

class AgentResponse(BaseModel):
    answer: str = Field(
        ...,
        description="Final answer in user's language, clear and natural. Do not mention tool names or parameters."
    )

async def create_orchestrator_agent():
    llm_client = get_llm_client()
    tools = await load_mcp_tools()

    # system_prompt = (
    #     "You are an orchestrator AI. Analyze the user's question and, "
    #     "if necessary, use the MCP tool or directly respond through LLM. "
    #     "Always call init context tool first before taking next action. "
    #     "Always answer in the user's language."
    # )
    system_prompt = (
        "~당신은 인사 AI챗봇이고 인사 관련 질문에 답변해야 합니다. 'n"
        "~사용자의 질의에 대해 분석하고 MCP툴을 활용하거나 LLM을 통해 직접 답변해야 합니다. 'n"
        "~항상 먼저 init context 툴을 호출해야 합니다. 다음 행동을 취하기 전입니다. 'n"
        "~사용자가 사용한 언어로 항상 답변해야 합니다. 'n"
    )

    return AssistantAgent(
        name="orchestrator",
        model=llm_client,
        tools=tools,
        system_message=system_prompt,
        reflect_on_tool_use=True,
        max_tool_iterations=3,
        # output_content_type=AgentResponse
    )