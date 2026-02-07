# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-07

- Added `.copy()`, `__copy__`, and `__deepcopy__` support with corresponding tests
- Added index-based access (`obj[0]`, `obj[2]`, etc.) and tests
- Implemented core parsing functionality in `core.py`:
  - `make_struct_class(name, layout)` factory
  - `ByteStruct` base class with `__getattr__`, `__getitem__`
  - Layout as list of `(name, size, type)` tuples
  - Supported types: "raw", "uint_le", "uint_be", "int_le", "int_be"
  - Zero-copy slicing via `memoryview`
  - Basic unpacking using `struct` internally
- Refactored away from original `Field` + `make_struct` approach
- Added initial tests in `tests/test_core.py` (basic fields, integers, short-data errors, etc.)
- Updated README partially to reflect new API (work in progress)

## [0.1.0-alpha.1] - 2026-02-06

- Initial project setup
- Added `setup.py`, requirements files, `.gitignore`, LICENSE (MIT)
- Created early README with original Field-based design and philosophy
- Added basic module structure (`bytestruct/__init__.py`)