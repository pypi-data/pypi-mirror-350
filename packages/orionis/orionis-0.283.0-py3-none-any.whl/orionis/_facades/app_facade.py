from typing import Any
from orionis._application import Application
from orionis._container.resolve import Resolve

def app(abstract: Any = None) -> Any:
    """
    Retrieve an instance from the application container.

    Parameters
    ----------
    abstract : Any, optional
        The abstract class or interface to resolve. If None, returns the application instance.

    Returns
    -------
    Any
        The resolved instance from the container if an abstract is provided,
        otherwise the singleton instance of the application.
    """

    # If an abstract class or interface is provided, attempt to resolve it from the container
    if abstract is not None:
        return Resolve(abstract)

    # If no abstract is provided, return the singleton instance of the application container
    return Application.getInstance().container()