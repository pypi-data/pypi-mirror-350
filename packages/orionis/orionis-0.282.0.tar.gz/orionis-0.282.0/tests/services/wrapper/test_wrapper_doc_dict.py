from orionis.services.wrapper.dicts.dot_dict import DotDict
from orionis.unittesting import TestCase

class TestDotDict(TestCase):
    """
    Test cases for the DotDict class which provides dictionary with dot notation access.
    """

    async def testDotNotationAccess(self):
        """
        Test that dictionary values can be accessed using dot notation.
        Verifies that both existing and non-existing keys can be accessed via dot notation,
        with None returned for missing keys.
        """
        dd = DotDict({'key1': 'value1', 'nested': {'inner': 42}})
        self.assertEqual(dd.key1, 'value1')
        self.assertEqual(dd.nested.inner, 42)
        self.assertIsNone(dd.non_existent)

    async def testDotNotationAssignment(self):
        """
        Test that dictionary values can be set using dot notation.
        Verifies that new keys can be added and existing keys can be updated using dot notation,
        with automatic conversion of nested dictionaries to DotDict.
        """
        dd = DotDict()
        dd.key1 = 'value1'
        dd.nested = {'inner': 42}

        self.assertEqual(dd['key1'], 'value1')
        self.assertIsInstance(dd.nested, DotDict)
        self.assertEqual(dd.nested.inner, 42)

    async def testDotNotationDeletion(self):
        """
        Test that dictionary keys can be deleted using dot notation.
        Verifies that existing keys can be deleted and appropriate AttributeError is raised
        when trying to delete non-existent keys.
        """
        dd = DotDict({'key1': 'value1', 'key2': 'value2'})
        del dd.key1
        self.assertNotIn('key1', dd)

        with self.assertRaises(AttributeError):
            del dd.non_existent

    async def testGetMethod(self):
        """
        Test that the get method works with automatic DotDict conversion.
        Verifies that the get method returns the correct value or default,
        and converts nested dictionaries to DotDict instances.
        """
        dd = DotDict({'key1': 'value1', 'nested': {'inner': 42}})

        self.assertEqual(dd.get('key1'), 'value1')
        self.assertEqual(dd.get('non_existent', 'default'), 'default')
        self.assertIsInstance(dd.get('nested'), DotDict)
        self.assertEqual(dd.get('nested').inner, 42)

    async def testExportMethod(self):
        """
        Test that the export method converts to regular dictionary recursively.
        Verifies that all nested DotDict instances are converted back to regular dicts.
        """
        dd = DotDict({
            'key1': 'value1',
            'nested': DotDict({
                'inner': 42,
                'deep': DotDict({'a': 1})
            })
        })

        exported = dd.export()
        self.assertIsInstance(exported, dict)
        self.assertIsInstance(exported['nested'], dict)
        self.assertIsInstance(exported['nested']['deep'], dict)
        self.assertEqual(exported['nested']['inner'], 42)

    async def testCopyMethod(self):
        """
        Test that the copy method creates a deep copy with DotDict conversion.
        Verifies that the copy is independent of the original and maintains DotDict structure.
        """
        original = DotDict({
            'key1': 'value1',
            'nested': {'inner': 42}
        })

        copied = original.copy()
        copied.key1 = 'modified'
        copied.nested.inner = 100

        self.assertEqual(original.key1, 'value1')
        self.assertEqual(original.nested.inner, 42)
        self.assertEqual(copied.key1, 'modified')
        self.assertEqual(copied.nested.inner, 100)
        self.assertIsInstance(copied.nested, DotDict)

    async def testNestedDictConversion(self):
        """
        Test that nested dictionaries are automatically converted to DotDict.
        Verifies that nested dicts are converted both during initialization and assignment.
        """
        dd = DotDict({
            'level1': {
                'level2': {
                    'value': 42
                }
            }
        })

        self.assertIsInstance(dd.level1, DotDict)
        self.assertIsInstance(dd.level1.level2, DotDict)
        self.assertEqual(dd.level1.level2.value, 42)

        # Test dynamic assignment
        dd.new_nested = {'a': {'b': 1}}
        self.assertIsInstance(dd.new_nested, DotDict)
        self.assertIsInstance(dd.new_nested.a, DotDict)

    async def testReprMethod(self):
        """
        Test that the string representation correctly identifies as DotDict.
        Verifies that the __repr__ method includes the DotDict prefix.
        """
        dd = DotDict({'key': 'value'})
        self.assertTrue(repr(dd).startswith('DotDict({'))
        self.assertTrue(repr(dd).endswith('})'))
        self.assertIn("'key': 'value'", repr(dd))
