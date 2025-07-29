from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.logging.entities.channels import Channels
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestLogging(TestCase):

    async def testDefaultValues(self):
        """
        Test that the Logging instance is initialized with correct default values.
        Verifies that a new Logging object has 'stack' as default channel
        and an instance of Channels as channels attribute.
        """
        logging = Logging()
        self.assertEqual(logging.default, "stack")
        self.assertIsInstance(logging.channels, Channels)

    async def testToDictMethod(self):
        """
        Test the toDict method returns a proper dictionary representation.
        Checks that the toDict method converts the Logging instance
        into a dictionary with all expected fields.
        """
        logging = Logging()
        result = logging.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("default", result)
        self.assertIn("channels", result)

    async def testPostInitValidation(self):
        """
        Test the __post_init__ validation works correctly.
        Verifies that invalid default channel or channels type
        raises OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Logging(default="invalid_channel")

        with self.assertRaises(OrionisIntegrityException):
            Logging(channels="invalid_channels")

    async def testKwOnlyInitialization(self):
        """
        Test that Logging requires keyword arguments for initialization.
        Verifies that the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Logging("stack", Channels())