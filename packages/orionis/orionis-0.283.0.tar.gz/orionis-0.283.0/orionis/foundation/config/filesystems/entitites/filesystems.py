from dataclasses import dataclass, field, asdict, fields
from orionis.foundation.config.filesystems.entitites.disks import Disks
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Filesystems:
    """
    Represents the filesystems configuration.

    Attributes
    ----------
    default : str
        The default filesystem disk to use.
    disks : Disks
        A collection of available filesystem disks.
    """

    default: str = field(
        default="local",
        metadata={
            "description": "The default filesystem disk to use.",
            "default": "local",
        }
    )

    disks: Disks = field(
        default_factory=Disks,
        metadata={
            "description": "A collection of available filesystem disks.",
            "default": "Disks()",
        }
    )

    def __post_init__(self):
        """
        Validates the types of the attributes after initialization.
        """
        options = [f.name for f in fields(Disks)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        if not isinstance(self.disks, Disks):
            raise OrionisIntegrityException(
                "The 'disks' property must be an instance of Disks."
            )

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.
        """
        return asdict(self)
