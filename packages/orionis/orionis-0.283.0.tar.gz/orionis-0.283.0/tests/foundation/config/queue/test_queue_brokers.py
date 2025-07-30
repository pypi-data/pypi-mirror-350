from orionis.foundation.config.queue.entities.brokers import Brokers
from orionis.foundation.config.queue.entities.database import Database
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestBrokers(TestCase):

    async def testDefaultInitialization(self):
        """
        Test that Brokers instance is initialized with correct default values.
        Verifies that sync is True by default and database is a Database instance.
        """
        brokers = Brokers()
        self.assertTrue(brokers.sync)
        self.assertIsInstance(brokers.database, Database)

    async def testSyncValidation(self):
        """
        Test validation for sync attribute.
        Verifies that non-boolean values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Brokers(sync="true")
        with self.assertRaises(OrionisIntegrityException):
            Brokers(sync=1)

    async def testDatabaseValidation(self):
        """
        Test validation for database attribute.
        Verifies that non-Database values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Brokers(database="invalid_database")
        with self.assertRaises(OrionisIntegrityException):
            Brokers(database={})

    async def testCustomInitialization(self):
        """
        Test custom initialization with valid parameters.
        Verifies that valid boolean and Database instances are accepted.
        """
        custom_db = Database(table="custom_queue")
        brokers = Brokers(sync=False, database=custom_db)
        self.assertFalse(brokers.sync)
        self.assertIs(brokers.database, custom_db)
        self.assertEqual(brokers.database.table, "custom_queue")

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.
        Verifies all fields are included with correct values.
        """
        brokers = Brokers()
        result = brokers.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("sync", result)
        self.assertIn("database", result)
        self.assertTrue(result["sync"])
        self.assertIsInstance(result["database"], dict)

    async def testKwOnlyInitialization(self):
        """
        Test that Brokers requires keyword arguments for initialization.
        Verifies the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Brokers(True, Database())