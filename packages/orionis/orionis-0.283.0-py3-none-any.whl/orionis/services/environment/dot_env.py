import os
import ast
import threading
from pathlib import Path
from typing import Any, Optional, Union
from dotenv import dotenv_values, load_dotenv, set_key, unset_key
from orionis.patterns.singleton.meta_class import Singleton

class DotEnv(metaclass=Singleton):
    """
    DotEnv is a singleton class for managing environment variables using a `.env` file.
    This class provides methods to load, get, set, unset, and list environment variables,
    with automatic serialization and deserialization of common Python data types.
    It ensures that changes to the `.env` file are reflected in the current process's
    environment variables and vice versa.
    """

    _lock = threading.RLock()

    def __init__(self, path: str = None) -> None:
        """
        Initializes the environment service by resolving the path to the `.env` file, ensuring its existence,
        and loading environment variables from it.
        Args:
            path (str, optional): The path to the `.env` file. If not provided, defaults to a `.env` file
                in the current working directory.
        Raises:
            OSError: If the `.env` file cannot be created when it does not exist.
        """

        with self._lock:
            if path:
                self._resolved_path = Path(path).expanduser().resolve()
            else:
                self._resolved_path = Path(os.getcwd()) / ".env"

            if not self._resolved_path.exists():
                self._resolved_path.touch()

            load_dotenv(self._resolved_path)

    def get(self, key: str, default: Optional[Any] = None, is_path:bool=False) -> Any:
        """
        Retrieve the value of an environment variable by key.

        This method first attempts to fetch the value from the dotenv file specified by
        `self._resolved_path`. If the key is not found in the dotenv file, it falls back
        to the system environment variables. If the key is not found in either location,
        the provided `default` value is returned.

        The returned value is parsed using the internal `__parseValue` method if found.

        Args:
            key (str): The name of the environment variable to retrieve.
            default (Optional[Any], optional): The value to return if the key is not found.
                Defaults to None.
            is_path (bool, optional): If True, the value is treated as a file path and backslashes are replaced with forward slashes.
                This is useful for Windows paths. Defaults to False.

        Returns:
            Any: The parsed value of the environment variable, or the default if not found.
        """
        with self._lock:
            value = dotenv_values(self._resolved_path).get(key)
            if value is None:
                value = os.getenv(key)
            return self.__parseValue(value, is_path) if value is not None else default

    def set(self, key: str, value: Union[str, int, float, bool, list, dict], is_path:bool=False) -> bool:
        """
        Sets an environment variable with the specified key and value.

        This method serializes the given value and updates both the .env file and the current process's environment variables.

        Args:
            key (str): The name of the environment variable to set.
            value (Union[str, int, float, bool, list, dict]): The value to assign to the environment variable. Supported types include string, integer, float, boolean, list, and dictionary.
            is_path (bool, optional): If True, the value is treated as a file path and backslashes are replaced with forward slashes.
            This is useful for Windows paths. Defaults to False.

        Returns:
            bool: True if the environment variable was successfully set.
        """

        with self._lock:
            serialized_value = self.__serializeValue(value, is_path)
            set_key(str(self._resolved_path), key, serialized_value)
            os.environ[key] = str(value)
            return True

    def unset(self, key: str) -> bool:
        """
        Removes the specified environment variable from both the .env file and the current process environment.

        Args:
            key (str): The name of the environment variable to unset.

        Returns:
            bool: True if the operation was successful.
        """
        with self._lock:
            unset_key(str(self._resolved_path), key)
            os.environ.pop(key, None)
            return True

    def all(self) -> dict:
        """
        Retrieves all environment variables from the resolved .env file.

        Returns:
            dict: A dictionary containing all environment variable key-value pairs,
                  with values parsed using the internal __parseValue method.
        """
        with self._lock:
            raw_values = dotenv_values(self._resolved_path)
            return {k: self.__parseValue(v) for k, v in raw_values.items()}

    def toJson(self) -> str:
        """
        Serializes all environment variables managed by this instance to a JSON-formatted string.

        Returns:
            str: A JSON string representation of all environment variables, formatted with indentation for readability.
        """
        import json
        with self._lock:
            return json.dumps(self.all(), indent=4)

    def toBase64(self) -> str:
        """
        Serializes all environment variables to a JSON string and encodes it in Base64.

        Returns:
            str: A Base64-encoded string representation of all environment variables.
        """
        import base64
        import json
        with self._lock:
            return base64.b64encode(json.dumps(self.all()).encode()).decode()

    def __parseValue(self, value: Any, is_path:bool=False) -> Any:
        """
        Parses and converts the input value to an appropriate Python data type.

        Args:
            value (Any): The value to parse and convert.

        Returns:
            Any: The parsed value, which may be of type None, bool, int, float, or the original string.
                - Returns None for None, empty strings, or strings like 'none', 'null', 'nan' (case-insensitive).
                - Returns a boolean for 'true'/'false' strings (case-insensitive).
                - Returns an int if the string represents an integer.
                - Returns a float if the string represents a float.
                - Attempts to evaluate the string as a Python literal (e.g., list, dict, tuple).
                - Returns the original string if no conversion is possible.
        """
        if value is None:
            return None

        if isinstance(value, (bool, int, float)):
            return value

        value_str = str(value).strip()
        if not value_str or value_str.lower() in {'none', 'null', 'nan'}:
            return None

        if value_str.lower() == 'true':
            return True

        if value_str.lower() == 'false':
            return False

        if is_path:
            return value_str.replace("\\", "/")

        try:
            if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
                return int(value_str)
        except Exception:
            pass

        try:
            float_val = float(value_str)
            if '.' in value_str or 'e' in value_str.lower():
                return float_val
        except Exception:
            pass

        try:
            return ast.literal_eval(value_str)
        except Exception:
            pass

        return value_str

    def __serializeValue(self, value: Any, is_path:bool=False) -> str:
        """
        Serializes a given value to a string suitable for storage in a .env file.

        Parameters:
            value (Any): The value to serialize. Supported types are None, str, bool, int, float, list, and dict.
            is_path (bool): If True, the value is treated as a file path and backslashes are replaced with forward slashes.
            This is useful for Windows paths.

        Returns:
            str: The serialized string representation of the value.

        Raises:
            ValueError: If a float value is in scientific notation.
            TypeError: If the value's type is not serializable for .env files.
        """
        if is_path:
            return str(value).replace("\\", "/")

        if value is None:
            return "None"

        if isinstance(value, str):
            return value

        if isinstance(value, bool):
            return str(value).lower()

        if isinstance(value, int):
            return str(value)

        if isinstance(value, float):
            value = str(value)
            if 'e' in value or 'E' in value:
                raise ValueError('scientific notation is not supported, use a string instead')
            return value

        if isinstance(value, (list, dict)):
            return repr(value)

        if hasattr(value, '__dict__'):
            raise TypeError(f"Type {type(value).__name__} is not serializable for .env")

        if not isinstance(value, (list, dict, bool, int, float, str)):
            raise TypeError(f"Type {type(value).__name__} is not serializable for .env")

        if isinstance(value, (list, dict, bool, int, float, str)):
            if type(value).__module__ != "builtins" and not isinstance(value, str):
                raise TypeError(f"Type {type(value).__name__} is not serializable for .env")
            return repr(value) if not isinstance(value, str) else value

        raise TypeError(f"Type {type(value).__name__} is not serializable for .env")
