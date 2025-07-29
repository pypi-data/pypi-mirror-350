import ast
import inspect
import re
from typing import List, Type
from dataclasses import dataclass

@dataclass
class ClassDecorators:
    """
    ClassDecorators is a dataclass that encapsulates information about class decorators.

    Attributes
    ----------
    user_defined : tuple[str, ...]
        A tuple containing the names of user-defined decorators applied to a class.
    native : tuple[str, ...]
        A tuple containing the names of native or built-in decorators applied to a class.
    all : tuple[str, ...]
        A tuple containing the names of all decorators (both user-defined and native) applied to a class.
    """
    user_defined: tuple[str, ...]
    native: tuple[str, ...]
    all: tuple[str, ...]

@dataclass
class MethodDecorators:
    """
    MethodDecorators is a dataclass that encapsulates information about method decorators.

    Attributes
    ----------
    user_defined : tuple[str, ...]
        A tuple containing the names of user-defined decorators applied to a method.
    native : tuple[str, ...]
        A tuple containing the names of native or built-in decorators applied to a method.
    all : tuple[str, ...]
        A tuple containing the names of all decorators (both user-defined and native) applied to a method.
    """
    user_defined: tuple[str, ...]
    native: tuple[str, ...]
    all: tuple[str, ...]

class ReflectDecorators(ast.NodeVisitor):
    """
    A class to analyze and extract decorators applied to a specific class or its methods.

    This class uses the `ast` module to parse the source code of a given class and
    extract the names of decorators applied to the class or its methods.

    Parameters
    ----------
    cls : Type
        The class to analyze for decorators.

    Attributes
    ----------
    decorators : List[str]
        A list of unique decorator names applied to the class or its methods.

    Methods
    -------
    parse()
        Parses the source code of the class and extracts decorator names.
    visit_FunctionDef(node)
        Visits function definitions in the AST and extracts their decorators.
    visit_ClassDef(node)
        Visits the class definition in the AST and extracts its decorators.
    get_class_decorators() -> List[str]
        Retrieves the decorators applied to the class itself.
    get_method_decorators(method_name: str) -> List[str]
        Retrieves the decorators for a specific method in the class.
    """

    def __init__(self, cls: Type):
        """
        Initializes the ReflectiveDecorators with the class to analyze.

        Parameters
        ----------
        cls : Type
            The class to analyze for decorators.
        """
        self._decorators: List[str] = []
        self._method_decorators: dict = {}
        self._class_decorators: List[str] = []
        self._cls = cls
        self._parsed = False

    def visit_ParseSource(self) -> None:
        """
        Parses the source code of the class and extracts decorator names.

        This method retrieves the source code of the class using `inspect.getsource`,
        parses it into an abstract syntax tree (AST), and visits relevant nodes
        to extract decorator names.

        Returns
        -------
        dict
            A dictionary containing lists of decorators:
            - 'decorators': All unique decorators found in the class and its methods.
            - 'method_decorators': A dictionary mapping method names to their decorators.
            - 'class_decorators': A list of decorators applied to the class itself.
        """
        if not self._parsed:

            # Try to get the source code of the class
            try:
                source = inspect.getsource(self._cls)
            except (OSError, TypeError):
                source = ""

            # Parsed flag to avoid re-parsing
            self._parsed = True

            # If source code is not available, return empty lists
            if not source:
                return

            # Parse the source code into an AST
            tree = ast.parse(source)

            # Visit the AST to extract decorators
            self.visit(tree)

            # Remove duplicates and non-decorator entries
            self._decorators = list(set(self._decorators))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visits function definitions in the AST and extracts their decorators.

        Parameters
        ----------
        node : ast.FunctionDef
            The function definition node in the AST.

        Returns
        -------
        None
        """
        method_decos = []
        for deco in node.decorator_list:
            if isinstance(deco, ast.Name):
                self._decorators.append(deco.id)
                method_decos.append(deco.id)
            elif isinstance(deco, ast.Call):
                # Handles decorators with arguments like @deco(arg)
                if isinstance(deco.func, ast.Name):
                    self._decorators.append(deco.func.id)
                    method_decos.append(deco.func.id)
            elif isinstance(deco, ast.Attribute):
                self._decorators.append(deco.attr)
                method_decos.append(deco.attr)

        # Store method-specific decorators
        self._method_decorators[node.name] = method_decos

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visits the class definition in the AST and extracts its decorators.

        Parameters
        ----------
        node : ast.ClassDef
            The class definition node in the AST.

        Returns
        -------
        None
        """
        if node.name == self._cls.__name__:
            for deco in node.decorator_list:
                if isinstance(deco, ast.Name):
                    self._decorators.append(deco.id)
                    self._class_decorators.append(deco.id)
                elif isinstance(deco, ast.Call):
                    # Handles decorators with arguments like @deco(arg)
                    if isinstance(deco.func, ast.Name):
                        self._decorators.append(deco.func.id)
                        self._class_decorators.append(deco.func.id)
                elif isinstance(deco, ast.Attribute):
                    self._decorators.append(deco.attr)
                    self._class_decorators.append(deco.attr)

            # Visit methods within the class
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    self.visit_FunctionDef(child)

            # No need to visit deeper
            return

    def visit_NativeDecorator(self, decorator_name: str) -> bool:
        """
        Checks if a decorator name matches Python's native decorator patterns.
        Parameters
        ----------
        decorator_name : str
            The name of the decorator to check.
        Returns
        -------
        bool
            True if the decorator name matches any of the predefined native patterns,
            False otherwise.
        Notes
        -----
        The method uses a list of regular expressions to identify native Python
        decorators, including built-ins, standard library modules (e.g., `functools`,
        `dataclasses`, `contextlib`), and other commonly used patterns. It also
        accounts for deprecated or obsolete decorators.
        """

        native_decorator_regular_expr = [
            # Built-ins
            r"^property$",
            r"^\w+\.setter$",
            r"^\w+\.deleter$",
            r"^classmethod$",
            r"^staticmethod$",

            # abc module
            r"^abstractmethod$",
            r"^abstractclassmethod$",
            r"^abstractstaticmethod$",

            # functools
            r"^functools\.cache$",
            r"^functools\.lru_cache(\(.*\))?$",
            r"^functools\.cached_property$",
            r"^functools\.singledispatch$",
            r"^functools\.singledispatchmethod$",
            r"^functools\.wraps(\(.*\))?$",

            # dataclasses
            r"^dataclasses\.dataclass(\(.*\))?$",

            # contextlib
            r"^contextlib\.contextmanager$",

            # typing
            r"^typing\.final$",
            r"^typing\.overload$",

            # enum
            r"^enum\.unique$",

            # asyncio (obsoleto)
            r"^asyncio\.coroutine$",

            # unittest.mock
            r"^unittest\.mock\.patch(\(.*\))?$",

            # Añadidos adicionales
            r"^contextlib\.asynccontextmanager$",
            r"^typing\.runtime_checkable$",
            r"^collections\.abc\.abstractproperty$",
        ]

        return any(re.fullmatch(pattern, decorator_name) for pattern in native_decorator_regular_expr)

    def getClassDecorators(self) -> ClassDecorators:
        """
        Retrieves the decorators applied to the class itself.

        Returns
        -------
        ClassDecorators
            An object containing lists of decorator names for the class.
        """

        # Parse the source code to extract decorators
        self.visit_ParseSource()

        # Filter decorators into user-defined and native
        user_defined = []
        native = []

        # Filter decorators into user-defined and native
        for deco in self._class_decorators:
            if not self.visit_NativeDecorator(deco):
                user_defined.append(deco)
            else:
                native.append(deco)

        # Return a ClassDecorators object containing the filtered lists
        return ClassDecorators(
            user_defined=tuple(user_defined),
            native=tuple(native),
            all=tuple(self._class_decorators)
        )

    def getMethodDecorators(self, method_name: str = None) -> MethodDecorators:
        """
        Retrieves the decorators for a specific method in the class.

        Parameters
        ----------
        method_name : str
            The name of the method to retrieve decorators for.

        Returns
        -------
        MethodDecorators
            An object containing lists of decorator names for the specified method.
        """

        # Parse the source code to extract decorators
        self.visit_ParseSource()

        # Handle mangled names for private methods
        # Check if the method name is mangled (private)
        if method_name.startswith("__") and not method_name.endswith("__"):
            method_name = f"_{self._cls.__name__}{method_name}"

        # Get the decorators for the specified method
        decorators = self._method_decorators.get(method_name, [])

        # Filter decorators into user-defined and native
        user_defined = []
        native = []

        # Filter decorators into user-defined and native
        for deco in decorators:
            if not self.visit_NativeDecorator(deco):
                user_defined.append(deco)
            else:
                native.append(deco)

        # Return a MethodDecorators object containing the filtered lists
        return MethodDecorators(
            user_defined=tuple(user_defined),
            native=tuple(native),
            all=tuple(decorators)
        )