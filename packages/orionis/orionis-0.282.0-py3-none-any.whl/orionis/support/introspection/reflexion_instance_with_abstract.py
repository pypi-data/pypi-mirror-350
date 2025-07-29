import abc
import inspect
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union
from orionis.support.introspection.abstracts.reflect_abstract import ReflexionAbstract
from orionis.support.introspection.instances.reflection_instance import ReflectionInstance

T = TypeVar('T')
ABC = TypeVar('ABC', bound=abc.ABC)

class ReflexionInstanceWithAbstract:
    """Advanced reflection tool for analyzing concrete implementations against abstract bases.

    Combines inspection of both concrete instances and their abstract parent classes,
    providing detailed comparison and compatibility analysis.

    Parameters
    ----------
    instance : Any
        The concrete instance to inspect
    abstract : Type[ABC]
        The abstract base class/interface being implemented

    Attributes
    ----------
    _instance : Any
        The concrete instance being analyzed
    _abstract : Type[ABC]
        The abstract base class/interface
    _concrete_reflexion : ReflexionInstance
        Reflection helper for the concrete instance
    _abstract_reflexion : ReflexionAbstract
        Reflection helper for the abstract class
    """

    def __init__(self, instance: Any, abstract: Type[ABC]) -> None:
        self._instance = instance
        self._abstract = abstract
        self._concrete_reflexion = ReflectionInstance(instance)
        self._abstract_reflexion = ReflexionAbstract(abstract)

    @property
    def concrete(self) -> ReflectionInstance:
        """Access the concrete instance reflection helper."""
        return self._concrete_reflexion

    @property
    def abstract(self) -> ReflexionAbstract:
        """Access the abstract class reflection helper."""
        return self._abstract_reflexion

    def getImplementationAnalysis(self) -> Dict[str, Dict[str, Union[bool, str, inspect.Signature]]]:
        """Comprehensive analysis of implementation compliance.

        Returns
        -------
        Dict[str, Dict[str, Union[bool, str, inspect.Signature]]]
            Detailed analysis including:
            - 'implemented': Whether method is implemented
            - 'signature_match': Whether signatures match
            - 'abstract_signature': Signature from abstract class
            - 'concrete_signature': Signature from concrete class
        """
        analysis = {}
        abstract_methods = self._abstract_reflexion.getAbstractMethods()
        for method in abstract_methods:
            entry = {
                'implemented': False,
                'abstract_signature': None,
                'concrete_signature': None,
                'signature_match': False,
                'type' : 'method'
            }

            if hasattr(self._instance, method):
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
                'type' : 'property'
            }

            if hasattr(self._instance, prop):
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

    def getNonInheritedImplementation(self) -> Dict[str, Any]:
        """Get implementation details for methods, properties, and attributes not inherited from other parents.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing:
            - 'methods': List of non-inherited method names
            - 'properties': List of non-inherited property names
            - 'attributes': Dict of non-inherited attributes
        """
        # Get all members from concrete class (non-inherited methods, properties, and attributes)
        concrete_members = set(dir(self._instance.__class__))

        # Get members from the abstract class (base class)
        base_members = set(dir(self._abstract))

        # Filter out inherited members (methods, properties, and attributes)
        non_inherited_methods = [
            name for name in concrete_members
            if callable(getattr(self._instance.__class__, name)) and name not in base_members
        ]

        non_inherited_properties = [
            name for name in concrete_members
            if isinstance(getattr(self._instance.__class__, name, None), property) and name not in base_members
        ]

        non_inherited_attributes = {
            name: getattr(self._instance.__class__, name)
            for name in concrete_members
            if not callable(getattr(self._instance.__class__, name)) and not isinstance(getattr(self._instance.__class__, name, None), property) and name not in base_members
        }

        return {
            'methods': non_inherited_methods,
            'properties': non_inherited_properties,
            'attributes': non_inherited_attributes
        }

    def validateImplementation(self) -> Tuple[bool, Dict[str, List[str]]]:
        """Validate the implementation against the abstract base.

        Returns
        -------
        Tuple[bool, Dict[str, List[str]]]
            - First element: True if fully valid implementation
            - Second element: Dictionary of issues by category:
                * 'missing': Missing required methods
                * 'signature_mismatch': Methods with signature mismatches
                * 'type_mismatch': Methods with return type mismatches
        """
        issues = {
            'missing': [],
            'signature_mismatch': [],
            'type_mismatch': []
        }

        analysis = self.getImplementationAnalysis()
        for method, data in analysis.items():
            if not data['implemented']:
                issues['missing'].append(method)
            elif not data['signature_match']:
                issues['signature_mismatch'].append(method)
                # Check specifically for return type mismatch
                abstract_return = data['abstract_signature'].return_annotation
                concrete_return = data['concrete_signature'].return_annotation
                if abstract_return != concrete_return and abstract_return is not inspect.Parameter.empty:
                    issues['type_mismatch'].append(method)

        is_valid = not any(issues.values())
        return (is_valid, issues)

    def getHierarchyAnalysis(self) -> Dict[str, List[str]]:
        """Analyze the class hierarchy relationships.

        Returns
        -------
        Dict[str, List[str]]
            Dictionary containing:
            - 'concrete_hierarchy': List of class names in concrete hierarchy
            - 'abstract_hierarchy': List of class names in abstract hierarchy
            - 'common_ancestors': List of common ancestor class names
        """
        concrete_hierarchy = [cls.__name__ for cls in inspect.getmro(self._instance.__class__)]
        abstract_hierarchy = [cls.__name__ for cls in inspect.getmro(self._abstract)]

        concrete_bases = set(inspect.getmro(self._instance.__class__))
        abstract_bases = set(inspect.getmro(self._abstract))
        common = concrete_bases & abstract_bases - {self._abstract, object}

        return {
            'concrete_hierarchy': concrete_hierarchy,
            'abstract_hierarchy': abstract_hierarchy,
            'common_ancestors': [cls.__name__ for cls in common]
        }

    def getImplementationCoverage(self) -> float:
        """Calculate the percentage of abstract methods implemented.

        Returns
        -------
        float
            Implementation coverage percentage (0.0 to 1.0)
        """
        attr = self.getImplementationAnalysis()
        attr_len = len(attr) * 2
        attr_implemented = 0
        for method in attr.values():
            if method.get('implemented'):
                attr_implemented += 2 if method.get('signature_match') else 1

        return attr_implemented / attr_len if attr_len > 0 else 0.0