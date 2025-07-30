
from orionis.foundation.config.cors.entities.cors import Cors
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.unittesting import TestCase

class TestCorsConfig(TestCase):
    """
    Unit tests for Cors configuration defaults and validation.
    """

    async def testDefaultValues(self):
        """
        Test the default values of the Cors configuration.

        This test verifies that a newly instantiated Cors object has the following default settings:
        - allow_origins: ["*"]
        - allow_origin_regex: None
        - allow_methods: ["*"]
        - allow_headers: ["*"]
        - expose_headers: []
        - allow_credentials: False
        - max_age: 600
        """
        cors = Cors()
        self.assertEqual(cors.allow_origins, ["*"])
        self.assertIsNone(cors.allow_origin_regex)
        self.assertEqual(cors.allow_methods, ["*"])
        self.assertEqual(cors.allow_headers, ["*"])
        self.assertEqual(cors.expose_headers, [])
        self.assertFalse(cors.allow_credentials)
        self.assertEqual(cors.max_age, 600)

    async def testCustomValues(self):
        """
        Test that the Cors configuration correctly sets custom values for all parameters.

        This test verifies that:
        - `allow_origins` is set to the provided list of origins.
        - `allow_origin_regex` is set to the provided regex pattern.
        - `allow_methods` is set to the provided list of HTTP methods.
        - `allow_headers` is set to the provided list of headers.
        - `expose_headers` is set to the provided list of exposed headers.
        - `allow_credentials` is set to True.
        - `max_age` is set to the provided integer value.

        Ensures that the Cors object accurately reflects the custom configuration values.
        """
        cors = Cors(
            allow_origins=["https://example.com"],
            allow_origin_regex="^https://.*\\.example\\.com$",
            allow_methods=["GET", "POST"],
            allow_headers=["Authorization", "Content-Type"],
            expose_headers=["X-Custom-Header"],
            allow_credentials=True,
            max_age=3600
        )
        self.assertEqual(cors.allow_origins, ["https://example.com"])
        self.assertEqual(cors.allow_origin_regex, "^https://.*\\.example\\.com$")
        self.assertEqual(cors.allow_methods, ["GET", "POST"])
        self.assertEqual(cors.allow_headers, ["Authorization", "Content-Type"])
        self.assertEqual(cors.expose_headers, ["X-Custom-Header"])
        self.assertTrue(cors.allow_credentials)
        self.assertEqual(cors.max_age, 3600)

    async def testInvalidAllowOriginsType(self):
        """
        Test that passing a string instead of a list to the 'allow_origins' parameter of the Cors class
        raises an OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_origins="*")

    async def testInvalidAllowOriginRegexType(self):
        """
        Test that passing a non-string, non-None value (specifically an integer) to the
        `allow_origin_regex` parameter of the `Cors` class raises an OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_origin_regex=123)

    async def testInvalidAllowMethodsType(self):
        """
        Test that initializing the Cors class with an invalid type for 'allow_methods' raises an OrionisIntegrityException.

        This test verifies that passing a string instead of a list to the 'allow_methods' parameter
        of the Cors class triggers the expected exception, ensuring type validation is enforced.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_methods="GET")

    async def testInvalidAllowHeadersType(self):
        """
        Test that initializing the Cors class with a non-list type for 'allow_headers' (specifically a string)
        raises an OrionisIntegrityException, ensuring type validation for the 'allow_headers' parameter.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_headers="Authorization")

    async def testInvalidExposeHeadersType(self):
        """
        Test that initializing the Cors class with a non-list type for 'expose_headers'
        raises an OrionisIntegrityException. Ensures type validation for the 'expose_headers' parameter.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(expose_headers="X-Custom-Header")

    async def testInvalidAllowCredentialsType(self):
        """
        Test that initializing the Cors class with a non-boolean value for 'allow_credentials'
        raises an OrionisIntegrityException, ensuring type validation for the parameter.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(allow_credentials="yes")

    async def testInvalidMaxAgeType(self):
        """
        Test that passing a non-integer value (specifically a string) to the `max_age` parameter of the `Cors` class
        raises an `OrionisIntegrityException`. This ensures that `max_age` only accepts integer or None values.
        """
        with self.assertRaises(OrionisIntegrityException):
            Cors(max_age="3600")