from _typeshed import Incomplete
from gllm_agents.tools.nested_agent_tool import NestedAgentTool as NestedAgentTool
from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.schema import MultimodalOutput as MultimodalOutput, MultimodalPrompt as MultimodalPrompt
from langchain.agents import AgentExecutor as LangchainAgentExecutor, BaseMultiActionAgent
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import AsyncCallbackManagerForChainRun as AsyncCallbackManagerForChainRun, CallbackManagerForChainRun as CallbackManagerForChainRun, Callbacks as Callbacks
from langchain_core.tools import BaseTool as BaseTool
from typing import Any, Sequence

manager: Incomplete
logger: Incomplete

class GLLMMultiActionAgent(BaseMultiActionAgent):
    '''Bridges a GLLM Agent with LangChain\'s BaseMultiActionAgent interface.

    This class allows a GLLM Agent (which uses an LMInvoker internally) to be
    used within LangChain\'s execution framework (e.g., with an AgentExecutor).
    It handles the conversion of prompts and responses between the GLLM Agent\'s
    LMInvoker system and the format expected by LangChain.

    Primarily designed for asynchronous operation via the `aplan` method.

    Attributes:
        instruction (str): The system instruction for the language model.
        invoker (BaseLMInvoker): The LMInvoker instance associated with the GLLM Agent,
            used for making calls to the language model.
        tools (List[BaseTool]): A list of tools available to the GLLM Agent.
        event_emitter (Optional[EventEmitter]): An optional event emitter for streaming
            intermediate steps and other events. Defaults to None.
        input_keys_arg (List[str]): The list of input keys that the agent expects.
            Defaults to ["input"].
        return_keys_arg (List[str]): The list of keys for the agent\'s return values.
            Defaults to ["output"].
        prompt_memory (List[Tuple[PromptRole, List[Any]]]): Pre-formatted prompt memory.
    '''
    instruction: str
    invoker: BaseLMInvoker
    tools: list[BaseTool]
    event_emitter: EventEmitter | None
    input_keys_arg: list[str]
    return_keys_arg: list[str]
    prompt_memory: MultimodalPrompt | None
    model_config: Incomplete
    def __init__(self, instruction: str, invoker: BaseLMInvoker, tools: list[BaseTool], event_emitter: EventEmitter | None = None, prompt_memory: MultimodalPrompt | None = None) -> None:
        """Initializes the GLLMMultiActionAgent.

        Args:
            instruction (str): The system instruction for the language model.
            invoker (BaseLMInvoker): The LMInvoker from the GLLM Agent.
            tools (List[BaseTool]): Tools available to the GLLM Agent.
            event_emitter (Optional[EventEmitter], optional): Event emitter for streaming.
                Defaults to None.
            prompt_memory (Optional[MultimodalPrompt], optional):
                Pre-formatted prompt memory. Defaults to None.
        """
    @property
    def input_keys(self) -> list[str]:
        """Input keys for the agent."""
    @property
    def return_values(self) -> list[str]:
        """Return values of the agent."""
    def plan(self, intermediate_steps: list[tuple[AgentAction, str]], callbacks: Callbacks = None, **kwargs: Any) -> list[AgentAction] | AgentFinish:
        """Synchronous planning. (Not Implemented)

        This method is intentionally not implemented to encourage asynchronous
        operations. Please use the `aplan` method.

        Args:
            intermediate_steps: Steps the LLM has taken to date, along with observations.
            callbacks: Callbacks to run.
            **kwargs: User inputs.

        Raises:
            NotImplementedError: This method is not implemented.
        """
    async def aplan(self, intermediate_steps: list[tuple[AgentAction, str]], callbacks: Callbacks = None, **kwargs: Any) -> list[AgentAction] | AgentFinish:
        '''Asynchronously decides the next action(s) or finishes execution.

        Args:
            intermediate_steps (List[Tuple[AgentAction, str]]): A list of previous
                agent actions and their corresponding string observations.
            callbacks (Callbacks, optional): LangChain callbacks. Not directly used by
                this method but maintained for interface compatibility. Defaults to None.
            **kwargs (Any): Additional keyword arguments representing the initial inputs
                to the agent (e.g., `input="user\'s query"`).

        Returns:
            Union[List[AgentAction], AgentFinish]: A list of `AgentAction` objects if the
                agent decides to take one or more actions, or an `AgentFinish` object
                if the agent has completed its work.
        '''
    def get_allowed_tools(self) -> list[str] | None:
        """Returns a list of tool names that this agent is allowed to use."""
    def return_stopped_response(self, early_stopping_method: str, _intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any) -> AgentFinish:
        '''Returns an AgentFinish object when the agent is stopped early.

        Args:
            early_stopping_method (str): The method used for early stopping.
                Currently, only "force" is supported.
            _intermediate_steps (List[Tuple[AgentAction, str]]): The history of
                actions and observations.
            **kwargs (Any): Additional inputs.

        Returns:
            AgentFinish: An AgentFinish object indicating the agent stopped.

        Raises:
            ValueError: If `early_stopping_method` is not "force".
        '''
    def tool_run_logging_kwargs(self) -> dict[str, Any]:
        """Returns keyword arguments for logging tool runs. Currently empty."""

class AgentExecutor(LangchainAgentExecutor):
    """Custom GLLM AgentExecutor extending LangChain's AgentExecutor.

    This executor orchestrates the execution loop for a GLLM Agent. It receives
    the GLLM Agent instance and necessary components (invoker, tools) and internally
    creates the `GLLMMultiActionAgent` adapter needed for the LangChain execution flow.

    It prioritizes asynchronous operations (`_aperform_agent_action`) and integrates
    with the GLLM event emitter system.
    """
    def __init__(self, instruction: str, invoker: BaseLMInvoker, tools: Sequence[BaseTool], max_iterations: int | None = 15, max_execution_time: float | None = None, verbose: bool = False, event_emitter: EventEmitter | None = None, handle_parsing_errors: bool = True, prompt_memory: MultimodalPrompt | None = None, **kwargs: Any) -> None:
        """Initializes the custom AgentExecutor.

        Args:
            instruction (str): The system instruction to be passed to the GLLMMultiActionAgent.
            invoker (BaseLMInvoker): The LMInvoker to be used by the adapter.
            tools (Sequence[BaseTool]): Tools available for execution.
            max_iterations (Optional[int], optional): Max iterations for the loop. Defaults to 15.
            max_execution_time (Optional[float], optional): Max wall time. Defaults to None.
            verbose (bool, optional): Enable verbose logging. Defaults to False.
            event_emitter (Optional[EventEmitter], optional): Emitter for events. Defaults to None.
            handle_parsing_errors (bool, optional): Handle output parsing errors. Defaults to True.
            prompt_memory (Optional[MultimodalPrompt], optional):
                Formatted prompt memory. Defaults to None.
            **kwargs (Any): Additional keyword arguments passed to the parent
                `LangchainAgentExecutor` constructor.
        """
    @property
    def event_emitter(self) -> EventEmitter | None:
        """Get the event emitter."""
