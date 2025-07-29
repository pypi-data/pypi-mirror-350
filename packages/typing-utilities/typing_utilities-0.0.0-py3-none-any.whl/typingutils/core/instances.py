from typing import Callable, Type, TypeVar, Any, Generic, Union, overload, cast
from types import UnionType, NoneType
from collections import abc
from inspect import stack as get_stack

from typingutils.core.attributes import  ORIGIN, ORIGINAL_CLASS, ARGS
from typingutils.core.types import (
    TypeParameter, UnionParameter, AnyType, TypeArgs,
    is_subscripted_generic_type, is_generic_type, get_generic_origin, issubclass_typing
)

def get_original_class(obj: Any) -> TypeParameter:
    """
    Returns the original generic type from a class instance.
    This is useful for generic types because instances of these doesn't derive from them,
    thus having no generic arguments specified. Will even work when called from within a constructor of a class.

    Notes:
        Won't work with builtin generic types like list and tuple.

    Examples:
        class GenClass[T]:
            def __init__(self): # self == GenClass
                self.org = get_original_class(self) # org == GenClass[x]

        t = GenClass[str]() # type(t) == GenClass
        g = get_original_class(t) # g == GenClass[str]

    Args:
        obj (Any): An instance of a class.

    Returns:
        type: The objects original class if any - otherwise the class itself is returned.
    """

    cls: TypeParameter = type(obj) if not is_type(obj) else obj # pyright: ignore[reportUnknownVariableType]

    if hasattr(obj, ORIGINAL_CLASS):
        return getattr(obj, ORIGINAL_CLASS)
    elif is_generic_type(cls) or is_subscripted_generic_type(cls):
        stack = get_stack()
        for frame in stack[2:]:
            if frame.filename == __file__:
                continue # pragma: no cover
            locals = frame[0].f_locals
            if "self" in locals:
                self = locals["self"]
                if hasattr(self, ORIGIN) and getattr(self, ORIGIN) == cls:
                    return self

    return cls

def _extract_args(obj: Any, *, extract_types_from_typevars: bool = False, include_typevars: bool = True) -> tuple[TypeArgs, bool]:
    """
    Extracts arguments from a generic object or type.

    Examples:
        T = TypeVar('T', bound=str)
        class GenClass(Generic[T]): pass
        args = _extract_args(GenClass) # => (~T<str>,)
        args = _extract_args(GenClass, extract_types_from_typevars=True) # => (str,)
        args = _extract_args(GenClass[str]) # => (str,)

    Args:
        obj (Any): A class or an instance of a class.
        extract_types_from_typevars (bool, optional): Extracts and returns types from typevars instead of the typevars themselves. Defaults to False.
        include_typevars (bool, optional): Whether or not to include typevars. If any typevars are present, ordinary args won't be returned. Defaults to True.

    Returns:
        tuple[TypeArgs, bool]: A sequence of type arguments and a bool indicating prescence of args or not.
    """

    if hasattr(obj, ARGS):
        from typingutils.core.types import get_types_from_typevar

        args = tuple(
            (
                arg,
                get_types_from_typevar(arg) if isinstance(arg, TypeVar) else arg,
                isinstance(arg, TypeVar)
            )
            for arg in cast(tuple[Any], getattr(obj, ARGS))
        )
        typevar_args = tuple( arg for arg, _, typevar in args if typevar )
        ordinary_args = tuple( arg for arg, _, typevar in args if not typevar )
        result_args = tuple( arg if not typevar or not extract_types_from_typevars else value for arg, value, typevar in args if not typevar or extract_types_from_typevars )

        # in python 3.13 certain types may contain both typevars and types in the __args__ attribyte,
        # case in point typing.ContextManager[T] which has ` ~T, bool |None ` except of the expected ` ~T `

        if include_typevars and typevar_args:
            if extract_types_from_typevars:
                return result_args, True
            else:
                return typevar_args, True
        elif not include_typevars and not typevar_args and ordinary_args:
            return ordinary_args, True

        return (), True

    return (), False

