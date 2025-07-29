import multiprocessing
import math
import psutil
from orionis.services.system.contracts.workers import IWorkers

class Workers(IWorkers):
    """
    Calculates the optimal number of workers a machine can handle based on CPU and memory resources.

    This class estimates the maximum number of Uvicorn (or similar) workers by considering:
    - The number of available CPU cores.
    - The total system memory (RAM).
    - The estimated memory usage per worker (configurable).

    Parameters
    ----------
    ram_per_worker : float, optional
        Estimated amount of RAM (in GB) that each worker will consume. Default is 0.5 GB.
    """

    def __init__(self, ram_per_worker: float = 0.5):
        self._cpu_count = multiprocessing.cpu_count()
        self._ram_total_gb = psutil.virtual_memory().total / (1024 ** 3)
        self._ram_per_worker = ram_per_worker

    def calculate(self) -> int:
        """
        Computes the maximum number of workers supported by the current machine.

        Returns
        -------
        int
            The recommended number of worker processes based on CPU and memory limits.
        """
        max_workers_by_cpu = self._cpu_count
        max_workers_by_ram = math.floor(self._ram_total_gb / self._ram_per_worker)
        return min(max_workers_by_cpu, max_workers_by_ram)
