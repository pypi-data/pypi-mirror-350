from dataclasses import dataclass
from typing import List
from orionis.support.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.support.introspection.instances.entities.class_attributes import ClassAttributes
from orionis.support.introspection.instances.entities.class_method import ClassMethod
from orionis.support.introspection.instances.entities.class_property import ClassProperty

@dataclass(frozen=True, kw_only=True)
class ClassParsed:
    """
    A class to represent the parsed information of a class instance.
    """
    name : str = None
    module : str = None
    attributes : ClassAttributes = None
    methods : ClassMethod = None
    properties : List[ClassProperty] = None,
    dependencies : ClassDependency = None