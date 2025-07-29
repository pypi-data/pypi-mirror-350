from orionis.services.environment.contracts.env import IEnv
from orionis.services.environment.dot_env import DotEnv
from typing import Any, Optional, Dict

def env(key: str, default: Any = None) -> Any:
    """
    Helper function to retrieve the value of an environment variable by key.
    """
    return DotEnv().get(key, default)

class Env(IEnv):
    """
    Env is a utility class that provides static methods for managing environment variables
    using the DotEnv class. It allows getting, setting, unsetting, listing, destroying,
    and serializing environment variables.
    """

    _dotenv_instance: Optional[DotEnv] = None

    @classmethod
    def _dotenv(cls) -> DotEnv:
        if cls._dotenv_instance is None:
            cls._dotenv_instance = DotEnv()
        return cls._dotenv_instance

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Retrieve the value of an environment variable by key.
        """
        return Env._dotenv().get(key, default)

    @staticmethod
    def set(key: str, value: str) -> bool:
        """
        Sets the value of an environment variable.
        """
        return Env._dotenv().set(key, value)

    @staticmethod
    def unset(key: str) -> bool:
        """
        Removes the specified environment variable from the environment.
        """
        return Env._dotenv().unset(key)

    @staticmethod
    def all() -> Dict[str, Any]:
        """
        Retrieve all environment variables from the DotEnv instance.
        """
        return Env._dotenv().all()

    @staticmethod
    def toJson() -> str:
        """
        Serializes the current environment variables managed by the DotEnv instance to a JSON-formatted string.
        """
        return Env._dotenv().toJson()

    @staticmethod
    def toBase64() -> str:
        """
        Converts the current environment variables to a Base64-encoded string.
        """
        return Env._dotenv().toBase64()
