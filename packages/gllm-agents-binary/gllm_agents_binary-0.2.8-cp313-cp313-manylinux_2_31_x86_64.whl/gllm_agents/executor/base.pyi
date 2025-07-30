import abc
from abc import ABC, abstractmethod
from typing import Any

class BaseExecutor(ABC, metaclass=abc.ABCMeta):
    """Base class for agent executors.

    This concrete base class provides a default structure for executing agents.

    Attributes:
        None. This is an abstract base class that defines an interface.
    """
    @abstractmethod
    def invoke(self, inputs: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Invoke the agent executor.

        Subclasses must implement this method with their specific implementation.

        Args:
            inputs: A dictionary of inputs for the executor.
            **kwargs: Additional keyword arguments for customizing execution behavior.

        Returns:
            A dictionary containing the execution result.
        """
    @abstractmethod
    async def ainvoke(self, inputs: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Asynchronously invoke the agent executor.

        Subclasses must implement this method with their specific implementation.

        Args:
            inputs: A dictionary of inputs for the executor.
            **kwargs: Additional keyword arguments for customizing execution behavior.

        Returns:
            A dictionary containing the execution result.
        """
