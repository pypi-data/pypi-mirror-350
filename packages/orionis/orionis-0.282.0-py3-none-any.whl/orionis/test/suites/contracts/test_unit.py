from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from orionis.test.enums.test_mode import ExecutionMode

class IUnitTest(ABC):
    """
    IUnitTest is an abstract base class that defines the contract for a unit testing interface within the Orionis framework.
    This interface provides methods for configuring the test runner, discovering tests in folders or modules, executing tests, retrieving test information, and managing the test suite. Implementations of this interface are expected to provide mechanisms for flexible test discovery, execution, and result handling, supporting features such as verbosity control, parallel execution, test filtering, and result reporting.
    """

    @abstractmethod
    def configure(
            self,
            verbosity: int = None,
            execution_mode: ExecutionMode = None,
            max_workers: int = None,
            fail_fast: bool = None,
            print_result: bool = None
        ):
        """
        Configures the UnitTest instance with the specified parameters.

        Parameters:
            verbosity (int, optional): The verbosity level for test output. Defaults to None.
            execution_mode (ExecutionMode, optional): The mode in which the tests will be executed. Defaults to None.
            max_workers (int, optional): The maximum number of workers to use for parallel execution. Defaults to None.
            fail_fast (bool, optional): Whether to stop execution upon the first failure. Defaults to None.
            print_result (bool, optional): Whether to print the test results after execution. Defaults to None.

        Returns:
            UnitTest: The configured UnitTest instance.
        """
        pass

    @abstractmethod
    def discoverTestsInFolder(
        self,
        folder_path: str,
        base_path: str = "tests",
        pattern: str = "test_*.py",
        test_name_pattern: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Discovers and loads unit tests from a specified folder.
        Args:
            folder_path (str): The relative path to the folder containing the tests.
            base_path (str, optional): The base directory where the test folder is located. Defaults to "tests".
            pattern (str, optional): The filename pattern to match test files. Defaults to "test_*.py".
            test_name_pattern (Optional[str], optional): A pattern to filter test names. Defaults to None.
            tags (Optional[List[str]], optional): A list of tags to filter tests. Defaults to None.
        Returns:
            UnitTest: The current instance of the UnitTest class with the discovered tests added.
        Raises:
            ValueError: If the test folder does not exist, no tests are found, or an error occurs during test discovery.
        """
        pass

    @abstractmethod
    def discoverTestsInModule(self, module_name: str, test_name_pattern: Optional[str] = None):
        """
        Discovers and loads tests from a specified module, optionally filtering them
        by a test name pattern, and adds them to the test suite.
        Args:
            module_name (str): The name of the module to discover tests from.
            test_name_pattern (Optional[str]): A pattern to filter test names. Only
                tests matching this pattern will be included. Defaults to None.
        Returns:
            UnitTest: The current instance of the UnitTest class, allowing method chaining.
        Raises:
            ValueError: If the specified module cannot be imported.
        """
        pass

    @abstractmethod
    def run(self, print_result: bool = None, throw_exception: bool = False) -> Dict[str, Any]:
        """
        Executes the test suite and processes the results.
        Args:
            print_result (bool, optional): If provided, overrides the instance's
                `print_result` attribute to determine whether to print the test results.
            throw_exception (bool, optional): If True, raises an exception if any
                test failures or errors are detected.
        Returns:
            Dict[str, Any]: A summary of the test execution, including details such as
            execution time, test results, and a timestamp.
        Raises:
            OrionisTestFailureException: If `throw_exception` is True and there are
            test failures or errors.
        """
        pass

    @abstractmethod
    def getTestNames(self) -> List[str]:
        """
        Retrieves a list of test names from the test suite.

        This method flattens the test suite and extracts the unique identifier
        (`id`) of each test case.

        Returns:
            List[str]: A list of test names (unique identifiers) from the test suite.
        """
        pass

    @abstractmethod
    def getTestCount(self) -> int:
        """
        Calculate the total number of tests in the test suite.

        This method flattens the test suite structure and counts the total
        number of individual test cases.

        Returns:
            int: The total number of test cases in the test suite.
        """
        pass

    @abstractmethod
    def clearTests(self) -> None:
        """
        Clears the current test suite by reinitializing it to an empty `unittest.TestSuite`.

        This method is used to reset the test suite, removing any previously added tests.
        """
        pass