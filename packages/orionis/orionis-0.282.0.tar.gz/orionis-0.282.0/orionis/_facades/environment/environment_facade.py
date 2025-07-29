from orionis._contracts.facades.environment.environment_facade import IEnv
from orionis._contracts.services.environment.environment_service import IEnvironmentService
from orionis._facades.app_facade import app

class Env(IEnv):

    @staticmethod
    def get(key: str, default=None) -> str:
        """
        Retrieves the value of an environment variable from the .env file
        or from system environment variables if not found.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        default : optional
            Default value if the key does not exist. Defaults to None.

        Returns
        -------
        str
            The value of the environment variable or the default value.
        """

        _env_service : IEnvironmentService = app(IEnvironmentService)
        return _env_service.get(key, default)

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Sets the value of an environment variable in the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        value : str
            The value to set.
        """
        _env_service : IEnvironmentService = app(IEnvironmentService)
        return _env_service.set(key, value)

    @staticmethod
    def unset(key: str) -> None:
        """
        Removes an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        _env_service : IEnvironmentService = app(IEnvironmentService)
        return _env_service.unset(key)

    @staticmethod
    def all() -> dict:
        """
        Retrieves all environment variable values from the .env file.

        Returns
        -------
        dict
            A dictionary of all environment variables and their values.
        """
        _env_service : IEnvironmentService = app(IEnvironmentService)
        return _env_service.all()