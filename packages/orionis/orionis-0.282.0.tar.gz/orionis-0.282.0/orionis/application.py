from orionis.foundation.config.startup import Configuration

class Orionis:

    def __init__(
        self,
        config: Configuration = None
    ):
        """
        Initializes the Orionis instance with optional configuration objects.

        Args:
            config (Configuration, optional): Custom application configuration.
        """
        self.__config = config or Configuration()