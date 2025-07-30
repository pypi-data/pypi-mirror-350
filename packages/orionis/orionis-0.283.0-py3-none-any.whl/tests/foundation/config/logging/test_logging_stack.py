from orionis.foundation.config.logging.entities.stack import Stack
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigStack(TestCase):
    """
    Test cases for the Stack logging configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Stack instance is created with correct default values.
        Verifies default path and level match expected values from class definition.
        """
        stack = Stack()
        self.assertEqual(stack.path, "storage/log/application.log")
        self.assertEqual(stack.level, Level.INFO.value)

    async def testPathValidation(self):
        """
        Test path attribute validation.
        Verifies that empty or non-string paths raise exceptions.
        """
        # Test empty path
        with self.assertRaises(OrionisIntegrityException):
            Stack(path="")
        # Test non-string path
        with self.assertRaises(OrionisIntegrityException):
            Stack(path=123)
        # Test valid path
        try:
            Stack(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.
        Verifies string, int and enum level values are properly handled.
        """
        # Test string level
        stack = Stack(level="debug")
        self.assertEqual(stack.level, Level.DEBUG.value)

        # Test int level
        stack = Stack(level=Level.WARNING.value)
        self.assertEqual(stack.level, Level.WARNING.value)

        # Test enum level
        stack = Stack(level=Level.ERROR)
        self.assertEqual(stack.level, Level.ERROR.value)

        # Test invalid string level
        with self.assertRaises(OrionisIntegrityException):
            Stack(level="invalid")

        # Test invalid int level
        with self.assertRaises(OrionisIntegrityException):
            Stack(level=999)

        # Test invalid type
        with self.assertRaises(OrionisIntegrityException):
            Stack(level=[])

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.
        Verifies whitespace is preserved in path and trimmed in level strings.
        """
        # Test path with whitespace
        spaced_path = "  logs/app.log  "
        stack = Stack(path=spaced_path)
        self.assertEqual(stack.path, spaced_path)

        # Test level with whitespace
        stack = Stack(level="  debug  ")
        self.assertEqual(stack.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies both path and level are correctly included in dictionary.
        """
        stack = Stack()
        stack_dict = stack.toDict()

        self.assertIsInstance(stack_dict, dict)
        self.assertEqual(stack_dict['path'], "storage/log/application.log")
        self.assertEqual(stack_dict['level'], Level.INFO.value)

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary representation.
        """
        custom_stack = Stack(
            path="custom/logs/app.log",
            level="warning"
        )
        stack_dict = custom_stack.toDict()
        self.assertEqual(stack_dict['path'], "custom/logs/app.log")
        self.assertEqual(stack_dict['level'], Level.WARNING.value)

    async def testHashability(self):
        """
        Test that Stack maintains hashability due to unsafe_hash=True.
        Verifies Stack instances can be used in sets and as dictionary keys.
        """
        stack1 = Stack()
        stack2 = Stack()
        stack_set = {stack1, stack2}

        self.assertEqual(len(stack_set), 1)

        custom_stack = Stack(path="custom.log")
        stack_set.add(custom_stack)
        self.assertEqual(len(stack_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Stack enforces keyword-only initialization.
        """
        with self.assertRaises(TypeError):
            Stack("path.log", "info")