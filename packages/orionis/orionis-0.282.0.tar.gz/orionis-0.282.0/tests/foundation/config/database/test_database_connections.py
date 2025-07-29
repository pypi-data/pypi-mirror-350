from orionis.foundation.config.database.entities.connections import Connections
from orionis.foundation.config.database.entities.mysql import MySQL
from orionis.foundation.config.database.entities.oracle import Oracle
from orionis.foundation.config.database.entities.pgsql import PGSQL
from orionis.foundation.config.database.entities.sqlite import SQLite
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigConnections(TestCase):
    """
    Test cases for the Connections configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that Connections instance is created with correct default values.
        Verifies all default connections are properly initialized with their respective types.
        """
        connections = Connections()
        self.assertIsInstance(connections.sqlite, SQLite)
        self.assertIsInstance(connections.mysql, MySQL)
        self.assertIsInstance(connections.pgsql, PGSQL)
        self.assertIsInstance(connections.oracle, Oracle)

    async def testSqliteTypeValidation(self):
        """
        Test sqlite attribute type validation.
        Verifies that only SQLite instances are accepted for sqlite attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Connections(sqlite="not_a_sqlite_instance")
        with self.assertRaises(OrionisIntegrityException):
            Connections(sqlite=123)
        with self.assertRaises(OrionisIntegrityException):
            Connections(sqlite=None)

    async def testMysqlTypeValidation(self):
        """
        Test mysql attribute type validation.
        Verifies that only MySQL instances are accepted for mysql attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Connections(mysql="not_a_mysql_instance")
        with self.assertRaises(OrionisIntegrityException):
            Connections(mysql=123)
        with self.assertRaises(OrionisIntegrityException):
            Connections(mysql=None)

    async def testPgsqlTypeValidation(self):
        """
        Test pgsql attribute type validation.
        Verifies that only PGSQL instances are accepted for pgsql attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Connections(pgsql="not_a_pgsql_instance")
        with self.assertRaises(OrionisIntegrityException):
            Connections(pgsql=123)
        with self.assertRaises(OrionisIntegrityException):
            Connections(pgsql=None)

    async def testOracleTypeValidation(self):
        """
        Test oracle attribute type validation.
        Verifies that only Oracle instances are accepted for oracle attribute.
        """
        with self.assertRaises(OrionisIntegrityException):
            Connections(oracle="not_an_oracle_instance")
        with self.assertRaises(OrionisIntegrityException):
            Connections(oracle=123)
        with self.assertRaises(OrionisIntegrityException):
            Connections(oracle=None)

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies all connections are correctly included in dictionary.
        """
        connections = Connections()
        connections_dict = connections.toDict()
        self.assertIsInstance(connections_dict, dict)
        self.assertIsInstance(connections_dict['sqlite'], dict)
        self.assertIsInstance(connections_dict['mysql'], dict)
        self.assertIsInstance(connections_dict['pgsql'], dict)
        self.assertIsInstance(connections_dict['oracle'], dict)

    async def testCustomConnections(self):
        """
        Test that custom connections are properly stored and validated.
        Verifies custom connection configurations are correctly handled.
        """
        custom_sqlite = SQLite(database='custom.db')
        custom_mysql = MySQL(database='custom_db')
        custom_pgsql = PGSQL(database='custom_db')
        custom_oracle = Oracle(service_name='CUSTOM_SID')

        connections = Connections(
            sqlite=custom_sqlite,
            mysql=custom_mysql,
            pgsql=custom_pgsql,
            oracle=custom_oracle
        )

        self.assertEqual(connections.sqlite.database, 'custom.db')
        self.assertEqual(connections.mysql.database, 'custom_db')
        self.assertEqual(connections.pgsql.database, 'custom_db')
        self.assertEqual(connections.oracle.service_name, 'CUSTOM_SID')

    async def testHashability(self):
        """
        Test that Connections maintains hashability due to unsafe_hash=True.
        Verifies that Connections instances can be used in sets and as dictionary keys.
        """
        conn1 = Connections()
        conn2 = Connections()
        conn_set = {conn1, conn2}

        self.assertEqual(len(conn_set), 1)

        custom_conn = Connections(sqlite=SQLite(database='custom.db'))
        conn_set.add(custom_conn)
        self.assertEqual(len(conn_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that Connections enforces keyword-only initialization.
        Verifies that positional arguments are not allowed for initialization.
        """
        with self.assertRaises(TypeError):
            Connections(SQLite(), MySQL(), PGSQL(), Oracle())