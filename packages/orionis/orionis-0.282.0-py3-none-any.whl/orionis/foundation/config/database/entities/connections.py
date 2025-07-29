from dataclasses import asdict, dataclass, field
from orionis.foundation.config.database.entities.mysql import MySQL
from orionis.foundation.config.database.entities.oracle import Oracle
from orionis.foundation.config.database.entities.pgsql import PGSQL
from orionis.foundation.config.database.entities.sqlite import SQLite
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Connections:
    """
    Data class to represent all database connections used by the application.

    Attributes
    ----------
    sqlite : Sqlite
        Configuration for the SQLite database connection.
    mysql : MySQL
        Configuration for the MySQL database connection.
    pgsql : Pgsql
        Configuration for the PostgreSQL database connection.
    oracle : Oracle
        Configuration for the Oracle database connection.
    """
    sqlite: SQLite = field(
        default_factory=SQLite,
        metadata={
            "description": "SQLite database connection configuration",
            "default": "SQLite()"
        }
    )

    mysql: MySQL = field(
        default_factory=MySQL,
        metadata={
            "description": "MySQL database connection configuration",
            "default": "MySQL()"
        }
    )

    pgsql: PGSQL = field(
        default_factory=PGSQL,
        metadata={
            "description": "PostgreSQL database connection configuration",
            "default": "PGSQL()"
        }
    )

    oracle: Oracle = field(
        default_factory=Oracle,
        metadata={
            "description": "Oracle database connection configuration",
            "default": "Oracle()"
        }
    )

    def __post_init__(self):
        """
        Post-initialization method to validate the types of database connection attributes.
        Ensures that the attributes `sqlite`, `mysql`, `pgsql`, and `oracle` are instances of their respective classes.
        Raises:
            OrionisIntegrityException: If any attribute is not an instance of its expected class.
        """
        if not isinstance(self.sqlite, SQLite):
            raise OrionisIntegrityException(
                f"Invalid type for 'sqlite': expected 'Sqlite', got '{type(self.sqlite).__name__}'."
            )

        if not isinstance(self.mysql, MySQL):
            raise OrionisIntegrityException(
                f"Invalid type for 'mysql': expected 'Mysql', got '{type(self.mysql).__name__}'."
            )

        if not isinstance(self.pgsql, PGSQL):
            raise OrionisIntegrityException(
                f"Invalid type for 'pgsql': expected 'Pgsql', got '{type(self.pgsql).__name__}'."
            )

        if not isinstance(self.oracle, Oracle):
            raise OrionisIntegrityException(
                f"Invalid type for 'oracle': expected 'Oracle', got '{type(self.oracle).__name__}'."
            )

    def toDict(self) -> dict:
        """
        Convert the object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the Dataclass object.
        """
        return asdict(self)