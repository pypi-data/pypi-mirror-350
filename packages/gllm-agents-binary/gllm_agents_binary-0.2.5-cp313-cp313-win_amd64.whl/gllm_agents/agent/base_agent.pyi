import abc
from _typeshed import Incomplete
from a2a.types import AgentCard
from gllm_agents.a2a.server.langgraph_executor import LangGraphA2AExecutor as LangGraphA2AExecutor
from gllm_agents.agent.interface import AgentInterface as AgentInterface
from gllm_agents.agent.types import A2AClientConfig as A2AClientConfig
from gllm_agents.utils.a2a_connector import A2AConnector as A2AConnector
from gllm_agents.utils.logger_manager import LoggerManager as LoggerManager
from starlette.applications import Starlette
from typing import Any, AsyncGenerator

logger: Incomplete
AGENT_EXECUTOR_MAPPING: Incomplete

class BaseAgent(AgentInterface, metaclass=abc.ABCMeta):
    """Base class for agents, providing common A2A client method implementations.

    Concrete agent implementations (e.g., LangGraphAgent, GoogleADKAgent)
    should inherit from this class if they need to utilize the shared A2A
    client functionalities.
    """
    mcp_config: Incomplete
    def __init__(self, name: str, instruction: str, description: str | None = None, **kwargs: Any) -> None:
        """Initializes the BaseAgent.

        Passes arguments to the AgentInterface constructor.
        The AgentInterface constructor handles parsing of a2a_config dict
        into an A2AClientConfig object.

        After initialization, if a2a_config is provided and contains discovery_urls,
        this method will attempt to discover and register agents from those URLs.
        """
    def to_a2a(self, agent_card: AgentCard, **kwargs: Any) -> Starlette:
        """Converts the agent to an A2A-compatible ASGI application.

        This implementation provides a base setup for A2A server components.
        Subclasses can override this method if they need custom executor
        or task store implementations.

        Args:
            agent_card: The agent card to use for the A2A application.

        Returns:
            A Starlette ASGI application that can be used with any ASGI server.
        """
    @classmethod
    def discover_agents(cls, a2a_config: A2AClientConfig, **kwargs: Any) -> list[AgentCard]:
        """Discover agents from the URLs specified in a2a_config.discovery_urls.

        This concrete implementation fetches and parses .well-known/agent.json
        from each discovery URL to build a list of available agents.

        Args:
            **kwargs: Additional keyword arguments (unused in this implementation).

        Returns:
            A list of AgentCard objects representing discovered agents.
        """
    def send_to_agent(self, agent_card: AgentCard, message: str | dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Synchronously sends a message to another agent using the A2A protocol.

        This method is a synchronous wrapper around asend_to_agent. It handles the creation
        of an event loop if one doesn't exist, and manages the asynchronous call internally.

        Args:
            agent_card: The AgentCard instance containing the target agent's details including
                URL, authentication requirements, and capabilities.
            message: The message to send to the agent. Can be either a string for simple text
                messages or a dictionary for structured data.
            **kwargs: Additional keyword arguments passed to asend_to_agent.

        Returns:
            A dictionary containing the response details:
                - status (str): 'success' or 'error'
                - content (str): Extracted text content from the response
                - task_id (str, optional): ID of the created/updated task
                - task_state (str, optional): Current state of the task
                - raw_response (str): Complete JSON response from the A2A client
                - error_type (str, optional): Type of error if status is 'error'
                - message (str, optional): Error message if status is 'error'

        Raises:
            RuntimeError: If called from within an existing event loop or if asend_to_agent
                encounters an unhandled exception.
        """
    async def asend_to_agent(self, agent_card: AgentCard, message: str | dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Asynchronously sends a message to another agent using the A2A protocol.

        This method handles the core A2A communication logic, creating and sending properly
        formatted A2A messages and processing the responses.

        Args:
            agent_card: The AgentCard instance containing the target agent's details including
                URL, authentication requirements, and capabilities.
            message: The message to send to the agent. Can be either a string for simple text
                messages or a dictionary for structured data.
            **kwargs: Additional keyword arguments.

        Returns:
            A dictionary containing the response details:
                - status (str): 'success' or 'error'
                - content (str): Extracted text content from the response
                - task_id (str, optional): ID of the created/updated task
                - task_state (str, optional): Current state of the task
                - raw_response (str): Complete JSON response from the A2A client
                - error_type (str, optional): Type of error if status is 'error'
                - message (str, optional): Error message if status is 'error'

        Raises:
            httpx.HTTPError: If there's an HTTP-related error during the request.
            Exception: For any other unexpected errors during message sending or processing.
        """
    async def astream_to_agent(self, agent_card: AgentCard, message: str | dict[str, Any], **kwargs: Any) -> AsyncGenerator[dict[str, Any], None]:
        """Asynchronously sends a streaming message to another agent using the A2A protocol.

        This method supports streaming responses from the target agent, yielding chunks of
        the response as they become available. It handles various types of streaming events
        including task status updates, artifact updates, and message parts.

        Args:
            agent_card: The AgentCard instance containing the target agent's details including
                URL, authentication requirements, and capabilities.
            message: The message to send to the agent. Can be either a string for simple text
                messages or a dictionary for structured data.
            **kwargs: Additional keyword arguments.

        Yields:
            Dictionaries containing streaming response chunks:
                For successful chunks:
                    - status (str): 'success'
                    - content (str): Extracted text content from the chunk
                    - task_id (str): ID of the associated task
                    - task_state (str): Current state of the task
                    - final (bool): Whether this is the final chunk
                    - artifact_name (str, optional): Name of the artifact if chunk is an artifact update
                For error chunks:
                    - status (str): 'error'
                    - error_type (str): Type of error encountered
                    - message (str): Error description

        Raises:
            httpx.HTTPError: If there's an HTTP-related error during the streaming request.
            Exception: For any other unexpected errors during message streaming or processing.
        """
