from config import MCP_SERVERS
from autogen_ext.tools.mcp import SseServerParams, StreamableHttpServerParams, mcp_server_tools,McpWorkbench, StdioServerParams
from autogen_core.tools import ToolSchema
from autogen_core.tools import FunctionTool

async def load_mcp_tools():
    tools = []
    for conf in MCP_SERVERS:
        if conf["type"] == "streamable-http":
            params = StreamableHttpServerParams(
                url=conf["url"],
                timeout=conf["timeout"]
            )
        elif conf["type"] == "stdio":
            params = StdioServerParams(
                command=conf["command"],
                args=conf.get("args", []),
                env=conf.get("env", {})
            )
        else:
            continue
        tools += await mcp_server_tools(server_params=params)
    # for tool in tools:
    #     tool._strict = True
    return tools
