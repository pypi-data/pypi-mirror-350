from orionis.foundation.config.database.entities.pgsql import PGSQL
from orionis.foundation.config.database.enums.pgsql_charsets import PGSQLCharset
from orionis.foundation.config.database.enums.pgsql_mode import PGSQLSSLMode
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestConfigPGSQL(TestCase):
    """
    Test cases for the PGSQL database configuration class.
    """

    async def testDefaultValues(self):
        """
        Test that PGSQL instance is created with correct default values.
        Verifies all default values match expected defaults from class definition.
        """
        pgsql = PGSQL()
        self.assertEqual(pgsql.driver, 'pgsql')
        self.assertEqual(pgsql.host, '127.0.0.1')
        self.assertEqual(pgsql.port, '5432')
        self.assertEqual(pgsql.database, 'orionis')
        self.assertEqual(pgsql.username, 'root')
        self.assertEqual(pgsql.password, '')
        self.assertEqual(pgsql.charset, PGSQLCharset.UTF8.value)
        self.assertEqual(pgsql.prefix, '')
        self.assertTrue(pgsql.prefix_indexes)
        self.assertEqual(pgsql.search_path, 'public')
        self.assertEqual(pgsql.sslmode, PGSQLSSLMode.PREFER.value)

    async def testDriverValidation(self):
        """
        Test driver attribute validation.
        Verifies that empty or non-string drivers raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(driver='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(driver=123)

    async def testHostValidation(self):
        """
        Test host attribute validation.
        Verifies that empty or non-string hosts raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(host='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(host=123)

    async def testPortValidation(self):
        """
        Test port attribute validation.
        Verifies that non-numeric string ports raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(port='abc')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(port=5432)  # Should be string

    async def testDatabaseValidation(self):
        """
        Test database attribute validation.
        Verifies that empty or non-string database names raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(database='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(database=123)

    async def testUsernameValidation(self):
        """
        Test username attribute validation.
        Verifies that empty or non-string usernames raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(username='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(username=123)

    async def testPasswordValidation(self):
        """
        Test password attribute validation.
        Verifies that non-string passwords raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(password=123)

    async def testCharsetValidation(self):
        """
        Test charset attribute validation.
        Verifies enum conversion and invalid value handling.
        """
        # Test string conversion
        pgsql = PGSQL(charset='UTF8')
        self.assertEqual(pgsql.charset, PGSQLCharset.UTF8.value)

        # Test enum assignment
        pgsql = PGSQL(charset=PGSQLCharset.LATIN1)
        self.assertEqual(pgsql.charset, PGSQLCharset.LATIN1.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(charset='INVALID')

    async def testPrefixIndexesValidation(self):
        """
        Test prefix_indexes attribute validation.
        Verifies that non-boolean values raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(prefix_indexes='true')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(prefix_indexes=1)

    async def testSearchPathValidation(self):
        """
        Test search_path attribute validation.
        Verifies that empty or non-string search paths raise exceptions.
        """
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(search_path='')
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(search_path=123)

    async def testSSLModeValidation(self):
        """
        Test sslmode attribute validation.
        Verifies enum conversion and invalid value handling.
        """
        # Test string conversion
        pgsql = PGSQL(sslmode='REQUIRE')
        self.assertEqual(pgsql.sslmode, PGSQLSSLMode.REQUIRE.value)

        # Test enum assignment
        pgsql = PGSQL(sslmode=PGSQLSSLMode.DISABLE)
        self.assertEqual(pgsql.sslmode, PGSQLSSLMode.DISABLE.value)

        # Test invalid value
        with self.assertRaises(OrionisIntegrityException):
            PGSQL(sslmode='INVALID')

    async def testToDictMethod(self):
        """
        Test that toDict returns proper dictionary representation.
        Verifies all attributes are correctly included in dictionary.
        """
        pgsql = PGSQL()
        pgsql_dict = pgsql.toDict()
        self.assertEqual(pgsql_dict['driver'], 'pgsql')
        self.assertEqual(pgsql_dict['host'], '127.0.0.1')
        self.assertEqual(pgsql_dict['port'], '5432')
        self.assertEqual(pgsql_dict['database'], 'orionis')
        self.assertEqual(pgsql_dict['username'], 'root')
        self.assertEqual(pgsql_dict['password'], '')
        self.assertEqual(pgsql_dict['charset'], PGSQLCharset.UTF8.value)
        self.assertEqual(pgsql_dict['prefix'], '')
        self.assertTrue(pgsql_dict['prefix_indexes'])
        self.assertEqual(pgsql_dict['search_path'], 'public')
        self.assertEqual(pgsql_dict['sslmode'], PGSQLSSLMode.PREFER.value)

    async def testCustomValues(self):
        """
        Test that custom values are properly stored and validated.
        Verifies custom configuration values are correctly handled.
        """
        custom_pgsql = PGSQL(
            host='db.example.com',
            port='6432',
            database='custom_db',
            username='admin',
            password='secure123',
            charset='LATIN1',
            prefix='app_',
            prefix_indexes=False,
            search_path='app_schema',
            sslmode='VERIFY_FULL'
        )
        self.assertEqual(custom_pgsql.host, 'db.example.com')
        self.assertEqual(custom_pgsql.port, '6432')
        self.assertEqual(custom_pgsql.database, 'custom_db')
        self.assertEqual(custom_pgsql.username, 'admin')
        self.assertEqual(custom_pgsql.password, 'secure123')
        self.assertEqual(custom_pgsql.charset, PGSQLCharset.LATIN1.value)
        self.assertEqual(custom_pgsql.prefix, 'app_')
        self.assertFalse(custom_pgsql.prefix_indexes)
        self.assertEqual(custom_pgsql.search_path, 'app_schema')
        self.assertEqual(custom_pgsql.sslmode, PGSQLSSLMode.VERIFY_FULL.value)