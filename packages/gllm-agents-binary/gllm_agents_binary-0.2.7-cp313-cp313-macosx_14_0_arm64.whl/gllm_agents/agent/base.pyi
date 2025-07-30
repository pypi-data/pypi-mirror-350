import abc
import logging
from _typeshed import Incomplete
from gllm_agents.constants import DEFAULT_AGENT_TIMEOUT as DEFAULT_AGENT_TIMEOUT
from gllm_agents.credentials.manager import CredentialsManager as CredentialsManager
from gllm_agents.executor.agent_executor import AgentExecutor as AgentExecutor
from gllm_agents.memory.base import BaseMemory as BaseMemory
from gllm_agents.tools.base import BaseTool as BaseTool
from gllm_agents.tools.nested_agent_tool import NestedAgentTool as NestedAgentTool
from gllm_agents.types import AgentProtocol as AgentProtocol, ChatMessage as ChatMessage
from gllm_core.event import EventEmitter
from gllm_core.event.handler import StreamEventHandler
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.schema import MultimodalPrompt as MultimodalPrompt
from gllm_rag.preset.initializer.model_id import ModelId as ModelId
from langchain_core.language_models import BaseChatModel as BaseChatModel
from typing import Any, AsyncGenerator

manager: Incomplete
logger: Incomplete

