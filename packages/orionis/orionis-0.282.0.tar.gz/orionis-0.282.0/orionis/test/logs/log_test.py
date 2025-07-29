import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from contextlib import closing
from orionis.services.environment.env import Env

class LogTest:
    """
    A utility class for managing test execution reports using a local SQLite database.

    This class provides methods to create a report table, insert new test reports,
    retrieve stored reports, reset the database, and close the connection.

    Each test report is stored as a JSON string along with individual statistical fields
    for easier filtering and analysis.

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

    def __init__(self, test_path_root: Optional[str] = None) -> None:
        """
        Initialize the LogTest instance and configure the database path.

        Parameters
        ----------
        test_path_root : str, optional
            Absolute or relative path to the directory where the SQLite file will be stored.
            If None, the path is derived from the current file location.

        Raises
        ------
        ValueError
            If the path cannot be resolved correctly.
        """
        if test_path_root:
            db_dir = Path(test_path_root).resolve()
        else:
            env_path = Env.get("TEST_PATH_ROOT")
            if env_path:
                db_dir = Path(env_path).resolve()
            else:
                db_dir = Path(__file__).resolve().parent

        dbPath = db_dir.joinpath(self.DB_NAME)
        Env.set("TEST_PATH_ROOT", str(dbPath).replace("\\", "\\\\"))
        self._conn: Optional[sqlite3.Connection] = None

    def __connect(self) -> None:
        """
        Establish a connection to the SQLite database.

        Raises
        ------
        ConnectionError
            If the connection to the database cannot be established.
        """
        if self._conn is None:
            try:
                self._conn = sqlite3.connect(Env.get("TEST_PATH_ROOT"))
            except sqlite3.Error as e:
                raise ConnectionError(f"Database connection error: {e}")

    def createTableIfNotExists(self) -> None:
        """
        Create the 'reportes' table if it does not already exist.

        The table includes fields for the full JSON report and individual
        statistics for querying and filtering.

        Raises
        ------
        RuntimeError
            If table creation fails due to a database error.
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
        Insert a test report into the database.

        Parameters
        ----------
        report : dict
            Dictionary containing test statistics and metadata.

            Required keys:
                - total_tests : int
                - passed : int
                - failed : int
                - errors : int
                - skipped : int
                - total_time : float
                - success_rate : float
                - timestamp : str (ISO format)

        Raises
        ------
        ValueError
            If required keys are missing from the report.
        RuntimeError
            If insertion into the database fails.
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

    def getReports(self) -> List[Tuple]:
        """
        Retrieve all test reports from the database.

        Returns
        -------
        List[Tuple]
            A list of tuples representing each row in the `reportes` table.

        Raises
        ------
        RuntimeError
            If retrieval fails due to a database error.
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
        Drop the `reportes` table, effectively clearing the report history.

        Raises
        ------
        RuntimeError
            If table deletion fails.
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
        Close the SQLite database connection gracefully.
        """
        if self._conn:
            self._conn.close()
            self._conn = None
