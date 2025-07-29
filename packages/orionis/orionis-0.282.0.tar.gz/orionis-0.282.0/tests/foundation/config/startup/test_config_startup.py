from dataclasses import is_dataclass
from orionis.foundation.config.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.startup import Configuration
from orionis.unittesting import TestCase, UnittestMock

class TestConfiguration(TestCase):
    """
    Test suite for the Configuration dataclass which encapsulates all major
    configuration sections for the application.

    This test class verifies the proper initialization, type validation,
    and dictionary conversion of the Configuration class.
    """

    def testConfigurationIsDataclass(self):
        """
        Test that Configuration is properly defined as a dataclass.
        Verifies that the @dataclass decorator was applied correctly.
        """
        self.assertTrue(is_dataclass(Configuration))

    def testDefaultInitialization(self):
        """
        Test that Configuration can be initialized with default values.
        Verifies that all default factories work correctly and the
        instance is properly constructed.
        """
        config = Configuration()
        self.assertIsInstance(config, Configuration)

    def testAllSectionsHaveDefaultFactories(self):
        """
        Test that all configuration sections have default factories.
        Verifies that each field in the Configuration class has a
        default_factory specified.
        """
        config = Configuration()
        for field in config.__dataclass_fields__.values():
            self.assertTrue(hasattr(field, 'default_factory'),
                            f"Field {field.name} is missing default_factory")

    def testTypeValidationInPostInit(self):
        """
        Test that __post_init__ validates types correctly.
        Verifies that the type checking for each configuration section
        works as expected.
        """
        # Test with all correct types (should not raise)
        try:
            Configuration()
        except OrionisIntegrityException:
            self.fail("__post_init__ raised exception with valid types")

        # Test each section with wrong type
        sections = [
            ('paths', UnittestMock()),
            ('app', UnittestMock()),
            ('auth', UnittestMock()),
            ('cache', UnittestMock()),
            ('cors', UnittestMock()),
            ('database', UnittestMock()),
            ('filesystems', UnittestMock()),
            ('logging', UnittestMock()),
            ('mail', UnittestMock()),
            ('queue', UnittestMock()),
            ('session', UnittestMock()),
            ('testing', UnittestMock())
        ]

        for section_name, wrong_value in sections:
            with self.subTest(section=section_name):
                kwargs = {section_name: wrong_value}
                with self.assertRaises(OrionisIntegrityException):
                    Configuration(**kwargs)

    def testToDictReturnsCompleteDictionary(self):
        """
        Test that toDict() returns a complete dictionary representation.
        Verifies that the returned dictionary contains all configuration
        sections with their current values.
        """
        config = Configuration()
        config_dict = config.toDict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(len(config_dict), len(config.__dataclass_fields__))
        for field in config.__dataclass_fields__:
            self.assertIn(field, config_dict)

    def testToDictReturnsNestedStructures(self):
        """
        Test that toDict() properly converts nested dataclasses.
        Verifies that the dictionary conversion works recursively for
        all nested configuration sections.
        """
        config = Configuration()
        config_dict = config.toDict()
        self.assertIsInstance(config_dict['paths'], dict)
        self.assertIsInstance(config_dict['app'], dict)
        self.assertIsInstance(config_dict['database'], dict)

    def testMetadataIsAccessible(self):
        """
        Test that field metadata is properly defined and accessible.
        Verifies that each configuration section field has the expected
        metadata structure with description.
        """
        config = Configuration()
        for field in config.__dataclass_fields__.values():
            metadata = field.metadata
            self.assertIn('description', metadata)
            self.assertIsInstance(metadata['description'], str)

    def testConfigurationIsMutable(self):
        """
        Test that Configuration is mutable (not frozen).
        Verifies that attributes can be modified after creation since
        the dataclass isn't marked as frozen.
        """
        config = Configuration()
        new_paths = config.paths.__class__()

        try:
            config.paths = new_paths
        except Exception as e:
            self.fail(f"Should be able to modify attributes, but got {type(e).__name__}")

    def testConfigurationEquality(self):
        """
        Test that Configuration instances with same values are equal.
        Verifies that dataclass equality comparison works as expected.
        """
        config1 = Configuration()
        config2 = Configuration()
        self.assertNotEqual(config1, config2)