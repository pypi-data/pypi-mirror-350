from abc import ABC, abstractmethod
import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from orionis.support.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.support.introspection.dependencies.entities.method_dependencies import MethodDependency
from orionis.support.introspection.instances.entities.class_attributes import ClassAttributes
from orionis.support.introspection.instances.entities.class_parsed import ClassParsed
from orionis.support.introspection.instances.entities.class_property import ClassProperty

class IReflectionInstance(ABC):
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

    @abstractmethod
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
        pass

    @abstractmethod
    def getClassName(self) -> str:
        """
        Get the name of the instance's class.

        Returns
        -------
        str
            The name of the class
        """
        pass

    @abstractmethod
    def getClass(self) -> Type:
        """
        Get the class of the instance.

        Returns
        -------
        Type
            The class object of the instance
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """
        Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        pass

    @abstractmethod
    def getAllAttributes(self) -> ClassAttributes:
        """
        Get all attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        pass

    @abstractmethod
    def getAttributes(self) -> Dict[str, Any]:
        """
        Get all attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        pass

    @abstractmethod
    def getPublicAttributes(self) -> Dict[str, Any]:
        """
        Get all public attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of public attribute names and their values
        """
        pass

    @abstractmethod
    def getPrivateAttributes(self) -> Dict[str, Any]:
        """
        Get all private attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of private attribute names and their values
        """
        pass

    @abstractmethod
    def getProtectedAttributes(self) -> Dict[str, Any]:
        """
        Get all Protected attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of Protected attribute names and their values
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getMethods(self) -> List[str]:
        """
        Get all method names of the instance.

        Returns
        -------
        List[str]
            List of method names
        """
        pass

    @abstractmethod
    def getProtectedMethods(self) -> List[str]:
        """
        Get all protected method names of the instance.

        Returns
        -------
        List[str]
            List of protected method names, excluding private methods (starting with '_')
        """
        pass

    @abstractmethod
    def getPrivateMethods(self) -> List[str]:
        """
        Get all private method names of the instance.

        Returns
        -------
        List[str]
            List of private method names, excluding protected methods (starting with '_')
        """
        pass

    @abstractmethod
    def getStaticMethods(self) -> List[str]:
        """
        Get all static method names of the instance.

        Returns
        -------
        List[str]
            List of static method names.
        """
        pass

    @abstractmethod
    def getAsyncMethods(self) -> List[str]:
        """
        Get all asynchronous method names of the instance that are not static methods.

        Returns
        -------
        List[str]
            List of asynchronous method names
        """
        pass

    @abstractmethod
    def getSyncMethods(self) -> List[str]:
        """
        Get all synchronous method names of the instance that are not static methods.

        Returns
        -------
        List[str]
            List of synchronous method names
        """
        pass

    @abstractmethod
    def getClassMethods(self) -> List[str]:
        """
        Get all class method names of the instance.

        Returns
        -------
        List[str]
            List of class method names.
        """
        pass

    @abstractmethod
    def getAsyncStaticMethods(self) -> List[str]:
        """
        Get all asynchronous method names of the instance that are not static methods.

        Returns
        -------
        List[str]
            List of asynchronous method names
        """
        pass

    @abstractmethod
    def getSyncStaticMethods(self) -> List[str]:
        """
        Get all synchronous static method names of the instance.

        Returns
        -------
        List[str]
            List of synchronous static method names
        """
        pass

    @abstractmethod
    def getMagicMethods(self) -> List[str]:
        """
        Get all magic method names of the instance.

        Returns
        -------
        List[str]
            List of magic method names
        """
        pass

    @abstractmethod
    def getAllProperties(self) -> Dict[str, ClassProperty]:
        """
        Get all properties of the instance.

        Returns
        -------
        List[str]
            List of property names
        """
        pass

    @abstractmethod
    def getPropertyNames(self) -> List[str]:
        """
        Get all property names of the instance.

        Returns
        -------
        List[str]
            List of property names
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getDocstring(self) -> Optional[str]:
        """
        Get the docstring of the instance's class.

        Returns
        -------
        Optional[str]
            The class docstring, or None if not available
        """
        pass

    @abstractmethod
    def getBaseClasses(self) -> Tuple[Type, ...]:
        """
        Get the base classes of the instance's class.

        Returns
        -------
        Tuple[Type, ...]
            Tuple of base classes
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getSourceCode(self) -> Optional[str]:
        """
        Get the source code of the instance's class.

        Returns
        -------
        Optional[str]
            The source code if available, None otherwise
        """
        pass

    @abstractmethod
    def getFileLocation(self) -> Optional[str]:
        """
        Get the file location where the class is defined.

        Returns
        -------
        Optional[str]
            The file path if available, None otherwise
        """
        pass

    @abstractmethod
    def getAnnotations(self) -> Dict[str, Any]:
        """
        Get type annotations of the class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their type annotations
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
