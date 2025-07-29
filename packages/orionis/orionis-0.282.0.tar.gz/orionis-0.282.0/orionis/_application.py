from typing import Dict, List, Type
from orionis._contracts.application import IApplication
from orionis._contracts.container.container import IContainer
from orionis._contracts.foundation.bootstraper import IBootstrapper
from orionis._contracts.providers.service_provider import IServiceProvider
from orionis._container.container import Container
# from orionis._foundation.config.config_bootstrapper import ConfigBootstrapper
from orionis._foundation.console.command_bootstrapper import CommandsBootstrapper
from orionis._foundation.environment.environment_bootstrapper import EnvironmentBootstrapper
from orionis._foundation.exceptions.exception_bootstrapper import BootstrapRuntimeError
from orionis._foundation.providers.service_providers_bootstrapper import ServiceProvidersBootstrapper
# from orionis.support.patterns.singleton import SingletonMeta

class Application:
    """
    Main application class that follows the Singleton pattern.

    This class manages service providers, environment variables, configurations,
    and commands for the application lifecycle.

    Attributes
    ----------
    _booted : bool
        Indicates whether the application has been booted.
    _custom_providers : List[Type[IServiceProvider]]
        Custom service providers defined by the developer.
    _service_providers : List[Type[IServiceProvider]]
        Core application service providers.
    _config : Dict
        Configuration settings of the application.
    _commands : Dict
        Registered console commands.
    _env : Dict
        Environment variables.
    _container : IContainer
        The service container instance.
    """

    _booted: bool = False

    def __init__(self):
        """
        Initializes the application by setting up the service container and preparing
        lists for custom service providers, service providers, configuration, commands,
        and environment variables.
        Attributes:
            _custom_providers (List[Type[IServiceProvider]]): List to store custom service providers.
            _service_providers (List[Type[IServiceProvider]]): List to store service providers.
            _config (Dict): Dictionary to store configuration settings.
            _commands (Dict): Dictionary to store commands.
            _env (Dict): Dictionary to store environment variables.
            _container (IContainer): The service container instance.
        Registers the application instance in the service container.
        """
        self._custom_providers: List[Type[IServiceProvider]] = []
        self._service_providers: List[Type[IServiceProvider]] = []
        self._config: Dict = {}
        self._commands: Dict = {}
        self._env: Dict = {}
        self._container: IContainer = Container()

        # Register the application instance in the service container
        self._container.instance(IApplication, self)

    @classmethod
    def boot(cls) -> None:
        """
        Marks the application as booted by setting the _booted class attribute to True.
        """
        cls._booted = True

    @classmethod
    def isRunning(cls) -> bool:
        """
        Checks if the application has been booted.

        Returns
        -------
        bool
            True if the application has been booted, otherwise False.
        """
        return cls._booted

    @classmethod
    def getInstance(cls) -> "Application":
        """
        Retrieves the singleton instance of the Application.

        Returns
        -------
        Application
            The current application instance.

        Raises
        ------
        RuntimeError
            If the application instance does not exist.
        """
        pass
        # if cls not in SingletonMeta._instances:
        #     raise RuntimeError("Application instance does not exist. Please create an instance first.")
        # return SingletonMeta._instances[cls]

    @classmethod
    def destroy(cls) -> None:
        """
        Destroys the singleton instance of the application if it exists.

        This method checks if the class has an instance in the SingletonMeta
        instances dictionary and deletes it if found.

        Returns
        -------
        None
        """
        pass
        # if cls in SingletonMeta._instances:
        #     del SingletonMeta._instances[cls]

    def withProviders(self, providers: List[Type[IServiceProvider]] = None) -> "Application":
        """
        This method allows you to specify a list of custom service providers
        that will be used by the application. If no providers are specified,
        an empty list will be used by default.
            A list of service provider classes to be used by the application.
            If not provided, defaults to an empty list.
        Returns
        -------
        Application
            The instance of the Application with the custom service providers set.
        """
        self._custom_providers = providers or []
        return self

    def container(self) -> IContainer:
        """
        Returns the service container instance.

        Returns
        -------
        IContainer
            The service container.
        """
        return self._container

    def create(self) -> None:
        """
        Initializes and boots the application.
        This method performs the following steps:
        1. Boots the application by calling the `_bootstrapping` method.
        2. Loads commands and service providers by calling the `_loadCommands` method.
        3. Boots service providers asynchronously using `AsyncExecutor.run` on the `_bootServiceProviders` method.
        4. Changes the application status to booted by calling `Application.boot`.
        Returns
        -------
        None
        """
        self._bootstrapping()
        self._loadCommands()
        # AsyncExecutor.run(self._bootServiceProviders())
        Application.boot()

    async def _bootServiceProviders(self) -> None:
        """
        This method iterates over all registered service providers, registers them,
        and calls their `boot` method if it exists and is callable.
        Raises
        ------
        RuntimeError
            If an error occurs while booting a service provider, a RuntimeError is raised
            with a message indicating which service provider failed and the original exception.
        """
        for service in self._service_providers:
            provider: IServiceProvider = service(app=self._container)
            provider.register()

            if hasattr(provider, 'boot') and callable(provider.boot):
                try:
                    await provider.boot()
                except Exception as e:
                    raise RuntimeError(f"Error booting service provider {service.__name__}: {e}") from e

    def _bootstrapping(self) -> None:
        """
        Initializes and loads essential components for the application.
        This method sets up the environment variables, configurations, commands,
        and service providers by utilizing their respective bootstrappers. It
        iterates through a list of bootstrappers, updating or extending the
        corresponding properties with the data provided by each bootstrapper.
        Raises
        ------
        BootstrapRuntimeError
            If an error occurs during the bootstrapping process, an exception is
            raised with details about the specific bootstrapper that failed.
        """
        bootstrappers = [
            {'property': self._env, 'instance': EnvironmentBootstrapper()},
            # {'property': self._config, 'instance': ConfigBootstrapper()},
            {'property': self._commands, 'instance': CommandsBootstrapper()},
            {'property': self._service_providers, 'instance': ServiceProvidersBootstrapper(self._custom_providers)},
        ]

        for bootstrapper in bootstrappers:
            try:
                property_ref: Dict = bootstrapper["property"]
                bootstrapper_instance: IBootstrapper = bootstrapper["instance"]
                if isinstance(property_ref, dict):
                    property_ref.update(bootstrapper_instance.get())
                elif isinstance(property_ref, list):
                    property_ref.extend(bootstrapper_instance.get())
                else:
                    property_ref = bootstrapper_instance.get()
            except Exception as e:
                raise BootstrapRuntimeError(f"Error bootstrapping {type(bootstrapper_instance).__name__}: {str(e)}") from e

    def _loadCommands(self) -> None:
        """
        This method iterates over the `_commands` dictionary and registers each command
        in the service container as a transient service. The command's signature and
        concrete implementation are retrieved from the dictionary and passed to the
        container's `transient` method.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for command, data_command in self._commands.items():
            self._container.transient(data_command.get('signature'), data_command.get('concrete'))