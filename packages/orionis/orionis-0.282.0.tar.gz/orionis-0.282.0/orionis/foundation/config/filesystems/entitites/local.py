from dataclasses import asdict, dataclass, field
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Local:
    """
    Represents a local filesystem configuration.

    Attributes
    ----------
    path : str
        The absolute or relative path where local files are stored.
    """
    path: str = field(
        default="storage/app/private",
        metadata={
            "description": "The absolute or relative path where local files are stored.",
            "default": "storage/app/private",
        }
    )

    def __post_init__(self):
        """
        Post-initialization method to ensure the 'path' attribute is a non-empty string.
        - Raises:
            ValueError: If the 'path' is empty.
        """
        if not isinstance(self.path, str):
            raise OrionisIntegrityException("The 'path' attribute must be a string.")
        if not self.path.strip():
            raise OrionisIntegrityException("The 'path' attribute cannot be empty.")

    def toDict(self) -> dict:
        """
        Convert the object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the Dataclass object.
        """
        return asdict(self)
