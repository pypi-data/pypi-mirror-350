from orionis.foundation.config.mail.entities.file import File
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestMailFile(TestCase):

    async def testDefaultPathValue(self):
        """
        Test that the File instance is initialized with the correct default path.
        Verifies that a new File object has 'storage/mail' as the default path.
        """
        file = File()
        self.assertEqual(file.path, "storage/mail")

    async def testPathValidation(self):
        """
        Test the path validation in __post_init__ method.
        Verifies that non-string paths raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            File(path=123)
        with self.assertRaises(OrionisIntegrityException):
            File(path="")

    async def testValidPathAssignment(self):
        """
        Test that valid path assignments work correctly.
        Verifies that string paths are accepted and stored properly.
        """
        test_path = "custom/path/to/mail"
        file = File(path=test_path)
        self.assertEqual(file.path, test_path)

    async def testToDictMethod(self):
        """
        Test the toDict method returns a proper dictionary representation.
        Checks that the toDict method converts the File instance
        into a dictionary with the expected path field.
        """
        file = File()
        result = file.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["path"], "storage/mail")

    async def testHashability(self):
        """
        Test that File instances are hashable due to unsafe_hash=True.
        Verifies that instances can be used in sets or as dictionary keys.
        """
        file1 = File()
        file2 = File(path="other/path")
        test_set = {file1, file2}
        self.assertEqual(len(test_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that File requires keyword arguments for initialization.
        Verifies that the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            File("storage/mail")