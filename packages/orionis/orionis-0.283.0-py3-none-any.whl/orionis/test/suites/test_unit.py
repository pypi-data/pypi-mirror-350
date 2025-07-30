import io
import re
import time
import inspect
import traceback
import unittest
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from contextlib import redirect_stdout, redirect_stderr
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from orionis.console.output.console import Console
from orionis.test.logs.history import TestHistory
from orionis.test.suites.contracts.test_unit import IUnitTest
from orionis.test.entities.test_result import TestResult
from orionis.test.enums.test_mode import ExecutionMode
from orionis.test.enums.test_status import TestStatus
from orionis.test.exceptions.test_failure_exception import OrionisTestFailureException
from rich.live import Live
import os

class UnitTest(IUnitTest):
    """
    UnitTest is a comprehensive testing utility class designed to facilitate the discovery, configuration,
    and execution of unit tests. It provides features for sequential and parallel test execution,
    customizable verbosity, fail-fast behavior, and rich output formatting using the `rich` library.
        loader (unittest.TestLoader): The test loader used to discover and load tests.
        suite (unittest.TestSuite): The test suite containing the discovered tests.
    """

    def __init__(self) -> None:
        """
        Initializes the test unit with default configurations.

        Attributes:
            loader (unittest.TestLoader): The test loader used to discover tests.
            suite (unittest.TestSuite): The test suite to hold the discovered tests.
            test_results (List[TestResult]): A list to store the results of executed tests.
            start_time (float): The start time of the test execution.
            print_result (bool): Flag to determine whether to print test results.
            verbosity (int): The verbosity level for test output.
            execution_mode (str): The mode of test execution (e.g., SEQUENTIAL or PARALLEL).
            max_workers (int): The maximum number of workers for parallel execution.
            fail_fast (bool): Flag to stop execution on the first failure.
            rich_console (RichConsole): Console for rich text output.
            orionis_console (Console): Console for standard output.
            discovered_tests (List): A list to store discovered test cases.
            width_table (int): The width of the table for displaying results.
            throw_exception (bool): Flag to determine whether to throw exceptions on test failures.
        """
        self.loader = unittest.TestLoader()
        self.suite = unittest.TestSuite()
        self.test_results: List[TestResult] = []
        self.start_time: float = 0.0
        self.print_result: bool = True
        self.verbosity: int = 2
        self.execution_mode: str = ExecutionMode.SEQUENTIAL.value
        self.max_workers: int = 4
        self.fail_fast: bool = False
        self.rich_console = RichConsole()
        self.orionis_console = Console()
        self.discovered_tests: List = []
        self.width_output_component: int = int(self.rich_console.width * 0.75)
        self.throw_exception: bool = False
        self.persistent: bool = False
        self.base_path: str = "tests"

    def configure(
            self,
            verbosity: int = None,
            execution_mode: str | ExecutionMode = None,
            max_workers: int = None,
            fail_fast: bool = None,
            print_result: bool = None,
            throw_exception: bool = False,
            persistent: bool = False
        ) -> 'UnitTest':
        """
        Configures the UnitTest instance with the specified parameters.

        Parameters:
            verbosity (int, optional): The verbosity level for test output. Defaults to None.
            execution_mode (ExecutionMode, optional): The mode in which the tests will be executed. Defaults to None.
            max_workers (int, optional): The maximum number of workers to use for parallel execution. Defaults to None.
            fail_fast (bool, optional): Whether to stop execution upon the first failure. Defaults to None.
            print_result (bool, optional): Whether to print the test results after execution. Defaults to None.
            throw_exception (bool, optional): Whether to throw an exception if any test fails. Defaults to False.
            persistent (bool, optional): Whether to persist the test results in a database. Defaults to False.

        Returns:
            UnitTest: The configured UnitTest instance.
        """
        if verbosity is not None:
            self.verbosity = verbosity

        if execution_mode is not None and isinstance(execution_mode, ExecutionMode):
            self.execution_mode = execution_mode.value
        else:
            self.execution_mode = execution_mode

        if max_workers is not None:
            self.max_workers = max_workers

        if fail_fast is not None:
            self.fail_fast = fail_fast

        if print_result is not None:
            self.print_result = print_result

        if throw_exception is not None:
            self.throw_exception = throw_exception

        if persistent is not None:
            self.persistent = persistent

        return self

    def discoverTestsInFolder(
        self,
        folder_path: str,
        base_path: str = "tests",
        pattern: str = "test_*.py",
        test_name_pattern: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> 'UnitTest':
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
        try:
            self.base_path = base_path

            full_path = Path(base_path) / folder_path
            if not full_path.exists():
                raise ValueError(f"Test folder not found: {full_path}")

            tests = self.loader.discover(
                start_dir=str(full_path),
                pattern=pattern,
                top_level_dir=None
            )

            if test_name_pattern:
                tests = self._filterTestsByName(tests, test_name_pattern)

            if tags:
                tests = self._filterTestsByTags(tests, tags)

            if not list(tests):
                raise ValueError(f"No tests found in '{full_path}' matching pattern '{pattern}'")

            self.suite.addTests(tests)

            test_count = len(list(self._flattenTestSuite(tests)))
            self.discovered_tests.append({
                "folder": str(full_path),
                "test_count": test_count,
            })

            return self

        except ImportError as e:
            raise ValueError(f"Error importing tests from '{full_path}': {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error discovering tests: {str(e)}")

    def discoverTestsInModule(self, module_name: str, test_name_pattern: Optional[str] = None) -> 'UnitTest':
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
        try:

            tests = self.loader.loadTestsFromName(module_name)

            if test_name_pattern:
                tests = self._filterTestsByName(tests, test_name_pattern)

            self.suite.addTests(tests)

            test_count = len(list(self._flattenTestSuite(tests)))
            self.discovered_tests.append({
                "module": module_name,
                "test_count": test_count,
            })

            return self
        except ImportError as e:
            raise ValueError(f"Error importing module '{module_name}': {str(e)}")

    def _startMessage(self) -> None:
        """
        Displays a formatted message indicating the start of the test suite execution.
        This method prints details about the test suite, including the total number of tests,
        the execution mode (parallel or sequential), and the start time. The message is styled
        and displayed using the `rich` library.
        Attributes:
            print_result (bool): Determines whether the message should be printed.
            suite (TestSuite): The test suite containing the tests to be executed.
            max_workers (int): The number of workers used in parallel execution mode.
            execution_mode (ExecutionMode): The mode of execution (parallel or sequential).
            orionis_console (Console): The console object for handling standard output.
            rich_console (Console): The rich console object for styled output.
            width_table (int): The calculated width of the message panel for formatting.
        Raises:
            AttributeError: If required attributes are not set before calling this method.
        """
        if self.print_result:
            test_count = len(list(self._flattenTestSuite(self.suite)))
            mode_text = f"[stat]Parallel with {self.max_workers} workers[/stat]" if self.execution_mode == ExecutionMode.PARALLEL.value else "Sequential"
            textlines = [
                f"[bold]Total Tests:[/bold] [dim]{test_count}[/dim]",
                f"[bold]Mode:[/bold] [dim]{mode_text}[/dim]",
                f"[bold]Started at:[/bold] [dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
            ]

            self.orionis_console.newLine()
            self.rich_console.print(
                Panel(
                    '\n'.join(textlines),
                    border_style="blue",
                    title="🧪 Orionis Framework - Component Test Suite",
                    title_align="center",
                    width=self.width_output_component,
                    padding=(0, 1)
                )
            )
            self.orionis_console.newLine()

    def run(self, print_result: bool = None, throw_exception: bool = None) -> Dict[str, Any]:
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
        if print_result is not None:
            self.print_result = print_result
        if throw_exception is not None:
            self.throw_exception = throw_exception

        self.start_time = time.time()
        self._startMessage()

        # Elegant "running" message using Rich Panel
        running_panel = Panel(
            "[bold yellow]⏳ Running tests...[/bold yellow]\n[dim]This may take a few seconds. Please wait...[/dim]",
            border_style="yellow",
            title="In Progress",
            title_align="left",
            width=self.width_output_component,
            padding=(1, 2)
        )

        # Print the panel and keep a reference to the live display
        with Live(running_panel, console=self.rich_console, refresh_per_second=4, transient=True):

            # Setup output capture
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()

            # Execute tests based on selected mode
            if self.execution_mode == ExecutionMode.PARALLEL.value:
                result = self._runTestsInParallel(output_buffer, error_buffer)
            else:
                result = self._runTestsSequentially(output_buffer, error_buffer)

        # Process results
        execution_time = time.time() - self.start_time
        summary = self._generateSummary(result, execution_time)

        # Print captured output
        if self.print_result:
            self._displayResults(summary, result)

        # Print Execution Time
        if not result.wasSuccessful() and self.throw_exception:
            raise OrionisTestFailureException(result)

        return summary

    def _runTestsSequentially(self, output_buffer: io.StringIO, error_buffer: io.StringIO) -> unittest.TestResult:
        """
        Executes the test suite sequentially, capturing the output and error streams.
        Args:
            output_buffer (io.StringIO): A buffer to capture the standard output during test execution.
            error_buffer (io.StringIO): A buffer to capture the standard error during test execution.
        Returns:
            unittest.TestResult: The result of the test suite execution, containing information about
            passed, failed, and skipped tests.
        """
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            runner = unittest.TextTestRunner(
                stream=output_buffer,
                verbosity=self.verbosity,
                failfast=self.fail_fast,
                resultclass=self._createCustomResultClass()
            )
            result = runner.run(self.suite)

        return result

    def _runTestsInParallel(self, output_buffer: io.StringIO, error_buffer: io.StringIO) -> unittest.TestResult:
        """
        Execute tests in parallel using a thread pool.
        This method runs all test cases in the provided test suite concurrently,
        utilizing a thread pool for parallel execution. It collects and combines
        the results of all test cases into a single result object.
        Args:
            output_buffer (io.StringIO): A buffer to capture standard output during test execution.
            error_buffer (io.StringIO): A buffer to capture standard error during test execution.
        Returns:
            unittest.TestResult: A combined result object containing the outcomes of all executed tests.
        Notes:
            - The method uses a custom result class to aggregate test results.
            - If `fail_fast` is enabled and a test fails, the remaining tests are canceled.
            - Minimal output is produced for individual test runs during parallel execution.
        """
        """Execute tests in parallel with thread pooling."""
        test_cases = list(self._flattenTestSuite(self.suite))

        # Create a custom result instance to collect all results
        result_class = self._createCustomResultClass()
        combined_result = result_class(io.StringIO(), descriptions=True, verbosity=self.verbosity)

        def run_single_test(test):
            """Helper function to run a single test and return its result."""
            runner = unittest.TextTestRunner(
                stream=io.StringIO(),
                verbosity=0,  # Minimal output for parallel runs
                failfast=False,
                resultclass=result_class
            )
            return runner.run(unittest.TestSuite([test]))

        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(run_single_test, test) for test in test_cases]

                for future in as_completed(futures):
                    test_result = future.result()
                    self._mergeTestResults(combined_result, test_result)

                    if self.fail_fast and not combined_result.wasSuccessful():
                        for f in futures:
                            f.cancel()
                        break

        return combined_result

    def _mergeTestResults(self, combined_result: unittest.TestResult, individual_result: unittest.TestResult) -> None:
        """
        Merges the results of two unittest.TestResult objects into a combined result.
        This method updates the combined_result object by adding the test run counts,
        failures, errors, skipped tests, expected failures, and unexpected successes
        from the individual_result object. Additionally, it merges any custom test
        results stored in the 'test_results' attribute, if present.
        Args:
            combined_result (unittest.TestResult): The TestResult object to which the
                results will be merged.
            individual_result (unittest.TestResult): The TestResult object containing
                the results to be merged into the combined_result.
        Returns:
            None
        """
        combined_result.testsRun += individual_result.testsRun
        combined_result.failures.extend(individual_result.failures)
        combined_result.errors.extend(individual_result.errors)
        combined_result.skipped.extend(individual_result.skipped)
        combined_result.expectedFailures.extend(individual_result.expectedFailures)
        combined_result.unexpectedSuccesses.extend(individual_result.unexpectedSuccesses)

        # Merge our custom test results
        if hasattr(individual_result, 'test_results'):
            if not hasattr(combined_result, 'test_results'):
                combined_result.test_results = []
            combined_result.test_results.extend(individual_result.test_results)

    def _createCustomResultClass(self) -> type:
        """
        Creates a custom test result class that extends `unittest.TextTestResult` to provide enhanced
        functionality for tracking test execution details, including timings, statuses, and error information.
        Returns:
            type: A dynamically created class `EnhancedTestResult` that overrides methods to handle
            test results, including success, failure, error, and skipped tests. The class collects
            detailed information about each test, such as execution time, error messages, traceback,
            and file path.
        The `EnhancedTestResult` class includes:
            - `startTest`: Records the start time of a test.
            - `stopTest`: Calculates and stores the elapsed time for a test.
            - `addSuccess`: Logs details of a successful test.
            - `addFailure`: Logs details of a failed test, including error message and traceback.
            - `addError`: Logs details of a test that encountered an error, including error message and traceback.
            - `addSkip`: Logs details of a skipped test, including the reason for skipping.
        Note:
            This method uses the `this` reference to access the outer class's methods, such as `_extractErrorInfo`.
        """
        this = self

        class EnhancedTestResult(unittest.TextTestResult):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.test_results = []
                self._test_timings = {}
                self._current_test_start = None

            def startTest(self, test):
                self._current_test_start = time.time()
                super().startTest(test)

            def stopTest(self, test):
                elapsed = time.time() - self._current_test_start
                self._test_timings[test] = elapsed
                super().stopTest(test)

            def addSuccess(self, test):
                super().addSuccess(test)
                elapsed = self._test_timings.get(test, 0.0)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.PASSED,
                        execution_time=elapsed,
                        class_name=test.__class__.__name__,
                        method=getattr(test, "_testMethodName", None),
                        module=getattr(test, "__module__", None),
                        file_path=inspect.getfile(test.__class__),
                        doc_string=getattr(getattr(test, test._testMethodName, None), "__doc__", None),
                    )
                )

            def addFailure(self, test, err):
                super().addFailure(test, err)
                elapsed = self._test_timings.get(test, 0.0)
                tb_str = ''.join(traceback.format_exception(*err))
                file_path, clean_tb = this._extractErrorInfo(tb_str)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.FAILED,
                        execution_time=elapsed,
                        error_message=str(err[1]),
                        traceback=clean_tb,
                        class_name=test.__class__.__name__,
                        method=getattr(test, "_testMethodName", None),
                        module=getattr(test, "__module__", None),
                        file_path=inspect.getfile(test.__class__),
                        doc_string=getattr(getattr(test, test._testMethodName, None), "__doc__", None),
                    )
                )

            def addError(self, test, err):
                super().addError(test, err)
                elapsed = self._test_timings.get(test, 0.0)
                tb_str = ''.join(traceback.format_exception(*err))
                file_path, clean_tb = this._extractErrorInfo(tb_str)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.ERRORED,
                        execution_time=elapsed,
                        error_message=str(err[1]),
                        traceback=clean_tb,
                        class_name=test.__class__.__name__,
                        method=getattr(test, "_testMethodName", None),
                        module=getattr(test, "__module__", None),
                        file_path=inspect.getfile(test.__class__),
                        doc_string=getattr(getattr(test, test._testMethodName, None), "__doc__", None),
                    )
                )

            def addSkip(self, test, reason):
                super().addSkip(test, reason)
                elapsed = self._test_timings.get(test, 0.0)
                self.test_results.append(
                    TestResult(
                        id=test.id(),
                        name=str(test),
                        status=TestStatus.SKIPPED,
                        execution_time=elapsed,
                        error_message=reason,
                        class_name=test.__class__.__name__,
                        method=getattr(test, "_testMethodName", None),
                        module=getattr(test, "__module__", None),
                        file_path=inspect.getfile(test.__class__),
                        doc_string=getattr(getattr(test, test._testMethodName, None), "__doc__", None),
                    )
                )

        return EnhancedTestResult

    def _generateSummary(self, result: unittest.TestResult, execution_time: float) -> Dict[str, Any]:
        """
        Generates a summary of the test results, including details about each test, 
        performance data, and overall statistics.
        Args:
            result (unittest.TestResult): The result object containing details of the test execution.
            execution_time (float): The total execution time of the test suite in seconds.
        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - "total_tests" (int): The total number of tests executed.
                - "passed" (int): The number of tests that passed.
                - "failed" (int): The number of tests that failed.
                - "errors" (int): The number of tests that encountered errors.
                - "skipped" (int): The number of tests that were skipped.
                - "total_time" (float): The total execution time of the test suite.
                - "success_rate" (float): The percentage of tests that passed.
                - "test_details" (List[Dict[str, Any]]): A list of dictionaries containing details about each test:
                    - "id" (str): The unique identifier of the test.
                    - "class" (str): The class name of the test.
                    - "method" (str): The method name of the test.
                    - "status" (str): The status of the test (e.g., "PASSED", "FAILED").
                    - "execution_time" (float): The execution time of the test in seconds.
                    - "error_message" (str): The error message if the test failed or errored.
                    - "traceback" (str): The traceback information if the test failed or errored.
                    - "file_path" (str): The file path of the test.
        """
        test_details = []

        for test_result in result.test_results:
            rst: TestResult = test_result
            test_details.append({
                'id': rst.id,
                'class': rst.class_name,
                'method': rst.method,
                'status': rst.status.name,
                'execution_time': float(rst.execution_time),
                'error_message': rst.error_message,
                'traceback': rst.traceback,
                'file_path': rst.file_path,
                'doc_string': rst.doc_string
            })

        passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
        success_rate = (passed / result.testsRun * 100) if result.testsRun > 0 else 100.0

        # Create a summary report
        report = {
            "total_tests": result.testsRun,
            "passed": passed,
            "failed": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
            "total_time": float(execution_time),
            "success_rate": success_rate,
            "test_details": test_details,
            "timestamp": datetime.now().isoformat()
        }

        # Handle persistence of the report
        if self.persistent:
            self._persistTestResults(report)

        # Return the summary
        return {
            "total_tests": result.testsRun,
            "passed": passed,
            "failed": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
            "total_time": float(execution_time),
            "success_rate": success_rate,
            "test_details": test_details
        }

    def _persistTestResults(self, summary: Dict[str, Any]) -> None:
        """
        Persists the test results in a SQLite database.
        Args:
            summary (Dict[str, Any]): A dictionary containing the test summary data.
                Expected keys in the dictionary:
                    - "total_tests" (int): Total number of tests executed.
                    - "passed" (int): Number of tests that passed.
                    - "failed" (int): Number of tests that failed.
                    - "errors" (int): Number of tests that encountered errors.
                    - "skipped" (int): Number of tests that were skipped.
                    - "total_time" (float): Total duration of the test run in seconds.
                    - "success_rate" (float): Percentage of tests that passed.
        Returns:
            None
        """
        full_path = os.path.abspath(os.path.join(os.getcwd(), self.base_path))
        log = TestHistory(full_path)
        try:
            log.createTableIfNotExists()
            log.insertReport(summary)
        finally:
            log.close()

    def _printSummaryTable(self, summary: Dict[str, Any]) -> None:
        """
        Prints a summary table of test results using the Rich library.

        Args:
            summary (Dict[str, Any]): A dictionary containing the test summary data.
                Expected keys in the dictionary:
                    - "total_tests" (int): Total number of tests executed.
                    - "passed" (int): Number of tests that passed.
                    - "failed" (int): Number of tests that failed.
                    - "errors" (int): Number of tests that encountered errors.
                    - "skipped" (int): Number of tests that were skipped.
                    - "total_time" (float): Total duration of the test run in seconds.
                    - "success_rate" (float): Percentage of tests that passed.

        Returns:
            None
        """
        table = Table(
            show_header=True,
            header_style="bold white",
            width=self.width_output_component,
            border_style="blue"
        )
        table.add_column("Total", justify="center")
        table.add_column("Passed", justify="center")
        table.add_column("Failed", justify="center")
        table.add_column("Errors", justify="center")
        table.add_column("Skipped", justify="center")
        table.add_column("Duration", justify="center")
        table.add_column("Success Rate", justify="center")
        table.add_row(
            str(summary["total_tests"]),
            str(summary["passed"]),
            str(summary["failed"]),
            str(summary["errors"]),
            str(summary["skipped"]),
            f"{summary['total_time']:.2f}s",
            f"{summary['success_rate']:.2f}%"
        )
        self.rich_console.print(table)
        self.orionis_console.newLine()

    def _filterTestsByName(self, suite: unittest.TestSuite, pattern: str) -> unittest.TestSuite:
        """
        Filters the tests in a given test suite based on a specified name pattern.
        Args:
            suite (unittest.TestSuite): The test suite containing the tests to filter.
            pattern (str): A regular expression pattern to match test names.
        Returns:
            unittest.TestSuite: A new test suite containing only the tests that match the pattern.
        Raises:
            ValueError: If the provided pattern is not a valid regular expression.
        Notes:
            - The method flattens the input test suite to iterate over individual tests.
            - A test is included in the filtered suite if its ID matches the provided regex pattern.
        """
        filtered_suite = unittest.TestSuite()
        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid test name pattern: {str(e)}")

        for test in self._flattenTestSuite(suite):
            if regex.search(test.id()):
                filtered_suite.addTest(test)

        return filtered_suite

    def _filterTestsByTags(self, suite: unittest.TestSuite, tags: List[str]) -> unittest.TestSuite:
        """
        Filters a unittest TestSuite to include only tests that match the specified tags.
        This method iterates through all tests in the provided TestSuite and checks
        for a `__tags__` attribute either on the test method or the test case class.
        If any of the specified tags match the tags associated with the test, the test
        is added to the filtered TestSuite.
        Args:
            suite (unittest.TestSuite): The original TestSuite containing all tests.
            tags (List[str]): A list of tags to filter the tests by.
        Returns:
            unittest.TestSuite: A new TestSuite containing only the tests that match
            the specified tags.
        """
        filtered_suite = unittest.TestSuite()
        tag_set = set(tags)

        for test in self._flattenTestSuite(suite):
            # Get test method if this is a TestCase instance
            test_method = getattr(test, test._testMethodName, None)

            # Check for tags attribute on the test method
            if hasattr(test_method, '__tags__'):
                method_tags = set(getattr(test_method, '__tags__'))
                if tag_set.intersection(method_tags):
                    filtered_suite.addTest(test)
            # Also check on the test case class
            elif hasattr(test, '__tags__'):
                class_tags = set(getattr(test, '__tags__'))
                if tag_set.intersection(class_tags):
                    filtered_suite.addTest(test)

        return filtered_suite

    def _flattenTestSuite(self, suite: unittest.TestSuite) -> List[unittest.TestCase]:
        """
        Flattens a nested unittest.TestSuite into a list of individual unittest.TestCase instances.
        This method recursively traverses the given TestSuite, extracting all TestCase instances
        while avoiding duplicates. It ensures that each TestCase appears only once in the resulting list.
        Args:
            suite (unittest.TestSuite): The TestSuite to be flattened.
        Returns:
            List[unittest.TestCase]: A list of unique TestCase instances extracted from the TestSuite.
        """
        tests = []
        seen = set()

        def _flatten(item):
            if isinstance(item, unittest.TestSuite):
                for sub_item in item:
                    _flatten(sub_item)
            elif item not in seen:
                seen.add(item)
                tests.append(item)

        _flatten(suite)
        return tests

    def _sanitizeTraceback(self, test_path: str, traceback_test: str) -> str:
        """
        Sanitizes a traceback string to extract and display the most relevant parts
        related to a specific test file.
        Args:
            test_path (str): The file path of the test file being analyzed.
            traceback_test (str): The full traceback string to be sanitized.
        Returns:
            str: A sanitized traceback string containing only the relevant parts
            related to the test file. If no relevant parts are found, the full
            traceback is returned. If the traceback is empty, a default message
            "No traceback available" is returned.
        """
        if not traceback_test:
            return "No traceback available"

        # Try to extract the test file name
        file_match = re.search(r'([^/\\]+)\.py', test_path)
        file_name = file_match.group(1) if file_match else None

        if not file_name:
            return traceback_test

        # Process traceback to show most relevant parts
        lines = traceback_test.splitlines()
        relevant_lines = []
        found_test_file = False if file_name in traceback_test else True

        for line in lines:
            if file_name in line and not found_test_file:
                found_test_file = True
            if found_test_file:
                if 'File' in line:
                    relevant_lines.append(line.strip())
                elif line.strip() != '':
                    relevant_lines.append(line)

        # If we didn't find the test file, return the full traceback
        if not relevant_lines:
            return traceback_test

        return '\n'.join(relevant_lines)

    def _displayResults(self, summary: Dict[str, Any], result: unittest.TestResult) -> None:
        """
        Displays the results of the test execution, including a summary table and detailed
        information about failed or errored tests grouped by their test classes.
        Args:
            summary (Dict[str, Any]): A dictionary containing the summary of the test execution,
                including test details, statuses, and execution times.
            result (unittest.TestResult): The result object containing information about the
                test run, including successes, failures, and errors.
        Behavior:
            - Prints a summary table of the test results.
            - Groups failed and errored tests by their test class and displays them in a
              structured format using panels.
            - For each failed or errored test, displays the traceback in a syntax-highlighted
              panel with additional metadata such as the test method name and execution time.
            - Uses different icons and border colors to distinguish between failed and errored tests.
            - Calls a finishing message method after displaying all results.
        """
        self._printSummaryTable(summary)

        # Group failures and errors by test class
        failures_by_class = {}
        for test in summary["test_details"]:
            if test["status"] in (TestStatus.FAILED.name, TestStatus.ERRORED.name):
                class_name = test["class"]
                if class_name not in failures_by_class:
                    failures_by_class[class_name] = []
                failures_by_class[class_name].append(test)

        # Display grouped failures
        for class_name, tests in failures_by_class.items():

            class_panel = Panel.fit(f"[bold]{class_name}[/bold]", border_style="red", padding=(0, 2))
            self.rich_console.print(class_panel)

            for test in tests:
                traceback_str = self._sanitizeTraceback(test['file_path'], test['traceback'])
                syntax = Syntax(
                    traceback_str,
                    lexer="python",
                    line_numbers=False,
                    background_color="default",
                    word_wrap=True,
                    theme="monokai"
                )

                icon = "❌" if test["status"] == TestStatus.FAILED.name else "💥"
                border_color = "yellow" if test["status"] == TestStatus.FAILED.name else "red"

                if test['execution_time'] == 0:
                    test['execution_time'] = 0.001

                panel = Panel(
                    syntax,
                    title=f"{icon} {test['method']}",
                    subtitle=f"Duration: {test['execution_time']:.3f}s",
                    border_style=border_color,
                    title_align="left",
                    padding=(1, 1),
                    subtitle_align="right",
                    width=self.width_output_component
                )
                self.rich_console.print(panel)
                self.orionis_console.newLine()

        self._finishMessage(summary)

    def _extractErrorInfo(self, traceback_str: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts error information from a traceback string.
        This method processes a traceback string to extract the file path of the
        Python file where the error occurred and cleans up the traceback by
        removing framework internals and irrelevant noise.
        Args:
            traceback_str (str): The traceback string to process.
        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing:
                - The file path of the Python file where the error occurred, or None if not found.
                - The cleaned-up traceback string, or the original traceback string if no cleanup was performed.
        """
        # Extract file path
        file_matches = re.findall(r'File ["\'](.*?.py)["\']', traceback_str)
        file_path = file_matches[-1] if file_matches else None

        # Clean up traceback by removing framework internals and noise
        tb_lines = traceback_str.split('\n')
        clean_lines = []
        relevant_lines_started = False

        for line in tb_lines:
            # Skip framework internal lines
            if any(s in line for s in ['unittest/', 'lib/python', 'site-packages']):
                continue

            # Start capturing when we hit the test file
            if file_path and file_path in line and not relevant_lines_started:
                relevant_lines_started = True

            if relevant_lines_started:
                clean_lines.append(line)

        clean_tb = '\n'.join(clean_lines) if clean_lines else traceback_str

        return file_path, clean_tb

    def _finishMessage(self, summary: Dict[str, Any]) -> None:
        """
        Displays a summary message for the test suite execution if result printing is enabled.
        Args:
            summary (Dict[str, Any]): A dictionary containing the test suite summary,
                including keys such as 'failed', 'errors', and 'total_time'.
        Behavior:
            - If `self.print_result` is False, the method returns without displaying anything.
            - Constructs a message indicating the total execution time of the test suite.
            - Displays a status icon (✅ for success, ❌ for failure) based on the presence of
              failures or errors in the test suite.
            - Formats and prints the message within a styled panel using the `rich` library.
        """
        if not self.print_result:
            return

        status_icon = "✅" if (summary['failed'] + summary['errors']) == 0 else "❌"
        msg = f"Test suite completed in {summary['total_time']:.2f} seconds"
        self.rich_console.print(
            Panel(
                msg,
                border_style="blue",
                title=f"{status_icon} Test Suite Finished",
                title_align='left',
                width=self.width_output_component,
                padding=(0, 1)
            )
        )
        self.rich_console.print()

    def getTestNames(self) -> List[str]:
        """
        Retrieves a list of test names from the test suite.

        This method flattens the test suite and extracts the unique identifier
        (`id`) of each test case.

        Returns:
            List[str]: A list of test names (unique identifiers) from the test suite.
        """
        return [test.id() for test in self._flattenTestSuite(self.suite)]

    def getTestCount(self) -> int:
        """
        Calculate the total number of tests in the test suite.

        This method flattens the test suite structure and counts the total
        number of individual test cases.

        Returns:
            int: The total number of test cases in the test suite.
        """
        return len(list(self._flattenTestSuite(self.suite)))

    def clearTests(self) -> None:
        """
        Clears the current test suite by reinitializing it to an empty `unittest.TestSuite`.

        This method is used to reset the test suite, removing any previously added tests.
        """
        self.suite = unittest.TestSuite()