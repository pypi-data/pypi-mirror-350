from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass(frozen=True, kw_only=True)
class AbstractClassAttributes:
    """
    A class to represent the attributes of an entity.
    """
    public: Dict[str, Any] = field()
    private: Dict[str, Any] = field()
    protected: Dict[str, Any] = field()

    def __post_init__(self):
        """
        Post-initialization method to validate attribute types.

        Ensures that the 'public', 'private', and 'protected' attributes of the instance
        are all dictionaries. Raises a TypeError if any of these attributes are not of type dict.

        Raises:
            TypeError: If 'public', 'private', or 'protected' is not a dict.
        """
        if not isinstance(self.public, dict):
            raise TypeError(
                f"Invalid type for 'public' attribute in {self.__class__.__name__}: "
                f"expected 'dict', got '{type(self.public).__name__}'."
            )
        if not isinstance(self.private, dict):
            raise TypeError(
                f"Invalid type for 'private' attribute in {self.__class__.__name__}: "
                f"expected 'dict', got '{type(self.private).__name__}'."
            )
        if not isinstance(self.protected, dict):
            raise TypeError(
                f"Invalid type for 'protected' attribute in {self.__class__.__name__}: "
                f"expected 'dict', got '{type(self.protected).__name__}'."
            )