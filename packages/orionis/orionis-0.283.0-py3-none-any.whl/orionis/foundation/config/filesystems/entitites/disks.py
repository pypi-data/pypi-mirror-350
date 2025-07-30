from dataclasses import asdict, dataclass, field
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.filesystems.entitites.aws import S3
from orionis.foundation.config.filesystems.entitites.public import Public
from orionis.foundation.config.filesystems.entitites.local import Local

@dataclass(unsafe_hash=True, kw_only=True)
class Disks:
    """
    Represents the configuration for different filesystem disks.
    Attributes:
        local (Local): The disk configuration for local file storage.
        public (Public): The disk configuration for public file storage.
    Methods:
        __post_init__():
            Ensures the 'path' attribute is a non-empty Path object and of the correct type.
        toDict() -> dict:
            Converts the Disks object into a dictionary representation.
    """

    local : Local = field(
        default_factory=Local,
        metadata={
            "description": "The absolute or relative path where local files are stored.",
            "default": "Local()",
        }
    )

    public : Public = field(
        default_factory=Public,
        metadata={
            "description": "The absolute or relative path where public files are stored.",
            "default": "Public()",
        }
    )

    aws : S3 = field(
        default_factory=S3,
        metadata={
            "description": "The configuration for AWS S3 storage.",
            "default": "S3()",
        }
    )

    def __post_init__(self):
        """
        Post-initialization method to ensure the 'path' attribute is a non-empty Path object.
        - Converts 'path' to a Path instance if it is not already.
        - Raises:
            ValueError: If the 'path' is empty after conversion.
        """

        if not isinstance(self.local, Local):
            raise OrionisIntegrityException("The 'local' attribute must be a Local object.")

        if not isinstance(self.public, Public):
            raise OrionisIntegrityException("The 'public' attribute must be a Public object.")

        if not isinstance(self.aws, S3):
            raise OrionisIntegrityException("The 'aws' attribute must be a S3 object.")

    def toDict(self) -> dict:
        """
        Convert the object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the Dataclass object.
        """
        return asdict(self)
