from a2a.types import AgentCard as AgentCard
from pydantic import BaseModel

class HttpxClientOptions(BaseModel):
    """Options for the HTTP client.

    Args:
        timeout: The timeout for the HTTP client.
    """
    timeout: float | None
    class Config:
        extra: str

class A2AClientConfig(BaseModel):
    """Configuration for A2A client.

    Args:
        discovery_urls: A list of base URLs to discover agents from using .well-known/agent.json.
        known_agents: A dictionary of known agents, keyed by AgentCard.name,
                      storing the parsed AgentCard objects. Can be pre-populated or
                      augmented by discovery.
        httpx_client_options: Options for the HTTP client.
    """
    discovery_urls: list[str] | None
    known_agents: dict[str, AgentCard]
    httpx_client_options: HttpxClientOptions | None
