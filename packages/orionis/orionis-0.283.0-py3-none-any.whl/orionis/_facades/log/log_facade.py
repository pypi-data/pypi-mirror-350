from orionis._contracts.facades.facade import Facade
from orionis._contracts.services.log.log_service import ILogguerService

class Log(Facade):
    """
    Log Facade class. This is the friendly interface for interacting with the logging service.
    It's like the concierge of your application's logging system—always ready to help!
    """

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the service accessor for the logging system. In this case, it's the `ILogguerService`.
        This is where the magic of the Facade pattern comes alive—connecting the interface to the actual service.
        """
        return ILogguerService