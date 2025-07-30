from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class ITestHistory(ABC):

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

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
        pass

    def resetDatabase(self) -> None:
        """
        Drop the `reportes` table, effectively clearing the report history.

        Raises
        ------
        RuntimeError
            If table deletion fails.
        """
        pass

    def close(self) -> None:
        """
        Close the SQLite database connection gracefully.
        """
        pass