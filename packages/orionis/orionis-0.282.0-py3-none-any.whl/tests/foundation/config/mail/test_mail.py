from orionis.foundation.config.mail.entities.mail import Mail
from orionis.foundation.config.mail.entities.mailers import Mailers
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestMail(TestCase):

    async def testDefaultInitialization(self):
        """
        Test that Mail instance is initialized with correct default values.
        Verifies that default mailer is 'smtp' and mailers is an instance of Mailers.
        """
        mail = Mail()
        self.assertEqual(mail.default, "smtp")
        self.assertIsInstance(mail.mailers, Mailers)

    async def testDefaultValidation(self):
        """
        Test validation of default mailer against available options.
        Verifies that invalid default mailer raises OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Mail(default="invalid_mailer")
        with self.assertRaises(OrionisIntegrityException):
            Mail(default=123)

    async def testMailersTypeValidation(self):
        """
        Test validation of mailers attribute type.
        Verifies that non-Mailers objects raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Mail(mailers="invalid_mailers_object")

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.
        Verifies the method returns a dict containing all fields.
        """
        mail = Mail()
        result = mail.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("default", result)
        self.assertIn("mailers", result)
        self.assertEqual(result["default"], "smtp")

    async def testHashability(self):
        """
        Test that Mail instances are hashable due to unsafe_hash=True.
        Verifies instances can be used in sets or as dictionary keys.
        """
        mail1 = Mail()
        mail2 = Mail(default="smtp")
        test_set = {mail1, mail2}
        self.assertEqual(len(test_set), 1)

    async def testKwOnlyInitialization(self):
        """
        Test that Mail requires keyword arguments for initialization.
        Verifies the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Mail("smtp", Mailers())

    async def testValidCustomInitialization(self):
        """
        Test valid custom initialization with proper values.
        Verifies instance can be created with valid non-default values.
        """
        # Assuming 'smtp' is a valid mailer option from Mailers
        mail = Mail(default="smtp", mailers=Mailers())
        self.assertEqual(mail.default, "smtp")
        self.assertIsInstance(mail.mailers, Mailers)