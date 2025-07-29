from abc import ABC, abstractmethod

class IWorkers(ABC):
    """
    Interface - Calculates the optimal number of workers a machine can handle based on CPU and memory resources.
    """

    @abstractmethod
    def calculate(self) -> int:
        """
        Computes the maximum number of workers supported by the current machine.

        Returns
        -------
        int
            The recommended number of worker processes based on CPU and memory limits.
        """
        pass