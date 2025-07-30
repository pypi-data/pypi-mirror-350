class OrionisIntegrityException(Exception):
    """
    Exception raised for integrity-related errors within the Orionis framework configuration.
    This exception is intended to signal issues or inconsistencies detected in the test configuration,
    helping developers quickly identify and resolve configuration problems. It provides a clear,
    contextual error message to facilitate debugging and maintain the integrity of the framework's setup.
    Attributes:
        msg (str): Human-readable description of the integrity error.
    Example:
        raise OrionisIntegrityException("Duplicate test case identifier found in configuration.")
        msg (str): Detailed explanation of the integrity violation encountered.
    """

    def __init__(self, msg: str):
        """
        Initializes the exception with a custom error message.

        Args:
            msg (str): The error message describing the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Return a string representation of the exception, including the class name and the first argument.

        Returns:
            str: A string in the format '<ClassName>: <first argument>'.
        """
        return f"{self.__class__.__name__}: {self.args[0]}"
