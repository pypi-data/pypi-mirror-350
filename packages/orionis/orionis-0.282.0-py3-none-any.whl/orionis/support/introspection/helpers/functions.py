from typing import Any, Type
import inspect
import importlib

class HelpersReflection:
    """
    A collection of helper functions for reflection and inspection.
    """

    @staticmethod
    def isValidModule(module_name: str) -> bool:
        """Check if a module name is valid and can be imported.

        Parameters
        ----------
        module_name : str
            The name of the module to check

        Returns
        -------
        bool
            True if the module is valid and can be imported, False otherwise
        """
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def ensureValidModule(module_name: str) -> None:
        """Ensure a module name is valid and can be imported.

        Parameters
        ----------
        module_name : str
            The name of the module to check

        Raises
        ------
        ValueError
            If the module cannot be imported or is invalid
        """
        if not isinstance(module_name, str):
            raise TypeError(f"Module name must be a string, got {type(module_name)}")
        if not HelpersReflection.isValidModule(module_name):
            raise ValueError(f"Invalid or non-importable module: {module_name}")

    @staticmethod
    def isInstantiableClass(cls: Type) -> bool:
        """Check if a class is concrete and can be instantiated.

        Parameters
        ----------
        cls : Type
            The class to check

        Returns
        --
        bool
            True if the class is concrete and can be instantiated, False otherwise
        """
        if not isinstance(cls, type):
            return False
        if HelpersReflection.isAbstractClass(cls):
            return False
        try:
            # Try to create an instance to verify it's truly concrete
            cls()
            return True
        except TypeError:
            return False

    @staticmethod
    def ensureNotBuiltinType(cls: Type) -> None:
        """Ensure a class is not a built-in or primitive type.

        Parameters
        ----------
        cls : Type
            The class to check

        Raises
        ------
        TypeError
            If the input is not a class
        ValueError
            If the class is a built-in or primitive type
        """
        if not isinstance(cls, type):
            raise TypeError(f"Expected a class, got {type(cls)}")

        builtin_types = {
            int, float, str, bool, bytes, type(None), complex,
            list, tuple, dict, set, frozenset
        }

        if cls in builtin_types:
            raise ValueError(f"Class '{cls.__name__}' is a built-in or primitive type and cannot be used.")

    @staticmethod
    def ensureInstantiableClass(cls: Type) -> None:
        """Ensure a class is concrete and can be instantiated.

        Parameters
        ----------
        cls : Type
            The class to check

        Raises
        ------
        TypeError
            If the input is not a class
        ValueError
            If the class is abstract or cannot be instantiated
        """
        if HelpersReflection.ensureNotBuiltinType(cls):
            raise TypeError(f"Invalid class: {cls!r}")
        if not isinstance(cls, type):
            raise TypeError(f"Expected a class, got {type(cls)}")
        if HelpersReflection.isAbstractClass(cls):
            raise ValueError(f"Class '{cls.__name__}' is abstract")
        try:
            cls()
        except TypeError as e:
            raise ValueError(f"Class '{cls.__name__}' cannot be instantiated: {str(e)}")

    @staticmethod
    def isValidClassName(module_name: str, class_name: str) -> bool:
        """Check if a class exists in a given module.

        Parameters
        ----------
        module_name : str
            The name of the module to check
        class_name : str
            The name of the class to look for

        Returns
        -------
        bool
            True if the class exists in the module, False otherwise
        """
        try:
            module = importlib.import_module(module_name)
            return hasattr(module, class_name) and inspect.isclass(getattr(module, class_name))
        except ImportError:
            return False

    @staticmethod
    def ensureValidClassName(module_name: str, class_name: str) -> None:
        """Ensure a class exists in a given module.

        Parameters
        ----------
        module_name : str
            The name of the module to check
        class_name : str
            The name of the class to look for

        Raises
        ------
        ValueError
            If the class doesn't exist in the module
        """
        if not HelpersReflection.isValidClassName(module_name, class_name):
            raise ValueError(f"Class '{class_name}' not found in module '{module_name}'")

    @staticmethod
    def isUserDefinedClassInstance(instance: Any) -> bool:
        """Check if an object is an instance of a user-defined class.

        Parameters
        ----------
        instance : Any
            The object to check

        Returns
        -------
        bool
            True if the object is an instance of a user-defined class, False otherwise
        """
        return isinstance(instance, object) and type(instance).__module__ not in {'builtins', 'abc', '__main__'}

    @staticmethod
    def ensureUserDefinedClassInstance(instance: Any) -> None:
        """Ensure an object is an instance of a user-defined class.

        Parameters
        ----------
        instance : Any
            The object to check

        Raises
        ------
        TypeError
            If the input is not an object instance
        ValueError
            If the instance is from builtins, abc, or __main__
        """
        if not isinstance(instance, object):
            raise TypeError(f"Invalid object: {instance!r}")
        module = type(instance).__module__
        if module in {'builtins', 'abc'}:
            raise ValueError(f"'{instance!r}' is not a user-defined class instance, belongs to '{module}'.")
        if module == '__main__':
            raise ValueError("Instance originates from '__main__', origin indeterminate.")

    @staticmethod
    def isAbstractClass(cls: Type) -> bool:
        """Check if a class is abstract.

        Parameters
        ----------
        cls : Type
            The class to check

        Returns
        -------
        bool
            True if the class is abstract, False otherwise
        """
        return isinstance(cls, type) and bool(getattr(cls, '__abstractmethods__', False))

    @staticmethod
    def ensureAbstractClass(cls: Type) -> None:
        """Ensure a class is abstract.

        Parameters
        ----------
        cls : Type
            The class to check

        Raises
        ------
        TypeError
            If the input is not a class
        ValueError
            If the class is not abstract
        """
        if not isinstance(cls, type):
            raise TypeError(f"Invalid class: {cls!r}")
        if not HelpersReflection.isAbstractClass(cls):
            raise ValueError(f"Class '{cls.__name__}' is not abstract.")

    @staticmethod
    def isConcreteClass(cls: Type) -> bool:
        """Check if a class is concrete.

        Parameters
        ----------
        cls : Type
            The class to check

        Returns
        -------
        bool
            True if the class is concrete, False otherwise
        """
        return isinstance(cls, type) and not HelpersReflection.isAbstractClass(cls)

    @staticmethod
    def ensureConcreteClass(cls: Type) -> None:
        """Ensure a class is concrete.

        Parameters
        ----------
        cls : Type
            The class to check

        Raises
        ------
        TypeError
            If the input is not a class
        ValueError
            If the class is not concrete
        """
        if not isinstance(cls, type):
            raise TypeError(f"Invalid class: {cls!r}")
        if not HelpersReflection.isConcreteClass(cls):
            raise ValueError(f"Class '{cls.__name__}' is not concrete.")