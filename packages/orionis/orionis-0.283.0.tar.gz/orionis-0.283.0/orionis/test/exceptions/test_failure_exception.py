import unittest

class OrionisTestFailureException(Exception):
    """
    OrionisTestFailureException is a custom exception class used to handle test failures and errors
    in a structured manner. It provides detailed information about the failed and errored tests,
    including their IDs and formatted error messages.
    Methods:
        __init__(result: unittest.TestResult):
        __str__() -> str:
    """

    def __init__(self, result: unittest.TestResult):
        """
        Initializes the exception with details about failed and errored tests.
        Args:
            result (unittest.TestResult): The test result object containing information
                about test failures and errors.
        Attributes:
            failed_tests (list): A list of IDs for tests that failed.
            errored_tests (list): A list of IDs for tests that encountered errors.
            error_messages (list): A list of formatted error messages for failed and errored tests.
            text (str): A formatted string summarizing the test failures and errors.
        Raises:
            Exception: An exception with a message summarizing the number of failed
                and errored tests along with their details.
        """
        failed_tests = [test.id() for test, _ in result.failures]
        errored_tests = [test.id() for test, _ in result.errors]

        error_messages = []
        for test in failed_tests:
            error_messages.append(f"Test Fail: {test}")
        for test in errored_tests:
            error_messages.append(f"Test Error: {test}")

        text = "\n".join(error_messages)

        super().__init__(f"{len(failed_tests) + len(errored_tests)} test(s) failed or errored:\n{text}")

    def __str__(self) -> str:
        """
        Returns a string representation of the exception.

        The string includes the exception name and the first argument
        passed to the exception, providing a clear description of the
        test failure.

        Returns:
            str: A formatted string describing the exception.
        """
        return f"{self.__class__.__name__}: {self.args[0]}"
