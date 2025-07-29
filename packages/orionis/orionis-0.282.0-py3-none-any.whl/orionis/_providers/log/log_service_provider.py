from orionis._contracts.services.config.config_service import IConfigService
from orionis._contracts.services.log.log_service import ILogguerService
from orionis._providers.service_provider import ServiceProvider
from orionis._services.config.config_service import ConfigService
from orionis._services.log.log_service import LogguerService

class LogServiceProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers services or bindings into the given container.
        """
        if not self.app.bound(IConfigService):
            self.app.scoped(IConfigService, ConfigService)

        self.app.singleton(ILogguerService, LogguerService)

    async def boot(self) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.
        """
        await self.app.make(ILogguerService)