from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

class IEnv(ABC):
    """Interface contract for environment management operations."""

    @staticmethod
    @abstractmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves an environment variable's value.

        Args:
            key: Environment variable name
            default: Default value if key doesn't exist

        Returns:
            The parsed value or default if not found
        """
        pass

    @staticmethod
    @abstractmethod
    def set(key: str, value: str) -> bool:
        """
        Sets an environment variable.

        Args:
            key: Environment variable name
            value: Value to set

        Returns:
            True if successful, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def unset(key: str) -> bool:
        """
        Removes an environment variable.

        Args:
            key: Environment variable name

        Returns:
            True if successful, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def all() -> Dict[str, Any]:
        """
        Retrieves all environment variables.

        Returns:
            Dictionary of all key-value pairs
        """
        pass

    @staticmethod
    @abstractmethod
    def toJson() -> str:
        """
        Serializes environment to JSON.

        Returns:
            JSON string representation
        """
        pass

    @staticmethod
    @abstractmethod
    def toBase64() -> str:
        """
        Encodes environment to Base64.

        Returns:
            Base64 encoded string
        """
        pass