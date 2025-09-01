from typing import Union, List
from starlette import status
from fastapi import HTTPException
from autogen_agentchat.base import TaskResult

class AgentException(HTTPException):
    status_code: int
    detail: str
    ex: HTTPException

    def __init__(self, detail: str = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, ex: HTTPException = None):
        self.status_code = status_code
        self.detail = detail
        self.ex = ex

class InvalidToolCallException(AgentException):
    def __init__(self, detail: str | TaskResult = "Tool call returned in content instead of tool calls", ex: HTTPException = None):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            ex=ex
        )
