import abc
from typing import Any, Type, TypeVar
from orionis._contracts.support.reflection import IReflection
from orionis.support.introspection.helpers.functions import HelpersReflection
from orionis.support.introspection.abstracts.reflect_abstract import ReflexionAbstract
from orionis.support.introspection.reflexion_concrete import ReflexionConcrete
from orionis.support.introspection.reflexion_concrete_with_abstract import ReflexionConcreteWithAbstract
from orionis.support.introspection.instances.reflection_instance import ReflectionInstance
from orionis.support.introspection.reflexion_instance_with_abstract import ReflexionInstanceWithAbstract
from orionis.support.introspection.reflexion_module import ReflexionModule
from orionis.support.introspection.reflexion_module_with_classname import ReflexionModuleWithClassName

T = TypeVar('T')
ABC = TypeVar('ABC', bound=abc.ABC)

class Reflection(IReflection):
    """A static class providing factory methods for creating reflection objects.

    This class provides methods to create various types of reflection objects
    that encapsulate different aspects of Python's reflection capabilities.
    Each method validates its inputs before creating the appropriate reflection object.

    Methods
    -------
    instance(instance: Any) -> ReflexionInstance
        Creates a reflection object for a class instance
    instanceWithAbstract(instance: Any, abstract: Type[ABC]) -> ReflexionInstanceWithAbstract
        Creates a reflection object for a class instance with its abstract parent
    abstract(abstract: Type[ABC]) -> ReflexionAbstract
        Creates a reflection object for an abstract class
    concrete(concrete: Type[T]) -> ReflexionConcrete
        Creates a reflection object for a concrete class
    concreteWithAbstract(concrete: Type[T], abstract: Type[ABC]) -> ReflexionConcreteWithAbstract
        Creates a reflection object for a concrete class with its abstract parent
    module(module: str) -> ReflexionModule
        Creates a reflection object for a module
    moduleWithClassName(module: str, class_name: str) -> ReflexionModuleWithClassName
        Creates a reflection object for a module with a specific class name
    """

    @staticmethod
    def instance(instance: Any) -> 'ReflectionInstance':
        """Create a reflection object for a class instance.

        Parameters
        ----------
        instance : Any
            The instance to reflect upon

        Returns
        -------
        ReflectionInstance
            A reflection object encapsulating the instance

        Raises
        ------
        TypeError
            If the input is not an object instance
        ValueError
            If the instance is from builtins, abc, or __main__
        """
        HelpersReflection.ensureUserDefinedClassInstance(instance)
        return ReflectionInstance(instance)

    @staticmethod
    def instanceWithAbstract(instance: Any, abstract: Type[ABC]) -> 'ReflexionInstanceWithAbstract':
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
        HelpersReflection.ensureUserDefinedClassInstance(instance)
        HelpersReflection.ensureAbstractClass(abstract)
        return ReflexionInstanceWithAbstract(instance, abstract)

    @staticmethod
    def abstract(abstract: Type[ABC]) -> 'ReflexionAbstract':
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
        HelpersReflection.ensureAbstractClass(abstract)
        return ReflexionAbstract(abstract)

    @staticmethod
    def concrete(concrete: Type[T]) -> 'ReflexionConcrete':
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
        HelpersReflection.ensureInstantiableClass(concrete)
        return ReflexionConcrete(concrete)

    @staticmethod
    def concreteWithAbstract(concrete: Type[T], abstract: Type[ABC]) -> 'ReflexionConcreteWithAbstract':
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
            A reflection object encapsulating the concrete class and its abstract parent

        Raises
        ------
        TypeError
            If either input is not a class
        ValueError
            If concrete is not instantiable or abstract is not actually abstract
        """
        HelpersReflection.ensureInstantiableClass(concrete)
        HelpersReflection.ensureAbstractClass(abstract)
        return ReflexionConcreteWithAbstract(concrete, abstract)

    @staticmethod
    def module(module: str) -> 'ReflexionModule':
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
        HelpersReflection.ensureValidModule(module)
        return ReflexionModule(module)

    @staticmethod
    def moduleWithClassName(module: str, class_name: str) -> 'ReflexionModuleWithClassName':
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
            A reflection object encapsulating the module and class name

        Raises
        ------
        TypeError
            If either input is not a string
        ValueError
            If the module cannot be imported or the class doesn't exist in it
        """
        HelpersReflection.ensureValidModule(module)
        HelpersReflection.ensureValidClassName(class_name)
        return ReflexionModuleWithClassName(module, class_name)