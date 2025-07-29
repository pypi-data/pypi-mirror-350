from orionis.support.introspection.reflexion_concrete_with_abstract import ReflexionConcreteWithAbstract
from orionis.test import TestCase
from tests.support.inspection.fakes.fake_reflection_concrete_with_abstract import AbstractService, PartiallyImplementedService

class TestReflexionConcreteWithAbstract(TestCase):

    async def testReflexionInstanceWithAbstractGetImplementationAnalysis(self):
        """Test reflexion con AbstractService y PartiallyImplementedService."""
        inspector = ReflexionConcreteWithAbstract(PartiallyImplementedService, AbstractService)

        # Get Implementation analysis
        analysis = inspector.getImplementationAnalysis()

        # Verifying implemented methods
        self.assertFalse(analysis['configure']['implemented'])
        self.assertIsNone(analysis['configure']['abstract_signature'])
        self.assertIsNone(analysis['configure']['concrete_signature'])
        self.assertFalse(analysis['configure']['signature_match'])
        self.assertEqual(analysis['configure']['type'], 'method')

        self.assertTrue(analysis['get_logs']['implemented'])
        self.assertEqual(str(analysis['get_logs']['abstract_signature']), "(self, limit: int = 10) -> List[str]")
        self.assertEqual(str(analysis['get_logs']['concrete_signature']), "(self, limit: int = 10) -> List[str]")
        self.assertTrue(analysis['get_logs']['signature_match'])
        self.assertEqual(analysis['get_logs']['type'], 'method')

        self.assertFalse(analysis['reset']['implemented'])
        self.assertIsNone(analysis['reset']['abstract_signature'])
        self.assertIsNone(analysis['reset']['concrete_signature'])
        self.assertFalse(analysis['reset']['signature_match'])
        self.assertEqual(analysis['reset']['type'], 'method')

        self.assertTrue(analysis['process']['implemented'])
        self.assertEqual(str(analysis['process']['abstract_signature']), "(self, data: str) -> bool")
        self.assertEqual(str(analysis['process']['concrete_signature']), "(self, data: str) -> bool")
        self.assertTrue(analysis['process']['signature_match'])
        self.assertEqual(analysis['process']['type'], 'method')

        self.assertFalse(analysis['status']['implemented'])
        self.assertIsNone(analysis['status']['abstract_signature'])
        self.assertIsNone(analysis['status']['concrete_signature'])
        self.assertFalse(analysis['status']['signature_match'])
        self.assertEqual(analysis['status']['type'], 'property')

    async def testReflexionConcreteWithAbstractGetNonInheritedImplementation(self):
        """Test reflexion con AbstractService y PartiallyImplementedService."""
        inspector = ReflexionConcreteWithAbstract(PartiallyImplementedService, AbstractService)

        # Get Non-Inherited implementation analysis
        analysis = inspector.getNonInheritedImplementation()

        self.assertIn('extra', analysis['methods'])
        self.assertListEqual(analysis['properties'], [])
        self.assertIn('__annotations__', analysis['attributes'])

    async def testReflexionConcreteWithAbstractValidateImplementation(self):
        """Test reflexion con AbstractService y PartiallyImplementedService."""
        inspector = ReflexionConcreteWithAbstract(PartiallyImplementedService, AbstractService)

        # Get Implementation analysis
        is_valid, issues = inspector.validateImplementation()

        # Verifying implemented methods
        self.assertFalse(is_valid)
        self.assertIn('reset', issues['missing'])

    async def testReflexionConcreteWithAbstractGetHierarchyAnalysis(self):
        """Test reflexion con AbstractService y PartiallyImplementedService."""
        inspector = ReflexionConcreteWithAbstract(PartiallyImplementedService, AbstractService)

        # Get Hierarchy analysis
        analysis = inspector.getHierarchyAnalysis()

        # Verifying implemented methods
        self.assertEqual(analysis['common_ancestors'], [])
        self.assertIn('AbstractService', analysis['abstract_hierarchy'])
        self.assertIn('PartiallyImplementedService', analysis['concrete_hierarchy'])

    async def testReflexionConcreteWithAbstractGetImplementationCoverage(self):
        """Test reflexion con AbstractService y PartiallyImplementedService."""
        inspector = ReflexionConcreteWithAbstract(PartiallyImplementedService, AbstractService)

        # Get Implementation coverage
        coverage = inspector.getImplementationCoverage()

        # Verifying implemented methods
        self.assertTrue(coverage >= 0.4)