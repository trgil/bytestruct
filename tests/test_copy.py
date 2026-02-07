import copy
from bytestruct.core import make_struct_class, ByteStruct


def test_copy_independent_buffer():
    # Simple layout for testing
    layout = [
        ("magic", 4, "raw"),
        ("number", 4, "uint_le"),
    ]
    TestStruct = make_struct_class("TestStruct", layout)

    original_data = b"TEST" + (123456).to_bytes(4, "little")
    original = TestStruct(original_data)

    copied = original.copy()

    # Same class, different instances
    assert isinstance(copied, TestStruct)
    assert copied is not original

    # Same values
    assert copied.magic == original.magic == b"TEST"
    assert copied.number == original.number == 123456

    # Separate buffers (different memoryview objects)
    assert copied._data is not original._data

    # But content is the same
    assert bytes(copied._data) == bytes(original._data)


def test_copy_via_copy_module():
    layout = [("value", 8, "raw")]
    TestStruct = make_struct_class("TestStruct", layout)

    data = b"original-data"
    original = TestStruct(data)

    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    # All are separate instances
    assert shallow is not original
    assert deep is not original
    assert shallow is not deep

    # Same class
    assert isinstance(shallow, TestStruct)
    assert isinstance(deep, TestStruct)

    # Same content
    assert bytes(shallow._data) == data
    assert bytes(deep._data) == data

    # Different buffers
    assert shallow._data is not original._data
    assert deep._data is not original._data


def test_copy_with_extra_bytes():
    # Make sure extra data after header is also copied
    layout = [("header", 4, "raw")]
    TestStruct = make_struct_class("TestStruct", layout)

    full_data = b"HEADextra-payload"
    original = TestStruct(full_data)

    copied = original.copy()

    assert bytes(copied._data) == full_data
    assert copied.header == b"HEAD"
    assert copied._data is not original._data


def test_copy_does_not_share_memoryview():
    layout = [("a", 4, "raw")]
    TestStruct = make_struct_class("TestStruct", layout)

    original = TestStruct(b"abcd")
    copied = original.copy()

    # Change the original buffer (if someone mutates the underlying bytes)
    original._data = memoryview(b"XXXX")

    # Copy should still have the original content
    assert copied.a == b"abcd"
    assert original.a == b"XXXX"   # original changed, copy did not
