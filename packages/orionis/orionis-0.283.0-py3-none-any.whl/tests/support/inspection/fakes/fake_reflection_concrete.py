class BaseExample:
    """Base class to test inheritance."""

    def baseMethod(self) -> str:
        return "Base method called"

class FakeExample(BaseExample):
    """This is a fake example class for testing reflection."""

    class_attr: int = 42
    another_attr = "hello"

    def __init__(self, value: int = 10) -> None:
        self.instance_attr = value

    @property
    def prop(self) -> int:
        """A read-only property returning a fixed number."""
        return 10

    @property
    def prop_with_getter(self) -> str:
        return "read-only"

    def method_one(self, x: int) -> int:
        return x * 2

    def method_two(self, a: str, b: str = "default") -> str:
        return a + b

    @staticmethod
    def static_method() -> str:
        return "I am static"

    @staticmethod
    def _private_static():
        pass

    @classmethod
    def class_method(cls) -> str:
        return f"I am class method of {cls.__name__}"

    def _private_method(self):
        pass
