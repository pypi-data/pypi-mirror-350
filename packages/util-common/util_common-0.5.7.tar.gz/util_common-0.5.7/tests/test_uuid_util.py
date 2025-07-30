import pytest

from util_common.uuid_util import UUID, UUIDGenerator, generate_short_uuid


@pytest.mark.unit
def test_generate_short_uuid():
    """Test basic UUID generation"""
    uuid1 = generate_short_uuid()
    uuid2 = generate_short_uuid()

    # Test uniqueness
    assert uuid1 != uuid2

    # Test type
    assert isinstance(uuid1, str)
    assert isinstance(uuid2, str)


@pytest.mark.unit
class TestUUID:
    def test_get_method(self):
        """Test the get() method"""
        uuid1 = UUID().get()
        uuid2 = UUID().get()

        assert isinstance(uuid1, str)
        assert uuid1 != uuid2

    def test_get_short_default(self):
        """Test get_short() with default parameters"""
        uuid = UUID().get_short()
        assert len(uuid) == 8

    def test_get_short_custom_length(self):
        """Test get_short() with custom length"""
        length = 10
        uuid = UUID().get_short(length=length)
        assert len(uuid) == length

    def test_get_short_custom_charset(self):
        """Test get_short() with custom character set"""
        str_set = "ABC123"
        uuid = UUID().get_short(str_set=str_set)
        assert all(c in str_set for c in uuid)

    def test_get_short_uniqueness(self):
        """Test uniqueness of get_short()"""
        uuid = UUID()
        uuids = [uuid.get_short() for _ in range(10)]
        assert len(set(uuids)) == 10

    def test_get_short_retry_limit(self):
        """Test retry limit when generating short UUIDs"""
        # Force collisions by using a tiny character set
        uuid = UUID()
        with pytest.raises(Exception) as exc_info:
            for _ in range(10):
                uuid.get_short(length=1, str_set="A")
        assert "Not enough uuids to use" in str(exc_info.value)


@pytest.mark.unit
class TestUUIDGenerator:
    def test_singleton_pattern(self):
        """Test that UUIDGenerator follows singleton pattern"""
        generator1 = UUIDGenerator.instance()
        generator2 = UUIDGenerator.instance()
        assert generator1 is generator2

    def test_inheritance(self):
        """Test that UUIDGenerator inherits UUID methods"""
        generator = UUIDGenerator.instance()
        uuid = generator.get_short()
        assert len(uuid) == 8

    def test_direct_instantiation(self):
        """Test that direct instantiation is not allowed"""
        with pytest.raises(RuntimeError) as exc_info:
            UUIDGenerator()
        assert "outside of instance()" in str(exc_info.value)

    def test_static_methods_through_instance(self):
        """Test that static methods work through instance"""
        generator = UUIDGenerator.instance()

        # Test get method
        uuid1 = generator.get()
        uuid2 = generator.get()
        assert uuid1 != uuid2

        # Test get_short method
        short_uuid = generator.get_short(length=10)
        assert len(short_uuid) == 10
