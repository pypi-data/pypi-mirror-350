from orionis.foundation.config.startup import Configuration
from orionis.patterns.singleton.meta_class import Singleton

class Orionis(metaclass=Singleton):

    def __init__(
        self,
        config: Configuration = None
    ):
        self.__config = config or Configuration()