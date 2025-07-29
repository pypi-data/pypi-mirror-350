from orionis.foundation.config.queue.entities.database import Database
from orionis.foundation.config.queue.enums.strategy import Strategy
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestDatabaseQueue(TestCase):

    async def testDefaultInitialization(self):
        """
        Test that Database instance is initialized with correct default values.
        Verifies that default table name, queue name, retry_after, and strategy are set properly.
        """
        db_queue = Database()
        self.assertEqual(db_queue.table, "jobs")
        self.assertEqual(db_queue.queue, "default")
        self.assertEqual(db_queue.retry_after, 90)
        self.assertEqual(db_queue.strategy, Strategy.FIFO.value)

    async def testTableNameValidation(self):
        """
        Test validation for table name attribute.
        Verifies that invalid table names raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Database(table="1jobs")  # Starts with number
        with self.assertRaises(OrionisIntegrityException):
            Database(table="Jobs")  # Uppercase letter
        with self.assertRaises(OrionisIntegrityException):
            Database(table="jobs-table")  # Invalid character
        with self.assertRaises(OrionisIntegrityException):
            Database(table=123)  # Non-string value

    async def testQueueNameValidation(self):
        """
        Test validation for queue name attribute.
        Verifies that non-ASCII queue names raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Database(queue="café")  # Non-ASCII character
        with self.assertRaises(OrionisIntegrityException):
            Database(queue=123)  # Non-string value

    async def testRetryAfterValidation(self):
        """
        Test validation for retry_after attribute.
        Verifies that non-positive integers raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Database(retry_after=0)
        with self.assertRaises(OrionisIntegrityException):
            Database(retry_after=-1)
        with self.assertRaises(OrionisIntegrityException):
            Database(retry_after="90")  # String instead of int

    async def testStrategyValidation(self):
        """
        Test validation and normalization for strategy attribute.
        Verifies both string and Strategy enum inputs are properly handled.
        """
        # Test string inputs (case-insensitive)
        db1 = Database(strategy="fifo")
        self.assertEqual(db1.strategy, Strategy.FIFO.value)
        db2 = Database(strategy="LIFO")
        self.assertEqual(db2.strategy, Strategy.LIFO.value)

        # Test enum inputs
        db3 = Database(strategy=Strategy.PRIORITY)
        self.assertEqual(db3.strategy, Strategy.PRIORITY.value)

        # Test invalid inputs
        with self.assertRaises(OrionisIntegrityException):
            Database(strategy="invalid_strategy")
        with self.assertRaises(OrionisIntegrityException):
            Database(strategy=123)

    async def testToDictMethod(self):
        """
        Test the toDict method returns proper dictionary representation.
        Verifies all fields are included with correct values.
        """
        db_queue = Database()
        result = db_queue.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["table"], "jobs")
        self.assertEqual(result["queue"], "default")
        self.assertEqual(result["retry_after"], 90)
        self.assertEqual(result["strategy"], Strategy.FIFO.value)

    async def testKwOnlyInitialization(self):
        """
        Test that Database requires keyword arguments for initialization.
        Verifies the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            Database("jobs", "default", 90, Strategy.FIFO)