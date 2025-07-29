from orionis._contracts.services.commands.reactor_commands_service import IReactorCommandsService
from orionis._contracts.services.config.config_service import IConfigService
from orionis._contracts.services.log.log_service import ILogguerService
from orionis._providers.service_provider import ServiceProvider
from orionis._services.commands.reactor_commands_service import ReactorCommandsService
from orionis._services.config.config_service import ConfigService
from orionis._services.log.log_service import LogguerService

class ReactorCommandsServiceProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers services or bindings into the given container.
        """
        if not self.app.bound(IConfigService):
            self.app.scoped(IConfigService, ConfigService)

        if not self.app.bound(ILogguerService):
            self.app.singleton(ILogguerService, LogguerService)

        self.app.singleton(IReactorCommandsService, ReactorCommandsService)

    async def boot(self) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.
        """
        await self.app.make(IReactorCommandsService)