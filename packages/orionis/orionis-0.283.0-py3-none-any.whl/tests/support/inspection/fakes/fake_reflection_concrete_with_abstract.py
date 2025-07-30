import abc
from typing import Any, Dict, List

class AbstractService(abc.ABC):
    """
    Abstract interface for service-like behavior.

    Methods
    -------
    process(data: str) -> bool
        Perform processing on input data.

    reset() -> None
        Reset the internal state of the service.

    configure(options: Dict[str, Any]) -> None
        Apply configuration settings to the service.

    get_logs(limit: int = 10) -> List[str]
        Retrieve a limited number of log messages.

    Properties
    ----------
    status : str
        Current status of the service.
    """

    @abc.abstractmethod
    def process(self, data: str) -> bool:
        """Perform processing on input data."""
        pass

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the internal state of the service."""
        pass

    @abc.abstractmethod
    def configure(self, options: Dict[str, Any]) -> None:
        """Apply configuration settings to the service."""
        pass

    @abc.abstractmethod
    def get_logs(self, limit: int = 10) -> List[str]:
        """Retrieve a limited number of log messages."""
        pass

    @property
    @abc.abstractmethod
    def status(self) -> str:
        """Current status of the service."""
        pass

class PartiallyImplementedService:
    """
    A partial implementation of AbstractService.

    This class mimics the interface but lacks some methods/properties,
    making it useful for testing reflection-based validation.
    """

    def process(self, data: str) -> bool:
        """Basic processing implementation."""
        return bool(data)

    def get_logs(self, limit: int = 10) -> List[str]:
        """Return a fixed list of logs (mock implementation)."""
        return [f"log {i}" for i in range(limit)]

    # ❌ Missing: reset()
    # ❌ Missing: configure()
    # ❌ Missing: status (property)

    def extra(self) -> str:
        """An extra method not part of the abstract interface."""
        return "Just extra"

    version: str = "1.0"