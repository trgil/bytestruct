

import struct
from typing import Any, Type, Union


class ByteStruct:
    # These will be set by the factory on the subclass
    _layout: list[tuple[str, int, str]] = []  # (name, size, type)
    _name_to_info: dict[str, tuple[int, int, str]] = {}  # name → (offset, size, type)

    def __init__(self, data: Union[bytes, bytearray, memoryview], strict_size: bool = False):
        self._data = memoryview(data)

        # Size checks
        total_size = sum(size for _, size, _ in self._layout)
        if len(self._data) < total_size:
            raise ValueError(
                f"Data too short for {self.__class__.__name__}: "
                f"got {len(self._data)} bytes, need at least {total_size}"
            )

        if strict_size and len(self._data) != total_size:
            raise ValueError(f"Data must be exactly {total_size} bytes for strict mode")

    # Attribute access
    def __getattr__(self, name: str) -> Any:
        if name not in self._name_to_info:
            raise AttributeError(f"No field named {name!r} in {self.__class__.__name__}")

        offset, size, field_type = self._name_to_info[name]
        raw = self._data[offset : offset + size]

        if field_type == "raw":
            return bytes(raw)  # return copy as bytes

        elif field_type in ("uint_le", "uint_be", "int_le", "int_be"):
            if field_type.endswith("_le"):
                endian = "<"
            else:
                endian = ">"

            if field_type.startswith("uint"):
                fmt = "I" if size == 4 else "H" if size == 2 else "B" if size == 1 else None
            else:  # int
                fmt = "i" if size == 4 else "h" if size == 2 else "b" if size == 1 else None

            if fmt is None:
                raise ValueError(f"Unsupported integer size {size} for field {name!r}")

            return struct.unpack(f"{endian}{fmt}", raw)[0]

        else:
            raise ValueError(f"Unknown field type {field_type!r} for {name}")

    # Dict-like access
    def __getitem__(self, key: Union[str, int]) -> Any:
        if isinstance(key, str):
            return getattr(self, key)
        if isinstance(key, int):
            name, _, _ = self._layout[key]
            return getattr(self, name)
        raise TypeError("Key must be a field name or an integer")

    def __repr__(self):
        fields = ", ".join(f"{name}={getattr(self, name)!r}" for name, _, _ in self._layout)
        return f"{self.__class__.__name__}({fields})"


def make_struct_class(name: str, layout: list[tuple[str, int, str]]) -> Type[ByteStruct]:
    """
    Creates a new struct class with the given name and layout.
    Layout items: (field_name: str, size_in_bytes: int, type_str: str)
    """

    # Precompute offsets and validate
    offsets = []
    current_offset = 0
    name_to_info = {}

    for fname, size, ftype in layout:
        if size <= 0:
            raise ValueError(f"Size must be positive for field {fname!r}")
        if ftype not in ("raw", "uint_le", "uint_be", "int_le", "int_be"):
            raise ValueError(f"Unsupported type {ftype!r} for field {fname!r}")

        offsets.append(current_offset)
        name_to_info[fname] = (current_offset, size, ftype)
        current_offset += size

    # Create subclass
    class SpecificStruct(ByteStruct):
        __module__ = "bytestruct"
        __qualname__ = name

        _layout = layout
        _name_to_info = name_to_info

    SpecificStruct.__name__ = name
    return SpecificStruct
