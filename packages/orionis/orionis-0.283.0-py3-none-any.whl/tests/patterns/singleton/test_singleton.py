from orionis.patterns.singleton.meta_class import Singleton
from orionis.test.cases.test_case import TestCase

class TestsAsyncCoroutine(TestCase):

    async def testSingleton(self):
        """
        Test the Singleton metaclass to ensure that only one instance of a class is created.
        """
        class SingletonClass(metaclass=Singleton):
            def __init__(self, value):
                self.value = value

        instance1 = SingletonClass(1)
        instance2 = SingletonClass(2)

        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.value, 1)