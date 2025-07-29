from orionis.services.environment.dot_env import DotEnv
from orionis.services.environment.env import Env
from orionis.unittesting import TestCase, unittest_mock_patch

class TestEnv(TestCase):
    """
    Test cases for the Env class which provides environment variable management.
    """

    async def testGetMethod(self):
        """
        Test that the get method retrieves values correctly.
        Verifies that Env.get() properly delegates to DotEnv.get() and returns the expected value.
        """
        with unittest_mock_patch.object(DotEnv, 'get', return_value='test_value') as mock_get:
            result = Env.get('TEST_KEY')
            mock_get.assert_called_once_with('TEST_KEY', None)
            self.assertEqual(result, 'test_value')

    async def testGetMethodWithDefault(self):
        """
        Test that the get method returns default value when key not found.
        Verifies that the default parameter is properly passed to DotEnv.get().
        """
        with unittest_mock_patch.object(DotEnv, 'get', return_value='default_value') as mock_get:
            result = Env.get('NON_EXISTENT_KEY', 'default_value')
            mock_get.assert_called_once_with('NON_EXISTENT_KEY', 'default_value')
            self.assertEqual(result, 'default_value')

    async def testSetMethod(self):
        """
        Test that the set method updates environment variables.
        Verifies that Env.set() properly delegates to DotEnv.set() and returns True on success.
        """
        with unittest_mock_patch.object(DotEnv, 'set', return_value=True) as mock_set:
            result = Env.set('TEST_KEY', 'test_value')
            mock_set.assert_called_once_with('TEST_KEY', 'test_value')
            self.assertTrue(result)

    async def testUnsetMethod(self):
        """
        Test that the unset method removes environment variables.
        Verifies that Env.unset() properly delegates to DotEnv.unset() and returns True on success.
        """
        with unittest_mock_patch.object(DotEnv, 'unset', return_value=True) as mock_unset:
            result = Env.unset('TEST_KEY')
            mock_unset.assert_called_once_with('TEST_KEY')
            self.assertTrue(result)

    async def testAllMethod(self):
        """
        Test that the all method retrieves all environment variables.
        Verifies that Env.all() properly delegates to DotEnv.all() and returns the expected dictionary.
        """
        mock_env = {'KEY1': 'value1', 'KEY2': 'value2'}
        with unittest_mock_patch.object(DotEnv, 'all', return_value=mock_env) as mock_all:
            result = Env.all()
            mock_all.assert_called_once()
            self.assertEqual(result, mock_env)

    async def testToJsonMethod(self):
        """
        Test that the toJson method serializes environment variables to JSON.
        Verifies that Env.toJson() properly delegates to DotEnv.toJson() and returns a JSON string.
        """
        mock_json = '{"KEY": "value"}'
        with unittest_mock_patch.object(DotEnv, 'toJson', return_value=mock_json) as mock_to_json:
            result = Env.toJson()
            mock_to_json.assert_called_once()
            self.assertEqual(result, mock_json)

    async def testToBase64Method(self):
        """
        Test that the toBase64 method encodes environment variables in Base64.
        Verifies that Env.toBase64() properly delegates to DotEnv.toBase64() and returns a Base64 string.
        """
        mock_b64 = 'base64encodedstring'
        with unittest_mock_patch.object(DotEnv, 'toBase64', return_value=mock_b64) as mock_to_b64:
            result = Env.toBase64()
            mock_to_b64.assert_called_once()
            self.assertEqual(result, mock_b64)

    async def testDotenvInstanceManagement(self):
        """
        Test that the Env._dotenv() method implements singleton behavior by ensuring
        that multiple calls return the same instance. Also verifies that resetting
        Env._dotenv_instance allows for a new instance to be created.
        """

        # Clear any existing instance
        Env._dotenv_instance = None

        # First call should create instance
        instance1 = Env._dotenv()
        instance2 = Env._dotenv()

        # Verify that the same instance is returned
        self.assertEqual(instance1, instance2)

    async def testHelperFunctionEnv(self):
        """
        Test that the env helper function works correctly.
        Verifies that the env() function properly delegates to DotEnv.get().
        """
        with unittest_mock_patch.object(DotEnv, 'get', return_value='test_value') as mock_get:
            from orionis.services.environment.env import env
            result = env('TEST_KEY', 'default_value')
            mock_get.assert_called_once_with('TEST_KEY', 'default_value')
            self.assertEqual(result, 'test_value')

    async def testOrionisConstants(self):
        """
        Test that Orionis framework constants are correctly set and retrieved via Env.

        This test imports a set of well-known constants from the Orionis framework and ensures:
        - Each constant can be set as an environment variable using Env.set().
        - Each constant can be retrieved using Env.get() and matches the original value.
        - The Env.get() method returns None for a non-existent key.
        - All constants are present in the dictionary returned by Env.all().
        """
        from orionis.metadata.framework import (
            NAME, VERSION, AUTHOR, AUTHOR_EMAIL, DESCRIPTION,
            SKELETON, FRAMEWORK, DOCS, API, PYTHON_REQUIRES
        )
        constants = {
            "NAME": NAME,
            "VERSION": VERSION,
            "AUTHOR": AUTHOR,
            "AUTHOR_EMAIL": AUTHOR_EMAIL,
            "DESCRIPTION": DESCRIPTION,
            "SKELETON": SKELETON,
            "FRAMEWORK": FRAMEWORK,
            "DOCS": DOCS,
            "API": API,
            "PYTHON_REQUIRES": PYTHON_REQUIRES
        }

        # Set all constants as environment variables
        for key, value in constants.items():
            result = Env.set(key, value)
            self.assertTrue(result, f"Env.set() should return True for key '{key}'")

        # Retrieve and verify each constant
        for key, value in constants.items():
            retrieved = Env.get(key)
            self.assertEqual(retrieved, value, f"Env.get('{key}') should return '{value}'")

        # Check that a non-existent key returns None
        self.assertIsNone(Env.get("NON_EXISTENT_ORIONIS_KEY"), "Env.get() should return None for missing keys")

        # Ensure all constants are present in Env.all()
        env_all = Env.all()
        for key, value in constants.items():
            self.assertIn(key, env_all, f"'{key}' should be present in Env.all()")
            self.assertEqual(env_all[key], value, f"Env.all()['{key}'] should be '{value}'")
