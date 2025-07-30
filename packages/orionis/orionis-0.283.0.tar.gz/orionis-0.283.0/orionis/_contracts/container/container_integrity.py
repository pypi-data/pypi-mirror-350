from abc import ABC, abstractmethod
from typing import Any, Callable, Type

class IContainerIntegrity(ABC):

    @abstractmethod
    def ensureImplementation(abstract: Type, concrete: Type) -> None:
        """
        Verify at runtime if `concrete` implements all methods of `abstract`.

        :param abstract: Abstract class or interface.
        :param concrete: Concrete class that should implement the abstract class.
        :raises TypeError: If `concrete` does not implement all methods of `abstract`.
        """
        pass

    @abstractmethod
    def ensureIsAbstract(abstract: Callable[..., Any]) -> None:
        """
        Ensure that the given abstract is a valid abstract class.

        :param abstract: Class to check
        :raises OrionisContainerValueError: If the class is not a valid abstract interface
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass