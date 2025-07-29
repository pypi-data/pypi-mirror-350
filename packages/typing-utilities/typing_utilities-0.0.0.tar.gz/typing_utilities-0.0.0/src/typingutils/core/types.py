from typing import Annotated, Type, TypeVar, Sequence, Any, Generic, Union, Callable, cast
from typing import _GenericAlias, GenericAlias, _SpecialGenericAlias, _UnionGenericAlias, _SpecialForm # pyright: ignore[reportUnknownVariableType, reportAttributeAccessIssue, reportPrivateUsage ]
from types import UnionType, NoneType, EllipsisType
from collections import abc

from typingutils.core.attributes import (
    BASES, NAME, QUALIFIED_NAME, MODULE, ORIGIN, ARGS, PARAMETERS,
    GENERIC_CONSTRUCTOR, SPECIAL_CONSTRUCTOR, BOUND, CONSTRAINTS
)

TypeParameter = Annotated[ type | type[Any], "Represents any type." ]
UnionParameter = Annotated[ UnionType | tuple[TypeParameter, ...], "Represents a union of types." ]
AnyType = Annotated[ TypeParameter | UnionParameter | TypeVar, "Represents any type, union or typevar." ]
TypeArgs = Annotated[ tuple[AnyType, ...], "Represents a sequence of types, unions or typevars." ]

SetOfAny = set((Any,))

GENERIC_BASE_TYPES: set[type] = set(cast(list[type], [ _GenericAlias, GenericAlias, _SpecialGenericAlias ]))
GENERIC_SPECIAL_TYPES: set[type] = set(cast(list[type], [ _SpecialGenericAlias, _SpecialForm, _UnionGenericAlias ]))


def is_generic_type(cls: AnyType) -> bool:
    """
    Indicates whether or not type is a generic type, i.e. a type capable of subscripted generics like list[T].

    Args:
        cls (AnyType): A type.

    Returns:
        bool: A boolean indicating if type is a generic type or not.
    """

    if type(cls) is TypeVar:
        return False
    elif hasattr(cls, ORIGIN):
        from typingutils.core.instances import _extract_args # pyright: ignore[reportPrivateUsage]
        args, success = _extract_args(cls, extract_types_from_typevars = False, include_typevars = True)
        if success:
            return any(args)
        return True
    elif hasattr(cls, BASES) and Generic in getattr(cls, BASES):
        return True
    # elif hasattr(cls, PARAMETERS) and not hasattr(cls, ORIGINAL_CLASS) and get_generic_parameters(cls):
    #     return True
    elif type(cls) in GENERIC_BASE_TYPES:
        return True # pragma: no cover
    else:
        return False


def _is_special_generic_type(cls: AnyType) -> bool:
    """
    Indicates if type is a special generic type from the typing module.

    Args:
        cls (AnyType): A type.

    Returns:
        bool: A boolean indicating if type is a special generic type or not.
    """

    return type(cls) in GENERIC_SPECIAL_TYPES # pragma: no cover


def is_subscripted_generic_type(cls: AnyType) -> bool:
    from typingutils.core.instances import get_generic_arguments

    return hasattr(cls, ARGS) and any(get_generic_arguments(cls))
    # return is_generic_type(cls) and any(get_generic_arguments(cls, include_typevars = False))


def get_generic_parameters(obj: TypeParameter, *, extract_types_from_typevars: bool = False) -> TypeArgs:
    """
    Returns the generic typevars required to create a subscripted generic type
    of an object. Will even work when called from within a constructor of the class.

    Examples:
        T = TypeVar('T')
        class GenClass(Generic[T]): pass
        a = get_generic_parameters(GenClass[str]) => ~T

    Args:
        obj (TypeParameter): A type.

    Returns:
        TypeArgs: A sequence of types.
    """
    if hasattr(obj, PARAMETERS):
        if params := getattr(obj, PARAMETERS):
            return tuple(
                get_types_from_typevar(param) if extract_types_from_typevars and isinstance(param, TypeVar) else param
                for param in params
            )

    return ()


