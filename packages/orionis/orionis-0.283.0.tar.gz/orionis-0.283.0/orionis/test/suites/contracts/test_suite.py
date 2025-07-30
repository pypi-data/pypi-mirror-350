from abc import ABC, abstractmethod
from orionis.foundation.config.testing.entities.testing import Testing as Configuration
from orionis.test.suites.test_unit import UnitTest

class ITestSuite(ABC):
    """
    Interface for configuring and running a UnitTest suite using a provided Configuration.
    Methods:
        run(config: Configuration = None) -> UnitTest
    """

    @abstractmethod
    def run(self, config: Configuration = None) -> UnitTest:
        """
        Runs the test suite based on the provided configuration.
        Args:
            config (Configuration, optional): An optional Configuration object for the test suite.
        Returns:
            UnitTest: The result of the executed test suite.
        Raises:
            OrionisTestConfigException: If the config parameter is not an instance of Configuration.
        """
        pass
