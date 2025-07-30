from dataclasses import dataclass
import inspect
from typing import Any

@dataclass(frozen=True, kw_only=True)
class ClassProperty:
    """
    A class to represent a property of a class instance.
    """
    name: str
    value: Any
    signature: inspect.Signature
    doc: str