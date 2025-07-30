class ReflexionModule:
    """A reflection object encapsulating a module.

    Parameters
    ----------
    module : str
        The module name being reflected upon

    Attributes
    ----------
    _module : str
        The encapsulated module name
    """

    def __init__(self, module: str) -> None:
        """Initialize with the module name."""
        self._module = module


