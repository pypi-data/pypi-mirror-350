from orionis._contracts.services.files.path_resolver_service import IPathResolverService
from orionis._providers.service_provider import ServiceProvider
# from orionis._services.files.path_resolver_service import PathResolverService

class PathResolverProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers services or bindings into the given container.
        """
        pass
        # self.app.singleton(IPathResolverService, PathResolverService)

    async def boot(self) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.
        """
        await self.app.make(IPathResolverService)