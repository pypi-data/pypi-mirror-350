[![Test](https://github.com/apmadsen/typing-utilities/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/typing-utilities/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/typing-utilities/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/typing-utilities/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/typing-utilities?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/typing-utilities/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/typing-utilities?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/typing-utilities)
[![PyPI Downloads](https://static.pepy.tech/badge/typing-utilities/week)](https://pepy.tech/projects/typing-utilities)

# typing-utilities: Runtime reflection and validation of types and generics.

`typing-utilities` extends Python with the ability to check instances and types of generic types and unions introduced in the `typing` module.

## Conventions

This project differs from Python and other projects in some aspects:

- Generic subscripted types like `list[str]` are always a subclass of its base type `list` whereas the opposite is not true.
- Any type is a subclass of `type[Any]`.
- `type[Any]` is not an instance of `type[Any]`.
- Builtin types and `typing` types are interchangeable, i.e. `list[T]` is interchangeable with `typing.List[T]` etc.

## What's not included

### Deep validation checks

This project does not check the contents of objects like lists and dicts, which is why `isinstance_typing([1, 2, 3], list[int])` returns false. The reason is, that while it's relatively easy to compare every item in a list to the type argument of `list[str]`, other generic types are not as straight forward, thus it's better left to the programmer.

### Generic types

It's not the goal of this project to deliver generic types such as generically enforced lists and dicts.

## API

### Types

#### issubclass_typing

The `issubclass_typing(cls, base) -> bool` function extends the builtin `issubclass(cls, base)` function allowing both `cls` and `base` to be either a type, typevar or union object.

#### is_optional

The `is_optional(cls) -> bool` function checks whenter or not type is optional, i.e. a union containing `None` a `typing.Optional[T]` or `typing.Union[T, None]`

#### is_union

The `is_union(cls) -> bool` function checks whenter or not type is a union. This includes both `x|y` and `typing.Union` unions.

#### is_subscripted_generic_type

The `is_subscripted_generic_type(cls) -> bool` function indicates whether or not `cls` is a subscripted generic type as `list[str]` is a subscripted generic type of `list[T]` etc.

#### is_generic_type

The `is_generic_type(cls) -> bool` function  indicates whether or not `cls` is a generic type like `list[T]`.

#### get_type_name

The `get_type_name(cls) -> str` function returns the name of type `cls`. It's used throughout the tests of this package and for documentational purposes.

#### get_optional_type

The `get_optional_type(cls) -> tuple[type|union, bool]` function extracts any types from `cls` regardless if it's an ordinary type, a union or a `typing.Optional[T]` object, and returns it along with a bool indicatig if optional or not.

### Objects

#### isinstance_typing

The `isinstance_typing(obj, cls) -> bool` function extends the builtin `isinstance(obj, cls)` function allowing `cls` to be either a type, typevar or union object.

#### is_type

The `is_type(obj) -> bool` function checks whenter or not `obj` is recognized as a type. This includes unions and `type[Any]`.

### Internal

#### get_generic_arguments

The `internal.get_generic_arguments(obj) -> tuple[type|union, ...]` function returns the types used to create the subscripted generic type or instance `obj`.

#### get_generic_parameters

The `internal.get_generic_parameters(cls) -> tuple[type|union|TypeVar, ...]` function returns the typevars needed to create a subscripted generic type derived frol `cls`.

## Other similar projects

There are other similar projects out there like [typing-utils](https://pypi.org/project/typing-utils/) and [runtype](https://pypi.org/project/runtype/), and while typing-utils is outdated and pretty basic, runtype is very similar to `typing-utilities` when it comes to validation.