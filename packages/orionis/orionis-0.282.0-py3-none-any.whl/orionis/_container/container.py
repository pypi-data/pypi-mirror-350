import inspect
from threading import Lock
from typing import Callable, Any, Dict, Deque, Optional, Type, get_origin, get_args
from collections import deque
from orionis._container.container_integrity import ContainerIntegrity
from orionis._container.lifetimes import Lifetime
from orionis._container.exception import OrionisContainerException, OrionisContainerValueError, OrionisContainerTypeError
from orionis._contracts.container.container import IContainer

class Container(IContainer):
    """
    Service container and dependency injection manager.

    This class follows the singleton pattern to manage service bindings, instances,
    and different lifecycle types such as transient, singleton, and scoped.
    """

    _instance = None
    _lock = Lock()

    @classmethod
    def destroy(cls):
        """
        Destroys the container instance.
        """
        cls._instance = None

    def __new__(cls):
        """
        Create a new instance of the container.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._scoped_instances = {}
                    cls._instance._singleton_instances = {}
                    cls._instance._instances_services = {}
                    cls._instance._transient_services = {}
                    cls._instance._scoped_services = {}
                    cls._instance._singleton_services = {}
                    cls._instance._aliases_services = {}
                    cls._instance.instance(IContainer, cls._instance)
        return cls._instance

    def bind(self, abstract: Callable[..., Any], concrete: Callable[..., Any], lifetime: str = Lifetime.TRANSIENT.value) -> None:
        """
        Binds an abstract type to a concrete implementation with a specified lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or alias to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.
        lifetime : str
            The lifecycle of the binding. Must be one of 'transient', 'scoped', or 'singleton'.

        Raises
        ------
        OrionisContainerValueError
            If an invalid lifetime is provided or the concrete implementation is None.

        Examples
        --------
        >>> container.bind(MyService, MyServiceImplementation, "singleton")
        """
        if lifetime not in [member.value for member in Lifetime]:
            raise OrionisContainerValueError(f"Invalid lifetime type '{lifetime}'.")

        if concrete is None:
            raise OrionisContainerValueError("Concrete implementation cannot be None when binding a service.")

        abstract = abstract or concrete
        ContainerIntegrity.ensureIsCallable(concrete)
        ContainerIntegrity.ensureNotMain(concrete)

        service_entry = {
            "concrete": concrete,
            "async": inspect.iscoroutinefunction(concrete)
        }

        service_registry = {
            Lifetime.TRANSIENT.value: self._transient_services,
            Lifetime.SCOPED.value: self._scoped_services,
            Lifetime.SINGLETON.value: self._singleton_services
        }

        if ContainerIntegrity.isAbstract(abstract):
            ContainerIntegrity.ensureImplementation(abstract, concrete)
            service_registry[lifetime][abstract] = service_entry
            return

        if ContainerIntegrity.isAlias(abstract):
            service_registry[lifetime][abstract] = service_entry
            return

        raise OrionisContainerValueError(f"Invalid abstract type '{abstract}'. It must be a valid alias or an abstract class.")

    def transient(self, abstract: Callable[..., Any], concrete: Callable[..., Any]) -> None:
        """
        Registers a service with a transient lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or alias to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.

        Examples
        --------
        >>> container.transient(MyService, MyServiceImplementation)
        """

        self.bind(abstract, concrete, Lifetime.TRANSIENT.value)

    def scoped(self, abstract: Callable[..., Any], concrete: Callable[..., Any]) -> None:
        """
        Registers a service with a scoped lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or alias to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.

        Examples
        --------
        >>> container.scoped(MyService, MyServiceImplementation)
        """

        self.bind(abstract, concrete, Lifetime.SCOPED.value)

    def singleton(self, abstract: Callable[..., Any], concrete: Callable[..., Any]) -> None:
        """
        Registers a service with a singleton lifetime.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or alias to be bound.
        concrete : Callable[..., Any]
            The concrete implementation to associate with the abstract type.

        Examples
        --------
        >>> container.singleton(MyService, MyServiceImplementation)
        """

        self.bind(abstract, concrete, Lifetime.SINGLETON.value)

    def instance(self, abstract: Callable[..., Any], instance: Any) -> None:
        """
        Registers an already instantiated object in the container.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base type or alias to be bound.
        instance : Any
            The instance to be stored.

        Raises
        ------
        OrionisContainerValueError
            If the instance is None.

        Examples
        --------
        >>> container.instance(MyService, my_service_instance)
        """

        if instance is None:
            raise OrionisContainerValueError("The provided instance cannot be None.")

        ContainerIntegrity.ensureIsInstance(instance)

        if ContainerIntegrity.isAbstract(abstract):
            ContainerIntegrity.ensureImplementation(abstract, instance.__class__)
            self._instances_services[abstract] = instance
            return

        if ContainerIntegrity.isAlias(abstract):
            self._instances_services[abstract] = instance
            return

        raise OrionisContainerValueError(f"Invalid abstract type '{abstract}'. It must be a valid alias or an abstract class.")

    def bound(self, abstract_or_alias: Callable[..., Any]) -> bool:
        """
        Checks if a service or alias is bound in the container.

        Parameters
        ----------
        abstract_or_alias : Callable[..., Any]
            The abstract type or alias to check.

        Returns
        -------
        bool
            True if the service is bound, False otherwise.

        Examples
        --------
        >>> container.bound(MyService)
        True
        """

        service_dicts = [
            self._instances_services,
            self._transient_services,
            self._scoped_services,
            self._singleton_services,
            self._aliases_services
        ]
        return any(abstract_or_alias in service_dict for service_dict in service_dicts)

    def has(self, abstract_or_alias: Callable[..., Any]) -> bool:
        """
        Alias for `bound()` method.

        Parameters
        ----------
        abstract_or_alias : Callable[..., Any]
            The abstract type or alias to check.

        Returns
        -------
        bool
            True if the service is bound, False otherwise.

        Examples
        --------
        >>> container.has(MyService)
        True
        """

        return self.bound(abstract_or_alias)

    def alias(self, alias: Callable[..., Any], abstract: Callable[..., Any]) -> None:
        """
        Creates an alias for an existing abstract binding.

        Parameters
        ----------
        alias : Callable[..., Any]
            The alias name.
        abstract : Callable[..., Any]
            The existing abstract type to alias.

        Raises
        ------
        OrionisContainerValueError
            If the abstract type is not registered or the alias is already in use.

        Examples
        --------
        >>> container.alias("DatabaseService", MyDatabaseService)
        """

        if not self.has(abstract):
            raise OrionisContainerValueError(f"Abstract '{abstract}' is not registered in the container.")

        if alias in self._aliases_services:
            raise OrionisContainerValueError(f"Alias '{alias}' is already in use.")

        if not ContainerIntegrity.isAlias(abstract):
            raise OrionisContainerValueError(f"Invalid target abstract type: {abstract}. It must be an alias.")

        self._aliases_services[alias] = abstract

    def isAlias(self, name: str) -> bool:
        """
        Checks if a given name is an alias.

        Parameters
        ----------
        name : str
            The name to check.

        Returns
        -------
        bool
            True if the name is an alias, False otherwise.

        Raises
        ------
        OrionisContainerTypeError
            If the name is not a string.

        Examples
        --------
        >>> container.isAlias("DatabaseService")
        True
        """

        if not isinstance(name, str):
            raise OrionisContainerTypeError("The name must be a valid string.")
        return name in self._aliases_services

    def getBindings(self) -> Dict[str, Any]:
        """
        Retrieves all registered service bindings.

        Returns
        -------
        dict
            A dictionary containing all instances, transient, scoped, singleton, and alias services.

        Examples
        --------
        >>> container.getBindings()
        """

        return {
            "instances": self._instances_services,
            "transient": self._transient_services,
            "scoped": self._scoped_services,
            "singleton": self._singleton_services,
            "aliases": self._aliases_services
        }

    def getAlias(self, name: str) -> Callable[..., Any]:
        """
        Retrieves the abstract type associated with an alias.

        Parameters
        ----------
        name : str
            The alias name.

        Returns
        -------
        Callable[..., Any]
            The abstract type associated with the alias.

        Raises
        ------
        OrionisContainerValueError
            If the alias is not registered.

        Examples
        --------
        >>> container.getAlias("DatabaseService")
        <class 'MyDatabaseService'>
        """

        if not isinstance(name, str):
            raise OrionisContainerValueError("The name must be a valid string.")

        if name not in self._aliases_services:
            raise OrionisContainerValueError(f"Alias '{name}' is not registered in the container.")

        return self._aliases_services[name]

    def forgetScopedInstances(self) -> None:
        """
        Clears all scoped instances.

        Examples
        --------
        >>> container.forgetScopedInstances()
        """

        self._scoped_instances = {}

    def newRequest(self) -> None:
        """
        Resets scoped instances to handle a new request.

        Examples
        --------
        >>> container.newRequest()
        """

        self.forgetScopedInstances()

    async def make(self, abstract_or_alias: Callable[..., Any]) -> Any:
        """
        Resolves and instantiates a service from the container.

        Parameters
        ----------
        abstract_or_alias : Callable[..., Any]
            The abstract type or alias to resolve.

        Returns
        -------
        Any
            The instantiated service.

        Raises
        ------
        OrionisContainerException
            If the service is not found.

        Examples
        --------
        >>> service = await container.make(MyService)
        """
        if abstract_or_alias in self._aliases_services:
            abstract_or_alias = self._aliases_services[abstract_or_alias]

        if abstract_or_alias in self._instances_services:
            return self._instances_services[abstract_or_alias]

        if abstract_or_alias in self._singleton_services:
            if abstract_or_alias not in self._singleton_instances:
                service = self._singleton_services[abstract_or_alias]
                self._singleton_instances[abstract_or_alias] = await self._resolve(service['concrete'])
            return self._singleton_instances[abstract_or_alias]

        if abstract_or_alias in self._scoped_services:
            if abstract_or_alias not in self._scoped_instances:
                service = self._scoped_services[abstract_or_alias]
                self._scoped_instances[abstract_or_alias] = await self._resolve(service['concrete'])
            return self._scoped_instances[abstract_or_alias]

        if abstract_or_alias in self._transient_services:
            service = self._transient_services[abstract_or_alias]
            return await self._resolve(service['concrete'])

        raise OrionisContainerException(f"No binding found for '{abstract_or_alias}' in the container.")

    async def _resolve(self, concrete: Callable[..., Any], resolving: Optional[Deque[Type]] = None) -> Any:
        """
        Asynchronous method to resolve dependencies recursively and instantiate a class.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The concrete implementation to instantiate.
        resolving : Optional[Deque[Type]], optional
            A queue to track resolving dependencies and prevent circular dependencies.

        Returns
        -------
        Any
            The instantiated object.

        Raises
        ------
        OrionisContainerException
            If circular dependencies are detected or instantiation fails.

        Examples
        --------
        >>> instance = await container._resolve(MyClass)
        """
        if resolving is None:
            resolving = deque()

        if concrete in resolving:
            raise OrionisContainerException(f"Circular dependency detected for {concrete}.")

        resolving.append(concrete)

        try:
            signature = inspect.signature(concrete)
        except ValueError as e:
            raise OrionisContainerException(f"Unable to inspect signature of {concrete}: {str(e)}")

        resolved_dependencies: Dict[str, Any] = {}
        unresolved_dependencies = deque()

        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue

            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            if param.annotation is param.empty and param.default is param.empty:
                unresolved_dependencies.append(param_name)
                continue

            if param.default is not param.empty:
                resolved_dependencies[param_name] = param.default
                continue

            if param.annotation is not param.empty:
                param_type = param.annotation

                if get_origin(param_type) is not None:
                    param_type = get_args(param_type)[0]

                if isinstance(param_type, type) and not issubclass(param_type, (int, str, bool, float)):
                    if self.has(param_type):
                        resolved_dependencies[param_name] = await self.make(param_type)
                    else:
                        resolved_dependencies[param_name] = await self._resolve_dependency(param_type, resolving)
                else:
                    resolved_dependencies[param_name] = param_type

        while unresolved_dependencies:
            dep_name = unresolved_dependencies.popleft()
            if dep_name not in resolved_dependencies:
                resolved_dependencies[dep_name] = await self._resolve_dependency(dep_name, resolving)

        try:
            instance = concrete(**resolved_dependencies)
            resolving.pop()
            return instance
        except Exception as e:
            raise OrionisContainerException(f"Failed to instantiate {concrete}: {str(e)}")

    async def _resolve_dependency(self, dep_type: Any, resolving: Optional[Deque[Type]] = None) -> Any:
        """
        Asynchronously resolves a dependency by instantiating or retrieving it from the container.

        Parameters
        ----------
        dep_type : Any
            The dependency type to resolve.
        resolving : Optional[Deque[Type]], optional
            A queue to track resolving dependencies.

        Returns
        -------
        Any
            The resolved dependency.

        Raises
        ------
        OrionisContainerException
            If the dependency cannot be resolved.

        Examples
        --------
        >>> dependency = await container._resolve_dependency(MyDependency)
        """
        if resolving is None:
            resolving = deque()

        if isinstance(dep_type, type):
            if self.has(dep_type):
                return await self.make(dep_type)
            else:
                return await self._resolve(dep_type, resolving)

        raise OrionisContainerException(f"Cannot resolve dependency of type {dep_type}")