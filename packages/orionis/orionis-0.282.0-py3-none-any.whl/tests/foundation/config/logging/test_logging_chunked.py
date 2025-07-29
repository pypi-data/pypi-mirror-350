from orionis.foundation.config.logging.entities.chunked import Chunked
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigChunked(TestCase):
    """
    Test cases for the Chunked logging configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Chunked instance is created with correct default values.
        Verifies default path, level, mb_size and files match expected values.
        """
        chunked = Chunked()
        self.assertEqual(chunked.path, "storage/log/application.log")
        self.assertEqual(chunked.level, Level.INFO.value)
        self.assertEqual(chunked.mb_size, 10)
        self.assertEqual(chunked.files, 5)

    async def testPathValidation(self):
        """
        Test path attribute validation.
        Verifies that empty or non-string paths raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            Chunked(path="")
        with self.assertRaises(OrionisIntegrityException):
            Chunked(path=123)
        try:
            Chunked(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.
        """
        # Test string level
        chunked = Chunked(level="debug")
        self.assertEqual(chunked.level, Level.DEBUG.value)

        # Test int level
        chunked = Chunked(level=Level.WARNING.value)
        self.assertEqual(chunked.level, Level.WARNING.value)

        # Test enum level
        chunked = Chunked(level=Level.ERROR)
        self.assertEqual(chunked.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Chunked(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Chunked(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(level=[])

    async def testMbSizeValidation(self):
        """
        Test mb_size attribute validation with different input formats.
        """
        # Test valid integer values
        try:
            Chunked(mb_size=1)
            Chunked(mb_size=100)
        except OrionisIntegrityException:
            self.fail("Valid mb_size should not raise exception")

        # Test string formats
        chunked = Chunked(mb_size="10MB")
        self.assertEqual(chunked.mb_size, 10)

        chunked = Chunked(mb_size="10240KB")
        self.assertEqual(chunked.mb_size, 10)

        chunked = Chunked(mb_size="10485760B")
        self.assertEqual(chunked.mb_size, 10)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Chunked(mb_size=0)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(mb_size=-1)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(mb_size="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Chunked(mb_size="10GB")

    async def testFilesValidation(self):
        """
        Test files attribute validation.
        """
        # Test valid values
        try:
            Chunked(files=1)
            Chunked(files=10)
        except OrionisIntegrityException:
            self.fail("Valid files count should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Chunked(files=0)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(files=-1)
        with self.assertRaises(OrionisIntegrityException):
            Chunked(files="5")

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.
        """
        chunked = Chunked(path="  logs/app.log  ", level="  debug  ")
        self.assertEqual(chunked.path, "  logs/app.log  ")
        self.assertEqual(chunked.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        """
        chunked = Chunked()
        chunked_dict = chunked.toDict()

        self.assertIsInstance(chunked_dict, dict)
        self.assertEqual(chunked_dict['path'], "storage/log/application.log")
        self.assertEqual(chunked_dict['level'], Level.INFO.value)
        self.assertEqual(chunked_dict['mb_size'], 10)
        self.assertEqual(chunked_dict['files'], 5)

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary.
        """
        custom_chunked = Chunked(
            path="custom/logs/app.log",
            level="warning",
            mb_size=20,
            files=10
        )
        chunked_dict = custom_chunked.toDict()
        self.assertEqual(chunked_dict['path'], "custom/logs/app.log")
        self.assertEqual(chunked_dict['level'], Level.WARNING.value)
        self.assertEqual(chunked_dict['mb_size'], 20)
        self.assertEqual(chunked_dict['files'], 10)

    async def testHashability(self):
        """
        Test that Chunked maintains hashability due to unsafe_hash=True.
        """
        chunked1 = Chunked()
        chunked2 = Chunked()
        chunked_set = {chunked1, chunked2}

        self.assertEqual(len(chunked_set), 1)

        custom_chunked = Chunked(path="custom.log")
        chunked_set.add(custom_chunked)
        self.assertEqual(len(chunked_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Chunked enforces keyword-only initialization.
        """
        with self.assertRaises(TypeError):
            Chunked("path.log", "info", 10, 5)