def get_generic_arguments(obj: Any) -> TypeArgs:
    """
    Returns the type arguments used to create a subscripted generic type.
    Will even work when called from within a constructor of the class.

    Notes:
        The class must inherit Generic[T], and it must me the first inherited type to work.

    Examples:
        T = TypeVar('T')
        class GenClass(Generic[T]): pass
        a = get_generic_arguments(GenClass[str]) => (str,)

    Args:
        obj (Any): A type, object or instance of an object.

    Returns:
        TypeArgs: A sequence of types.
    """

    args, success = _extract_args(obj, extract_types_from_typevars = False, include_typevars = False)
    if success:
        return args
    elif not is_type(obj):
        orig_class = get_original_class(obj)
        if orig_class is not type(obj):
            return cast(Callable[[Any], tuple[type, ...]], get_generic_arguments)(orig_class)
    elif isinstance(obj, type) and Generic in obj.__bases__:
        orig_class = get_original_class(obj)
        if orig_class != obj:
            return cast(Callable[[Any], tuple[type, ...]], get_generic_arguments)(orig_class)


    return ()


def is_type(obj: Any) -> bool:
    """
    Checks if object is a type (or a generic type) or not.

    Notes:
        TypeVar's aren't recognized as types.

    Args:
        obj (Any): A type, object or instance of an object.

    Returns:
        bool: A boolean value indicating if object is a type.
    """

    if type(obj) is TypeVar:
        return False
    elif obj is object:
        return False
    elif obj is Any:
        return False
    elif isinstance(obj, UnionType) or get_generic_origin(obj) == Union:
        return True

    return isinstance(obj, type) or is_generic_type(obj) or is_subscripted_generic_type(obj)


@overload
def isinstance_typing(obj: Any) -> bool:
    """
    Checks if object is an instance of an object or not.

    Args:
        obj (Any): A type, object or instance of an object.

    Returns:
        bool: A boolean value indicating if object is an instance of an object or not.
    """
    ...
@overload
def isinstance_typing(obj: Any, cls: AnyType | tuple[AnyType, ...]) -> bool:
    """
    Checks if object is an instance of the specified type/types. This implementation
    works similarly to the builtin isinstance(), but supports generics as well.

    Args:
        obj (Any): An object or instance of an object.
        cls (type): A type or sequence of types.

    Returns:
        bool: A boolean value indicating if object is an instance of the specified type/types.
    """
    ...
def isinstance_typing(obj: Any, cls: AnyType | tuple[AnyType, ...] | None = None) -> bool:
    if cls is None and not is_type(obj):
        return True
    elif obj is cls is object:
        return True # object is always an instance of itself
    elif obj is cls:
        return False # an object is never an instance of itself (unless it is object - see previous line)
    elif obj is type and cls in (object, type[Any], Type, Type[Any]):
        return True # types are only derived from object and type[Any]
    elif type(obj) is type and cls in (object, type, type[Any], Type, Type[Any]):
        return True # all classes are derived from type and object
    elif type(obj) is not type and cls in (object, type[Any], Type[Any]):
        return True # all class instances are derived from type and object
    elif type(obj) is NoneType and cls in (object, type[Any], Type[Any], NoneType):
        return True # None is derived from type and object
    elif is_type(obj):
        return cls is object # all other types are only an instance of object

    if is_type(cls):
        if not is_type(obj) and cls is type:
            return False # only other types are derived from type object
        if get_generic_origin(cast(type, cls)) is Union:
            for cls1 in getattr(cls, ARGS):
                if isinstance_typing(obj, cls1):
                    return True
            return False
        if issubclass_typing(type(obj), cast(type, cls)): # pyright: ignore[reportUnknownArgumentType]
            return True

    if isinstance(cls, abc.Collection):
        for cls1 in cls:
            if isinstance_typing(obj, cls1):
                return True
        return False

    if hasattr(obj, ORIGINAL_CLASS) and getattr(obj, ORIGINAL_CLASS) != type:
        origin = getattr(obj, ORIGINAL_CLASS)
        if origin == cls:
            return True

    if not hasattr(obj, ORIGINAL_CLASS) and hasattr(cls, ORIGIN) and hasattr(cls, ARGS):
        cls = getattr(cls, ORIGIN)

    if not is_subscripted_generic_type(cast(TypeParameter | UnionParameter, cls)) and not is_generic_type(cast(TypeParameter, type(obj))):
        return isinstance(obj, cast(type, cls))

    elif isinstance(cls, TypeVar):
        from typingutils.core.types import get_types_from_typevar
        return isinstance_typing(obj, get_types_from_typevar(cls))

    return False