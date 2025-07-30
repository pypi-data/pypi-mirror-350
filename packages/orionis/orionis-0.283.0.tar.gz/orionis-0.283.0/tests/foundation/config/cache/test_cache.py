from orionis.unittesting import TestCase
from orionis.foundation.config.cache.entities.cache import Cache
from orionis.foundation.config.cache.enums.drivers import Drivers
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.cache.entities.stores import Stores

class TestConfigCache(TestCase):
    """
    Test cases for the Cache configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that the Cache instance is created with the correct default values.
        Verifies that default values match the expected defaults from the class definition.
        """
        cache = Cache()
        self.assertEqual(cache.default, Drivers.MEMORY.value)
        self.assertIsInstance(cache.stores, Stores)

    async def testDriverValidation(self):
        """
        Test that the default driver attribute is properly validated and converted.
        Verifies that string drivers are converted to enum values and invalid drivers raise exceptions.
        """
        # Test valid string driver
        cache = Cache(default="FILE")
        self.assertEqual(cache.default, Drivers.FILE.value)


        # Test invalid driver
        with self.assertRaises(OrionisIntegrityException):
            Cache(default="INVALID_DRIVER")

    async def testDriverCaseInsensitivity(self):
        """
        Test that driver names are case-insensitive when provided as strings.
        Verifies that different case variations of driver names are properly normalized.
        """
        # Test lowercase
        cache = Cache(default="file")
        self.assertEqual(cache.default, Drivers.FILE.value)

        # Test mixed case
        cache = Cache(default="FiLe")
        self.assertEqual(cache.default, Drivers.FILE.value)

        # Test uppercase
        cache = Cache(default="FILE")
        self.assertEqual(cache.default, Drivers.FILE.value)

    async def testTypeValidation(self):
        """
        Test that type validation works correctly for all attributes.
        Verifies that invalid types for each attribute raise OrionisIntegrityException.
        """
        # Test invalid default type
        with self.assertRaises(OrionisIntegrityException):
            Cache(default=123)

        # Test invalid stores type
        with self.assertRaises(OrionisIntegrityException):
            Cache(stores="invalid_stores")

    async def testToDictMethod(self):
        """
        Test that the toDict method returns a proper dictionary representation.
        Verifies that the returned dictionary contains all expected keys and values.
        """
        cache = Cache()
        cache_dict = cache.toDict()

        self.assertIsInstance(cache_dict, dict)
        self.assertEqual(cache_dict['default'], Drivers.MEMORY.value)
        self.assertIsInstance(cache_dict['stores'], dict)

    async def testStoresInstanceValidation(self):
        """
        Test that stores attribute must be an instance of Stores class.
        Verifies that only Stores instances are accepted for the stores attribute.
        """
        # Test with proper Stores instance
        stores = Stores()  # Assuming Stores has a default constructor
        cache = Cache(stores=stores)
        self.assertIsInstance(cache.stores, Stores)

        # Test with invalid stores type
        with self.assertRaises(OrionisIntegrityException):
            Cache(stores={"file": "some_path"})

    async def testDriverEnumConversion(self):
        """
        Test that Drivers enum values are properly converted to their string representations.
        Verifies that enum members are converted to their value representations.
        """
        # Test with enum member
        cache = Cache(default=Drivers.MEMORY)
        self.assertEqual(cache.default, Drivers.MEMORY.value)