class Agent(AgentProtocol, metaclass=abc.ABCMeta):
    """Concrete Base class for agents.

    This class provides a basic structure and default implementations.
    Derived classes can override methods to add specific functionality.

    Attributes:
        name (str): The name of the agent.
        instruction (str): The system instruction for the agent.
        description (Optional[str]): A description of what the agent does. Defaults to instruction.
        memory (Optional[BaseMemory]): The memory component for the agent.
        timeout (int): Maximum execution time in seconds for an agent run.
        max_iterations (int): Maximum number of iterations (LLM calls) allowed in an agent run.
        verbose (bool): Whether to enable verbose logging for agent execution steps.
        logger (logging.Logger): Logger instance for the agent.
        streaming (bool): Whether this agent should use its internal event emitter for streaming by default.
        lm_invoker (Optional[BaseLMInvoker]): The LM Invoker used by the agent for LLM calls.
        tools (List[BaseTool]): List of tools (including nested agents wrapped as tools) available to the agent.
        event_emitter (Optional[EventEmitter]): Internal event emitter for the agent, initialized if streaming=True.
    """
    name: str
    instruction: str
    description: str | None
    memory: BaseMemory | None
    timeout: int
    max_iterations: int
    verbose: bool
    logger: logging.Logger
    streaming: bool
    lm_invoker: BaseLMInvoker | None
    tools: list[BaseTool]
    event_emitter: EventEmitter | None
    def __init__(self, name: str, instruction: str = 'You are a helpful assistant.', description: str | None = None, memory: BaseMemory | None = None, timeout: int = ..., max_iterations: int = 15, verbose: bool = False, log_level: int = ..., streaming: bool = False, event_emitter: EventEmitter | None = None, tools: list[BaseTool] | None = None, agents: list[AgentProtocol] | None = None, model: str | ModelId | None = 'openai/gpt-4o', model_config: dict[str, Any] | None = None, llm: BaseChatModel | None = None) -> None:
        '''Initializes the base agent.

        Args:
            name (str): The name of the agent.
            instruction (str, optional): The system instruction for the agent.
                Defaults to "You are a helpful assistant.".
            description (Optional[str], optional): A description of what the agent does.
                Defaults to the instruction.
            memory (Optional[BaseMemory], optional): Memory component for chat history.
                Defaults to None.
            timeout (int, optional): Maximum execution time in seconds.
                Defaults to DEFAULT_AGENT_TIMEOUT.
            max_iterations (int, optional): Maximum execution iterations. Defaults to 15.
            verbose (bool, optional): Enable verbose logging. Defaults to False.
            log_level (int, optional): Logging level for the agent\'s logger.
                Defaults to logging.INFO.
            streaming (bool, optional): If True, initializes an internal EventEmitter
                for default streaming. Defaults to False.
            event_emitter (Optional[EventEmitter], optional): An event emitter to use
                for this specific run. Overrides the internal emitter and the
                streaming flag if provided. Defaults to None.
            tools (Optional[List[BaseTool]], optional): List of tools for the agent.
                Defaults to None.
            agents (Optional[List[AgentProtocol]], optional): List of nested agents to
                be wrapped as tools. Defaults to None.
            model (Optional[str | ModelId], optional): Model ID or alias for the LM Invoker.
                Defaults to "openai/gpt-4o". Ignored if llm is provided.
            model_config (Optional[dict[str, Any]], optional): Configuration for the LM Invoker,
                must include "credentials". Defaults to None. Ignored if llm is provided.
            llm (Optional[BaseChatModel], optional): A LangChain BaseChatModel instance.
                If provided, this will be used instead of model/model_config. Defaults to None.
        '''
    def run(self, query: str, event_emitter: EventEmitter | None = None, **kwargs: Any) -> dict[str, Any]:
        """Synchronously run the agent. **Not Implemented.**

        This method is intentionally not implemented to encourage asynchronous
        operations via the `arun` method.

        Args:
            query (str): The query string to process.
            event_emitter (Optional[EventEmitter]): Ignored.
            **kwargs (Any): Ignored.

        Raises:
            NotImplementedError: Always raised.
        """
    def get_stream_handler(self, event_emitter: EventEmitter | None = None) -> StreamEventHandler | None:
        """Returns the first StreamEventHandler from the provided or internal event emitter.

        Provides a safe way to access the handler for consuming streamed events.
        If an event_emitter is provided, it takes precedence over the internal one.

        Args:
            event_emitter (Optional[EventEmitter], optional): Event emitter to get handler from.
                If None, uses the agent's internal emitter. Defaults to None.

        Returns:
            Optional[StreamEventHandler]: The first StreamEventHandler instance found,
                or None if no suitable handler exists.
        """
    def setup_executor(self, *args: Any, **kwargs: Any) -> AgentExecutor:
        """Setup the executor for the agent.

        Args:
            **kwargs: Additional keyword arguments passed to the executor.
        """
    async def arun(self, query: str, streaming: bool = False, event_emitter: EventEmitter | None = None, **kwargs: Any) -> dict[str, Any]:
        """Run the agent asynchronously.

        Handles loading chat history, selecting the event emitter, invoking the
        agent executor, and saving the interaction to memory.

        Args:
            query (str): The query string to process.
            streaming (bool, optional): Explicitly request streaming for this run.
                If True and event_emitter is None, the agent's internal emitter
                (if available) will be used. Defaults to False.
            event_emitter (Optional[EventEmitter], optional): An event emitter to use
                for this specific run. Overrides the internal emitter and the
                streaming flag if provided. Defaults to None.
            **kwargs (Any): Additional keyword arguments passed to the execution logic
                (e.g., forwarded to the executor inputs).

        Returns:
            dict[str, Any]: A dictionary containing the agent's response or an error.

        Raises:
            ValueError: If streaming=True is requested but no event_emitter is provided
                and the agent was not initialized with streaming=True (no internal
                emitter is available) - this is now caught and returned in the dict.
        """
    async def stream(self, query: str, event_emitter: EventEmitter | None = None, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Stream the agent's response asynchronously.

        This is an async-only method as streaming is inherently asynchronous.
        Provides a direct streaming interface that yields chunks as they become
        available, similar to Google ADK's implementation.

        Args:
            query (str): The query string to process.
            event_emitter (Optional[EventEmitter], optional): An event emitter to use
                for this specific run. If not provided, uses the agent's internal
                emitter.
            **kwargs (Any): Additional keyword arguments passed to the execution logic.

        Yields:
            str: Chunks of the agent's response as they become available.

        Raises:
            ValueError: If no event emitter is available for streaming.
            RuntimeError: If execution fails or streaming cannot be initialized.
        """
