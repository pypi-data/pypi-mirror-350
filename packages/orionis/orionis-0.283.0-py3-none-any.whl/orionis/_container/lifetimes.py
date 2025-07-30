from enum import Enum

class Lifetime(Enum):
    """Defines the lifecycle types for dependency injection."""

    # Creates a new instance every time it is requested
    TRANSIENT = "transient"

    # A single instance is shared throughout the application
    SINGLETON = "singleton"

    # A new instance is created per request or context
    SCOPED = "scoped"
