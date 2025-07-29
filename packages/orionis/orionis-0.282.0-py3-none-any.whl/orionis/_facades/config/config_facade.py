from typing import Any, Optional
from orionis._contracts.facades.config.config_facade import IConfig
from orionis._contracts.services.config.config_service import IConfigService
from orionis._facades.app_facade import app

class Config(IConfig):

    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Dynamically sets a configuration value using dot notation.

        Parameters
        ----------
        key : str
            The configuration key (e.g., 'app.debug').
        value : Any
            The value to set.
        """
        _config_service_provider : IConfigService = app(IConfigService)
        return _config_service_provider.set(key, value)

    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration value using dot notation.

        Parameters
        ----------
        key : str
            The configuration key (e.g., 'app.debug').
        default : Optional[Any]
            The default value to return if the key is not found.

        Returns
        -------
        Any
            The configuration value or the default value if the key is not found.
        """
        _config_service_provider : IConfigService = app(IConfigService)
        return _config_service_provider.get(key, default)