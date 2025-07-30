from abc import ABC, abstractmethod

class IContainer(ABC):

    @abstractmethod
    def bind(self, abstract, concrete, lifetime):
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
        pass

    @abstractmethod
    def transient(self, abstract, concrete):
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
        pass

    @abstractmethod
    def scoped(self, abstract, concrete):
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
        pass

    @abstractmethod
    def singleton(self, abstract, concrete):
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
        pass

    @abstractmethod
    def instance(self, abstract, instance):
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
        pass

    @abstractmethod
    def bound(self, abstract_or_alias):
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
        pass

    @abstractmethod
    def has(self, abstract_or_alias):
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
        pass

    @abstractmethod
    def alias(self, alias, abstract):
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
        pass

    @abstractmethod
    def isAlias(self, name):
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
        pass

    @abstractmethod
    def getBindings(self):
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
        pass

    @abstractmethod
    def getAlias(self, name):
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
        pass

    @abstractmethod
    def forgetScopedInstances(self):
        """
        Clears all scoped instances.

        Examples
        --------
        >>> container.forgetScopedInstances()
        """
        pass

    @abstractmethod
    def newRequest(self):
        """
        Resets scoped instances to handle a new request.

        Examples
        --------
        >>> container.newRequest()
        """
        pass

    @abstractmethod
    async def make(self, abstract_or_alias):
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
        pass

    @abstractmethod
    def _resolve(self, concrete, resolving=None):
        """
        Resolves dependencies recursively and instantiates a class.

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
        >>> instance = container._resolve(MyClass)
        """
        pass

    @abstractmethod
    def _resolve_dependency(self, dep_type, resolving=None):
        """
        Resolves a dependency by instantiating or retrieving it from the container.

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
        >>> dependency = container._resolve_dependency(MyDependency)
        """
        pass
