from orionis._contracts.container.container import IContainer
from orionis._contracts.providers.service_provider import IServiceProvider

class ServiceProvider(IServiceProvider):
    """
    Base class for service providers.

    Parameters
    ----------
    container : Container
        The container instance to be used by the service provider.
    """

    def __init__(self, app : IContainer) -> None:
        """
        Initialize the service provider with the given container.

        Parameters
        ----------
        container : Container
            The container instance to be used by the service provider.
        """
        self.app = app

    def register(self) -> None:
        """
        Register services in the container.

        This method should be overridden in the subclass to register
        specific services.

        Parameters
        ----------
        container : Container
            The container instance where services will be registered.
        """
        raise NotImplementedError("This method should be overridden in the subclass")