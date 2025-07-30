class OrionisTestConfigException(Exception):
    """
    Custom exception for test configuration errors in the Orionis framework.

    This exception is raised when there is an issue with the test configuration,
    providing a clear and descriptive error message to aid in debugging.
    """

    def __init__(self, msg: str):
        """
        Initializes the OrionisTestConfigException with a specific error message.

        Args:
            msg (str): A descriptive error message explaining the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the exception.

        The string includes the exception name and the error message, providing
        a clear and concise description of the issue.

        Returns:
            str: A formatted string describing the exception.
        """
        return f"{self.__class__.__name__}: {self.args[0]}"
