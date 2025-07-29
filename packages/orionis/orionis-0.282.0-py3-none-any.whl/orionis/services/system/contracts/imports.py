from abc import ABC, abstractmethod

class IImports(ABC):
    """
    Interface for a utility to collect and display information about currently loaded Python modules.
    """

    @abstractmethod
    def collect(self):
        """
        Collects information about user-defined Python modules currently loaded in sys.modules.
        Returns:
            IImports: The current instance with updated imports information.
        """
        pass

    @abstractmethod
    def display(self) -> None:
        """
        Displays a formatted table of collected import statements.
        Returns:
            None
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the collected imports list.
        """
        pass