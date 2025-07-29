from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.database.entities.connections import Connections
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigDatabase(TestCase):
    """
    Test cases for the Database configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Database instance is created with correct default values.
        Verifies default connection is 'sqlite' and connections object is properly initialized.
        """
        db = Database()
        self.assertEqual(db.default, 'sqlite')
        self.assertIsInstance(db.connections, Connections)

    async def testDefaultConnectionValidation(self):
        """
        Test default connection attribute validation.
        Verifies that only valid connection types are accepted as default.
        """
        # Test valid connection types
        valid_connections = ['sqlite', 'mysql', 'pgsql', 'oracle']
        for conn in valid_connections:
            try:
                Database(default=conn)
            except OrionisIntegrityException:
                self.fail(f"Valid connection type '{conn}' should not raise exception")

        # Test invalid connection type
        with self.assertRaises(OrionisIntegrityException):
            Database(default='invalid_connection')

        # Test empty default
        with self.assertRaises(OrionisIntegrityException):
            Database(default='')

        # Test non-string default
        with self.assertRaises(OrionisIntegrityException):
            Database(default=123)

    async def testConnectionsValidation(self):
        """
        Test connections attribute validation.
        Verifies that only Connections instances are accepted.
        """
        # Test invalid connections type
        with self.assertRaises(OrionisIntegrityException):
            Database(connections="not_a_connections_instance")

        # Test None connections
        with self.assertRaises(OrionisIntegrityException):
            Database(connections=None)

        # Test valid connections
        try:
            Database(connections=Connections())
        except OrionisIntegrityException:
            self.fail("Valid Connections instance should not raise exception")

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies all attributes are correctly included in dictionary.
        """
        db = Database()
        db_dict = db.toDict()
        self.assertIsInstance(db_dict, dict)
        self.assertEqual(db_dict['default'], 'sqlite')
        self.assertIsInstance(db_dict['connections'], dict)

    async def testCustomValues(self):
        """
        Test that custom values are properly stored and validated.
        Verifies custom configurations are correctly handled.
        """
        custom_connections = Connections()
        custom_db = Database(
            default='mysql',
            connections=custom_connections
        )
        self.assertEqual(custom_db.default, 'mysql')
        self.assertIs(custom_db.connections, custom_connections)

    async def testHashability(self):
        """
        Test that Database maintains hashability due to unsafe_hash=True.
        Verifies that Database instances can be used in sets and as dictionary keys.
        """
        db1 = Database()
        db2 = Database()
        db_set = {db1, db2}
        self.assertEqual(len(db_set), 1)

        custom_db = Database(default='pgsql')
        db_set.add(custom_db)
        self.assertEqual(len(db_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Database enforces keyword-only initialization.
        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Database('sqlite', Connections())