from _typeshed import Incomplete
from gllm_agents.agent.base_agent import BaseAgent as BaseAgent
from gllm_agents.utils.logger_manager import LoggerManager as LoggerManager
from google.adk.agents import LlmAgent
from typing import Any, AsyncIterator, Callable

logger: Incomplete
MODEL_TEMPERATURE: float

class GoogleADKAgent(BaseAgent):
    """An agent that wraps a native Google ADK Agent.

    This class implements the AgentInterface and uses Google's LlmAgent
    to handle the core conversation and tool execution logic via ADK's
    async-first design.
    """
    adk_native_agent: LlmAgent
    model: Incomplete
    max_iterations: Incomplete
    tools: Incomplete
    session_service: Incomplete
    def __init__(self, name: str, instruction: str, model: str, tools: list[Callable] | None = None, description: str | None = None, max_iterations: int = 3, **kwargs: Any) -> None:
        '''Initializes the GoogleADKAgent.

        Args:
            name: The name of this wrapper agent.
            instruction: The instruction for this wrapper agent.
            model: The name of the Google ADK model to use (e.g., "gemini-1.5-pro-latest").
            tools: An optional list of callable tools for the ADK agent.
            description: An optional human-readable description.
            max_iterations: Maximum number of iterations to run (default: 3).
            **kwargs: Additional keyword arguments passed to the parent `__init__`.
        '''
    def run(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Synchronously runs the Google ADK agent by wrapping `arun`.

        Args:
            query: The input query for the agent.
            **kwargs: Additional keyword arguments passed to `arun`.

        Returns:
            A dictionary containing the agent's response.

        Raises:
            RuntimeError: If `asyncio.run()` is called from an already running event loop.
        """
    async def arun(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Asynchronously runs the agent with the given query and returns the response.

        Args:
            query: The user's query to process.
            **kwargs: Additional keyword arguments.

        Returns:
            A dictionary containing the output and other metadata.

        Raises:
            ValueError: If the ADK native agent is not initialized.
        """
    async def arun_stream(self, query: str, **kwargs: Any) -> AsyncIterator[str]:
        """Runs the agent with the given query and streams the response parts.

        Args:
            query: The user's query to process.
            **kwargs: Additional keyword arguments.

        Yields:
            Text response chunks from the model.

        Raises:
            ValueError: If the ADK native agent is not initialized.
        """
    def register_a2a_agents(self, agents: list):
        """Register A2A agents for this agent.

        Args:
            agents: A list of A2A agents to register.
        """
    def add_mcp_server(self, mcp_config: dict[str, dict[str, Any]]) -> None:
        """Adds a new MCP server configuration.
        Args:
            mcp_config: Dictionary containing server name as key and its configuration as value.
        Raises:
            ValueError: If mcp_config is empty or None, or if any server configuration is invalid.
            KeyError: If any server name already exists in the configuration.
        """
