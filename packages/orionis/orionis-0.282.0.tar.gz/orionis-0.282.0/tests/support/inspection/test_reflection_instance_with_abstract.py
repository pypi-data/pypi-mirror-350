from orionis.support.introspection.reflexion_instance_with_abstract import ReflexionInstanceWithAbstract
from orionis.test import TestCase
from tests.support.inspection.fakes.fake_reflection_instance_with_abstract import FakeDataProcessor, IDataProcessor

class TestReflexionInstanceWithAbstract(TestCase):

    async def testReflexionInstanceWithAbstractGetImplementationAnalysis(self):
        """Test reflexion con IDataProcessor y FakeDataProcessor."""
        processor = FakeDataProcessor()
        inspector = ReflexionInstanceWithAbstract(processor, IDataProcessor)

        # Get Implementation analysis
        analysis = inspector.getImplementationAnalysis()

        # Verifying implemented methods
        self.assertTrue(analysis['validate_input']['implemented'])
        self.assertEqual(str(analysis['validate_input']['abstract_signature']), "(self, raw_data: str) -> bool")
        self.assertEqual(str(analysis['validate_input']['concrete_signature']), "(source: str) -> bool")
        self.assertFalse(analysis['validate_input']['signature_match'])
        self.assertEqual(analysis['validate_input']['type'], 'method')

        self.assertTrue(analysis['process']['implemented'])
        self.assertEqual(str(analysis['process']['abstract_signature']), "(self, data: List[float]) -> Dict[str, float]")
        self.assertEqual(str(analysis['process']['concrete_signature']), "(values: List[float]) -> Dict[str, float]")
        self.assertFalse(analysis['process']['signature_match'])
        self.assertEqual(analysis['process']['type'], 'method')

        self.assertTrue(analysis['config']['implemented'])
        self.assertEqual(str(analysis['config']['abstract_signature']), "(self) -> Dict[str, str]")
        self.assertEqual(str(analysis['config']['concrete_signature']), "(self) -> Dict[str, str]")
        self.assertTrue(analysis['config']['signature_match'])
        self.assertEqual(analysis['config']['type'], 'property')

    async def testReflexionInstanceWithAbstractGetNonInheritedImplementation(self):
        """Test reflexion con IDataProcessor y FakeDataProcessor."""
        processor = FakeDataProcessor()
        inspector = ReflexionInstanceWithAbstract(processor, IDataProcessor)

        # Get Non-Inherited implementation analysis
        analysis = inspector.getNonInheritedImplementation()

        # Verifying implemented methods
        self.assertIn('extra_method', analysis['methods'])

    async def testReflexionInstanceWithAbstractValidateImplementation(self):
        """Test reflexion con IDataProcessor y FakeDataProcessor."""
        processor = FakeDataProcessor()
        inspector = ReflexionInstanceWithAbstract(processor, IDataProcessor)

        # Get Implementation analysis
        is_valid, issues = inspector.validateImplementation()

        # Verifying implemented methods
        self.assertFalse(is_valid)
        self.assertIn('process', issues['signature_mismatch'])

    async def testReflexionInstanceWithAbstractGetHierarchyAnalysis(self):
        """Test reflexion con IDataProcessor y FakeDataProcessor."""
        processor = FakeDataProcessor()
        inspector = ReflexionInstanceWithAbstract(processor, IDataProcessor)

        # Get Hierarchy analysis
        analysis = inspector.getHierarchyAnalysis()

        # Verifying implemented methods
        self.assertEqual(analysis['common_ancestors'], [])
        self.assertIn('IDataProcessor', analysis['abstract_hierarchy'])
        self.assertIn('FakeDataProcessor', analysis['concrete_hierarchy'])

    async def testReflexionInstanceWithAbstractGetImplementationCoverage(self):
        """Test reflexion con IDataProcessor y FakeDataProcessor."""
        processor = FakeDataProcessor()
        inspector = ReflexionInstanceWithAbstract(processor, IDataProcessor)

        # Get Implementation coverage
        coverage = inspector.getImplementationCoverage()

        # Verifying implemented methods
        self.assertTrue(coverage >= 0.66)