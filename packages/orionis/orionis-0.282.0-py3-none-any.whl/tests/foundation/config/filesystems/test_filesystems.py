from orionis.foundation.config.filesystems.entitites.disks import Disks
from orionis.foundation.config.filesystems.entitites.filesystems import Filesystems
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigFilesystems(TestCase):
    """
    Test cases for the Filesystems configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Filesystems instance is created with correct default values.
        Verifies default disk is 'local' and disks object is properly initialized.
        """
        fs = Filesystems()
        self.assertEqual(fs.default, "local")
        self.assertIsInstance(fs.disks, Disks)

    async def testDefaultDiskValidation(self):
        """
        Test default disk attribute validation.
        Verifies that only valid disk types are accepted as default.
        """
        # Test valid disk types
        valid_disks = ["local", "public", "aws"]
        for disk in valid_disks:
            try:
                Filesystems(default=disk)
            except OrionisIntegrityException:
                self.fail(f"Valid disk type '{disk}' should not raise exception")

        # Test invalid disk type
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(default="invalid_disk")

        # Test empty default
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(default="")

        # Test non-string default
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(default=123)

    async def testDisksValidation(self):
        """
        Test disks attribute validation.
        Verifies that only Disks instances are accepted.
        """
        # Test invalid disks type
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(disks="not_a_disks_instance")

        # Test None disks
        with self.assertRaises(OrionisIntegrityException):
            Filesystems(disks=None)

        # Test valid disks
        try:
            Filesystems(disks=Disks())
        except OrionisIntegrityException:
            self.fail("Valid Disks instance should not raise exception")

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies all attributes are correctly included in dictionary.
        """
        fs = Filesystems()
        fs_dict = fs.toDict()

        self.assertIsInstance(fs_dict, dict)
        self.assertEqual(fs_dict['default'], "local")
        self.assertIsInstance(fs_dict['disks'], dict)

    async def testCustomValues(self):
        """
        Test that custom values are properly stored and validated.
        Verifies custom configurations are correctly handled.
        """
        custom_disks = Disks()
        custom_fs = Filesystems(
            default="aws",
            disks=custom_disks
        )
        self.assertEqual(custom_fs.default, "aws")
        self.assertIs(custom_fs.disks, custom_disks)

    async def testHashability(self):
        """
        Test that Filesystems maintains hashability due to unsafe_hash=True.
        Verifies that Filesystems instances can be used in sets and as dictionary keys.
        """
        fs1 = Filesystems()
        fs2 = Filesystems()
        fs_set = {fs1, fs2}

        self.assertEqual(len(fs_set), 1)

        custom_fs = Filesystems(default="public")
        fs_set.add(custom_fs)
        self.assertEqual(len(fs_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Filesystems enforces keyword-only initialization.
        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Filesystems("local", Disks())