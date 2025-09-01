from autogen_agentchat.base import TaskResult
from exceptions.exceptions import InvalidToolCallException

async def run_agent_with_validation(agent, query):
    result = await agent.run(task=query)
    # result.messages = [{"type": "function", "name": "search_knowledge", "parameters": {"query": "some query"}}]
    answer = result.messages[-1].content
    # print(f"answer=run agent_with_validation========={answer}")
    # print(type(result))
    if isinstance(answer, str) and "\"name\":" in answer and "\"parameters\":" in answer:
        raise InvalidToolCallException(result)
    return result

async def run_stream_agent_with_validation(agent, query):
    async for event in agent.run_stream(task=query):
        # print(f"+++++++========={event}")
        # print(type(event))
        if isinstance(event, TaskResult):
            result = event
            # result.messages = [{"type": "function", "name": "search_knowledge", "parameters": {"query": "some query"}}]
    answer = result.messages[-1].content
    if isinstance(answer, str) and "\"name\":" in answer and "\"parameters\":" in answer:
        raise InvalidToolCallException(result)
    return result
