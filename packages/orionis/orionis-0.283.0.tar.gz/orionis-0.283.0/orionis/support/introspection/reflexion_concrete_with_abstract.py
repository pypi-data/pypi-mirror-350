import abc
import inspect
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union
from orionis.support.introspection.abstracts.reflect_abstract import ReflexionAbstract
from orionis.support.introspection.reflexion_concrete import ReflexionConcrete

T = TypeVar('T')
ABC = TypeVar('ABC', bound=abc.ABC)

class ReflexionConcreteWithAbstract:
    """Advanced reflection tool for analyzing concrete classes against abstract bases.

    Allows static analysis of class definitions to verify compatibility
    and adherence to interface contracts without instantiation.

    Parameters
    ----------
    concrete : Type[T]
        The concrete class to inspect
    abstract : Type[ABC]
        The abstract base class/interface being implemented

    Attributes
    ----------
    _concrete : Type[T]
        The concrete class being analyzed
    _abstract : Type[ABC]
        The abstract base class/interface
    _concrete_reflexion : ReflexionConcrete
        Reflection helper for the concrete class
    _abstract_reflexion : ReflexionAbstract
        Reflection helper for the abstract class
    """

    def __init__(self, concrete: Type[T], abstract: Type[ABC]) -> None:
        self._concrete = concrete
        self._abstract = abstract
        self._concrete_reflexion = ReflexionConcrete(concrete)
        self._abstract_reflexion = ReflexionAbstract(abstract)

    @property
    def concrete(self) -> ReflexionConcrete:
        """Access the concrete class reflection helper."""
        return self._concrete_reflexion

    @property
    def abstract(self) -> ReflexionAbstract:
        """Access the abstract class reflection helper."""
        return self._abstract_reflexion

    def getImplementationAnalysis(self) -> Dict[str, Dict[str, Union[bool, str, inspect.Signature]]]:
        """Comprehensive analysis of implementation compliance."""
        analysis = {}

        abstract_methods = self._abstract_reflexion.getAbstractMethods()
        for method in abstract_methods:
            entry = {
                'implemented': False,
                'abstract_signature': None,
                'concrete_signature': None,
                'signature_match': False,
                'type': 'method'
            }

            if hasattr(self._concrete, method):
                entry['implemented'] = True
                abstract_sig = self._abstract_reflexion.getMethodSignature(method)
                concrete_sig = self._concrete_reflexion.getMethodSignature(method)

                entry.update({
                    'abstract_signature': abstract_sig,
                    'concrete_signature': concrete_sig,
                    'signature_match': (
                        abstract_sig.parameters == concrete_sig.parameters and
                        abstract_sig.return_annotation == concrete_sig.return_annotation
                    )
                })

            analysis[method] = entry

        abstract_properties = self._abstract_reflexion.getAbstractProperties()
        for prop in abstract_properties:
            entry = {
                'implemented': False,
                'abstract_signature': None,
                'concrete_signature': None,
                'signature_match': False,
                'type': 'property'
            }

            if hasattr(self._concrete, prop):
                entry['implemented'] = True
                abstract_sig = self._abstract_reflexion.getPropertySignature(prop)
                concrete_sig = self._concrete_reflexion.getPropertySignature(prop)

                entry.update({
                    'abstract_signature': abstract_sig,
                    'concrete_signature': concrete_sig,
                    'signature_match': (
                        abstract_sig.parameters == concrete_sig.parameters and
                        abstract_sig.return_annotation == concrete_sig.return_annotation
                    )
                })

            analysis[prop] = entry

        return analysis

    def validateImplementation(self) -> Tuple[bool, Dict[str, List[str]]]:
        """Validate the implementation against the abstract base."""
        issues = {
            'missing': [],
            'signature_mismatch': [],
            'type_mismatch': []
        }

        analysis = self.getImplementationAnalysis()
        for name, data in analysis.items():
            if not data['implemented']:
                issues['missing'].append(name)
            elif not data['signature_match']:
                issues['signature_mismatch'].append(name)
                abstract_return = data['abstract_signature'].return_annotation
                concrete_return = data['concrete_signature'].return_annotation
                if abstract_return != concrete_return and abstract_return is not inspect.Parameter.empty:
                    issues['type_mismatch'].append(name)

        is_valid = not any(issues.values())
        return (is_valid, issues)

    def getImplementationCoverage(self) -> float:
        """Calculate the percentage of abstract methods/properties implemented."""
        analysis = self.getImplementationAnalysis()
        total = len(analysis) * 2
        implemented = 0
        for item in analysis.values():
            if item['implemented']:
                implemented += 2 if item['signature_match'] else 1
        return implemented / total if total else 0.0

    def getNonInheritedImplementation(self) -> Dict[str, Any]:
        """Get implementation details for methods, properties, and attributes not inherited from the abstract base."""
        concrete_members = set(dir(self._concrete))
        base_members = set(dir(self._abstract))

        non_inherited_methods = [
            name for name in concrete_members
            if callable(getattr(self._concrete, name, None)) and name not in base_members
        ]

        non_inherited_properties = [
            name for name in concrete_members
            if isinstance(getattr(self._concrete, name, None), property) and name not in base_members
        ]

        non_inherited_attributes = {
            name: getattr(self._concrete, name, None)
            for name in concrete_members
            if (
                not callable(getattr(self._concrete, name, None)) and
                not isinstance(getattr(self._concrete, name, None), property) and
                name not in base_members
            )
        }

        return {
            'methods': non_inherited_methods,
            'properties': non_inherited_properties,
            'attributes': non_inherited_attributes
        }

    def getHierarchyAnalysis(self) -> Dict[str, List[str]]:
        """Analyze the class hierarchy relationships."""
        concrete_hierarchy = [cls.__name__ for cls in inspect.getmro(self._concrete)]
        abstract_hierarchy = [cls.__name__ for cls in inspect.getmro(self._abstract)]

        concrete_bases = set(inspect.getmro(self._concrete))
        abstract_bases = set(inspect.getmro(self._abstract))
        common = concrete_bases & abstract_bases - {self._abstract, object}

        return {
            'concrete_hierarchy': concrete_hierarchy,
            'abstract_hierarchy': abstract_hierarchy,
            'common_ancestors': [cls.__name__ for cls in common]
        }
