from orionis.foundation.config.queue.entities.queue import Queue
from orionis.foundation.config.queue.entities.brokers import Brokers
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestQueue(TestCase):

    async def testDefaultInitialization(self):
        """
        Test that Queue instance is initialized with correct default values.
        Verifies that default connection is 'sync' and brokers is a Brokers instance.
        """
        queue = Queue()
        self.assertEqual(queue.default, "sync")
        self.assertIsInstance(queue.brokers, Brokers)

    async def testDefaultValidation(self):
        """
        Test validation for default attribute.
        Verifies that invalid default values raise OrionisIntegrityException.
        """
        invalid_options = ["invalid", "", 123, None]
        for option in invalid_options:
            with self.assertRaises(OrionisIntegrityException):
                Queue(default=option)

    async def testBrokersValidation(self):
        """
        Test validation for brokers attribute.
        Verifies that non-Brokers values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Queue(brokers="invalid_brokers")
        with self.assertRaises(OrionisIntegrityException):
            Queue(brokers={})

    async def testValidCustomInitialization(self):
        """
        Test custom initialization with valid parameters.
        Verifies that valid default and Brokers instances are accepted.
        """
        custom_brokers = Brokers(sync=False)
        queue = Queue(default="sync", brokers=custom_brokers)
        self.assertEqual(queue.default, "sync")
        self.assertIs(queue.brokers, custom_brokers)
        self.assertFalse(queue.brokers.sync)

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.
        Verifies all fields are included with correct values.
        """
        queue = Queue()
        result = queue.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["default"], "sync")
        self.assertIsInstance(result["brokers"], dict)
        self.assertTrue(result["brokers"]["sync"])