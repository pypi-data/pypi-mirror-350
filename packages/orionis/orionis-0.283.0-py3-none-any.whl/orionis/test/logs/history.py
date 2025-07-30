import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from contextlib import closing
from orionis.services.environment.env import Env
from orionis.test.logs.contracts.history import ITestHistory

class TestHistory(ITestHistory):
    """
    A utility class for managing test execution reports using a local SQLite database.

    Attributes
    ----------
    TABLE_NAME : str
        The name of the database table where reports are stored.
    DB_NAME : str
        The filename of the SQLite database.
    FIELDS : List[str]
        List of expected keys in the report dictionary.
    _conn : sqlite3.Connection or None
        SQLite database connection instance.
    """

    TABLE_NAME = "reportes"
    DB_NAME = "tests.sqlite"
    FIELDS = [
        "json", "total_tests", "passed", "failed", "errors",
        "skipped", "total_time", "success_rate", "timestamp"
    ]

    def __init__(self, test_db_path: Optional[str] = None) -> None:
        """
        Initializes the class instance, setting up the path to the test database.
        Parameters:
            test_db_path (Optional[str]): Optional path to the test database file or directory. If a directory is provided, the database file name is appended. If not provided, the method checks the 'TEST_DB_PATH' environment variable, or defaults to a database file in the current file's directory.
        Behavior:
            - Resolves the database path to an absolute path.
            - Ensures the parent directory for the database exists.
            - Stores the resolved database path in the 'TEST_DB_PATH' environment variable.
            - Prepares the instance for database connection initialization.
        """

        if test_db_path:

            # Resolve the provided test_db_path to an absolute path
            db_path = Path(test_db_path).resolve()

            # If the provided path is a directory, append the database name
            if db_path.is_dir():
                db_path = db_path / self.DB_NAME

        else:

            # Check if the TEST_DB_PATH environment variable is set
            env_path = Env.get(
                key="TEST_DB_PATH",
                default=None,
                is_path=True
            )

            # If the environment variable is set, resolve it to an absolute path
            if env_path:
                db_path = Path(env_path).resolve()
                if db_path.is_dir():
                    db_path = db_path / self.DB_NAME
            else:
                db_path = Path(__file__).parent / self.DB_NAME

        # Ensure directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Store the absolute string path in the environment
        Env.set(
            key="TEST_DB_PATH",
            value=str(db_path),
            is_path=True
        )

        # Initialize the database connection.
        self._conn: Optional[sqlite3.Connection] = None

    def __connect(self) -> None:
        """
        Establishes a connection to the SQLite database using the path specified in the
        'TEST_DB_PATH' environment variable. If the environment variable is not set,
        raises a ConnectionError. If a connection error occurs during the attempt to
        connect, raises a ConnectionError with the error details.
        Raises:
            ConnectionError: If the database path is not set or if a connection error occurs.
        """

        if self._conn is None:

            # Check if the TEST_DB_PATH environment variable is set
            db_path = Env.get(
                key="TEST_DB_PATH",
                default=None,
                is_path=True
            )

            # If not set, raise an error
            if not db_path:
                raise ConnectionError("Database path is not set in environment variables.")

            # Try to connect to the SQLite database
            try:
                self._conn = sqlite3.connect(db_path)
            except sqlite3.Error as e:
                raise ConnectionError(f"Database connection error: {e}")

    def createTableIfNotExists(self) -> None:
        """
        Creates the history table in the database if it does not already exist.
        This method establishes a connection to the database and attempts to create a table
        with the schema defined by `self.TABLE_NAME`. The table includes columns for test
        results and metadata such as total tests, passed, failed, errors, skipped, total time,
        success rate, and timestamp. If the table already exists, no changes are made.
        Raises a RuntimeError if the table creation fails due to a database error.
        """

        self.__connect()
        try:
            with closing(self._conn.cursor()) as cursor:
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        json TEXT NOT NULL,
                        total_tests INTEGER,
                        passed INTEGER,
                        failed INTEGER,
                        errors INTEGER,
                        skipped INTEGER,
                        total_time REAL,
                        success_rate REAL,
                        timestamp TEXT
                    )
                ''')
            self._conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")

    def insertReport(self, report: Dict) -> None:
        """
        Inserts a test report into the database.
        Args:
            report (Dict): A dictionary containing the report data. Must include the following keys:
                - total_tests
                - passed
                - failed
                - errors
                - skipped
                - total_time
                - success_rate
                - timestamp
        Raises:
            ValueError: If any required report fields are missing.
            RuntimeError: If there is an error inserting the report into the database.
        """

        self.__connect()
        missing = [key for key in self.FIELDS if key != "json" and key not in report]
        if missing:
            raise ValueError(f"Missing report fields: {missing}")

        try:
            with closing(self._conn.cursor()) as cursor:
                cursor.execute(f'''
                    INSERT INTO {self.TABLE_NAME} (
                        json, total_tests, passed, failed, errors,
                        skipped, total_time, success_rate, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    json.dumps(report),
                    report["total_tests"],
                    report["passed"],
                    report["failed"],
                    report["errors"],
                    report["skipped"],
                    report["total_time"],
                    report["success_rate"],
                    report["timestamp"]
                ))
            self._conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert report: {e}")

    def getReportsWhere(self, where: Optional[str] = None, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Retrieves reports from the database table with optional WHERE conditions.
        Args:
            where (Optional[str]): SQL WHERE clause (without the 'WHERE' keyword).
            params (Optional[Tuple]): Parameters to substitute in the WHERE clause.
        Returns:
            List[Tuple]: A list of tuples, each representing a row from the reports table.
        Raises:
            RuntimeError: If there is an error retrieving the reports from the database.
        """
        self.__connect()
        try:
            with closing(self._conn.cursor()) as cursor:
                query = f'SELECT * FROM {self.TABLE_NAME}'
                if where:
                    query += f' WHERE {where}'
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to retrieve reports: {e}")

    def getReports(self) -> List[Tuple]:
        """
        Retrieves all reports from the database table.
        Returns:
            List[Tuple]: A list of tuples, each representing a row from the reports table.
        Raises:
            RuntimeError: If there is an error retrieving the reports from the database.
        """

        self.__connect()
        try:
            with closing(self._conn.cursor()) as cursor:
                cursor.execute(f'SELECT * FROM {self.TABLE_NAME}')
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to retrieve reports: {e}")

    def resetDatabase(self) -> None:
        """
        Resets the database by dropping the table specified by TABLE_NAME if it exists.
        This method establishes a connection to the database, attempts to drop the table,
        and commits the changes. If an error occurs during the process, a RuntimeError is raised.
        Raises:
            RuntimeError: If the database reset operation fails.
        """

        self.__connect()
        try:
            with closing(self._conn.cursor()) as cursor:
                cursor.execute(f'DROP TABLE IF EXISTS {self.TABLE_NAME}')
            self._conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to reset database: {e}")

    def close(self) -> None:
        """
        Closes the current database connection if it exists and sets the connection attribute to None.
        """

        if self._conn:
            self._conn.close()
            self._conn = None
