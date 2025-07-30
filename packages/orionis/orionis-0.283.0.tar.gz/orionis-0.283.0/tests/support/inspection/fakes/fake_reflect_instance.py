import asyncio

class BaseFakeClass:
    pass

class FakeClass(BaseFakeClass):
    """This is a test class for ReflexionInstance."""

    class_attr: str = "class_value"

    def __init__(self) -> None:
        self.public_attr = 42
        self._protected_attr = "protected"
        self.__private_attr = "private"
        self.dynamic_attr = None

    def instanceMethod(self, x: int, y: int) -> int:
        """Adds two numbers."""
        return x + y

    @property
    def computed_property(self) -> str:
        """A computed property."""
        return f"Value: {self.public_attr}"

    @classmethod
    def classMethod(cls) -> str:
        """A class method."""
        return f"Class attr: {cls.class_attr}"

    @staticmethod
    def staticMethod(text: str) -> str:
        """A static method."""
        return text.upper()

    @staticmethod
    async def staticAsyncMethod(text: str) -> str:
        """An asynchronous static method."""
        await asyncio.sleep(0.1)
        return text.upper()

    def __privateMethod(self) -> str:
        """A 'private' method."""
        return "This is private"

    def _protectedMethod(self) -> str:
        """A 'protected' method."""
        return "This is protected"

    async def asyncMethod(self) -> str:
        """An async method."""
        return "This is async"