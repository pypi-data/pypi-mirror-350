from dataclasses import dataclass, field, asdict, fields
from orionis.foundation.config.logging.entities.channels import Channels
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Logging:
    """
    Represents the logging system configuration.

    Attributes
    ----------
    default : str
        The default logging channel to use.
    channels : Channels
        A collection of available logging channels.
    """
    default: str = field(
        default="stack",
        metadata={
            "description": "The default logging channel to use.",
            "default": "stack",
        }
    )
    channels: Channels = field(
        default_factory=Channels,
        metadata={
            "description": "A collection of available logging channels.",
            "default": "Channels()",
        }
    )

    def __post_init__(self):
        """
        Validates the types of the attributes after initialization.
        """
        options = [field.name for field in fields(Channels)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        if not isinstance(self.channels, Channels):
            raise OrionisIntegrityException(
                "The 'channels' property must be an instance of Channels."
            )

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.
        """
        return asdict(self)
