from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestOrionisIntegrityException(TestCase):
    """
    Test cases for the OrionisIntegrityException class.
    """

    async def testExceptionInitialization(self):
        """
        Test that OrionisIntegrityException is properly initialized with a message.
        Verifies that the exception stores and returns the provided message correctly.
        """
        test_msg = "Test integrity violation message"
        exception = OrionisIntegrityException(test_msg)
        self.assertEqual(str(exception), f"OrionisIntegrityException: {test_msg}")
        self.assertEqual(exception.args[0], test_msg)

    async def testExceptionInheritance(self):
        """
        Test that OrionisIntegrityException properly inherits from Exception.
        Verifies the exception hierarchy is correctly implemented.
        """
        exception = OrionisIntegrityException("Test")
        self.assertIsInstance(exception, Exception)
        self.assertTrue(issubclass(OrionisIntegrityException, Exception))

    async def testExceptionStringRepresentation(self):
        """
        Test the string representation of OrionisIntegrityException.
        Verifies the __str__ method returns the expected format.
        """
        test_msg = "Configuration validation failed"
        exception = OrionisIntegrityException(test_msg)
        self.assertEqual(str(exception), f"OrionisIntegrityException: {test_msg}")

    async def testExceptionWithEmptyMessage(self):
        """
        Test OrionisIntegrityException with an empty message.
        Verifies the exception handles empty messages correctly.
        """
        exception = OrionisIntegrityException("")
        self.assertEqual(str(exception), "OrionisIntegrityException: ")

    async def testExceptionWithNonStringMessage(self):
        """
        Test OrionisIntegrityException with non-string message types.
        Verifies the exception converts non-string messages to strings.
        """
        # Test with integer
        exception = OrionisIntegrityException(123)
        self.assertEqual(str(exception), "OrionisIntegrityException: 123")

        # Test with list
        exception = OrionisIntegrityException(["error1", "error2"])
        self.assertEqual(str(exception), "OrionisIntegrityException: ['error1', 'error2']")

    async def testExceptionRaiseAndCatch(self):
        """
        Test raising and catching OrionisIntegrityException.
        Verifies the exception can be properly raised and caught.
        """
        test_msg = "Test exception handling"
        try:
            raise OrionisIntegrityException(test_msg)
        except OrionisIntegrityException as e:
            self.assertEqual(str(e), f"OrionisIntegrityException: {test_msg}")
        except Exception:
            self.fail("OrionisIntegrityException should be caught by its specific handler")

    async def testExceptionChaining(self):
        """
        Test exception chaining with OrionisIntegrityException.
        Verifies the exception works correctly in chained exception scenarios.
        """
        try:
            try:
                raise ValueError("Original error")
            except ValueError as ve:
                raise OrionisIntegrityException("Wrapper error") from ve
        except OrionisIntegrityException as oe:
            self.assertIsInstance(oe.__cause__, ValueError)
            self.assertEqual(str(oe.__cause__), "Original error")