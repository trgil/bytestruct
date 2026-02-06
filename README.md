# bytestruct

 ![Author](https://img.shields.io/badge/Author-Gil_Treibush-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue.svg) ![Version](https://img.shields.io/badge/Version-1.0.0--alpha.1-violet)

**bytestruct** is a lightweight, declarative Python library for describing, parsing, and manipulating binary data layouts — inspired by C structs.

It is built for developers who work with **binary file formats, headers, protocols, and raw byte buffers**, and who want full control without the complexity of heavy parsing frameworks.

---

## Why bytestruct?

Binary formats are everywhere: image headers, audio containers, network packets, embedded protocols, and legacy file formats. Python already provides powerful low-level tools (`struct`, `memoryview`, `bytearray`), but assembling them into *maintainable, readable, and reusable* code is still tedious.

**bytestruct** fills that gap by providing:

- A **declarative layout system** for binary data
- A **C-struct–like mental model**, without magic
- **Named field access** instead of positional unpacking
- **Zero-copy views** over raw bytes
- Clean separation between **layout (class)** and **data (instance)**

The goal is not to hide binary details — but to make them *explicit, safe, and pleasant to work with*.

---

## Design philosophy

bytestruct is guided by a few core principles:

### Explicit over magical
No metaclass tricks, no hidden mutation, no implicit parsing rules. Every byte has a known offset and size.

### Declarative layouts
Binary formats are *described*, not imperatively parsed. Layouts live at the class level and are immutable once defined.

### Raw bytes are first-class
You always have direct access to the underlying buffer. bytestruct never takes control away from you.

### Struct-compatible thinking
Field definitions map cleanly to Python’s `struct` module. Endianness, size, and alignment behave exactly as expected.

### Lightweight by default
bytestruct is intentionally minimal. Advanced features are added carefully, without turning the library into a framework.

---

## Core concepts

### Fields
A **Field** describes a single region of binary data:

- field name
- binary format (struct-compatible)
- size (derived automatically)
- offset (explicit or auto-computed)

Fields are *metadata only* — they do not store data.

### Binary structures
A **binary structure** combines:

- a class-level layout (fields + offsets)
- an instance-level byte buffer

Instances behave like structured views over raw binary data.

---

## Example

```python
from bytestruct import Field, make_struct

BMPHeader = make_struct(
    "BMPHeader",
    fields=[
        Field("signature", "2s"),
        Field("file_size", "<I"),
        Field("reserved1", "<H"),
        Field("reserved2", "<H"),
        Field("data_offset", "<I"),
    ]
)

with open("image.bmp", "rb") as f:
    header = BMPHeader.from_file(f)

print(header.signature)   # b'BM'
print(header.file_size)   # integer

header.file_size += 1024  # modify underlying bytes safely
```

No unpacking tuples. No manual slicing. No ambiguity.

---

## Intended use cases

bytestruct is well suited for:

- File headers (BMP, WAV, ELF, ZIP, custom formats)
- Binary protocol frames
- Memory-mapped binary data
- Embedded or low-level tooling
- Reverse engineering and format exploration

It is **not** intended to replace:

- Full binary parsing frameworks
- Schema-driven serialization systems
- Bit-level compression codecs

---

## Project status

bytestruct is currently **early-stage and intentionally evolving slowly**. The API is designed with long-term stability in mind, and features are added only when they fit the core philosophy.

Planned areas of future exploration include:

- Nested structures
- Field arrays
- Optional validation hooks
- Safer string decoding helpers
- Better debugging and visualization tools

---

## License

bytestruct is released under the **MIT License**.

You are free to use it in personal, open-source, or commercial projects.
