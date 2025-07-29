from orionis.foundation.config.mail.entities.smtp import Smtp
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestSmtp(TestCase):

    async def testDefaultInitialization(self):
        """
        Test that Smtp instance is initialized with correct default values.
        Verifies all default values match the expected configuration.
        """
        smtp = Smtp()
        self.assertEqual(smtp.url, "smtp.mailtrap.io")
        self.assertEqual(smtp.host, "smtp.mailtrap.io")
        self.assertEqual(smtp.port, 587)
        self.assertEqual(smtp.encryption, "TLS")
        self.assertEqual(smtp.username, "")
        self.assertEqual(smtp.password, "")
        self.assertIsNone(smtp.timeout)

    async def testTypeValidation(self):
        """
        Test type validation for all Smtp attributes.
        Verifies that invalid types raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Smtp(url=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(host=456)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(port="invalid")
        with self.assertRaises(OrionisIntegrityException):
            Smtp(encryption=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(username=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(password=123)
        with self.assertRaises(OrionisIntegrityException):
            Smtp(timeout="invalid")

    async def testPortValidation(self):
        """
        Test specific validation for port attribute.
        Verifies that negative port numbers raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Smtp(port=-1)

    async def testTimeoutValidation(self):
        """
        Test specific validation for timeout attribute.
        Verifies that negative timeout values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Smtp(timeout=-1)

    async def testValidCustomInitialization(self):
        """
        Test custom initialization with valid parameters.
        Verifies that valid custom values are accepted and stored correctly.
        """
        custom_config = Smtp(
            url="smtp.example.com",
            host="mail.example.com",
            port=465,
            encryption="SSL",
            username="user",
            password="pass",
            timeout=30
        )
        self.assertEqual(custom_config.url, "smtp.example.com")
        self.assertEqual(custom_config.host, "mail.example.com")
        self.assertEqual(custom_config.port, 465)
        self.assertEqual(custom_config.encryption, "SSL")
        self.assertEqual(custom_config.username, "user")
        self.assertEqual(custom_config.password, "pass")
        self.assertEqual(custom_config.timeout, 30)

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.
        Verifies the method returns a dict containing all fields with correct values.
        """
        smtp = Smtp()
        result = smtp.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["url"], "smtp.mailtrap.io")
        self.assertEqual(result["host"], "smtp.mailtrap.io")
        self.assertEqual(result["port"], 587)
        self.assertEqual(result["encryption"], "TLS")
        self.assertEqual(result["username"], "")
        self.assertEqual(result["password"], "")
        self.assertIsNone(result["timeout"])


    async def testKwOnlyInitialization(self):
        """
        Test that Smtp requires keyword arguments for initialization.
        Verifies the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Smtp("smtp.mailtrap.io", "smtp.mailtrap.io", 587, "TLS", "", "", None)