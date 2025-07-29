from datetime import time
from orionis.foundation.config.logging.entities.daily import Daily
from orionis.foundation.config.logging.enums.levels import Level
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigDaily(TestCase):
    """
    Test cases for the Daily logging configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Daily instance is created with correct default values.
        Verifies default path, level, retention_days and at time match expected values.
        """
        daily = Daily()
        self.assertEqual(daily.path, "storage/log/application.log")
        self.assertEqual(daily.level, Level.INFO.value)
        self.assertEqual(daily.retention_days, 7)
        self.assertEqual(daily.at, "00:00:00")

    async def testPathValidation(self):
        """
        Test path attribute validation.
        Verifies that empty or non-string paths raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            Daily(path="")
        with self.assertRaises(OrionisIntegrityException):
            Daily(path=123)
        try:
            Daily(path="custom/log/path.log")
        except OrionisIntegrityException:
            self.fail("Valid path should not raise exception")

    async def testLevelValidation(self):
        """
        Test level attribute validation with different input types.
        """
        # Test string level
        daily = Daily(level="debug")
        self.assertEqual(daily.level, Level.DEBUG.value)

        # Test int level
        daily = Daily(level=Level.WARNING.value)
        self.assertEqual(daily.level, Level.WARNING.value)

        # Test enum level
        daily = Daily(level=Level.ERROR)
        self.assertEqual(daily.level, Level.ERROR.value)

        # Test invalid cases
        with self.assertRaises(OrionisIntegrityException):
            Daily(level="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Daily(level=999)
        with self.assertRaises(OrionisIntegrityException):
            Daily(level=[])

    async def testRetentionDaysValidation(self):
        """
        Test retention_days attribute validation.
        """
        # Test valid values
        try:
            Daily(retention_days=1)
            Daily(retention_days=90)
            Daily(retention_days=30)
        except OrionisIntegrityException:
            self.fail("Valid retention_days should not raise exception")

        # Test invalid values
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days=0)
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days=91)
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days=-1)
        with self.assertRaises(OrionisIntegrityException):
            Daily(retention_days="7")

    async def testAtTimeValidation(self):
        """
        Test at time attribute validation and conversion.
        """
        # Test time object
        daily = Daily(at=time(12, 30))
        self.assertEqual(daily.at, "12:30:00")

        # Test invalid type
        with self.assertRaises(OrionisIntegrityException):
            Daily(at="12:00:00")
        with self.assertRaises(OrionisIntegrityException):
            Daily(at=1200)

    async def testWhitespaceHandling(self):
        """
        Test whitespace handling in path and level attributes.
        """
        daily = Daily(path="  logs/app.log  ", level="  debug  ")
        self.assertEqual(daily.path, "  logs/app.log  ")
        self.assertEqual(daily.level, Level.DEBUG.value)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        """
        daily = Daily()
        daily_dict = daily.toDict()

        self.assertIsInstance(daily_dict, dict)
        self.assertEqual(daily_dict['path'], "storage/log/application.log")
        self.assertEqual(daily_dict['level'], Level.INFO.value)
        self.assertEqual(daily_dict['retention_days'], 7)
        self.assertEqual(daily_dict['at'], "00:00:00")

    async def testCustomValuesToDict(self):
        """
        Test that custom values are properly included in dictionary.
        """
        custom_daily = Daily(
            path="custom/logs/app.log",
            level="warning",
            retention_days=14,
            at=time(23, 59)
        )
        daily_dict = custom_daily.toDict()
        self.assertEqual(daily_dict['path'], "custom/logs/app.log")
        self.assertEqual(daily_dict['level'], Level.WARNING.value)
        self.assertEqual(daily_dict['retention_days'], 14)
        self.assertEqual(daily_dict['at'], "23:59:00")

    async def testHashability(self):
        """
        Test that Daily maintains hashability due to unsafe_hash=True.
        """
        daily1 = Daily()
        daily2 = Daily()
        daily_set = {daily1, daily2}

        self.assertEqual(len(daily_set), 1)

        custom_daily = Daily(path="custom.log")
        daily_set.add(custom_daily)
        self.assertEqual(len(daily_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Daily enforces keyword-only initialization.
        """
        with self.assertRaises(TypeError):
            Daily("path.log", "info", 7, time(0, 0))