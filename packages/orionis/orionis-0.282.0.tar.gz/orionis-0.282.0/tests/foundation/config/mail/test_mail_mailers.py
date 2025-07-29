from orionis.foundation.config.mail.entities.mailers import Mailers
from orionis.foundation.config.mail.entities.smtp import Smtp
from orionis.foundation.config.mail.entities.file import File
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestMailers(TestCase):

    async def testDefaultInitialization(self):
        """
        Test that Mailers instance is initialized with correct default factories.
        Verifies that smtp and file attributes are properly initialized with their respective types.
        """
        mailers = Mailers()
        self.assertIsInstance(mailers.smtp, Smtp)
        self.assertIsInstance(mailers.file, File)

    async def testTypeValidation(self):
        """
        Test type validation for smtp and file attributes.
        Verifies that invalid types raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Mailers(smtp="invalid_smtp")
        with self.assertRaises(OrionisIntegrityException):
            Mailers(file="invalid_file")

    async def testCustomInitialization(self):
        """
        Test custom initialization with valid parameters.
        Verifies that valid Smtp and File instances are accepted.
        """
        custom_smtp = Smtp()
        custom_file = File()
        mailers = Mailers(smtp=custom_smtp, file=custom_file)
        self.assertIs(mailers.smtp, custom_smtp)
        self.assertIs(mailers.file, custom_file)

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.
        Verifies the method returns a dict containing all fields with correct values.
        """
        mailers = Mailers()
        result = mailers.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("smtp", result)
        self.assertIn("file", result)
        self.assertIsInstance(result["smtp"], dict)
        self.assertIsInstance(result["file"], dict)

    async def testKwOnlyInitialization(self):
        """
        Test that Mailers requires keyword arguments for initialization.
        Verifies the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Mailers(Smtp(), File())