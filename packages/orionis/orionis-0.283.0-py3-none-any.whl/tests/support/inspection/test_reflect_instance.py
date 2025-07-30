import asyncio
from orionis.support.introspection import Reflection
from orionis.support.introspection.instances import ReflectionInstance
from orionis.test import TestCase
from tests.support.inspection.fakes.fake_reflect_instance import BaseFakeClass, FakeClass

class TestReflectInstance(TestCase):
    """
    Unit tests for the Reflection class.
    """

    async def testReflectionInstanceExceptionValueError(self):
        """Ensure Reflection.instance raises ValueError for invalid types."""
        with self.assertRaises(ValueError):
            Reflection.instance(str)

    async def testReflectionInstance(self):
        """Verify Reflection.instance returns an instance of ReflectionInstance."""
        self.assertIsInstance(Reflection.instance(FakeClass()), ReflectionInstance)

    async def testReflectionInstanceGetClassName(self):
        """Check that getClassName returns the correct class name."""
        reflex = Reflection.instance(FakeClass())
        self.assertEqual(reflex.getClassName(), "FakeClass")

    async def testReflectionInstanceGetClass(self):
        """Ensure getClass returns the correct class."""
        reflex = Reflection.instance(FakeClass())
        self.assertEqual(reflex.getClass(), FakeClass)

    async def testReflectionInstanceGetModuleName(self):
        """Verify getModuleName returns the correct module name."""
        reflex = Reflection.instance(FakeClass())
        self.assertEqual(reflex.getModuleName(), "tests.support.inspection.fakes.fake_reflect_instance")

    async def testReflectionInstanceGetAllAttributes(self):
        """Check that getAllAttributes returns all attributes of the class."""
        reflex = Reflection.instance(FakeClass())
        attributes = reflex.getAllAttributes()
        self.assertTrue("public_attr" in attributes.public)
        self.assertTrue("__private_attr" in attributes.private)
        self.assertTrue("_protected_attr" in attributes.protected)

    async def testReflectionInstanceGetAttributes(self):
        """Check that getAttributes returns all attributes of the class."""
        reflex = Reflection.instance(FakeClass())
        attributes = reflex.getAttributes()
        self.assertTrue("public_attr" in attributes)
        self.assertTrue("__private_attr" in attributes)
        self.assertTrue("dynamic_attr" in attributes)

    async def testReflectionInstanceGetPublicAttributes(self):
        """Ensure getPublicAttributes returns all public attributes."""
        reflex = Reflection.instance(FakeClass())
        attributes = reflex.getPublicAttributes()
        self.assertTrue("public_attr" in attributes)
        self.assertTrue("dynamic_attr" in attributes)

    async def testReflectionInstanceGetProtectedAttributes(self):
        """Check that getProtectedAttributes returns all protected attributes."""
        reflex = Reflection.instance(FakeClass())
        attributes = reflex.getProtectedAttributes()
        self.assertTrue("_protected_attr" in attributes)

    async def testReflectionInstanceGetPrivateAttributes(self):
        """Ensure getPrivateAttributes returns all private attributes."""
        reflex = Reflection.instance(FakeClass())
        attributes = reflex.getPrivateAttributes()
        self.assertTrue("__private_attr" in attributes)

    async def testReflectionInstanceGetAllMethods(self):
        """Check that getAllMethods returns all methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getAllMethods()
        self.assertTrue("__privateMethod" in methods.private)
        self.assertTrue("_protectedMethod" in methods.protected)
        self.assertTrue("asyncMethod" in methods.asynchronous)
        self.assertTrue("classMethod" in methods.class_methods)

    async def testReflectionInstanceGetMethods(self):
        """Ensure getMethods returns all methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getMethods()
        self.assertTrue("__privateMethod" in methods)
        self.assertTrue("_protectedMethod" in methods)
        self.assertTrue("asyncMethod" in methods)
        self.assertTrue("classMethod" in methods)
        self.assertTrue("instanceMethod" in methods)

    async def testReflectionInstanceGetProtectedMethods(self):
        """Check that getProtectedMethods returns all protected methods."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getProtectedMethods()
        self.assertTrue("_protectedMethod" in methods)

    async def testReflectionInstanceGetPrivateMethods(self):
        """Ensure getPrivateMethods returns all private methods."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getPrivateMethods()
        self.assertTrue("__privateMethod" in methods)

    async def testReflectionInstanceGetAsyncMethods(self):
        """Check that getAsyncMethods returns all async methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getAsyncMethods()
        self.assertTrue("asyncMethod" in methods)

    async def testReflectionInstanceGetSyncMethods(self):
        """Check that getASyncMethods returns all async methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getSyncMethods()
        self.assertTrue("__privateMethod" in methods)
        self.assertTrue("_protectedMethod" in methods)
        self.assertTrue("instanceMethod" in methods)

    async def testReflectionInstanceGetClassMethods(self):
        """Verify getClassMethods returns all class methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getClassMethods()
        self.assertTrue("classMethod" in methods)

    async def testReflectionInstanceGetStaticMethods(self):
        """Verify getStaticMethods returns all static methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getStaticMethods()
        self.assertTrue("staticAsyncMethod" in methods)
        self.assertTrue("staticMethod" in methods)

    async def testReflectionInstanceGetAsyncStaticMethods(self):
        """Ensure getSyncMethods returns all sync methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getAsyncStaticMethods()
        self.assertTrue("staticAsyncMethod" in methods)

    async def testReflectionInstanceGetSyncStaticMethods(self):
        """Check that getSyncMethods returns all sync methods of the class."""
        reflex = Reflection.instance(FakeClass())
        methods = reflex.getSyncStaticMethods()
        self.assertTrue("staticMethod" in methods)

    async def testReflectionInstanceGetAllProperties(self):
        """Check that getAllProperties returns all properties of the class."""
        reflex = Reflection.instance(FakeClass())
        properties = reflex.getAllProperties()
        self.assertTrue("computed_property" in properties.keys())

    async def testReflectionInstanceGetPropertyNames(self):
        """Check that getPropertyNames returns all property names."""
        reflex = Reflection.instance(FakeClass())
        properties = reflex.getPropertyNames()
        self.assertTrue("computed_property" in properties)

    async def testReflectionInstanceGetProperty(self):
        """Ensure getProperty retrieves the correct property value."""
        reflex = Reflection.instance(FakeClass())
        property_value = reflex.getProperty("computed_property")
        self.assertEqual(property_value, "Value: 42")

    async def testReflectionInstanceGetPropertyDoc(self):
        """Check that getPropertyDoc returns the correct property docstring."""
        reflex = Reflection.instance(FakeClass())
        doc = reflex.getPropertyDoc("computed_property")
        self.assertIn("A computed property", doc)

    async def testReflectionInstanceGetPropertySignature(self):
        """Ensure getPropertySignature returns the correct property signature."""
        reflex = Reflection.instance(FakeClass())
        signature = reflex.getPropertySignature("computed_property")
        self.assertEqual(str(signature), "(self) -> str")

    async def testReflectionInstanceCallMethod(self):
        """Ensure callMethod correctly invokes a method with arguments."""
        reflex = Reflection.instance(FakeClass())
        result = reflex.callMethod("instanceMethod", 1, 2)
        self.assertEqual(result, 3)
        result = await reflex.callMethod("asyncMethod")
        self.assertEqual(result, "This is async")

    async def testReflectionInstanceGetMethodSignature(self):
        """Verify getMethodSignature returns the correct method signature."""
        reflex = Reflection.instance(FakeClass())
        signature = reflex.getMethodSignature("instanceMethod")
        self.assertEqual(str(signature), "(x: int, y: int) -> int")
        signature = reflex.getMethodSignature("__privateMethod")
        self.assertEqual(str(signature), "() -> str")

    async def testReflectionInstanceGetDocstring(self):
        """Check that getDocstring returns the correct class docstring."""
        reflex = Reflection.instance(FakeClass())
        docstring = reflex.getDocstring()
        self.assertIn("This is a test class for", docstring)

    async def testReflectionInstanceGetBaseClasses(self):
        """Ensure getBaseClasses returns the correct base classes."""
        reflex = Reflection.instance(FakeClass())
        base_classes = reflex.getBaseClasses()
        self.assertIn(BaseFakeClass, base_classes)

    async def testReflectionInstanceIsInstanceOf(self):
        """Verify isInstanceOf checks inheritance correctly."""
        reflex = Reflection.instance(FakeClass())
        result = reflex.isInstanceOf(BaseFakeClass)
        self.assertTrue(result)

    async def testReflectionInstanceGetSourceCode(self):
        """Check that getSourceCode returns the class source code."""
        reflex = Reflection.instance(FakeClass())
        source_code = reflex.getSourceCode()
        self.assertIn("class FakeClass(BaseFakeClass):", source_code)

    async def testReflectionInstanceGetFileLocation(self):
        """Ensure getFileLocation returns the correct file path."""
        reflex = Reflection.instance(FakeClass())
        file_location = reflex.getFileLocation()
        self.assertIn("fake_reflect_instance.py", file_location)

    async def testReflectionInstanceGetAnnotations(self):
        """Verify getAnnotations returns the correct class annotations."""
        reflex = Reflection.instance(FakeClass())
        annotations = reflex.getAnnotations()
        self.assertEqual("{'class_attr': <class 'str'>}", str(annotations))

    async def testReflectionInstanceHasAttribute(self):
        """Check that hasAttribute correctly identifies attributes."""
        reflex = Reflection.instance(FakeClass())
        self.assertTrue(reflex.hasAttribute("public_attr"))
        self.assertFalse(reflex.hasAttribute("non_existent_attr"))

    async def testReflectionInstanceGetAttribute(self):
        """Ensure getAttribute retrieves the correct attribute value."""
        reflex = Reflection.instance(FakeClass())
        attr_value = reflex.getAttribute("public_attr")
        self.assertEqual(attr_value, 42)
        attr_value = reflex.getAttribute("__private_attr")
        self.assertEqual(attr_value, "private")

    async def testReflectionInstanceSetAttribute(self):
        """Check that setAttribute correctly sets a new attribute."""
        reflex = Reflection.instance(FakeClass())
        reflex.setAttribute("new_attr", 'Orionis')
        attr_value = reflex.getAttribute("new_attr")
        self.assertEqual(attr_value, 'Orionis')
        reflex.setAttribute("__new_private_attr", 'Hidden')
        attr_value = reflex.getAttribute("__new_private_attr")
        self.assertEqual(attr_value, 'Hidden')

    async def testReflectionInstanceRemoveAttribute(self):
        """Ensure removeAttribute correctly removes an attribute."""
        reflex = Reflection.instance(FakeClass())
        reflex.setAttribute("temp_attr", 'Temporary')
        reflex.removeAttribute("temp_attr")
        self.assertFalse(reflex.hasAttribute("temp_attr"))

    async def testReflectionInstanceSetMacro(self):
        """Check that setMacro correctly."""
        async def asyncMacro(cls: FakeClass, num):
            await asyncio.sleep(0.1)
            return cls.instanceMethod(10, 12) + num
        def syncMacro(cls: FakeClass, num):
            return cls.instanceMethod(10, 12) + num
        def __privateMacro(cls: FakeClass, num):
            return cls.instanceMethod(10, 12) + num

        reflex = Reflection.instance(FakeClass())

        reflex.setMacro("asyncMacro", asyncMacro)
        result = await reflex.callMethod("asyncMacro", reflex._instance, 3)
        self.assertEqual(result, 25)

        reflex.setMacro("syncMacro", syncMacro)
        result = reflex.callMethod("syncMacro", reflex._instance, 3)
        self.assertEqual(result, 25)

        reflex.setMacro("__privateMacro", __privateMacro)
        result = reflex.callMethod("__privateMacro", reflex._instance, 3)
        self.assertEqual(result, 25)

    async def testReflectionInstanceRemoveMacro(self):
        """Ensure removeMacro correctly removes a macro."""
        async def asyncMacro(cls: FakeClass, num):
            await asyncio.sleep(0.1)
            return cls.instanceMethod(10, 12) + num

        reflex = Reflection.instance(FakeClass())
        reflex.setMacro("asyncMacro", asyncMacro)
        reflex.removeMacro("asyncMacro")
        with self.assertRaises(Exception):
            await reflex.callMethod("asyncMacro", reflex._instance, 3)
