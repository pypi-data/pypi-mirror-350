from orionis.foundation.config.filesystems.entitites.local import Local
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigLocal(TestCase):
    """
    Test cases for the Local storage configuration class.
    """

    async def testDefaultPath(self):
        """
        Test that Local instance is created with correct default path.
        Verifies the default path matches the expected value from class definition.
        """
        local = Local()
        self.assertEqual(local.path, "storage/app/private")

    async def testCustomPath(self):
        """
        Test that custom path can be set during initialization.
        Verifies the path attribute accepts and stores valid custom paths.
        """
        custom_path = "custom/storage/path"
        local = Local(path=custom_path)
        self.assertEqual(local.path, custom_path)

    async def testEmptyPathValidation(self):
        """
        Test that empty paths are rejected.
        Verifies that an empty path raises OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Local(path="")

    async def testPathTypeValidation(self):
        """
        Test that non-string paths are rejected.
        Verifies that non-string path values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Local(path=123)
        with self.assertRaises(OrionisIntegrityException):
            Local(path=None)
        with self.assertRaises(OrionisIntegrityException):
            Local(path=[])

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies the returned dictionary contains the expected path value.
        """
        local = Local()
        config_dict = local.toDict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['path'], "storage/app/private")

    async def testCustomPathToDict(self):
        """
        Test that custom paths are properly included in dictionary representation.
        Verifies toDict() includes custom path values when specified.
        """
        custom_path = "another/storage/location"
        local = Local(path=custom_path)
        config_dict = local.toDict()
        self.assertEqual(config_dict['path'], custom_path)

    async def testWhitespacePathHandling(self):
        """
        Test that paths with whitespace are accepted but not automatically trimmed.
        Verifies the validation allows paths containing whitespace characters.
        """
        spaced_path = "  storage/with/space  "
        local = Local(path=spaced_path)
        self.assertEqual(local.path, spaced_path)

    async def testHashability(self):
        """
        Test that Local maintains hashability due to unsafe_hash=True.
        Verifies that Local instances can be used in sets and as dictionary keys.
        """
        local1 = Local()
        local2 = Local()
        local_set = {local1, local2}
        self.assertEqual(len(local_set), 1)
        custom_local = Local(path="custom/path")
        local_set.add(custom_local)
        self.assertEqual(len(local_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Local enforces keyword-only initialization.
        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Local("storage/path")