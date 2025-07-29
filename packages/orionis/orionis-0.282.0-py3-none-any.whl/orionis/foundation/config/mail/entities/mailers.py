from dataclasses import asdict, dataclass, field
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.mail.entities.file import File
from orionis.foundation.config.mail.entities.smtp import Smtp

@dataclass(unsafe_hash=True, kw_only=True)
class Mailers:
    """
    Represents the mail transport configurations for the application.
    Attributes:
        smtp (Smtp): The SMTP configuration used for sending emails.
        file (File): The file-based mail transport configuration.
    Methods:
        __post_init__():
            Validates that the 'smtp' and 'file' attributes are instances of their respective classes.
            Raises:
                OrionisIntegrityException: If 'smtp' is not a Smtp object or 'file' is not a File object.
        toDict() -> dict:
            Serializes the Mailers instance to a dictionary.
    """

    smtp: Smtp = field(
        default_factory=Smtp,
        metadata={"description": "The SMTP configuration used for sending emails."}
    )

    file: File = field(
        default_factory=File,
        metadata={"description": "The file-based mail transport configuration."}
    )

    def __post_init__(self):
        """
        Post-initialization method to validate attribute types.

        Ensures that the 'smtp' attribute is an instance of the Smtp class and the 'file' attribute is an instance of the File class.
        Raises:
            OrionisIntegrityException: If 'smtp' is not a Smtp object or 'file' is not a File object.
        """

        if not isinstance(self.smtp, Smtp):
            raise OrionisIntegrityException("The 'smtp' attribute must be a Smtp object.")

        if not isinstance(self.file, File):
            raise OrionisIntegrityException("The 'file' attribute must be a File object.")

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.

        Returns:
            dict: A dictionary containing all the fields of the instance.
        """
        return asdict(self)
