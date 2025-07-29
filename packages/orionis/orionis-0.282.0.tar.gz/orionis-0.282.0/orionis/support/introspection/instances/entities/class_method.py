from dataclasses import dataclass
from typing import List

@dataclass(frozen=False, kw_only=True)
class ClassMethod:
    """
    A class to represent the methods of a class instance.
    """
    public: List[str]
    private: List[str]
    protected: List[str]
    static: List[str]
    asynchronous: List[str]
    synchronous: List[str]
    class_methods: List[str]
    asynchronous_static: List[str]
    synchronous_static: List[str]
    magic: List[str]