from orionis.foundation.config.cache.entities.stores import Stores
from orionis.foundation.config.cache.entities.file import File
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigStores(TestCase):
    """
    Test cases for the Stores cache configuration entity.
    """

    async def testDefaultFileStore(self):
        """
        Test that Stores initializes with a default File instance.
        Verifies that the file attribute is properly initialized with default File configuration.
        """
        stores = Stores()
        self.assertIsInstance(stores.file, File)
        self.assertEqual(stores.file.path, 'storage/framework/cache/data')

    async def testCustomFileStore(self):
        """
        Test that Stores accepts a custom File configuration.
        Verifies that a custom File instance can be provided during initialization.
        """
        custom_file = File(path='custom/cache/path')
        stores = Stores(file=custom_file)
        self.assertIsInstance(stores.file, File)
        self.assertEqual(stores.file.path, 'custom/cache/path')

    async def testFileTypeValidation(self):
        """
        Test that Stores validates the file attribute type.
        Verifies that non-File instances raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Stores(file="not_a_file_instance")

        with self.assertRaises(OrionisIntegrityException):
            Stores(file=123)

        with self.assertRaises(OrionisIntegrityException):
            Stores(file=None)

    async def testToDictMethodWithDefaults(self):
        """
        Test that toDict returns proper dictionary with default values.
        Verifies the dictionary representation contains the correct default file path.
        """
        stores = Stores()
        stores_dict = stores.toDict()

        self.assertIsInstance(stores_dict, dict)
        self.assertIsInstance(stores_dict['file'], dict)
        self.assertEqual(stores_dict['file']['path'], 'storage/framework/cache/data')

    async def testToDictMethodWithCustomFile(self):
        """
        Test that toDict includes custom file configurations.
        Verifies the dictionary representation reflects custom file paths.
        """
        custom_file = File(path='alternate/cache/location')
        stores = Stores(file=custom_file)
        stores_dict = stores.toDict()

        self.assertEqual(stores_dict['file']['path'], 'alternate/cache/location')

    async def testHashability(self):
        """
        Test that Stores maintains hashability due to unsafe_hash=True.
        Verifies that Stores instances can be used in sets and as dictionary keys.
        """
        store1 = Stores()
        store2 = Stores()
        store_set = {store1, store2}

        self.assertEqual(len(store_set), 1)

        custom_store = Stores(file=File(path='custom/path'))
        store_set.add(custom_store)
        self.assertEqual(len(store_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Stores enforces keyword-only initialization.
        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Stores(File())