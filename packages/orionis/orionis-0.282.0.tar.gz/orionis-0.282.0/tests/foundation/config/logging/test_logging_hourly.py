from orionis.foundation.config.logging.entities.hourly import Hourly
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigHourly(TestCase):
    """
    Test cases for the Hourly logging configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Hourly instance is created with correct default values.
        Verifies default path, level and retention_hours match expected values.
        """
        hourly = Hourly()
        self.assertEqual(hourly.path, "storage/log/application.log")
        self.assertEqual(hourly.level, Level.INFO.value)
        self.assertEqual(hourly.retention_hours, 24)

    async def testPathValidation(self):
        """
        Test path attribute validation.
        Verifies that empty or non-string paths raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            Hourly(path="")
        with self.assertRaises(OrionisIntegrityException):
            Hourly(path=123)
        try:
            Hourly(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.
        """
        # Test string level
        hourly = Hourly(level="debug")
        self.assertEqual(hourly.level, Level.DEBUG.value)

        # Test int level
        hourly = Hourly(level=Level.WARNING.value)
        self.assertEqual(hourly.level, Level.WARNING.value)

        # Test enum level
        hourly = Hourly(level=Level.ERROR)
        self.assertEqual(hourly.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Hourly(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Hourly(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(level=[])

    async def testRetentionHoursValidation(self):
        """
        Test retention_hours attribute validation.
        """
        # Test valid values
        try:
            Hourly(retention_hours=1)
            Hourly(retention_hours=168)
            Hourly(retention_hours=72)
        except OrionisIntegrityException:
            self.fail("Valid retention_hours should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours=0)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours=169)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours=-1)
        with self.assertRaises(OrionisIntegrityException):
            Hourly(retention_hours="24")

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.
        """
        hourly = Hourly(path="  logs/app.log  ", level="  debug  ")
        self.assertEqual(hourly.path, "  logs/app.log  ")
        self.assertEqual(hourly.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        """
        hourly = Hourly()
        hourly_dict = hourly.toDict()
        self.assertIsInstance(hourly_dict, dict)
        self.assertEqual(hourly_dict['path'], "storage/log/application.log")
        self.assertEqual(hourly_dict['level'], Level.INFO.value)
        self.assertEqual(hourly_dict['retention_hours'], 24)

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary.
        """
        custom_hourly = Hourly(
            path="custom/logs/app.log",
            level="warning",
            retention_hours=48
        )
        hourly_dict = custom_hourly.toDict()
        self.assertEqual(hourly_dict['path'], "custom/logs/app.log")
        self.assertEqual(hourly_dict['level'], Level.WARNING.value)
        self.assertEqual(hourly_dict['retention_hours'], 48)

    async def testHashability(self):
        """
        Test that Hourly maintains hashability due to unsafe_hash=True.
        """
        hourly1 = Hourly()
        hourly2 = Hourly()
        hourly_set = {hourly1, hourly2}
        self.assertEqual(len(hourly_set), 1)
        custom_hourly = Hourly(path="custom.log")
        hourly_set.add(custom_hourly)
        self.assertEqual(len(hourly_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Hourly enforces keyword-only initialization.
        """
        with self.assertRaises(TypeError):
            Hourly("path.log", "info", 24)