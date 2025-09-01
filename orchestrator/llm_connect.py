from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import LLM_CONFIG

def get_llm_client():
    return OpenAIChatCompletionClient(
        model=LLM_CONFIG["model"],
        base_url=LLM_CONFIG["base_url"],
        api_key=LLM_CONFIG["api_key"],
        parallel_tool_calls=True,
        temperature=0.2,
        # http_client,
        # model_info={
        #     "vision": False,
        #     "function_calling": True,
        #     "json_output": True,
        #     "family": ModelFamily.R1,
        #     "structured_output": True,
        # },
    )
