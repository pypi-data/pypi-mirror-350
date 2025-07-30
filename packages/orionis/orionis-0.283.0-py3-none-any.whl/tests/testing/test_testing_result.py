
from orionis.unittesting import TestCase, TestResult, TestStatus

class TestTestResult(TestCase):
    """
    Test cases for the TestResult dataclass.
    """

    async def testDefaultValues(self):
        """
        Test that TestResult initializes with correct default values for optional fields.

        Verifies that optional fields are None when not provided during initialization.
        """
        result = TestResult(
            id=1,
            name="Sample Test",
            status=TestStatus.PASSED,
            execution_time=0.5
        )
        self.assertIsNone(result.error_message)
        self.assertIsNone(result.traceback)
        self.assertIsNone(result.class_name)
        self.assertIsNone(result.method)
        self.assertIsNone(result.module)
        self.assertIsNone(result.file_path)

    async def testRequiredFields(self):
        """
        Test that TestResult requires all non-optional fields during initialization.

        Ensures that missing any required field raises a TypeError.
        """
        with self.assertRaises(TypeError):
            TestResult()  # Missing all required fields

        with self.assertRaises(TypeError):
            # Missing id
            TestResult(
                name="Sample Test",
                status=TestStatus.PASSED,
                execution_time=0.5
            )

    async def testImmutable(self):
        """
        Test that TestResult instances are immutable (frozen dataclass).

        Verifies that attribute modification after creation raises a FrozenInstanceError.
        """
        result = TestResult(
            id=1,
            name="Sample Test",
            status=TestStatus.PASSED,
            execution_time=0.5
        )
        with self.assertRaises(Exception):
            result.name = "Modified Name"

    async def testStatusValues(self):
        """
        Test that TestResult correctly handles all possible TestStatus values.

        Verifies that all enum values can be assigned to the status field.
        """
        for status in TestStatus:
            result = TestResult(
                id=1,
                name="Status Test",
                status=status,
                execution_time=0.1
            )
            self.assertEqual(result.status, status)

    async def testErrorFields(self):
        """
        Test that error-related fields are properly stored when provided.

        Verifies that error_message and traceback are stored correctly when provided.
        """
        error_msg = "Test failed"
        traceback = "Traceback info"
        result = TestResult(
            id=1,
            name="Failing Test",
            status=TestStatus.FAILED,
            execution_time=0.2,
            error_message=error_msg,
            traceback=traceback
        )
        self.assertEqual(result.error_message, error_msg)
        self.assertEqual(result.traceback, traceback)