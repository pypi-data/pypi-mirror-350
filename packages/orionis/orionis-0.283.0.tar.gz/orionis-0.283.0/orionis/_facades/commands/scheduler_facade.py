from typing import Any
from orionis._contracts.facades.commands.scheduler_facade import ISchedule
from orionis._contracts.services.commands.schedule_service import IScheduleService
from orionis._facades.app_facade import app

class Schedule(ISchedule):

    @staticmethod
    def command(signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> 'IScheduleService':
        """
        Defines a Orionis command to be executed.

        Parameters
        ----------
        signature : str
            The signature of the command to execute.
        vars : dict, optional
            A dictionary of variables to pass to the command, by default an empty dictionary.
        *args : Any
            Additional positional arguments to pass to the command.
        **kwargs : Any
            Additional keyword arguments to pass to the command.

        Returns
        -------
        Schedule
            Returns the Schedule instance itself, allowing method chaining.
        """
        _scheduler_provider : IScheduleService = app(IScheduleService)
        return _scheduler_provider.command(signature, vars, *args, **kwargs)

    @staticmethod
    def start():
        """
        Starts the scheduler and stops automatically when there are no more jobs.
        """
        _scheduler_provider : IScheduleService = app(IScheduleService)
        return _scheduler_provider.start()