from typing import Dict, Any, List
from autogen.core.model_context import BufferedChatCompletionContext, UnboundedChatCompletionContext
from autogen.core.models import LLMMessage
from autogen.core.models import AssistantMessage, UserMessage

def messages_loader(history):
    messages: List[LLMMessage] = []
    for msg in history:
        messages.append(UserMessage(source="user", content=msg["message"]))
        messages.append(AssistantMessage(source="assistant", content=msg["response_message"]))
    return UnboundedChatCompletionContext(
        initial_messages=messages
    )