def get_type_name(cls: AnyType) -> str:
    """
    Gets the name of a type.

    Args:
        cls (AnyType): A type.

    Raises:
        Exception: An exception is raised if a type name cannot be produced.

    Returns:
        str: The name of the type.
    """

    if cls is None or cls == NoneType: # pyright: ignore[reportUnnecessaryComparison]
        return "None"
    if cls is EllipsisType:
        return "..."
    if isinstance(cls, TypeVar):
        if bound := getattr(cls, BOUND):
            return f"{cls}<{get_type_name(bound)}>"
        elif constraints := tuple( get_type_name(t) for t in getattr(cls, CONSTRAINTS) ):
            return f"{cls}<{'|'.join(constraints)}>"
        else:
            return f"{cls}"
    if isinstance(cls, tuple):
        return f"({', '.join( get_type_name(item) for item in cls )})"


    from typingutils.core.instances import get_generic_arguments
    args: Sequence[str] = [
        get_type_name(arg)
        for arg in get_generic_arguments(cls)
    ]

    if is_union(cls):
        return ' | '.join(args)

    type_name: str | None = None

    name = cls.__qualname__ if hasattr(cls, QUALIFIED_NAME) else getattr(cls, NAME) if hasattr(cls, NAME) else str(cls)

    if hasattr(cls, MODULE) and getattr(cls, MODULE) in [ "builtins", "__builtins__" ]:
        type_name = name
    elif hasattr(cls, MODULE) and not name.startswith(getattr(cls, MODULE)):
        type_name =  f"{getattr(cls, MODULE)}.{name}"
    else:
        type_name = name

    if args:
        return f"{type_name}[{', '.join(args)}]"
    elif type_name:
        return type_name
    else:
        raise Exception(f"Unable to get name of type {cls}") # pragma: no cover


def get_generic_origin(cls: AnyType) -> TypeParameter:
    """
    Gets the generic origin of a type i.e. the type a generic type originates from.

    Args:
        cls (AnyType): A type.

    Raises:
        ValueError: _description_

    Returns:
        TypeParameter: A type.
    """
    if type(cls) is TypeVar:
        raise ValueError("TypeVar is not a generic type")
    elif hasattr(cls, ORIGIN):
        return cast(type, getattr(cls, ORIGIN))
    elif isinstance(cls, UnionType):
        return UnionType # pyright: ignore[reportReturnType]

    return cast(type, cls)


def get_union_types(cls: UnionParameter) -> TypeArgs:
    """
    Returns the types which make up a union.

    Args:
        cls (UnionParameter): A union of types.

    Raises:
        ValueError: A ValueError is raised if type is not a union.

    Returns:
        TypeArgs: A sequence of types.
    """

    if type(cls) is not TypeVar and hasattr(cls, ARGS): # pyright: ignore[reportUnnecessaryComparison]
        args = tuple([
            arg
            for arg in cast(tuple[Any], getattr(cls, ARGS))
            if arg != NoneType
        ])
        return args
    else:
        raise ValueError(f"Type {get_type_name(cls)} is not a union") # pragma: no cover


def is_union(cls: AnyType) -> bool:
    """
    Indicates whenter or not type is a union of types.

    Args:
        cls (AnyType): A type.

    Returns:
        bool: Returns true if type is a union of types.
    """

    if type(cls) is TypeVar:
        return False
    elif isinstance(cls, UnionType):
        return True
    else:
       return get_generic_origin(cast(TypeParameter, cls)) is Union


def is_optional(cls: AnyType) -> bool:
    """
    Indicates if type is an optional type, i.e. a union containing None or a typing.Optional[T].

    Args:
        cls (AnyType): A type.

    Returns:
        bool: True if type is optional.
    """

    if is_union(cls):
        classes = getattr(cls, ARGS)
        if NoneType in classes:
            return True
    elif isinstance(cls, TypeVar):
        return is_optional(get_types_from_typevar(cls))
    return False



def get_optional_type(cls: AnyType) -> tuple[AnyType, bool]:
    """
    Returns the actual type from an optional type.

    Examples:
        get_optional_type(str) # => (str, False)
        get_optional_type(Optional[str]) # => (str, True)
        get_optional_type(str | int | None) # => (str | int, True)

    Args:
        cls (AnyType): A type.

    Returns:
        tuple[AnyType, bool]: A tuple with the type and a boolean indicating if optional or not.
    """

    if is_union(cls):
        classes_org = getattr(cls, ARGS)
        optional: bool = NoneType in classes_org
        classes = [ c for c in classes_org if c != NoneType ]

        if len(classes) == 1:
            return classes[0], optional
        else:
            return cast(type, Union[tuple(classes)]), optional

    elif isinstance(cls, TypeVar):
        return get_optional_type(get_types_from_typevar(cls))

    return cast(type, cls), False


