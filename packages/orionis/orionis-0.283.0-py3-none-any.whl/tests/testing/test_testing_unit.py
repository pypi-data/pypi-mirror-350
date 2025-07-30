from orionis.test.cases.test_case import TestCase
from orionis.unittesting import UnitTest, ExecutionMode, UnittestTestLoader, UnittestTestSuite, unittest_mock_patch, UnittestMagicMock, UnittestTestResult

class TestUnitTest(TestCase):
    """
    Test cases for the UnitTest class which handles test discovery and execution.
    """

    async def testDefaultConfiguration(self):
        """
        Test that UnitTest initializes with correct default configuration values.
        Verifies that all default attributes are set as expected upon initialization.
        """
        unit_test = UnitTest()
        self.assertEqual(unit_test.verbosity, 2)
        self.assertEqual(unit_test.execution_mode, ExecutionMode.SEQUENTIAL.value)
        self.assertEqual(unit_test.max_workers, 4)
        self.assertFalse(unit_test.fail_fast)
        self.assertTrue(unit_test.print_result)
        self.assertIsInstance(unit_test.loader, UnittestTestLoader)
        self.assertIsInstance(unit_test.suite, UnittestTestSuite)

    async def testConfigureMethod(self):
        """
        Test that configure method properly updates configuration values.
        Verifies that all configuration parameters can be updated through the configure method.
        """
        unit_test = UnitTest()
        configured = unit_test.configure(
            verbosity=1,
            execution_mode=ExecutionMode.PARALLEL,
            max_workers=8,
            fail_fast=True,
            print_result=False,
            throw_exception=True
        )

        self.assertEqual(unit_test.verbosity, 1)
        self.assertEqual(unit_test.execution_mode, ExecutionMode.PARALLEL.value)
        self.assertEqual(unit_test.max_workers, 8)
        self.assertTrue(unit_test.fail_fast)
        self.assertFalse(unit_test.print_result)
        self.assertTrue(unit_test.throw_exception)
        self.assertEqual(configured, unit_test)

    async def testDiscoverTestsInModule(self):
        """
        Test that discoverTestsInModule correctly loads tests from a module.
        Verifies that tests can be discovered from a module and added to the test suite.
        """
        unit_test = UnitTest()
        with unittest_mock_patch.object(unit_test.loader, 'loadTestsFromName') as mock_load:
            mock_load.return_value = UnittestTestSuite()
            result = unit_test.discoverTestsInModule('test_module')

            mock_load.assert_called_once_with('test_module')
            self.assertEqual(result, unit_test)
            self.assertEqual(len(unit_test.suite._tests), 0)

    async def testFlattenTestSuite(self):
        """
        Test that _flattenTestSuite correctly flattens nested test suites.

        Verifies that both simple and nested test suites are properly flattened.
        """
        unit_test = UnitTest()
        test_case1 = UnittestMagicMock()
        test_case2 = UnittestMagicMock()

        nested_suite = UnittestTestSuite()
        nested_suite.addTest(test_case1)
        nested_suite.addTest(test_case2)

        main_suite = UnittestTestSuite()
        main_suite.addTest(nested_suite)

        flattened = unit_test._flattenTestSuite(main_suite)
        self.assertEqual(len(flattened), 2)
        self.assertIn(test_case1, flattened)
        self.assertIn(test_case2, flattened)

    async def testMergeTestResults(self):
        """
        Test that _mergeTestResults correctly combines test results.

        Verifies that test counts, failures, and errors are properly merged.
        """
        unit_test = UnitTest()
        combined = UnittestTestResult()
        individual = UnittestTestResult()

        individual.testsRun = 2
        individual.failures = [('test1', 'failure')]
        individual.errors = [('test2', 'error')]

        unit_test._mergeTestResults(combined, individual)
        self.assertEqual(combined.testsRun, 2)
        self.assertEqual(len(combined.failures), 1)
        self.assertEqual(len(combined.errors), 1)

    async def testClearTests(self):
        """
        Test that clearTests method resets the test suite.
        Verifies that the test suite is emptied when clearTests is called.
        """
        unit_test = UnitTest()
        mock_test = UnittestMagicMock()
        unit_test.suite.addTest(mock_test)

        unit_test.clearTests()
        self.assertEqual(len(unit_test.suite._tests), 0)

    async def testGetTestNames(self):
        """
        Test that getTestNames returns correct test identifiers.
        Verifies that test names are properly extracted from the test suite.
        """
        unit_test = UnitTest()
        mock_test = UnittestMagicMock()
        mock_test.id.return_value = 'test_id'
        unit_test.suite.addTest(mock_test)

        names = unit_test.getTestNames()
        self.assertEqual(names, ['test_id'])

    async def testGetTestCount(self):
        """
        Test that getTestCount returns the correct number of tests.
        Verifies that the count matches the number of tests in the suite.
        """
        unit_test = UnitTest()
        mock_test1 = UnittestMagicMock()
        mock_test2 = UnittestMagicMock()
        unit_test.suite.addTest(mock_test1)
        unit_test.suite.addTest(mock_test2)

        count = unit_test.getTestCount()
        self.assertEqual(count, 2)