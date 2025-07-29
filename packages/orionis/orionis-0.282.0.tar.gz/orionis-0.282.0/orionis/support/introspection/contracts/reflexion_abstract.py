import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar

class IReflexionAbstract(ABC):
    """Interface for abstract class reflection operations.

    Defines the contract for inspecting and analyzing abstract classes,
    including their methods, properties, inheritance, and metadata.
    """

    @abstractmethod
    def getClassName(self) -> str:
        """Get the name of the abstract class.

        Returns
        -------
        str
            The class name
        """
        pass

    @abstractmethod
    def getModuleName(self) -> str:
        """Get the module name where the abstract class is defined.

        Returns
        -------
        str
            The module name
        """
        pass

    @abstractmethod
    def getAbstractMethods(self) -> Set[str]:
        """Get names of all abstract methods required by the class.

        Returns
        -------
        Set[str]
            Set of abstract method names (excluding properties)
        """
        pass

    @abstractmethod
    def getAbstractProperties(self) -> Set[str]:
        """Get names of all abstract properties required by the class.

        Returns
        -------
        Set[str]
            Set of abstract property names
        """
        pass

    @abstractmethod
    def getConcreteMethods(self) -> Dict[str, Callable]:
        """Get all implemented concrete methods in the abstract class.

        Returns
        -------
        Dict[str, Callable]
            Dictionary mapping method names to their implementations
        """
        pass

    @abstractmethod
    def getStaticMethods(self) -> List[str]:
        """Get names of all static methods in the class.

        Returns
        -------
        List[str]
            List of static method names
        """
        pass

    @abstractmethod
    def getClassMethods(self) -> List[str]:
        """Get names of all class methods in the abstract class.

        Returns
        -------
        List[str]
            List of class method names
        """
        pass

    @abstractmethod
    def getProperties(self) -> List[str]:
        """Get names of all properties in the abstract class.

        Returns
        -------
        List[str]
            List of property names
        """
        pass

    @abstractmethod
    def getMethodSignature(self, methodName: str) -> inspect.Signature:
        """Get the signature of a specific method.

        Parameters
        ----------
        methodName : str
            Name of the method to inspect

        Returns
        -------
        inspect.Signature
            The method signature

        Raises
        ------
        AttributeError
            If the method doesn't exist
        """
        pass

    @abstractmethod
    def getPropertySignature(self, propertyName: str) -> inspect.Signature:
        """Get the signature of a property's getter method.

        Parameters
        ----------
        propertyName : str
            Name of the property to inspect

        Returns
        -------
        inspect.Signature
            The getter signature

        Raises
        ------
        AttributeError
            If the property doesn't exist or has no getter
        """
        pass

    @abstractmethod
    def getDocstring(self) -> Optional[str]:
        """Get the class docstring.

        Returns
        -------
        Optional[str]
            The docstring if available
        """
        pass

    @abstractmethod
    def getBaseAbstractClasses(self) -> Tuple[Type[ABC], ...]:
        """Get direct abstract base classes.

        Returns
        -------
        Tuple[Type[ABC], ...]
            Tuple of abstract base classes
        """
        pass

    @abstractmethod
    def getInterfaceMethods(self) -> Dict[str, inspect.Signature]:
        """Get all abstract methods with their signatures.

        Returns
        -------
        Dict[str, inspect.Signature]
            Dictionary mapping method names to their signatures
        """
        pass

    @abstractmethod
    def isSubclassOf(self, abstract_class: Type[ABC]) -> bool:
        """Check inheritance relationship with another abstract class.

        Parameters
        ----------
        abstract_class : Type[ABC]
            The abstract class to check against

        Returns
        -------
        bool
            True if this class inherits from the given abstract class
        """
        pass

    @abstractmethod
    def getSourceCode(self) -> Optional[str]:
        """Get the class source code.

        Returns
        -------
        Optional[str]
            The source code if available
        """
        pass

    @abstractmethod
    def getFileLocation(self) -> Optional[str]:
        """Get the file where the class is defined.

        Returns
        -------
        Optional[str]
            File path if available
        """
        pass

    @abstractmethod
    def getAnnotations(self) -> Dict[str, Any]:
        """Get type annotations for the class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute annotations
        """
        pass

    @abstractmethod
    def getDecorators(self, method_name: str) -> List[str]:
        """Get decorators applied to a specific method.

        Parameters
        ----------
        method_name : str
            Name of the method to inspect

        Returns
        -------
        List[str]
            List of decorator names
        """
        pass

    @abstractmethod
    def isProtocol(self) -> bool:
        """Check if the class is a Protocol.

        Returns
        -------
        bool
            True if this is a Protocol class
        """
        pass

    @abstractmethod
    def getRequiredAttributes(self) -> Set[str]:
        """For Protocol classes, get required attributes.

        Returns
        -------
        Set[str]
            Set of required attribute names

        Notes
        -----
        Returns empty set for non-Protocol classes
        """
        pass