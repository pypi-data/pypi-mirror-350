class ReflexionModuleWithClassName:
    """A reflection object encapsulating a module and a class name.

    Parameters
    ----------
    module : str
        The module name being reflected upon
    class_name : str
        The class name in the module

    Attributes
    ----------
    _module : str
        The encapsulated module name
    _class_name : str
        The encapsulated class name
    """

    def __init__(self, module: str, class_name: str) -> None:
        """Initialize with the module name and class name."""
        self._module = module
        self._class_name = class_name