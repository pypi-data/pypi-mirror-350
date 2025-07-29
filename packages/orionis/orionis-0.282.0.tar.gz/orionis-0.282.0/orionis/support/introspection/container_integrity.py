import re
import inspect
from abc import ABC
from typing import Any, Callable, Set, Type
from orionis._container.exception import OrionisContainerValueError, OrionisContainerTypeError
from orionis._contracts.container.container_integrity import IContainerIntegrity

class ContainerIntegrity(IContainerIntegrity):

    @staticmethod
    def ensureImplementation(abstract: Type, concrete: Type, raise_exception: bool = True) -> bool:
        """
        Strictly verify that 'concrete' implements all abstract methods of 'abstract'.

        Args:
            abstract: Abstract class or interface to verify against
            concrete: Concrete class that should implement the abstract class

        Raises:
            OrionisContainerTypeError: If concrete doesn't properly implement abstract
        """

        # Check if abstract is a class
        if not inspect.isclass(abstract):
            if raise_exception:
                raise OrionisContainerTypeError(
                    f"Abstract must be a class, got {type(abstract).__name__}"
                )
            return False

        # Check if concrete is a class
        if not inspect.isclass(concrete):
            if raise_exception:
                raise OrionisContainerTypeError(
                    f"Concrete must be a class, got {type(concrete).__name__}"
                )
            return False

        # Check if concrete inherits from abstract
        if not issubclass(concrete, abstract):
            if raise_exception:
                raise OrionisContainerTypeError(
                    f"{concrete.__name__} must inherit from {abstract.__name__}"
                )
            return False

        abstract_methods: Set[str] = set()
        for base in abstract.__mro__:
            if hasattr(base, '__abstractmethods__'):
                abstract_methods.update(base.__abstractmethods__)

        if not abstract_methods:
            return  # No abstract methods to implement
            
        class_methods = {
            name for name, member in inspect.getmembers(concrete)
            if not name.startswith("_") and inspect.isfunction(member)
        }
        
        missing_methods = abstract_methods - class_methods
        if missing_methods:
            raise OrionisContainerTypeError(
                f"{concrete.__name__} must implement: {sorted(missing_methods)}"
            )
            
    def ensureImplementation(abstract: Type, concrete: Type) -> None:
        """
        Verify at runtime if `concrete` implements all methods of `abstract`.

        :param abstract: Abstract class or interface.
        :param concrete: Concrete class that should implement the abstract class.
        :raises TypeError: If `concrete` does not implement all methods of `abstract`.
        """
        # Get public methods of the interface (excluding magic methods)
        interface_methods = {
            name for name, func in inspect.getmembers(abstract, predicate=inspect.isfunction)
            if not name.startswith("_")
        }

        # Get public methods of the concrete class
        class_methods = {
            name for name, func in inspect.getmembers(concrete, predicate=inspect.isfunction)
            if not name.startswith("_")
        }

        # Verify that all interface methods are in the concrete class
        if not interface_methods.issubset(class_methods):
            missing_methods = interface_methods - class_methods
            raise OrionisContainerTypeError(f"{concrete.__name__} does not implement the required methods of {abstract.__name__}: {missing_methods}")


    @staticmethod
    def ensureIsAbstract(abstract: Callable[..., Any]) -> None:
        """
        Ensure that the given abstract is a valid abstract class.

        :param abstract: Class to check
        :raises OrionisContainerValueError: If the class is not a valid abstract interface
        """
        if not isinstance(abstract, type) or not issubclass(abstract, ABC) or abstract is ABC:
            raise OrionisContainerValueError("The provided class must inherit from ABC and not be ABC itself.")

        if not any(getattr(attr, "__isabstractmethod__", False) for attr in abstract.__dict__.values()):
            raise OrionisContainerValueError("The provided class must define at least one abstract method.")

    @staticmethod
    def ensureIsCallable(concrete: Callable[..., Any]) -> None:
        """
        Ensure that the given implementation is callable or instantiable.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The implementation to check.

        Raises
        ------
        OrionisContainerTypeError
            If the implementation is not callable.
        """
        if not callable(concrete):
            raise OrionisContainerTypeError(f"The implementation '{str(concrete)}' must be callable or an instantiable class.")

    @staticmethod
    def ensureIsInstance(instance: Any) -> None:
        """
        Ensure that the given instance is a valid object.

        Parameters
        ----------
        instance : Any
            The instance to check.

        Raises
        ------
        OrionisContainerValueError
            If the instance is not a valid object.
        """
        if not isinstance(instance, object):
            raise OrionisContainerValueError(f"The instance '{str(instance)}' must be a valid object.")

        module = type(instance).__module__
        if module in ['builtins', 'abc']:
            raise OrionisContainerValueError(f"The instance '{str(instance)}' is not a valid user-defined object. It belongs to the '{module}' module.")

    @staticmethod
    def ensureNotMain(concrete: Callable[..., Any]) -> str:
        """
        Ensure that a class is not defined in the main script.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The class or function to check.

        Returns
        -------
        str
            The fully qualified name of the class.

        Raises
        ------
        OrionisContainerValueError
            If the class is defined in the main module.
        """
        if concrete.__module__ == "__main__":
            raise OrionisContainerValueError("Cannot register a class from the (__main__) module in the container.")

    @staticmethod
    def ensureIsAlias(name: str) -> bool:
        """
        Ensure that the given alias name is a valid string, with no special characters or spaces, 
        and it is not a primitive type.

        Parameters
        ----------
        name : str
            The alias name to check.

        Raises
        ------
        OrionisContainerValueError
            If the alias is invalid.
        """
        if not isinstance(name, str):
            raise OrionisContainerValueError(f"The alias '{name}' must be a string.")

        if not re.match(r'^[a-zA-Z0-9_:]+$', name):
            raise OrionisContainerValueError(
                f"The alias '{name}' can only contain letters, numbers, underscores, and colons, without spaces or other special characters."
            )

        if name in {
            int, "int",
            float, "float",
            str, "str",
            bool, "bool",
            bytes, "bytes",
            type(None), "None",
            complex, "complex",
            list, "list",
            tuple, "tuple",
            dict, "dict",
            set, "set",
            frozenset, "frozenset"
        }:
            raise OrionisContainerValueError(f"The alias '{name}' cannot be a primitive type.")

    @staticmethod
    def isAlias(name: str) -> bool:
        """
        Check if the given alias name is a valid string, with no special characters or spaces,
        and it is not a primitive type.

        Parameters
        ----------
        name : str
            The alias name to check.

        Returns
        -------
        bool
            True if the alias is valid, False otherwise.
        """
        try:
            ContainerIntegrity.ensureIsAlias(name)
            return True
        except OrionisContainerValueError:
            return False

    @staticmethod
    def isCallable(concrete: Callable[..., Any]) -> bool:
        """
        Check if the given implementation is callable or instantiable.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The implementation to check.

        Returns
        -------
        bool
            True if the implementation is callable, False otherwise.
        """
        try:
            ContainerIntegrity.ensureIsCallable(concrete)
            return True
        except OrionisContainerTypeError:
            return False

    @staticmethod
    def isInstance(instance: Any) -> bool:
        """
        Check if the given instance is a valid object.

        Parameters
        ----------
        instance : Any
            The instance to check.

        Returns
        -------
        bool
            True if the instance is valid, False otherwise.
        """
        try:
            ContainerIntegrity.ensureIsInstance(instance)
            return True
        except OrionisContainerValueError:
            return False

    @staticmethod
    def isAbstract(abstract: Callable[..., Any]) -> bool:
        """
        Check if the given abstract is a valid abstract class.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The class to check.

        Returns
        -------
        bool
            True if the class is a valid abstract interface, False otherwise.
        """
        try:
            ContainerIntegrity.ensureIsAbstract(abstract)
            return True
        except OrionisContainerValueError:
            return False