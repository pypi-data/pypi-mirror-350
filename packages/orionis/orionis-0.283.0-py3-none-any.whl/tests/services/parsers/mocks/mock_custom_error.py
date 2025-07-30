class CustomError(Exception):
    """
    A custom exception class for handling errors with an optional error code.
    """

    def __init__(self, message, code=None):
        """
        Initialize the custom error with a message and an optional error code.

        Args:
            message (str): The error message describing the exception.
            code (Optional[Any]): An optional error code associated with the exception.
        """
        super().__init__(message)
        self.code = code