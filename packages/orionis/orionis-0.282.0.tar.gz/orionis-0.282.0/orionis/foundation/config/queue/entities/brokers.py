
from dataclasses import asdict, dataclass, field
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.queue.entities.database import Database

@dataclass(unsafe_hash=True, kw_only=True)
class Brokers:
    """
    Represents the configuration for queue brokers.
    Attributes:
        sync (bool): Indicates if the sync broker is enabled. Defaults to True.
        database (Database): The configuration for the database-backed queue. Defaults to a new Database instance.
    Methods:
        __post_init__():
            Validates and normalizes the properties after initialization.
            Ensures 'sync' is a boolean and 'database' is an instance of Database.
    """

    sync: bool = field(
        default=True,
        metadata={
            "description": "Indicates if the sync broker is enabled.",
            "default": True
        }
    )

    database: Database = field(
        default_factory=Database,
        metadata={
            "description": "The configuration for the database-backed queue.",
            "default": "Database()"
        }
    )

    def __post_init__(self):
        """
        Post-initialization validation for the Brokers entity.
        Validates and normalizes the following properties:
        - sync: Must be a boolean.
        - database: Must be an instance of the Database class.
        """
        if not isinstance(self.sync, bool):
            raise OrionisIntegrityException("sync must be a boolean.")

        if not isinstance(self.database, Database):
            raise OrionisIntegrityException("database must be an instance of the Database class.")

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.

        Returns:
            dict: A dictionary containing all the fields of the instance.
        """
        return asdict(self)
