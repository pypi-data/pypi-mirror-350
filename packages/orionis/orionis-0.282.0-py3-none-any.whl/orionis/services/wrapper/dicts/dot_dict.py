from typing import Any, Optional, Dict

class DotDict(dict):
    """
    A dictionary subclass that allows attribute-style access to keys, with full support for nested dictionaries.
    Nested dicts are automatically converted to DotDict instances, enabling recursive dot notation.
    Missing keys return None instead of raising AttributeError or KeyError.
    """

    __slots__ = ()

    def __getattr__(self, key: str) -> Optional[Any]:
        """
        Retrieve the value associated with the given key as an attribute.
        If the value is a dictionary (but not already a DotDict), it is converted to a DotDict and updated in-place.
        Returns None if the key does not exist.
        Args:
            key (str): The attribute name to retrieve.
        Returns:
            Optional[Any]: The value associated with the key, converted to DotDict if applicable, or None if the key is not found.
        """

        try:
            value = self[key]
            if isinstance(value, dict) and not isinstance(value, DotDict):
                value = DotDict(value)
                self[key] = value
            return value
        except KeyError:
            return None

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets an attribute on the DotDict instance.

        If the value assigned is a dictionary (but not already a DotDict), it is automatically converted into a DotDict.
        The attribute is stored as a key-value pair in the underlying dictionary.

        Args:
            key (str): The attribute name to set.
            value (Any): The value to assign to the attribute. If it's a dict, it will be converted to a DotDict.

        """
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        self[key] = value

    def __delattr__(self, key: str) -> None:
        """
        Deletes the attribute with the specified key from the dictionary.

        Args:
            key (str): The name of the attribute to delete.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'") from e

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Retrieve the value associated with the given key, returning a default value if the key is not found.

        If the retrieved value is a plain dictionary (not a DotDict), it is converted to a DotDict,
        stored back in the dictionary, and then returned.

        Args:
            key (str): The key to look up in the dictionary.
            default (Optional[Any], optional): The value to return if the key is not found. Defaults to None.

        Returns:
            Optional[Any]: The value associated with the key, converted to a DotDict if it is a dict,
            or the default value if the key is not present.
        """
        value = super().get(key, default)
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
            self[key] = value
        return value

    def export(self) -> Dict[str, Any]:
        """
        Recursively exports the contents of the DotDict as a standard dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the DotDict, where any nested DotDict instances
            are also converted to dictionaries via their own export method.
        """
        return {k: v.export() if isinstance(v, DotDict) else v for k, v in self.items()}

    def copy(self) -> 'DotDict':
        """
        Create a deep copy of the DotDict instance.

        Returns:
            DotDict: A new DotDict object with recursively copied contents. 
            Nested DotDict and dict instances are also copied to ensure no shared references.
        """
        return DotDict({k: v.copy() if isinstance(v, DotDict) else (DotDict(v) if isinstance(v, dict) else v)
                        for k, v in self.items()})

    def __repr__(self) -> str:
        """
        Return a string representation of the DotDict instance.

        This method overrides the default __repr__ implementation to provide a more informative
        string that includes the class name 'DotDict' and the representation of the underlying dictionary.

        Returns:
            str: A string representation of the DotDict object.
        """
        return f"DotDict({super().__repr__()})"