def issubclass_typing(cls: AnyType, base: AnyType | TypeArgs ) -> bool:
    """
    Indicates whether or not one type is a subclass of another. This implementation
    works similarly to the builtin issubclass(), but supports generics as well.

    Args:
        cls (AnyType): A type.
        base (AnyType | TypeArgs): A type or typevar.

    Raises:
        ValueError: A ValueError is raised if cls is a typevar.

    Returns:
        bool: True if cls is an instance of base.
    """

    if type(cls) is TypeVar: # or type(base) is TypeVar:
        raise ValueError("Argument cls cannot be an instance of TypeVar")
    if not cls:
        return False # pragma: no cover
    elif cls is base:
        return True
    elif base in (object, TypeParameter,  type[Any], Type[Any]):
        return True

    from typingutils.core.instances import get_generic_arguments, is_type

    if isinstance(base, abc.Collection):
        for base_cls in cast(Sequence[TypeParameter], base):
            if issubclass_typing(cls, base_cls):
                return True
        return False

    if is_subscripted_generic_type(cast(TypeParameter | UnionParameter | TypeVar, base)) and set(get_generic_arguments(base)) == SetOfAny:
        base = get_generic_origin(cast(TypeParameter | UnionParameter | TypeVar, base))

    if is_union(base):
        classes = get_generic_arguments(base)
        return any([ issubclass_typing(cls, b) for b in classes ]) or is_type(cls) and get_generic_origin(cast(type, cls)) is Union

    if is_type(cls):
        if is_type(base):
            cls_args = get_generic_arguments(cls) if is_subscripted_generic_type(cls) else get_union_types(cast(UnionParameter, cls)) if is_union(cls) else ()
            if is_generic_type(base):
                base_args = get_generic_parameters(cast(type[Any], base), extract_types_from_typevars = True)
            elif is_subscripted_generic_type(base):
                base_args = get_generic_arguments(base)
            else:
                base_args = get_generic_arguments(base)

            if get_generic_origin(cast(type, cls)) == get_generic_origin(base):
                if cls_args == base_args:
                    return True
                elif cls_args and base_args and len(cls_args) == len(base_args) and not [
                    t for t in zip(cls_args, base_args) if not issubclass_typing(t[0], t[1])
                ]:
                    return True
                else:
                    return not any(base_args)
            elif is_type(cls) and not is_generic_type(cls) and not is_subscripted_generic_type(base) and isinstance(base, type):
                return issubclass(cast(type[Any], cls), base)

            else:
                return False

        elif type(base) is TypeVar:
            return issubclass_typing(cls, get_types_from_typevar(base))

    return issubclass(cls, base) # fallback # pyright: ignore[reportArgumentType] # pragma: no cover

def get_types_from_typevar(typevar: TypeVar) -> TypeParameter | UnionParameter:
    if bound := getattr(typevar, BOUND):
        return Union[bound]
    elif constraints := getattr(typevar, CONSTRAINTS):
        return Union[constraints]
    else:
        return type[Any]

def construct_generic_type(cls: type, *generic_arguments: AnyType | EllipsisType) -> type:
    generic_arguments = tuple( arg if arg != EllipsisType else Ellipsis for arg in generic_arguments )

    if hasattr(cls, GENERIC_CONSTRUCTOR): # types derived from Generic[T]
        return cast(Callable[[tuple[type, ...]], type], getattr(cls, GENERIC_CONSTRUCTOR))(generic_arguments) # pyright: ignore[reportArgumentType]
    elif _is_special_generic_type(cls): # types like Optional[T] and Union[T, ...]
        if len(generic_arguments) == 1:
            return cast(Callable[[type], type], getattr(cls, SPECIAL_CONSTRUCTOR))(generic_arguments[0]) # pyright: ignore[reportArgumentType]
        else:
            return cast(Callable[[tuple[type, ...]], type], getattr(cls, SPECIAL_CONSTRUCTOR))(generic_arguments) # pyright: ignore[reportArgumentType]
    else:
        return cast(Callable[[tuple[type, ...]], type], getattr(cls, SPECIAL_CONSTRUCTOR))(generic_arguments) # pyright: ignore[reportArgumentType] # pragma: no cover

