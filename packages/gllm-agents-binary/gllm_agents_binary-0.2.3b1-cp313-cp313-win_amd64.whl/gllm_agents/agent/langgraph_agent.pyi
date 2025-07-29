from _typeshed import Incomplete
from a2a.types import AgentCard as AgentCard
from gllm_agents.agent.base_agent import BaseAgent as BaseAgent
from gllm_agents.mcp.client import MCPClient as MCPClient
from gllm_agents.utils.a2a_connector import A2AConnector as A2AConnector
from gllm_agents.utils.logger_manager import LoggerManager as LoggerManager
from langchain_core.messages import BaseMessage as BaseMessage
from langchain_core.runnables import Runnable as Runnable
from langchain_core.tools import BaseTool
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.prebuilt.tool_node import ToolNode
from typing import Any, AsyncGenerator, Callable, Sequence

logger: Incomplete
LangGraphTool = BaseTool | ToolExecutor | ToolNode

def create_a2a_tool(agent_card: AgentCard) -> Callable:
    """Creates a LangGraph tool for A2A communication."""

class LangGraphAgent(BaseAgent):
    """An agent that wraps a compiled LangGraph graph.

    This class implements AgentInterface and uses a LangGraph `Graph`
    (typically a compiled `StateGraph`) to manage execution flow.
    It inherits A2A client capabilities from BaseAgent.
    """
    agent_executor: Runnable
    thread_id_key: str
    model: Any
    tools: Sequence[LangGraphTool]
    def __init__(self, name: str, instruction: str, model: Any, tools: Sequence[LangGraphTool], description: str | None = None, thread_id_key: str = 'thread_id', verbose: bool = False, **kwargs: Any) -> None:
        """Initializes the LangGraphAgent.

        Args:
            name: The name of this agent.
            instruction: The system instruction for the agent, used if no initial
                         messages are provided in `arun` or `stream`.
            model: The language model instance to be used by the agent.
            tools: A list of tools the agent can use.
            description: An optional human-readable description.
            thread_id_key: The key used in the `configurable` dict to pass the thread ID
                           to the LangGraph methods (ainvoke, astream_events).
            verbose: If True, sets langchain.debug = True for verbose LangChain logs.
            **kwargs: Additional keyword arguments passed to the parent `__init__`.
        """
    def run(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Synchronously runs the LangGraph agent by wrapping `arun`.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration (e.g., thread_id).
            **kwargs: Additional keyword arguments passed to `arun`.

        Returns:
            A dictionary containing the agent's response.

        Raises:
            RuntimeError: If `asyncio.run()` is called from an already running event loop.
        """
    async def arun(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Asynchronously runs the LangGraph agent.

        If MCP configuration exists, connects to the MCP server and registers tools before running.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration (e.g., thread_id).
            **kwargs: Additional keyword arguments, including `messages` if providing
                      a full message history instead of a single query.

        Returns:
            A dictionary containing the agent's output and the full final state from the graph.
        """
    async def arun_stream(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> AsyncGenerator[str | dict[str, Any], None]:
        """Asynchronously streams the LangGraph agent's response.

        If MCP configuration exists, connects to the MCP server and registers tools before streaming.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration (e.g., thread_id).
            **kwargs: Additional keyword arguments, including `messages` if providing
                      a full message history instead of a single query.

        Yields:
            Text chunks from the language model's streaming response.
        """
    def add_mcp_server(self, mcp_config: dict[str, dict[str, Any]]) -> None:
        """Adds a new MCP server configuration.

        Args:
            mcp_config: Dictionary containing server name as key and its configuration as value.

        Raises:
            ValueError: If mcp_config is empty or None, or if any server configuration is invalid.
            KeyError: If any server name already exists in the configuration.
        """
    async def arun_a2a_stream(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> AsyncGenerator[dict[str, Any], None]:
        '''Asynchronously streams the agent\'s response in a generic format for A2A.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration.
            **kwargs: Additional keyword arguments.

        Yields:
            Dictionaries with "status" and "content" keys.
            Possible statuses: "working", "completed", "failed", "canceled".
        '''
    def register_a2a_agents(self, agent_cards: list[AgentCard]) -> None:
        """Convert known A2A agents to LangChain tools.

        This method takes the agents from a2a_config.known_agents, creates A2AAgent
        instances for each one, and wraps them in LangChain tools.

        Returns:
            None: The tools are added to the existing tools list.
        """
