import os
import sys
from orionis.test.output.contracts.dumper import ITestDumper

class TestDumper(ITestDumper):
    """
    TestDumper provides utility methods for debugging and outputting information during test execution.
    This class implements methods to determine if an object is a test case instance and to output debugging
    information using the Debug class. It ensures that standard output and error streams are properly managed
    during debugging dumps, and captures the caller's file and line number for context.
    """

    def __isTestCaseClass(self, value):
        """
        Determines if the given value is an instance of a test case class.
        This method checks whether the provided value is an instance of one of the
        predefined test case classes: AsyncTestCase, TestCase, or SyncTestCase.
        If the value is None or an ImportError occurs during the import of the
        test case classes, the method returns False.
        Args:
            value: The object to be checked.
        Returns:
            bool: True if the value is an instance of AsyncTestCase, TestCase,
            or SyncTestCase; False otherwise.
        """
        try:
            if value is None:
                return False
            from orionis.test.cases.test_async import AsyncTestCase
            from orionis.test.cases.test_case import TestCase
            from orionis.test.cases.test_sync import SyncTestCase
            return isinstance(value, (AsyncTestCase, TestCase, SyncTestCase))
        except Exception:
            return False

    def dd(self, *args):
        """
        Dumps debugging information using the Debug class.
        This method captures the caller's file, method, and line number,
        and uses the Debug class to output debugging information.
        Args:
            *args: Variable length argument list to be dumped.
        """
        if not args:
            return

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        try:
            from orionis.console.dumper.dump_die import Debug

            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            caller_frame = sys._getframe(1)
            _file = os.path.abspath(caller_frame.f_code.co_filename)
            _line = caller_frame.f_lineno

            dumper = Debug(f"{_file}:{_line}")
            if self.__isTestCaseClass(args[0]):
                dumper.dd(*args[1:])
            else:
                dumper.dd(*args)
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def dump(self, *args):
        """
        Dumps debugging information using the Debug class.
        This method captures the caller's file, method, and line number,
        and uses the Debug class to output debugging information.
        Args:
            *args: Variable length argument list to be dumped.
        """
        if not args:
            return

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        try:
            from orionis.console.dumper.dump_die import Debug

            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            caller_frame = sys._getframe(1)
            _file = os.path.abspath(caller_frame.f_code.co_filename)
            _line = caller_frame.f_lineno

            dumper = Debug(f"{_file}:{_line}")
            if self.__isTestCaseClass(args[0]):
                dumper.dump(*args[1:])
            else:
                dumper.dump(*args)
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr