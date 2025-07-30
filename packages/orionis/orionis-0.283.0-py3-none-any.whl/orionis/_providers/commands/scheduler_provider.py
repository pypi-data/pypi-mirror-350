from orionis._contracts.services.commands.schedule_service import IScheduleService
from orionis._providers.service_provider import ServiceProvider
from orionis._services.commands.scheduler_service import ScheduleService

class ScheduleServiceProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers services or bindings into the given container.
        """
        self.app.scoped(IScheduleService, ScheduleService)
