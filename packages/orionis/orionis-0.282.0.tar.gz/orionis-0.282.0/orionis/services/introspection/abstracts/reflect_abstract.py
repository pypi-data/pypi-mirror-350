import abc
import ast
import inspect
import types
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar
from orionis.services.introspection.abstracts.entities.abstract_class_attributes import AbstractClassAttributes

ABC = TypeVar('ABC', bound=abc.ABC)

class ReflexionAbstract:
    """A reflection object encapsulating an abstract class.

    Parameters
    ----------
    abstract : Type[ABC]
        The abstract class being reflected upon

    Attributes
    ----------
    _abstract : Type[ABC]
        The encapsulated abstract class
    """

    def __init__(self, abstract: Type[ABC]) -> None:
        """Initialize with the abstract class."""
        self._abstract = abstract

    def parse(self) -> None:
        pass

    def getClassName(self) -> str:
        """
        Get the name of the abstract class.

        Returns
        -------
        str
            The name of the abstract class
        """
        return self._abstract.__name__

    def getClass(self) -> RuntimeError:
        """
        Retrieve the class of the abstract base class.
        This method is intended to be overridden in subclasses to provide
        the actual abstract class. By default, it raises a RuntimeError
        since abstract classes cannot be instantiated directly.
            The abstract base class itself.
        Raises
        ------
        RuntimeError
            If called directly on the abstract class.
        """
        raise RuntimeError("Cannot instantiate an abstract class.")

    def getModuleName(self) -> str:
        """
        Get the name of the module where the abstract class is defined.

        Returns
        -------
        str
            The module name
        """
        return self._abstract.__module__

    def getAllAttributes(self) -> AbstractClassAttributes:
        """
        Get all attributes of the abstract class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        attributes = {
            name: value for name, value in vars(self._abstract).items()
            if not callable(value) and not isinstance(value, (staticmethod, classmethod, property))
            and not isinstance(value, types.MemberDescriptorType)
        }
        class_name = self.getClassName()
        public = {}
        private = {}
        protected = {}

        for attr, value in attributes.items():
            if (str(attr).startswith("__") and str(attr).endswith("__")) or str(attr).startswith("_abc_"):
                continue
            if str(attr).startswith("_") and not str(attr).startswith("__") and not str(attr).startswith(f"_{class_name}"):
                protected[attr] = value
            elif str(attr).startswith(f"_{class_name}"):
                private[str(attr).replace(f"_{class_name}", "")] = value
            else:
                public[attr] = value

        return AbstractClassAttributes(
            public=public,
            private=private,
            protected=protected
        )

    def getAttributes(self) -> Dict[str, Any]:
        """
        Get all attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their values
        """
        attr = self.getAllAttributes()
        return {**attr.public, **attr.private, **attr.protected}

    def getPublicAttributes(self) -> Dict[str, Any]:
        """
        Get all public attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of public attribute names and their values
        """
        attr = self.getAllAttributes()
        return attr.public

    def getPrivateAttributes(self) -> Dict[str, Any]:
        """
        Get all private attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of private attribute names and their values
        """
        attr = self.getAllAttributes()
        return attr.private

    def getProtectedAttributes(self) -> Dict[str, Any]:
        """
        Get all Protected attributes of the instance.

        Returns
        -------
        Dict[str, Any]
            Dictionary of Protected attribute names and their values
        """
        attr = self.getAllAttributes()
        return attr.protected

    def getAllMethods(self) -> Dict[str, List[str]]:
        """
        Categorize all methods and relevant members of the abstract class into public, private, protected,
        static, asynchronous, synchronous, class methods, magic methods, abstract methods, and properties.

        Returns
        -------
        Dict[str, List[str]]
            A dictionary categorizing methods and attributes into various types.
        """
        class_name = self.getClassName()
        private_prefix = f"_{class_name}"
        attributes = set(self.getAttributes().keys()) | {attr for attr in dir(self._abstract) if attr.startswith('_abc_')}

        result = {
            "public": [],
            "private": [],
            "protected": [],
            "static": [],
            "asynchronous": [],
            "synchronous": [],
            "class_methods": [],
            "asynchronous_static": [],
            "synchronous_static": [],
            "magic": [],
            "abstract": [],
            "abstract_class_methods": [],
            "abstract_static_methods": []
        }

        # Precompute all members once
        members = inspect.getmembers(self._abstract)
        static_attrs = {}

        # First pass to collect all relevant information
        for name, attr in members:
            if name in attributes:
                continue

            # Get static attribute once
            static_attr = inspect.getattr_static(self._abstract, name)
            static_attrs[name] = static_attr

            # Magic methods
            if name.startswith("__") and name.endswith("__"):
                result["magic"].append(name)
                continue

            # Static and class methods
            if isinstance(static_attr, staticmethod):
                result["static"].append(name)
            elif isinstance(static_attr, classmethod):
                result["class_methods"].append(name)

            # Private, protected, public
            if name.startswith(private_prefix):
                clean_name = name.replace(private_prefix, "")
                result["private"].append(clean_name)
            elif name.startswith("_"):
                result["protected"].append(name)
            else:
                result["public"].append(name)

            # Async methods
            if inspect.iscoroutinefunction(attr):
                clean_name = name.replace(private_prefix, "")
                if name in result["static"]:
                    result["asynchronous_static"].append(clean_name)
                else:
                    result["asynchronous"].append(clean_name)

        # Second pass for synchronous methods (needs info from first pass)
        for name, attr in members:
            if name in attributes or name in result["magic"] or name in result["class_methods"] or name in result["static"]:
                continue

            if inspect.isfunction(attr):
                clean_name = name.replace(private_prefix, "")
                if clean_name not in result["asynchronous"]:
                    result["synchronous"].append(clean_name)

        # Synchronous static methods
        for name in result["static"]:
            if name not in attributes and name not in result["asynchronous_static"] and name not in result["class_methods"]:
                result["synchronous_static"].append(name)

        # Abstract methods
        abstract_methods = getattr(self._abstract, "__abstractmethods__", set())
        for name in abstract_methods:
            if name in attributes:
                continue

            static_attr = static_attrs.get(name, inspect.getattr_static(self._abstract, name))
            if isinstance(static_attr, staticmethod):
                result["abstract_static_methods"].append(name)
            elif isinstance(static_attr, classmethod):
                result["abstract_class_methods"].append(name)
            elif not isinstance(static_attr, property):
                result["abstract"].append(name)

        return result













    def getAbstractProperties(self) -> Set[str]:
        """Get all abstract property names required by the class.

        Returns
        -------
        Set[str]
            Set of abstract property names
        """
        properties = []
        for name in getattr(self._abstract, '__abstractmethods__', set()):
            attr = getattr(self._abstract, name, None)
            if isinstance(attr, property):
                properties.append(name)
        return set(properties)

    def getConcreteMethods(self) -> Dict[str, Callable]:
        """Get all concrete methods implemented in the abstract class.

        Returns
        -------
        Dict[str, Callable]
            Dictionary of method names and their implementations
        """
        return {
            name: member for name, member in inspect.getmembers(
                self._abstract,
                predicate=inspect.isfunction
            ) if not name.startswith('_') and name not in self.getAbstractMethods()
        }

    def getStaticMethods(self) -> List[str]:
        """Get all static method names of the abstract class.

        Returns
        -------
        List[str]
            List of static method names
        """
        return [
            name for name in dir( self._abstract)
            if not name.startswith('_') and
            isinstance(inspect.getattr_static( self._abstract, name), staticmethod)
        ]

    def getClassMethods(self) -> List[str]:
        """Get all class method names of the abstract class.

        Returns
        -------
        List[str]
            List of class method names, excluding private/protected methods (starting with '_')

        Notes
        -----
        - Uses inspect.getattr_static to avoid method binding
        - Properly handles both @classmethod decorator and classmethod instances
        - Filters out private/protected methods (starting with '_')

        Examples
        --------
        >>> class MyAbstract(ABC):
        ...     @classmethod
        ...     def factory(cls): pass
        ...     @classmethod
        ...     def _protected_factory(cls): pass
        >>> reflex = ReflexionAbstract(MyAbstract)
        >>> reflex.getClassMethods()
        ['factory']
        """
        return [
            name for name in dir(self._abstract)
            if not name.startswith('_') and
            isinstance(
                inspect.getattr_static(self._abstract, name),
                (classmethod, types.MethodType)
            )
        ]

    def getProperties(self) -> List[str]:
        """Get all property names of the abstract class.

        Returns
        -------
        List[str]
            List of property names
        """
        return [
            name for name, member in inspect.getmembers(
                self._abstract,
                predicate=lambda x: isinstance(x, property))
            if not name.startswith('_')
        ]

    def getMethodSignature(self, methodName: str) -> inspect.Signature:
        """Get the signature of a method.

        Parameters
        ----------
        methodName : str
            Name of the method

        Returns
        -------
        inspect.Signature
            The method signature

        Raises
        ------
        AttributeError
            If the method doesn't exist
        """
        method = getattr(self._abstract, methodName)
        if callable(method):
            return inspect.signature(method)

    def getPropertySignature(self, propertyName: str) -> inspect.Signature:
        """Get the signature of an abstract property's getter.

        Parameters
        ----------
        propertyName : str
            Name of the abstract property

        Returns
        -------
        inspect.Signature
            The getter signature of the abstract property

        Raises
        ------
        AttributeError
            If the property doesn't exist or is not an abstract property
        """
        attr = getattr(self._abstract, propertyName, None)
        if isinstance(attr, property) and attr.fget is not None:
            return inspect.signature(attr.fget)
        raise AttributeError(f"{propertyName} is not an abstract property or doesn't have a getter.")

    def getDocstring(self) -> Optional[str]:
        """Get the docstring of the abstract class.

        Returns
        -------
        Optional[str]
            The class docstring
        """
        return self._abstract.__doc__

    def getBaseAbstractClasses(self) -> Tuple[Type[ABC], ...]:
        """Get the abstract base classes.

        Returns
        -------
        Tuple[Type[ABC], ...]
            Tuple of abstract base classes
        """
        return tuple(
            base for base in self._abstract.__bases__
            if inspect.isabstract(base) or issubclass(base, abc.ABC) or isinstance(base, abc.ABCMeta)
        )

    def getInterfaceMethods(self) -> Dict[str, inspect.Signature]:
        """Get all abstract methods with their signatures.

        Returns
        -------
        Dict[str, inspect.Signature]
            Dictionary of method names and their signatures
        """
        return {
            name: inspect.signature(getattr(self._abstract, name))
            for name in self.getAbstractMethods()
        }

    def isSubclassOf(self, abstract_class: Type[ABC]) -> bool:
        """Check if the abstract class inherits from another abstract class.

        Parameters
        ----------
        abstract_class : Type[ABC]
            The abstract class to check against

        Returns
        -------
        bool
            True if this is a subclass
        """
        return issubclass(self._abstract, abstract_class)

    def getSourceCode(self) -> Optional[str]:
        """Get the source code of the abstract class.

        Returns
        -------
        Optional[str]
            The source code if available
        """
        try:
            return inspect.getsource(self._abstract)
        except (TypeError, OSError):
            return None

    def getFileLocation(self) -> Optional[str]:
        """Get the file location where the abstract class is defined.

        Returns
        -------
        Optional[str]
            The file path if available
        """
        try:
            return inspect.getfile(self._abstract)
        except (TypeError, OSError):
            return None

    def getAnnotations(self) -> Dict[str, Any]:
        """Get type annotations of the abstract class.

        Returns
        -------
        Dict[str, Any]
            Dictionary of attribute names and their type annotations
        """
        return self._abstract.__annotations__

    def getDecorators(self, method_name: str) -> List[str]:
        """
        Get decorators applied to a method.

        Parameters
        ----------
        method_name : str
            Name of the method to inspect
        """
        method = getattr(self._abstract, method_name, None)
        if method is None:
            return []

        try:
            source = inspect.getsource(self._abstract)
        except (OSError, TypeError):
            return []

        tree = ast.parse(source)

        class DecoratorVisitor(ast.NodeVisitor):
            def __init__(self):
                self.decorators = []

            def visit_FunctionDef(self, node):
                if node.name == method_name:
                    for deco in node.decorator_list:
                        if isinstance(deco, ast.Name):
                            self.decorators.append(deco.id)
                        elif isinstance(deco, ast.Call):
                            # handles decorators with arguments like @deco(arg)
                            if isinstance(deco.func, ast.Name):
                                self.decorators.append(deco.func.id)
                        elif isinstance(deco, ast.Attribute):
                            self.decorators.append(deco.attr)
                    # No need to visit deeper
                    return

        visitor = DecoratorVisitor()
        visitor.visit(tree)

        return visitor.decorators

    def isProtocol(self) -> bool:
        """Check if the abstract class is a Protocol.

        Returns
        -------
        bool
            True if this is a Protocol class
        """
        return hasattr(self._abstract, '_is_protocol') and self._abstract._is_protocol

    def getRequiredAttributes(self) -> Set[str]:
        """For Protocol classes, get required attributes.

        Returns
        -------
        Set[str]
            Set of required attribute names
        """
        if not self.isProtocol():
            return set()

        return {
            name for name in dir(self._abstract)
            if not name.startswith('_') and not inspect.isfunction(getattr(self._abstract, name))
        }