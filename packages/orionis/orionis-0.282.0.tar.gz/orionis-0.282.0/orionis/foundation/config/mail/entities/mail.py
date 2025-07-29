from dataclasses import asdict, dataclass, field, fields
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.mail.entities.mailers import Mailers

@dataclass(unsafe_hash=True, kw_only=True)
class Mail:
    """
    Represents the mail configuration entity.
    Attributes:
        default (str): The default mailer transport to use.
        mailers (Mailers): The available mail transport configurations.
    Methods:
        __post_init__():
            Validates the integrity of the Mail instance after initialization.
            Raises OrionisIntegrityException if any attribute is invalid.
        toDict() -> dict:
            Serializes the Mail instance to a dictionary.
    """

    default: str = field(
        default="smtp",
        metadata={"description": "The default mailer transport to use."}
    )

    mailers: Mailers = field(
        default_factory=Mailers,
        metadata={"description": "The available mail transport configurations."}
    )

    def __post_init__(self):
        """
        Post-initialization method to validate the 'default' and 'mailers' attributes.
        Ensures that:
        - The 'default' attribute is a string and matches one of the available mailer options.
        - The 'mailers' attribute is an instance of the Mailers class.
        Raises:
            OrionisIntegrityException: If 'default' is not a valid string option or if 'mailers' is not a Mailers object.
        """

        options = [f.name for f in fields(Mailers)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        if not isinstance(self.mailers, Mailers):
            raise OrionisIntegrityException("The 'mailers' attribute must be a Mailers object.")

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.

        Returns:
            dict: A dictionary containing all the fields of the instance.
        """
        return asdict(self)
