from abc import ABC, abstractmethod
from typing import List, Dict

class IDataProcessor(ABC):
    """Interfaz para procesamiento de datos."""

    @property
    @abstractmethod
    def config(self) -> Dict[str, str]:
        """Configuración del procesador."""
        pass

    @abstractmethod
    def process(self, data: List[float]) -> Dict[str, float]:
        """Procesa una lista de números y devuelve métricas."""
        pass

    @abstractmethod
    def validate_input(self, raw_data: str) -> bool:
        """Valida si los datos en crudo pueden ser procesados."""
        pass

class FakeDataProcessor:
    """Implementación concreta fake de IDataProcessor."""

    def __init__(self):
        self._config = {"mode": "standard"}
        self._version = "1.0"

    @property
    def config(self) -> Dict[str, str]:
        """Implementación correcta de la propiedad."""
        return self._config

    def process(self, values: List[float]) -> Dict[str, float]:
        """Implementación con tipo de retorno incorrecto (float vs Dict)."""
        return sum(values) / len(values) if values else 0.0

    def validate_input(self, source: str) -> bool:
        """Implementación con parámetro renombrado (source vs raw_data)."""
        return bool(source)

    def extra_method(self) -> str:
        """Método adicional no definido en la interfaz."""
        return f"Processing with version {self._version}"