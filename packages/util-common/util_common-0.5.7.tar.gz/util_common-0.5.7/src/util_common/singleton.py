import threading
from typing import Any, Callable, Optional, Type, TypeVar

SingletonMixinT = TypeVar("SingletonMixinT", bound="SingletonMixin")


# See https://gist.github.com/werediver/4396488
class SingletonMixin:
    """Mixin class to make your class a Singleton class."""

    _instance: Optional[Any] = None
    _rlock = threading.RLock()
    _inside_instance = False

    @classmethod
    def instance(cls: Type[SingletonMixinT], *args: Any, **kwargs: Any) -> SingletonMixinT:
        """Get *the* instance of the class, constructed when needed using (kw)args.

        Return the instance of the class. If it did not yet exist, create it
        by calling the "constructor" with whatever arguments and keyword arguments
        provided.

        This routine is thread-safe. It uses the *double-checked locking* design
        pattern ``https://en.wikipedia.org/wiki/Double-checked_locking``_ for this.

        :param args: Used for constructing the instance, when not performed yet.
        :param kwargs: Used for constructing the instance, when not performed yet.
        :return: An instance of the class
        """
        if cls._instance is not None:
            return cls._instance
        with cls._rlock:
            # re-check, perhaps it was created in the mean time...
            if cls._instance is None:
                cls._inside_instance = True
                try:
                    cls._instance = cls(*args, **kwargs)
                finally:
                    cls._inside_instance = False
        return cls._instance

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        """Raise Exception when not called from the :func:``instance``_ class method.

        This method raises RuntimeError when not called from the instance class method.

        :param args: Arguments eventually passed to :func:``__init__``_
        :param kwargs: Keyword arguments eventually passed to :func:``__init__``_
        :return: the created instance.
        """
        if cls is SingletonMixin:
            raise TypeError(f"Attempt to instantiate mixin class {cls.__qualname__}")

        if cls._instance is None:
            with cls._rlock:
                if cls._instance is None and cls._inside_instance:
                    return super().__new__(cls)

        raise RuntimeError(f"Attempt to create a {cls.__qualname__} instance outside of instance()")


SingletonT = TypeVar("SingletonT")


def singleton(cls: Type[SingletonT]) -> Callable[..., SingletonT]:
    """
    A thread-safe singleton decorator.

    Usage:
        @singleton
        class MyClass:
            def __init__(self):
                self.value = 0

        # First instantiation creates the instance
        instance1 = MyClass()
        # Second instantiation returns the same instance
        instance2 = MyClass()
        assert instance1 is instance2  # True
    """
    instances: dict[Any, Any] = {}
    lock = threading.Lock()

    def get_instance(*args: Any, **kwargs: Any) -> SingletonT:
        if cls not in instances:
            with lock:
                if cls not in instances:  # Double-check pattern
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


if __name__ == "__main__":
    """Example of using the SingletonMixin class"""

    class MyClass(SingletonMixin):
        pass

        def __init__(self, value) -> None:
            self.value = value

    instance1 = MyClass.instance(value="Hello, World!")
    instance2 = MyClass.instance(value="2222")
    assert instance1 is instance2
    assert instance1.value == instance2.value

    """Example of using the singleton decorator"""

    @singleton
    class MyClass2:
        def __init__(self, value: str) -> None:
            self.value = value

    instance1 = MyClass2("Hello, World!")
    instance2 = MyClass2("2222")
    assert instance1 is instance2
    assert instance1.value == instance2.value
