# Import custom test case classes from the orionis.test.cases module
from orionis.test.cases.test_case import TestCase
from orionis.test.cases.test_sync import SyncTestCase
from orionis.test.cases.test_async import AsyncTestCase

# Import the custom TestResult entity
from orionis.test.entities.test_result import TestResult

# Import enums for execution mode and test status
from orionis.test.enums.test_mode import ExecutionMode
from orionis.test.enums.test_status import TestStatus

# Import custom exception for test failures
from orionis.test.exceptions.test_failure_exception import OrionisTestFailureException

# Import configuration and suite classes for organizing tests
from orionis.test.suites.test_suite import Configuration, TestSuite
from orionis.test.suites.test_unit import UnitTest

# Import standard unittest components for compatibility
from unittest import (
    TestLoader as UnittestTestLoader,
    TestSuite as UnittestTestSuite,
    TestResult as UnittestTestResult,
)

# Import mock classes for creating test doubles
from unittest.mock import (
    Mock as UnittestMock,
    MagicMock as UnittestMagicMock,
    patch as unittest_mock_patch,
)

# Define the public API of this module
__all__ = [
    "TestCase",
    "SyncTestCase",
    "AsyncTestCase",
    "TestResult",
    "ExecutionMode",
    "TestStatus",
    "OrionisTestFailureException",
    "Configuration",
    "TestSuite",
    "UnitTest",
    "UnittestTestLoader",
    "UnittestTestSuite",
    "UnittestTestResult",
    "UnittestMock",
    "UnittestMagicMock",
    "unittest_mock_patch",
]
