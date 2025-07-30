import threading
import time

import pytest

from util_common.singleton import SingletonMixin


class TestClass(SingletonMixin):
    def __init__(self, value=None):
        self.value = value


@pytest.mark.unit
class TestSingletonMixin:
    def test_instance_creation(self):
        """Test basic instance creation"""
        instance = TestClass.instance(value=1)
        assert instance.value == 1

    def test_singleton_pattern(self):
        """Test that multiple instances are the same object"""
        instance1 = TestClass.instance(value=1)
        instance2 = TestClass.instance(value=2)

        assert instance1 is instance2
        # Second instantiation shouldn't change the value
        assert instance1.value == instance2.value == 1

    def test_direct_instantiation(self):
        """Test that direct instantiation is not allowed"""
        with pytest.raises(RuntimeError) as exc_info:
            TestClass()
        assert "outside of instance()" in str(exc_info.value)

    def test_mixin_instantiation(self):
        """Test that SingletonMixin cannot be instantiated directly"""
        with pytest.raises(TypeError) as exc_info:
            SingletonMixin()
        assert "Attempt to instantiate mixin class" in str(exc_info.value)

    def test_thread_safety(self):
        """Test thread-safe instance creation"""
        results = []

        def create_instance(delay):
            time.sleep(delay)
            results.append(TestClass.instance(value=delay))

        # Create multiple threads that try to create instances
        threads = [threading.Thread(target=create_instance, args=(0.1,)) for _ in range(5)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # All threads should get the same instance
        assert len(set(results)) == 1
        # Value should be from the first creation
        assert all(r.value == results[0].value for r in results)

    @pytest.mark.parametrize(
        "args,kwargs",
        [
            ((1,), {}),
            ((), {"value": 1}),
        ],
    )
    def test_instance_with_different_args(self, args, kwargs):
        """Test instance creation with different argument patterns"""
        instance = TestClass.instance(*args, **kwargs)
        assert instance is not None
