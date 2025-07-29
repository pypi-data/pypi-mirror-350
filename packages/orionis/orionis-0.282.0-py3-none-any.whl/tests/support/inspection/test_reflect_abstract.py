from abc import ABC
import json
from orionis.support.introspection.reflection import Reflection
from orionis.test import TestCase
from tests.support.inspection.fakes.fake_reflect_abstract import FakeAbstractClass

class TestReflectAbstract(TestCase):
    """Test cases for ReflexionAbstract using FakeAbstractClass.

    This test suite verifies all functionality of the ReflexionAbstract class
    using FakeAbstractClass as the test subject.
    """

    async def testReflectionAbstractExceptionValueError(self):
        """Class setup method.

        Initializes the ReflexionAbstract instance with FakeAbstractClass
        before any tests run.
        """
        with self.assertRaises(ValueError):
            Reflection.abstract(str)

    async def testReflectionAbstractGetClassName(self):
        """Test getClassName() method.

        Verifies that:
        - The returned class name matches exactly
        - The return type is str
        """
        class_name = Reflection.abstract(FakeAbstractClass).getClassName()
        self.assertEqual(class_name, "FakeAbstractClass")
        self.assertIsInstance(class_name, str)

    async def testReflectionAbstractGetModuleName(self):
        """Test getModuleName() method.

        Verifies that:
        - The module name is returned
        - The name is a string
        """
        module_name = Reflection.abstract(FakeAbstractClass).getModuleName()
        self.assertTrue(module_name == 'tests.support.inspection.fakes.fake_reflect_abstract')
        self.assertIsInstance(module_name, str)

    async def testReflectionAbstractGetClass(self):
        """
        Test the `getClass()` method of the `Reflection.abstract` function.
        This test verifies the following:
        - The method raises a `RuntimeError` when attempting to retrieve a class
          from an abstract class.
        - Ensures that the behavior aligns with the expected handling of abstract
          classes in the reflection mechanism.
        """
        with self.assertRaises(RuntimeError):
            Reflection.abstract(FakeAbstractClass).getClass()

    async def testReflectionAbstractGetAllAttributes(self):
        """Test getAllAttributes() method.

        Verifies that:
        - All attributes are detected
        - No private/protected attributes are included
        - Return type is correct
        """
        attributes = Reflection.abstract(FakeAbstractClass).getAllAttributes()
        self.assertIn('__private_class_attribute', attributes.private)
        self.assertIn('_protected_class_attribute', attributes.protected)
        self.assertIn('public_class_attribute', attributes.public)

    async def testReflectionAbstractGetAttribute(self):
        """Test getAttribute() method.

        Verifies that:
        - Correct attribute is returned
        - Attribute type is correct
        """
        attr = Reflection.abstract(FakeAbstractClass).getAttributes()
        self.assertIn('__private_class_attribute', attr)
        self.assertIn('_protected_class_attribute', attr)
        self.assertIn('public_class_attribute', attr)

    async def testReflectionAbstractGetPublicAttributes(self):
        """Test getPublicAttributes() method.

        Verifies that:
        - Only public attributes are returned
        - No private/protected attributes are included
        """
        public_attributes = Reflection.abstract(FakeAbstractClass).getPublicAttributes()
        self.assertIn('public_class_attribute', public_attributes)
        self.assertNotIn('_protected_class_attribute', public_attributes)
        self.assertNotIn('__private_class_attribute', public_attributes)

    async def testReflectionAbstractGetProtectedAttributes(self):
        """Test getProtectedAttributes() method.

        Verifies that:
        - Only protected attributes are returned
        - No private/public attributes are included
        """
        protected_attributes = Reflection.abstract(FakeAbstractClass).getProtectedAttributes()
        self.assertIn('_protected_class_attribute', protected_attributes)
        self.assertNotIn('__private_class_attribute', protected_attributes)
        self.assertNotIn('public_class_attribute', protected_attributes)

    async def testReflectionAbstractGetPrivateAttributes(self):
        """Test getPrivateAttributes() method.

        Verifies that:
        - Only private attributes are returned
        - No protected/public attributes are included
        """
        private_attributes = Reflection.abstract(FakeAbstractClass).getPrivateAttributes()
        self.assertIn('__private_class_attribute', private_attributes)
        self.assertNotIn('_protected_class_attribute', private_attributes)
        self.assertNotIn('public_class_attribute', private_attributes)

    async def testReflectionAbstractGetAllMethods(self):
        """Test getAllMethods() method.

        Verifies that:
        - All methods are detected
        - No private/protected methods are included
        - Return type is correct
        """
        methods = Reflection.abstract(FakeAbstractClass).getAllMethods()
        self.console().info(message="Hola")
        # self.print(Reflection.abstract(FakeAbstractClass).getAllAttributes())
        # self.dd(json.dumps(methods, indent=4))











    # async def testReflectionAbstractGetAbstractMethods(self):
    #     """Test getAbstractMethods() method.

    #     Verifies that:
    #     - All abstract methods are detected
    #     - No concrete methods are included
    #     - Return type is correct
    #     """
    #     methods = Reflection.abstract(FakeAbstractClass).getAbstractMethods()
    #     expected = {'abstract_method', 'another_abstract'}
    #     self.assertEqual(methods, expected)
    #     self.assertIsInstance(methods, set)

    # async def testReflectionAbstractGetConcreteMethods(self):
    #     """Test getConcreteMethods() method.

    #     Verifies that:
    #     - Concrete methods are detected
    #     - Abstract methods are excluded
    #     - Protected/private methods are excluded
    #     """
    #     methods = Reflection.abstract(FakeAbstractClass).getConcreteMethods()
    #     self.assertIn('static_helper', methods)
    #     self.assertIn('concrete_method', methods)
    #     self.assertIn('decorated_method', methods)
    #     self.assertNotIn('abstract_method', methods)
    #     self.assertNotIn('_protected_method', methods)
    #     self.assertNotIn('__private_method', methods)

    # async def testReflectionAbstractGetStaticMethods(self):
    #     """Test getStaticMethods() method.

    #     Verifies that:
    #     - Static methods are detected
    #     - Only static methods are included
    #     - Protected/private methods are excluded
    #     """
    #     static_methods = Reflection.abstract(FakeAbstractClass).getStaticMethods()
    #     self.assertIn('static_helper', static_methods)
    #     self.assertEqual(len(static_methods), 1)
    #     self.assertNotIn('create_instance', static_methods)

    # async def testReflectionAbstractGetClassMethods(self):
    #     """Test getClassMethods() method.

    #     Verifies that:
    #     - Class methods are detected
    #     - Only class methods are included
    #     - Protected/private methods are excluded
    #     """
    #     class_methods = Reflection.abstract(FakeAbstractClass).getClassMethods()
    #     self.assertIn('create_instance', class_methods)
    #     self.assertEqual(len(class_methods), 1)
    #     self.assertNotIn('static_helper', class_methods)

    # async def testReflectionAbstractGetProperties(self):
    #     """Test getProperties() method.

    #     Verifies that:
    #     - Properties are detected
    #     - Only properties are included
    #     - Protected/private properties are excluded
    #     """
    #     props = Reflection.abstract(FakeAbstractClass).getProperties()
    #     self.assertIn('computed_property', props)
    #     self.assertEqual(len(props), 1)

    # async def testReflectionAbstractGetMethodSignature(self):
    #     """Test getMethodSignature() method.

    #     Verifies that:
    #     - Correct signature is returned
    #     - Parameters are properly detected
    #     - Return type is properly detected
    #     """
    #     sig = Reflection.abstract(FakeAbstractClass).getMethodSignature('abstract_method')
    #     params = list(sig.parameters.keys())
    #     self.assertEqual(params, ['self', 'x', 'y'])
    #     self.assertEqual(sig.return_annotation, int)

    # async def testReflectionAbstractGetDocstring(self):
    #     """Test getDocstring() method.

    #     Verifies that:
    #     - Docstring is returned
    #     - Docstring contains expected content
    #     """
    #     doc = Reflection.abstract(FakeAbstractClass).getDocstring()
    #     self.assertTrue(doc.startswith("A fake abstract class"))
    #     self.assertIsInstance(doc, str)

    # async def testReflectionAbstractGetBaseAbstractClasses(self):
    #     """Test getBaseAbstractClasses() method.

    #     Verifies that:
    #     - Base abstract classes are detected
    #     - Only abstract bases are included
    #     """
    #     bases = Reflection.abstract(FakeAbstractClass).getBaseAbstractClasses()
    #     self.assertEqual(bases, (ABC,))

    # async def testReflectionAbstractGetInterfaceMethods(self):
    #     """Test getInterfaceMethods() method.

    #     Verifies that:
    #     - Interface methods are detected
    #     - Signatures are correct
    #     - Only abstract methods are included
    #     """
    #     interface = Reflection.abstract(FakeAbstractClass).getInterfaceMethods()
    #     self.assertEqual(len(interface), 2)
    #     self.assertIn('abstract_method', interface)
    #     sig = interface['abstract_method']
    #     self.assertEqual(list(sig.parameters.keys()), ['self', 'x', 'y'])

    # async def testReflectionAbstractIsSubclassOf(self):
    #     """Test isSubclassOf() method.

    #     Verifies that:
    #     - Correctly identifies abstract base classes
    #     - Returns False for non-parent classes
    #     """
    #     self.assertTrue(Reflection.abstract(FakeAbstractClass).isSubclassOf(ABC))
    #     self.assertTrue(Reflection.abstract(FakeAbstractClass).isSubclassOf(object))

    # async def testReflectionAbstractGetSourceCode(self):
    #     """Test getSourceCode() method.

    #     Verifies that:
    #     - Source code is returned
    #     - Contains class definition
    #     """
    #     source = Reflection.abstract(FakeAbstractClass).getSourceCode()
    #     self.assertIsNotNone(source)
    #     self.assertIn("class FakeAbstractClass(ABC):", source)

    # async def testReflectionAbstractGetFileLocation(self):
    #     """Test getFileLocation() method.

    #     Verifies that:
    #     - File location is returned
    #     - Path ends with .py extension
    #     """
    #     location = Reflection.abstract(FakeAbstractClass).getFileLocation()
    #     self.assertIsNotNone(location)
    #     self.assertTrue('fake_reflection_abstract.py' in location)

    # async def testReflectionAbstractGetAnnotations(self):
    #     """Test getAnnotations() method.

    #     Verifies that:
    #     - Annotations are detected
    #     - Class attributes are included
    #     """
    #     annotations = Reflection.abstract(FakeAbstractClass).getAnnotations()
    #     self.assertIn('class_attr', annotations)
    #     self.assertEqual(annotations['class_attr'], str)

    # async def testReflectionAbstractGetDecorators(self):
    #     """Test getDecorators() method.

    #     Verifies that:
    #     - Decorators are detected
    #     - Correct number of decorators is returned
    #     - Decorator order is preserved
    #     """
    #     decorators = Reflection.abstract(FakeAbstractClass).getDecorators('decorated_method')
    #     for decorator in decorators:
    #         self.assertTrue(decorator in ['decorator_example', 'another_decorator'])

    # async def testReflectionAbstractIsProtocol(self):
    #     """Test isProtocol() method.

    #     Verifies that:
    #     - Correctly identifies non-Protocol classes
    #     """
    #     self.assertFalse(Reflection.abstract(FakeAbstractClass).isProtocol())

    # async def testReflectionAbstractGetRequiredAttributes(self):
    #     """Test getRequiredAttributes() method.

    #     Verifies that:
    #     - Returns empty set for non-Protocol classes
    #     """
    #     self.assertEqual(Reflection.abstract(FakeAbstractClass).getRequiredAttributes(), set())

    # async def testReflectionAbstractGetAbstractProperties(self):
    #     """Test getRequiredMethods() method."""
    #     self.assertEqual(Reflection.abstract(FakeAbstractClass).getAbstractProperties(), set())

    # async def testReflectionAbstractGetPropertySignature(self):
    #     """Test getPropertySignature() method."""
    #     signature = Reflection.abstract(FakeAbstractClass).getPropertySignature('computed_property')
    #     self.assertEqual(str(signature), '(self) -> float')