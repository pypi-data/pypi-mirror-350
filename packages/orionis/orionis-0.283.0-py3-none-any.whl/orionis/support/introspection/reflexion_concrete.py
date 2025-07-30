from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar
import inspect

T = TypeVar('T')

class ReflexionConcrete:
    """A reflection object encapsulating a concrete class.

    Parameters
    ----------
    concrete : Type[T]
        The concrete class being reflected upon

    Attributes
    ----------
    _concrete : Type[T]
        The encapsulated concrete class
    """

    def __init__(self, concrete: Type[T]) -> None:
        """Initialize with the concrete class."""
        self._concrete = concrete

    def getClassName(self) -> str:
        """Get the name of the concrete class.

        Returns
        -------
        str
            The name of the class
        """
        return self._concrete.__name__

    def getClass(self) -> Type:
        """Get the class of the instance.

        Returns
        -------
        Type
            The class object of the instance

        Examples
        --------
        >>> reflex.getClass() is SomeClass
        True
        """
        return self._concrete

    def getModuleName(self) -> str:
        """Get the name of the module where the class is defined.

        Returns
        -------
        str
            The module name
        """
        return self._concrete.__module__

    def getAttributes(self) -> Dict[str, Any]:
        """Get all class-level attributes.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        return {
            k: v for k, v in vars(self._concrete).items()
            if not callable(v) and not isinstance(v, staticmethod) and not isinstance(v, classmethod) and not k.startswith('_') and not isinstance(v, property)
        }

    def getMethods(self) -> List[str]:
        """Get all method names of the class.

        Returns
        -------
        List[str]
            List of method names
        """
        return [
            name for name, member in inspect.getmembers(self._concrete, predicate=inspect.isfunction)
            if not name.startswith('_')
        ]

    def getStaticMethods(self) -> List[str]:
        """Get all static method names of the class.

        Returns
        -------
        List[str]
            List of static method names, excluding private methods
        """
        return [
            name for name in dir(self._concrete)
            if not name.startswith('_') and isinstance(inspect.getattr_static(self._concrete, name), staticmethod)
        ]

    def getPropertyNames(self) -> List[str]:
        """Get all property names of the class.

        Returns
        -------
        List[str]
            List of property names
        """
        return [
            name for name, val in vars(self._concrete).items()
            if isinstance(val, property)
        ]

    def getMethodSignature(self, methodName: str) -> inspect.Signature:
        """Get the signature of a class method.

        Parameters
        ----------
        methodName : str
            Name of the method

        Returns
        -------
        inspect.Signature
            The method signature

        Raises
        ------
        AttributeError
            If the method doesn't exist
        """
        method = getattr(self._concrete, methodName)
        if callable(method):
            return inspect.signature(method)
        raise AttributeError(f"{methodName} is not a valid method.")

    def getPropertySignature(self, propertyName: str) -> inspect.Signature:
        """Get the signature of a property getter.

        Parameters
        ----------
        propertyName : str
            Name of the property

        Returns
        -------
        inspect.Signature
            The property's getter method signature

        Raises
        ------
        AttributeError
            If the property doesn't exist or is not a property
        """
        attr = getattr(self._concrete, propertyName, None)
        if isinstance(attr, property) and attr.fget is not None:
            return inspect.signature(attr.fget)
        raise AttributeError(f"{propertyName} is not a property or doesn't have a getter.")

    def getDocstring(self) -> Optional[str]:
        """Get the docstring of the class.

        Returns
        -------
        Optional[str]
            The class docstring, or None if not available
        """
        return self._concrete.__doc__

    def getBaseClasses(self) -> Tuple[Type, ...]:
        """Get the base classes of the class.

        Returns
        -------
        Tuple[Type, ...]
            Tuple of base classes
        """
        return self._concrete.__bases__

    def isSubclassOf(self, cls: Type) -> bool:
        """Check if the concrete class is a subclass of another.

        Parameters
        ----------
        cls : Type
            The parent class to check against

        Returns
        -------
        bool
            True if the concrete class is a subclass of the given class
        """
        return issubclass(self._concrete, cls)

    def getSourceCode(self) -> Optional[str]:
        """Get the source code of the class.

        Returns
        -------
        Optional[str]
            The source code if available, None otherwise
        """
        try:
            return inspect.getsource(self._concrete)
        except (TypeError, OSError):
            return None

    def getFileLocation(self) -> Optional[str]:
        """Get the file location where the class is defined.

        Returns
        -------
        Optional[str]
            The file path if available, None otherwise
        """
        try:
            return inspect.getfile(self._concrete)
        except (TypeError, OSError):
            return None

    def getAnnotations(self) -> Dict[str, Any]:
        """Get type annotations of the class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their type annotations
        """
        return getattr(self._concrete, '__annotations__', {})

    def hasAttribute(self, name: str) -> bool:
        """Check if the class has a specific attribute.

        Parameters
        ----------
        name : str
            The attribute name to check

        Returns
        -------
        bool
            True if the attribute exists
        """
        return hasattr(self._concrete, name)

    def getAttribute(self, name: str) -> Any:
        """Get a class attribute by name.

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
        return getattr(self._concrete, name)

    def getCallableMembers(self) -> Dict[str, Callable]:
        """Get all callable members (functions/methods) of the class.

        Returns
        -------
        Dict[str, Callable]
            Dictionary of method names and their callable objects
        """
        return {
            name: member for name, member in inspect.getmembers(
                self._concrete,
                callable
            ) if not name.startswith('__')
        }