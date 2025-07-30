from dataclasses import asdict, dataclass, field
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class File:
    """
    Represents a file configuration entity for storing outgoing emails.
    Attributes:
        path (str): The file path where outgoing emails are stored.
    Methods:
        __post_init__():
            Validates that the 'path' attribute is a non-empty string.
            Raises:
                OrionisIntegrityException: If 'path' is not a non-empty string.
        toDict() -> dict:
            Serializes the File instance to a dictionary.
    """

    path: str = field(
        default="storage/mail",
        metadata={"description": "The file path where outgoing emails are stored."}
    )

    def __post_init__(self):
        """
        Post-initialization method to validate the 'path' attribute.

        Raises:
            OrionisIntegrityException: If 'path' is not a non-empty string.
        """
        if not isinstance(self.path, str) or self.path.strip() == "":
            raise OrionisIntegrityException("The 'path' attribute must be a non-empty string.")

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.

        Returns:
            dict: A dictionary containing all the fields of the instance.
        """
        return asdict(self)
