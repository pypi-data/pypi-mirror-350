import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from orionis.support.asynchrony.async_io import AsyncIO
from orionis.support.introspection.dependencies import ReflectDependencies
from orionis.support.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.support.introspection.dependencies.entities.method_dependencies import MethodDependency
from orionis.support.introspection.instances.contracts.reflection_instance import IReflectionInstance
from orionis.support.introspection.instances.entities.class_attributes import ClassAttributes
from orionis.support.introspection.instances.entities.class_method import ClassMethod
from orionis.support.introspection.instances.entities.class_parsed import ClassParsed
from orionis.support.introspection.instances.entities.class_property import ClassProperty

class ReflectionInstance(IReflectionInstance):
    """
    A reflection object encapsulating a class instance.

    Parameters
    ----------
    instance : Any
        The instance being reflected upon

    Attributes
    ----------
    _instance : Any
        The encapsulated instance
    """

    def __init__(self, instance: Any) -> None:
        """Initialize with the instance to reflect upon."""
        self._instance = instance

    def parse(self) -> ClassParsed:
        """
        Parse the instance into a structured representation.

        This method extracts and organizes various details about the instance,
        including its class name, module, attributes, methods, and properties,
        into a `ClassParsed` object.

        Returns
        -------
        ClassParsed
            A structured representation of the instance, containing:
            - name: The name of the instance's class.
            - module: The module where the class is defined.
            - attributes: Categorized attributes (public, private, protected).
            - methods: Categorized methods (public, private, protected, static, etc.).
            - properties: A dictionary of properties with their details.
        """
        return ClassParsed(
            name=self.getClassName(),
            module=self.getModuleName(),
            attributes=self.getAllAttributes(),
            methods=self.getAllMethods(),
            properties=list(self.getAllProperties().values()),
            dependencies=self.getConstructorDependencies()
        )

    def getClassName(self) -> str:
        """
        Get the name of the instance's class.

        Returns
        -------
        str
            The name of the class
        """
        return self._instance.__class__.__name__

    def getClass(self) -> Type:
        """
        Get the class of the instance.

        Returns
        -------
        Type
            The class object of the instance
        """
        return self._instance.__class__

    def getModuleName(self) -> str:
        """
        Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        return self._instance.__class__.__module__

    def getAllAttributes(self) -> ClassAttributes:
        """
        Get all attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        attributes: dict = vars(self._instance)
        class_name: str = self.getClassName()
        public = {}
        private = {}
        protected = {}

        for attr, value in attributes.items():
            if (str(attr).startswith("__") and str(attr).endswith("__")):
                continue
            if str(attr).startswith("_") and not str(attr).startswith("__") and not str(attr).startswith(f"_{class_name}"):
                protected[attr] = value
            elif str(attr).startswith(f"_{class_name}"):
                private[str(attr).replace(f"_{class_name}", "")] = value
            else:
                public[attr] = value

        return ClassAttributes(
            public=public,
            private=private,
            protected=protected
        )

    def getAttributes(self) -> Dict[str, Any]:
        """
        Get all attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        attr = self.getAllAttributes()
        return {**attr.public, **attr.private, **attr.protected}

    def getPublicAttributes(self) -> Dict[str, Any]:
        """
        Get all public attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of public attribute names and their values
        """
        attr = self.getAllAttributes()
        return attr.public

    def getPrivateAttributes(self) -> Dict[str, Any]:
        """
        Get all private attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of private attribute names and their values
        """
        attr = self.getAllAttributes()
        return attr.private

    def getProtectedAttributes(self) -> Dict[str, Any]:
        """
        Get all Protected attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of Protected attribute names and their values
        """
        attr = self.getAllAttributes()
        return attr.protected

    def getAllMethods(self):
        """
        Retrieves and categorizes all methods of the instance's class into various classifications.
        This method inspects the instance's class and its methods, categorizing them into public, private,
        protected, static, asynchronous, synchronous, class methods, asynchronous static, synchronous static,
        and magic methods.
        Returns
        -------
        ClassMethod
            An object containing categorized lists of method names:
            - public: List of public instance methods.
            - private: List of private instance methods (names without the class prefix).
            - protected: List of protected instance methods.
            - static: List of static methods.
            - asynchronous: List of asynchronous instance methods.
            - synchronous: List of synchronous instance methods.
            - class_methods: List of class methods.
            - asynchronous_static: List of asynchronous static methods.
            - synchronous_static: List of synchronous static methods.
            - magic: List of magic methods (e.g., `__init__`, `__str__`).
        Notes
        -----
        - Magic methods are identified by their double underscore prefix and suffix (e.g., `__init__`).
        - Private methods are identified by a single underscore followed by the class name.
        - Protected methods are identified by a single underscore prefix.
        - Public methods are identified as methods without any leading underscores.
        - Static and class methods are identified using `inspect.getattr_static`.
        - Asynchronous methods are identified using `inspect.iscoroutinefunction`.
        - Synchronous methods are identified as methods that are not asynchronous, static, or class methods.
        """
        class_name = self.getClassName()
        cls = self._instance.__class__

        result = ClassMethod(
            public=[], private=[], protected=[], static=[],
            asynchronous=[], synchronous=[], class_methods=[],
            asynchronous_static=[], synchronous_static=[], magic=[]
        )

        # Categorize magic methods
        result.magic = [name for name in dir(self._instance) if name.startswith("__") and name.endswith("__")]

        # Classify static and class methods
        for name in dir(cls):
            attr = inspect.getattr_static(cls, name)
            if isinstance(attr, staticmethod):
                result.static.append(name)
            elif isinstance(attr, classmethod):
                result.class_methods.append(name)

        # Classify instance methods
        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            if name in result.class_methods or name in result.magic:
                continue
            if name.startswith(f"_{class_name}"):
                result.private.append(name.replace(f"_{class_name}", ""))
            elif name.startswith("_"):
                result.protected.append(name)
            else:
                result.public.append(name)

        # Classify asynchronous and synchronous methods
        for name, method in inspect.getmembers(cls, predicate=inspect.iscoroutinefunction):
            clean_name = name.replace(f"_{class_name}", "")
            if name in result.static:
                result.asynchronous_static.append(clean_name)
            else:
                result.asynchronous.append(clean_name)

        for name, method in inspect.getmembers(self._instance, predicate=inspect.ismethod):
            clean_name = name.replace(f"_{class_name}", "")
            if name not in result.static and clean_name not in result.asynchronous and name not in result.class_methods and name not in result.magic:
                result.synchronous.append(clean_name)

        # Determine synchronous static methods
        for name in result.static:
            if name not in result.asynchronous_static and name not in result.class_methods:
                result.synchronous_static.append(name)

        return result

    def getMethods(self) -> List[str]:
        """
        Get all method names of the instance.

        Returns
        -------
        List[str]
            List of method names
        """
        methods = self.getAllMethods()
        return methods.public + methods.private + methods.protected + methods.static + methods.class_methods

    def getProtectedMethods(self) -> List[str]:
        """
        Get all protected method names of the instance.

        Returns
        -------
        List[str]
            List of protected method names, excluding private methods (starting with '_')
        """
        methods = self.getAllMethods()
        return methods.protected

    def getPrivateMethods(self) -> List[str]:
        """
        Get all private method names of the instance.

        Returns
        -------
        List[str]
            List of private method names, excluding protected methods (starting with '_')
        """
        methods = self.getAllMethods()
        return methods.private

    def getStaticMethods(self) -> List[str]:
        """
        Get all static method names of the instance.

        Returns
        -------
        List[str]
            List of static method names.
        """
        methods = self.getAllMethods()
        return methods.static

    def getAsyncMethods(self) -> List[str]:
        """
        Get all asynchronous method names of the instance that are not static methods.

        Returns
        -------
        List[str]
            List of asynchronous method names
        """
        methods = self.getAllMethods()
        return methods.asynchronous

    def getSyncMethods(self) -> List[str]:
        """
        Get all synchronous method names of the instance that are not static methods.

        Returns
        -------
        List[str]
            List of synchronous method names
        """
        methods = self.getAllMethods()
        return methods.synchronous

    def getClassMethods(self) -> List[str]:
        """
        Get all class method names of the instance.

        Returns
        -------
        List[str]
            List of class method names.
        """
        methods = self.getAllMethods()
        return methods.class_methods

    def getAsyncStaticMethods(self) -> List[str]:
        """
        Get all asynchronous method names of the instance that are not static methods.

        Returns
        -------
        List[str]
            List of asynchronous method names
        """
        methods = self.getAllMethods()
        return methods.asynchronous_static

    def getSyncStaticMethods(self) -> List[str]:
        """
        Get all synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of synchronous static method names
        """
        methods = self.getAllMethods()
        return methods.synchronous_static

    def getMagicMethods(self) -> List[str]:
        """
        Get all magic method names of the instance.

        Returns
        -------
        List[str]
            List of magic method names
        """
        methods = self.getAllMethods()
        return methods.magic

    def getAllProperties(self) -> Dict[str, ClassProperty]:
        """
        Get all properties of the instance.

        Returns
        -------
        List[str]
            List of property names
        """

        properties = {}
        for name, prop in self._instance.__class__.__dict__.items():
            if isinstance(prop, property):
                properties[name] = ClassProperty(
                    name=name,
                    value=getattr(self._instance, name, None),
                    signature=inspect.signature(prop.fget) if prop.fget else None,
                    doc=prop.__doc__ or ""
                )
        return properties

    def getPropertyNames(self) -> List[str]:
        """
        Get all property names of the instance.

        Returns
        -------
        List[str]
            List of property names
        """
        return self.getAllProperties().keys()

    def getProperty(self, property_name: str) -> Any:
        """
        Get the value of a property.

        Parameters
        ----------
        property_name : str
            Name of the property

        Returns
        -------
        Any
            The value of the property

        Raises
        ------
        AttributeError
            If the property doesn't exist or is not a property
        """
        all_prop = self.getAllProperties()
        if property_name not in all_prop:
            raise ValueError(f"Property '{property_name}' not found.")
        return all_prop[property_name].value

    def getPropertySignature(self, property_name: str) -> inspect.Signature:
        """
        Get the signature of a property.

        Parameters
        ----------
        property_name : str
            Name of the property

        Returns
        -------
        inspect.Signature
            The property signature

        Raises
        ------
        AttributeError
            If the property doesn't exist or is not a property
        """
        all_prop = self.getAllProperties()
        if property_name not in all_prop:
            raise ValueError(f"Property '{property_name}' not found.")
        return all_prop[property_name].signature

    def getPropertyDoc(self, property_name: str) -> str:
        """
        Get the docstring of a property.

        Parameters
        ----------
        property_name : str
            Name of the property

        Returns
        -------
        str
            The docstring of the property

        Raises
        ------
        AttributeError
            If the property doesn't exist or is not a property
        """
        all_prop = self.getAllProperties()
        if property_name not in all_prop:
            raise ValueError(f"Property '{property_name}' not found.")
        return all_prop[property_name].doc

    def callMethod(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Call a method on the instance.

        Parameters
        ----------
        method_name : str
            Name of the method to call
        *args : Any
            Positional arguments for the method
        **kwargs : Any
            Keyword arguments for the method

        Returns
        -------
        Any
            The result of the method call

        Raises
        ------
        AttributeError
            If the method does not exist on the instance
        TypeError
            If the method is not callable
        """

        if method_name in self.getPrivateMethods():
            method_name = f"_{self.getClassName()}{method_name}"

        method = getattr(self._instance, method_name, None)

        if method is None:
            raise AttributeError(f"'{self.getClassName()}' object has no method '{method_name}'.")
        if not callable(method):
            raise TypeError(f"'{method_name}' is not callable on '{self.getClassName()}'.")

        if inspect.iscoroutinefunction(method):
            return AsyncIO.run(method(*args, **kwargs))

        return method(*args, **kwargs)

    def getMethodSignature(self, method_name: str) -> inspect.Signature:
        """
        Get the signature of a method.

        Parameters
        ----------
        method_name : str
            Name of the method

        Returns
        -------
        inspect.Signature
            The method signature
        """
        if method_name in self.getPrivateMethods():
            method_name = f"_{self.getClassName()}{method_name}"

        method = getattr(self._instance, method_name)
        if callable(method):
            return inspect.signature(method)

    def getDocstring(self) -> Optional[str]:
        """
        Get the docstring of the instance's class.

        Returns
        -------
        Optional[str]
            The class docstring, or None if not available
        """
        return self._instance.__class__.__doc__

    def getBaseClasses(self) -> Tuple[Type, ...]:
        """
        Get the base classes of the instance's class.

        Returns
        -------
        Tuple[Type, ...]
            Tuple of base classes
        """
        return self._instance.__class__.__bases__

    def isInstanceOf(self, cls: Type) -> bool:
        """
        Check if the instance is of a specific class.

        Parameters
        ----------
        cls : Type
            The class to check against

        Returns
        -------
        bool
            True if the instance is of the specified class
        """
        return isinstance(self._instance, cls)

    def getSourceCode(self) -> Optional[str]:
        """
        Get the source code of the instance's class.

        Returns
        -------
        Optional[str]
            The source code if available, None otherwise
        """
        try:
            return inspect.getsource(self._instance.__class__)
        except (TypeError, OSError):
            return None

    def getFileLocation(self) -> Optional[str]:
        """
        Get the file location where the class is defined.

        Returns
        -------
        Optional[str]
            The file path if available, None otherwise
        """
        try:
            return inspect.getfile(self._instance.__class__)
        except (TypeError, OSError):
            return None

    def getAnnotations(self) -> Dict[str, Any]:
        """
        Get type annotations of the class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their type annotations
        """
        return self._instance.__class__.__annotations__

    def hasAttribute(self, name: str) -> bool:
        """
        Check if the instance has a specific attribute.

        Parameters
        ----------
        name : str
            The attribute name to check

        Returns
        -------
        bool
            True if the attribute exists
        """
        return hasattr(self._instance, name)

    def getAttribute(self, name: str) -> Any:
        """
        Get an attribute value by name.

        Parameters
        ----------
        name : str
            The attribute name

        Returns
        -------
        Any
            The attribute value

        Raises
        ------
        AttributeError
            If the attribute doesn't exist
        """
        attrs = self.getAttributes()
        return attrs.get(name, getattr(self._instance, name, None))

    def setAttribute(self, name: str, value: Any) -> None:
        """
        Set an attribute value.

        Parameters
        ----------
        name : str
            The attribute name
        value : Any
            The value to set

        Raises
        ------
        AttributeError
            If the attribute is read-only
        """
        if callable(value):
            raise AttributeError(f"Cannot set attribute '{name}' to a callable. Use setMacro instead.")
        setattr(self._instance, name, value)

    def removeAttribute(self, name: str) -> None:
        """
        Remove an attribute from the instance.

        Parameters
        ----------
        name : str
            The attribute name to remove

        Raises
        ------
        AttributeError
            If the attribute doesn't exist or is read-only
        """
        if not hasattr(self._instance, name):
            raise AttributeError(f"'{self.getClassName()}' object has no attribute '{name}'.")
        delattr(self._instance, name)

    def setMacro(self, name: str, value: Callable) -> None:
        """
        Set a callable attribute value.

        Parameters
        ----------
        name : str
            The attribute name
        value : Callable
            The callable to set

        Raises
        ------
        AttributeError
            If the value is not callable
        """
        if not callable(value):
            raise AttributeError(f"The value for '{name}' must be a callable.")
        setattr(self._instance, name, value)

    def removeMacro(self, name: str) -> None:
        """
        Remove a callable attribute from the instance.

        Parameters
        ----------
        name : str
            The attribute name to remove

        Raises
        ------
        AttributeError
            If the attribute doesn't exist or is not callable
        """
        if not hasattr(self._instance, name) or not callable(getattr(self._instance, name)):
            raise AttributeError(f"'{self.getClassName()}' object has no callable macro '{name}'.")
        delattr(self._instance, name)

    def getConstructorDependencies(self) -> ClassDependency:
        """
        Get the resolved and unresolved dependencies from the constructor of the instance's class.

        Returns
        -------
        ClassDependency
            A structured representation of the constructor dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        return ReflectDependencies(self._instance.__class__).getConstructorDependencies()

    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Get the resolved and unresolved dependencies from a method of the instance's class.

        Parameters
        ----------
        method_name : str
            The name of the method to inspect

        Returns
        -------
        MethodDependency
            A structured representation of the method dependencies, containing:
            - resolved: Dictionary of resolved dependencies with their names and values.
            - unresolved: List of unresolved dependencies (parameter names without default values or annotations).
        """
        return ReflectDependencies(self._instance).getMethodDependencies(method_name)
