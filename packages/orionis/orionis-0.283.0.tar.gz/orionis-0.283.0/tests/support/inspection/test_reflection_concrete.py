from orionis.support.introspection.reflection import Reflection
from orionis.support.introspection.reflexion_concrete import ReflexionConcrete
from orionis.test import TestCase
from tests.support.inspection.fakes.fake_reflection_concrete import BaseExample, FakeExample

class TestReflectionConcrete(TestCase):
    """
    Unit tests for the Reflection class.
    """

    async def testReflectionConcreteExceptionValueError(self):
        """Ensure Reflection.instance raises ValueError for invalid types."""
        with self.assertRaises(ValueError):
            Reflection.concrete(str)

    async def testReflectionConcrete(self):
        """Verify Reflection.instance returns an instance of ReflexionInstance."""
        self.assertIsInstance(Reflection.concrete(FakeExample), ReflexionConcrete)

    async def testReflectionConcreteGetClassName(self):
        """Test getClassName method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getClassName(), "FakeExample")

    async def testReflectionConcreteGetClass(self):
        """Test getClass method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getClass(), FakeExample)

    async def testReflectionConcreteGetModuleName(self):
        """Test getModuleName method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getModuleName(), "tests.support.inspection.fakes.fake_reflection_concrete")

    async def testReflectionConcreteGetAttributes(self):
        """Test getAttributes method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getAttributes(), {'class_attr': 42, 'another_attr': 'hello'})

    async def testReflectionConcreteGetMethods(self):
        """Test getMethods method."""
        reflection = Reflection.concrete(FakeExample)
        expected_methods = [
            'baseMethod',
            'method_one',
            'method_two',
            'static_method',
        ]
        self.assertEqual(reflection.getMethods(), expected_methods)

    async def testReflectionConcreteGetStaticMethods(self):
        """Test getStaticMethods method."""
        reflection = Reflection.concrete(FakeExample)
        expected_static_methods = [
            'static_method'
        ]
        self.assertEqual(reflection.getStaticMethods(), expected_static_methods)

    async def testReflectionConcreteGetPropertyNames(self):
        """Test getPropertyNames method."""
        reflection = Reflection.concrete(FakeExample)
        expected_properties = [
            'prop',
            'prop_with_getter',
        ]
        self.assertEqual(reflection.getPropertyNames(), expected_properties)

    async def testReflectionConcreteGetMethodSignature(self):
        """Test getMethodSignature method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(str(reflection.getMethodSignature('method_one')), '(self, x: int) -> int')
        self.assertEqual(str(reflection.getMethodSignature('method_two')), '(self, a: str, b: str = \'default\') -> str')
        self.assertEqual(str(reflection.getMethodSignature('__init__')), '(self, value: int = 10) -> None')

    async def testReflectionConcreteGetPropertySignature(self):
        """Test getPropertySignature method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(str(reflection.getPropertySignature('prop')), '(self) -> int')
        self.assertEqual(str(reflection.getPropertySignature('prop_with_getter')), '(self) -> str')

    async def testReflectionConcreteGetDocstring(self):
        """Test getDocstring method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertIn('This is a fake example class for testing reflection', reflection.getDocstring())

    async def testReflectionConcreteGetBaseClasses(self):
        """Test getBaseClasses method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getBaseClasses(), (BaseExample,))

    async def testReflectionConcreteIsSubclassOf(self):
        """Test isSubclassOf method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertTrue(reflection.isSubclassOf(BaseExample))
        self.assertFalse(reflection.isSubclassOf(str))

    async def testReflectionConcreteGetSourceCode(self):
        """Test getSourceCode method."""
        reflection = Reflection.concrete(FakeExample)
        source_code = reflection.getSourceCode()
        self.assertIn('class FakeExample(BaseExample):', source_code)
        self.assertIn('def method_one(self, x: int) -> int:', source_code)

    async def testReflectionConcreteGetFileLocation(self):
        """Test getFileLocation method."""
        reflection = Reflection.concrete(FakeExample)
        file_location = reflection.getFileLocation()
        self.assertIn('tests', file_location)
        self.assertIn('support', file_location)
        self.assertIn('inspection', file_location)
        self.assertIn('fakes', file_location)
        self.assertIn('fake_reflection_concrete.py', file_location)

    async def testReflectionConcreteGetAnnotations(self):
        """Test getAnnotations method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getAnnotations(), {'class_attr': int})

    async def testReflectionConcreteHasAttribute(self):
        """Test hasAttribute method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertTrue(reflection.hasAttribute('class_attr'))
        self.assertFalse(reflection.hasAttribute('non_existent_attr'))

    async def testReflectionConcreteGetAttribute(self):
        """Test getAttribute method."""
        reflection = Reflection.concrete(FakeExample)
        self.assertEqual(reflection.getAttribute('class_attr'), 42)
        with self.assertRaises(AttributeError):
            reflection.getAttribute('non_existent_attr')

    async def testReflectionConcreteGetCallableMembers(self):
        """Test getCallableMembers method."""
        reflection = Reflection.concrete(FakeExample)
        callable_members = reflection.getCallableMembers()
        self.assertIn('_private_method', callable_members)
        self.assertIn('_private_static', callable_members)
        self.assertIn('baseMethod', callable_members)
        self.assertIn('class_method', callable_members)
        self.assertIn('method_one', callable_members)
        self.assertIn('method_two', callable_members)
        self.assertIn('static_method', callable_members)