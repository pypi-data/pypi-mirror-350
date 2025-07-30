from _typeshed import Incomplete
from langchain_core.tools import BaseTool as BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from types import TracebackType

class MCPClient:
    """MCP Client for GLLM Agents.

    This class provides a client for connecting to MCP servers.

    Attributes:
        connections (dict[str, dict]): Dictionary of connection dictionaries for MCP servers.
        client (MultiServerMCPClient): The MCP client instance.
        failed_connections (dict[str, Exception]): Dictionary of failed connections.
    """
    connections: Incomplete
    client: MultiServerMCPClient | None
    failed_connections: dict[str, Exception]
    log_level: Incomplete
    logger: Incomplete
    def __init__(self, connections: dict[str, dict], log_level: int = ...) -> None:
        '''Initialize the MCPClient with the provided connections.

        Example on how to initialize:
        ```python
        client = MCPClient({
            "sse": {
                "url": "http://localhost:8000",
                "transport": "sse",
            },
            "stdio": {
                "command": "python",
                "args": ["path/to/python/file.py"],
                "transport": "stdio",
            },
        })
        client = MCPClient(connections)
        async with client:
            tools = client.get_tools()
        ```

        Right now, as per the Langchain\'s MCP Adapter Library, the only supported transports
        are "sse" and "stdio". Python MCP also currently does not support HTTP Streams.

        Args:
            connections (dict[str, dict]): Dictionary of connection dictionaries for MCP servers.
        '''
    def get_tools(self) -> list[BaseTool]:
        """Get the tools from the MCPClient.

        This method returns the tools from the MCPClient. Example:

        ```python
        tools = client.get_tools()
        ```
        """
    async def __aenter__(self):
        """Initialize the MCPClient and connect to servers.

        Called automatically when entering an `async with` block.

        Returns:
            MCPClient: The initialized client instance.

        Raises:
            RuntimeError: If unable to initialize the core MCP client or
                          if all server connections fail.
        """
    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        """Clean up the MCPClient connections.

        Called automatically when exiting an `async with` block.

        Args:
            exc_type: The type of exception that was raised.
            exc_val: The exception that was raised.
            exc_tb: The traceback of the exception.

        Returns:
            None
        """
