from orionis.foundation.config.cache.entities.file import File
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigFile(TestCase):
    """
    Test cases for the File cache configuration entity.
    """

    async def testDefaultPath(self):
        """
        Test that the File instance is created with the correct default path.
        Verifies that the default path matches the expected value from the class definition.
        """
        file_config = File()
        self.assertEqual(file_config.path, 'storage/framework/cache/data')

    async def testCustomPath(self):
        """
        Test that a custom path can be set during initialization.
        Verifies that the path attribute accepts and stores valid custom paths.
        """
        custom_path = 'custom/cache/path'
        file_config = File(path=custom_path)
        self.assertEqual(file_config.path, custom_path)

    async def testEmptyPathValidation(self):
        """
        Test that empty paths are rejected.
        Verifies that an empty path raises an OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            File(path="")

    async def testPathTypeValidation(self):
        """
        Test that non-string paths are rejected.
        Verifies that non-string path values raise an OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            File(path=123)

        with self.assertRaises(OrionisIntegrityException):
            File(path=None)

        with self.assertRaises(OrionisIntegrityException):
            File(path=[])

    async def testToDictMethod(self):
        """
        Test that the toDict method returns a proper dictionary representation.
        Verifies that the returned dictionary contains the expected path value.
        """
        file_config = File()
        config_dict = file_config.toDict()

        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['path'], 'storage/framework/cache/data')

    async def testCustomPathToDict(self):
        """
        Test that custom paths are properly included in the dictionary representation.
        Verifies that toDict() includes custom path values when specified.
        """
        custom_path = 'another/cache/location'
        file_config = File(path=custom_path)
        config_dict = file_config.toDict()

        self.assertEqual(config_dict['path'], custom_path)

    async def testWhitespacePathHandling(self):
        """
        Test that paths with whitespace are accepted but not automatically trimmed.
        Verifies that the validation allows paths containing whitespace characters.
        """
        spaced_path = '  storage/cache/with/space  '
        file_config = File(path=spaced_path)
        self.assertEqual(file_config.path, spaced_path)