from typing import Any, Callable
from orionis._container.container import Container
from orionis._container.exception import OrionisContainerValueError

class Resolve:
    """
    A class to resolve dependencies from the dependency injection container.

    This class ensures that a given abstract class or alias exists in the container
    and resolves the associated service when an instance is created.

    Parameters
    ----------
    abstract_or_alias : Callable[..., Any] or str
        The abstract class, alias, or callable to resolve from the container.

    Returns
    -------
    Any
        The service associated with the abstract class or alias.

    Raises
    ------
    OrionisContainerValueError
        If the abstract class or alias is not found in the container.

    Examples
    --------
    >>> container = Container()
    >>> container.bind("my_service", MyService)
    >>> container.alias("my_alias", "my_service")
    >>> service = Resolve("my_alias")  # Returns the service associated with "my_alias"
    >>> service = Resolve(MyService)  # Returns the service associated with MyService
    """

    def __new__(cls, abstract_or_alias: Callable[..., Any] | str):
        """
        Create an instance of Resolve and return the resolved service.

        Parameters
        ----------
        abstract_or_alias : Callable[..., Any] or str
            The abstract class, alias, or callable to resolve from the container.

        Returns
        -------
        Any
            The service associated with the abstract class or alias.

        Raises
        ------
        OrionisContainerValueError
            If the abstract class or alias is not found in the container.
        """

        # Validate that the abstract or alias exists in the container
        container = Container()
        if not container.bound(abstract_or_alias):
            raise OrionisContainerValueError(
                f"Service or alias '{abstract_or_alias}' not found in the container."
            )

        # Resolve and return the service associated with the abstract or alias
        # return AsyncExecutor.run(container.make(abstract_or_alias))