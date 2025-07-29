
from orionis.foundation.config.auth.entities.auth import Auth
from orionis.unittesting import TestCase

class TestConfigApp(TestCase):
    """
    Test suite for verifying the behavior of the Auth configuration within the application.
    This class contains asynchronous test cases to ensure that the Auth object
    correctly handles the assignment and retrieval of new attribute values.
    """

    async def testNewValue(self):
        """
        Test that the default name of the App instance is 'Orionis Application'.

        This test creates a new App object and asserts that its 'name' attribute
        is set to the expected default value.
        """
        auth = Auth()
        auth.new_value = 'new_value'
        auth.new_value2 = 'new_value2'

        self.assertEqual(auth.new_value, 'new_value')
        self.assertEqual(auth.new_value2, 'new_value2')