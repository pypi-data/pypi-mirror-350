import abc
from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

T = TypeVar('T')
ABC = TypeVar('ABC', bound=abc.ABC)

class IReflection(ABC):
    """Interface for a static reflection factory class.

    Defines the contract for creating various types of reflection objects
    that encapsulate different aspects of Python's reflection capabilities.
    """

    @staticmethod
    @abstractmethod
    def instance(instance: Any):
        """Create a reflection object for a class instance.

        Parameters
        ----------
        instance : Any
            The instance to reflect upon

        Returns
        -------
        ReflexionInstance
            A reflection object encapsulating the instance

        Raises
        ------
        TypeError
            If the input is not an object instance
        ValueError
            If the instance is from builtins, abc, or __main__
        """
        pass

    @staticmethod
    @abstractmethod
    def instanceWithAbstract(instance: Any, abstract: Type[ABC]):
        """Create a reflection object for a class instance with its abstract parent.

        Parameters
        ----------
        instance : Any
            The instance to reflect upon
        abstract : Type[ABC]
            The abstract parent class

        Returns
        -------
        ReflexionInstanceWithAbstract
            A reflection object encapsulating the instance and its abstract parent

        Raises
        ------
        TypeError
            If the instance is not an object or abstract is not a class
        ValueError
            If the instance is invalid or abstract is not actually abstract
        """
        pass

    @staticmethod
    @abstractmethod
    def abstract(abstract: Type[ABC]):
        """Create a reflection object for an abstract class.

        Parameters
        ----------
        abstract : Type[ABC]
            The abstract class to reflect upon

        Returns
        -------
        ReflexionAbstract
            A reflection object encapsulating the abstract class

        Raises
        ------
        TypeError
            If the input is not a class
        ValueError
            If the class is not abstract
        """
        pass

    @staticmethod
    @abstractmethod
    def concrete(concrete: Type[T]):
        """Create a reflection object for a concrete class.

        Parameters
        ----------
        concrete : Type[T]
            The concrete class to reflect upon

        Returns
        -------
        ReflexionConcrete
            A reflection object encapsulating the concrete class

        Raises
        ------
        TypeError
            If the input is not a class
        ValueError
            If the class is abstract or cannot be instantiated
        """
        pass

    @staticmethod
    @abstractmethod
    def concreteWithAbstract(concrete: Type[T], abstract: Type[ABC]):
        """Create a reflection object for a concrete class with its abstract parent.

        Parameters
        ----------
        concrete : Type[T]
            The concrete class to reflect upon
        abstract : Type[ABC]
            The abstract parent class

        Returns
        -------
        ReflexionConcreteWithAbstract
            A reflection object encapsulating both classes

        Raises
        ------
        TypeError
            If either input is not a class
        ValueError
            If concrete is not instantiable or abstract is not actually abstract
        """
        pass

    @staticmethod
    @abstractmethod
    def module(module: str):
        """Create a reflection object for a module.

        Parameters
        ----------
        module : str
            The module name to reflect upon

        Returns
        -------
        ReflexionModule
            A reflection object encapsulating the module

        Raises
        ------
        TypeError
            If the input is not a string
        ValueError
            If the module cannot be imported
        """
        pass

    @staticmethod
    @abstractmethod
    def moduleWithClassName(module: str, class_name: str):
        """Create a reflection object for a module with a specific class name.

        Parameters
        ----------
        module : str
            The module name to reflect upon
        class_name : str
            The class name to look for in the module

        Returns
        -------
        ReflexionModuleWithClassName
            A reflection object encapsulating both the module and class name

        Raises
        ------
        TypeError
            If either input is not a string
        ValueError
            If the module cannot be imported or the class doesn't exist in it
        """
        pass