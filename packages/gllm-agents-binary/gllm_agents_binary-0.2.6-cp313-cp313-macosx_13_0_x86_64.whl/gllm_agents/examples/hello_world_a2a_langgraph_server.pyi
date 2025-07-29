from _typeshed import Incomplete
from gllm_agents.agent.langgraph_agent import LangGraphAgent as LangGraphAgent
from gllm_agents.examples.tools import weather_tool as weather_tool
from gllm_agents.utils.logger_manager import LoggerManager as LoggerManager

logger: Incomplete
SERVER_AGENT_NAME: str

def main(host: str, port: int):
    """Runs the LangGraph Weather A2A server."""
