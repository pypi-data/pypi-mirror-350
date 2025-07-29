# pyright: basic
from typing import Any, Generic, TypeVar, Union, Optional, List, Dict, cast
from types import NoneType, EllipsisType, UnionType
from pytest import raises as assert_raises

from typingutils import (
    is_type, is_union, get_type_name, is_optional, get_optional_type, TypeParameter, UnionParameter,
    is_subscripted_generic_type, is_generic_type, get_generic_arguments, get_generic_parameters
)
from typingutils.internal import get_generic_origin, get_original_class, get_union_types, get_types_from_typevar, construct_generic_type
from typingutils.core.attributes import ORIGIN

from tests.testcase_generators.issubclass import create_testcases_for_issubclass
from tests.testcase_generators.types import create_testcases_for_types
from tests.generic_types import non_generic_types, generic_types
from tests.generic_classes import ParentClass, GenericClass1

class TestClass:

    issubclass_testcases = list(create_testcases_for_issubclass())
    types_testcases = list(create_testcases_for_types())

    def test_is_type(self):
        tested: set[type[Any]] = set()

        assert not is_type(object)

        for testcase in self.types_testcases:

            if testcase.cls not in tested:
                tested.add(testcase.cls)

                result = is_type(testcase.cls)
                print(f"Testing is_type({get_type_name(testcase.cls)}) ==> {result}")
                if not result:
                    is_type(testcase.cls)
                assert result


    def test_get_generic_parameters(self):
        tested: set[type[Any]] = set()

        for testcase in self.types_testcases:
            if testcase.cls not in tested:
                tested.add(testcase.cls)

                result = get_generic_parameters(testcase.cls)

                print(f"Testing get_generic_parameters({get_type_name(testcase.cls)}) ==> {result}")

                if testcase.is_generic_type:
                    assert any(result)
                else:
                    assert not any(result)



    def test_get_generic_arguments(self):
        tested: set[type[Any]] = set()

        for testcase in self.types_testcases:
            if testcase.cls not in tested:
                tested.add(testcase.cls)

                result = get_generic_arguments(testcase.cls)

                print(f"Testing get_generic_arguments({get_type_name(testcase.cls)}) ==> {result}")

                if testcase.is_generic: # non-generic objects like types may still have generic arguments (values in __args__ attribute)
                    if not any(result):
                        get_generic_arguments(testcase.cls)
                    assert any(result)





    def test_get_generic_origin(self):
        tested: set[type[Any]] = set()

        for testcase in self.types_testcases:
            if testcase.cls not in tested:
                tested.add(testcase.cls)

                result = get_generic_origin(testcase.cls)

                if testcase.is_generic:
                    origin = getattr(testcase.cls, ORIGIN)
                    print(f"Testing get_generic_origin({get_type_name(testcase.cls)}) ==> {get_type_name(result)}")
                    assert result == origin

                elif testcase.is_generic_type:
                    if hasattr(testcase.cls, ORIGIN): # python 3.10 always has the __orig__ attribute
                        origin = getattr(testcase.cls, ORIGIN)
                        print(f"Testing get_generic_origin({get_type_name(testcase.cls)}) ==> {get_type_name(result)}")
                        assert result == origin
                else:
                    result = get_generic_origin(testcase.cls)
                    print(f"Testing get_generic_origin({get_type_name(testcase.cls)}) ==> {get_type_name(result)}")
                    assert result == testcase.cls


        for cls, expected in (
            (str | int, UnionType),
        ):
            result = get_generic_origin(cls)
            print(f"Testing get_generic_origin({get_generic_origin(cls)}) ==> {result}")
            assert result == expected

        with assert_raises(ValueError):
            get_generic_origin(TypeVar("T"))



    def test_is_generic_type(self):
        tested_base: set[type[Any]] = set()
        tested_comparison: set[type[Any]] = set()

        assert not is_generic_type(TypeVar("T"))
        assert is_generic_type(GenericClass1)

        for testcase in self.issubclass_testcases:
            if testcase.base not in tested_base:
                tested_base.add(testcase.base)

                if testcase.base_is_generic_type:
                    result = is_generic_type(testcase.base)
                    print(f"Testing is_generic_type({get_type_name(testcase.base)}) ==> {result}")
                    assert result
                else:
                    result = is_generic_type(testcase.base)
                    print(f"Testing !is_generic_type({get_type_name(testcase.base)}) ==> {result}")
                    assert not result


            if testcase.comparison not in tested_comparison:
                tested_comparison.add(testcase.comparison)

                if testcase.comparison_is_generic_type:
                    result = is_generic_type(testcase.comparison)
                    print(f"Testing is_generic_type({get_type_name(testcase.comparison)}) ==> {result}")
                    assert result
                else:
                    result = is_generic_type(testcase.comparison)
                    print(f"Testing !is_generic_type({get_type_name(testcase.comparison)}) ==> {result}")
                    assert not result


    def test_is_subscripted_generic_type(self):
        tested: set[type[Any]] = set()

        for cls in non_generic_types:
            assert not is_subscripted_generic_type(cls)

        for testcase in self.issubclass_testcases:
            if testcase.base not in tested:
                tested.add(testcase.base)

                result = is_subscripted_generic_type(testcase.base)

                if testcase.base_is_subscripted_generic:
                    print(f"Testing is_subscripted_generic_type({get_type_name(testcase.base)}) ==> {result}")
                    assert result
                else:
                    print(f"Testing !is_subscripted_generic_type({get_type_name(testcase.base)}) ==> {result}")
                    assert not result


            if testcase.comparison not in tested:
                tested.add(testcase.comparison)

                result = is_subscripted_generic_type(testcase.comparison)

                if testcase.base_is_subscripted_generic:
                    print(f"Testing is_generic({get_type_name(testcase.comparison)}) ==> {result}")
                    assert result
                else:
                    print(f"Testing !is_generic({get_type_name(testcase.comparison)}) ==> {result}")
                    assert not result



    def test_get_type_name(self):
        tested: set[type[Any] | TypeVar] = set()

        for cls in set([
            *generic_types,
            *non_generic_types,
            *[ t.base for t in self.issubclass_testcases ],
            *[ t.comparison for t in self.issubclass_testcases ],
        ]):
            if cls not in tested:
                tested.add(cls)
                result = get_type_name(cls)

                print(f"Testing get_type_name({get_type_name(cls)}) ==> {result}")

                assert len(result) > 0
                assert not result.startswith(".") or result == "..."
                assert not result.startswith("<class")

        for cls, expected in cast(tuple[tuple[TypeParameter|UnionParameter, str]], (
            (EllipsisType, "..."),
            (NoneType, "None"),
            (List[str], "typing.List[str]"),
            (list[str], "list[str]"),
            (Dict[str, int], "typing.Dict[str, int]"),
            (dict[str, int], "dict[str, int]"),
            ((str, int), "(str, int)"),
            (str | int, "str | int"),
            (str | int | None, "str | int | None"),
            (ParentClass, "tests.generic_classes.ParentClass"),
            (ParentClass.ChildClass, "tests.generic_classes.ParentClass.ChildClass"),
        )):
            result = get_type_name(cls)
            print(f"Testing get_type_name({get_type_name(cls)}) ==> {result}")
            assert result == expected

        for cls in (
            TypeVar("T"),
            TypeVar("T2", bound=str),
            TypeVar("T3", str, int)
        ):

            result = get_type_name(cls)
            print(f"Testing get_type_name({get_type_name(cls)}) ==> {result}")
            assert result.startswith("~T")


    def test_is_union(self):
        for cls, expected in cast(tuple[tuple[TypeParameter|UnionParameter, bool]], (
            (Optional[int], True),
            (Optional[Union[int, str]], True),
            (Union[int, None], True),
            (Union[int, str], True),
            (Union[int, str, None], True),
            (str, False),
            (int|str, True),
            (int|str|None, True),
        )):
            result = is_union(cls)
            print(f"Testing is_union({get_type_name(cls)}) ==> {result}")
            assert result == expected


    def test_get_union_types(self):
        for cls, expected in cast(tuple[tuple[TypeParameter|UnionParameter, tuple[TypeParameter, ...]]], (
            (Union[int, None], (int,)),
            (Union[int, str], (int, str)),
            (Union[int, str, None], (int, str)),
            (int|None, (int,)),
            (int|str, (int, str)),
            (int|str|None, (int, str)),
        )):
            result = get_union_types(cast(UnionParameter, cls))
            print(f"Testing get_union_types({get_type_name(cls)}) ==> {result}")
            assert result == expected


    def test_is_optional(self):
        for cls, expected in cast(tuple[tuple[TypeParameter|UnionParameter, bool]], (
            (str, False),
            (Optional[str], True),
            (Union[str, None], True),
            (Union[str, int], False),
            (Union[str, int, None], True),
            (str|None, True),
            (str|int, False),
            (str|int|None, True),
        )):
            result = is_optional(cls)
            print(f"Testing is_optional({get_type_name(cls)}) ==> {result}")
            assert result == expected


    def test_get_optional_type(self):
        for cls, expected in cast(tuple[tuple[TypeParameter|UnionParameter, tuple[TypeParameter|UnionParameter, bool]]], (
            (Union[str, list[str]], (Union[str, list[str]], False)),
            (Optional[list[str]], (list[str], True)),
            (Union[str, None], (str, True)),
            (Union[int, str, None], (Union[int, str], True)),
            (Optional[str], (str, True)),
            (str, (str, False)),
            (str|list[str], (str|list[str], False)),
            (str|None, (str, True)),
            (int|str|None, (int|str, True)),
        )):
            result = get_optional_type(cls)
            print(f"Testing get_optional_type({get_type_name(cls)}) ==> {result}")
            assert result == expected

    def test_get_types_from_typevar(self):
        for typevar, expected in cast(tuple[tuple[TypeVar, TypeParameter]], (
            (TypeVar("T1"), type[Any]),
            (TypeVar("T1", bound=str), str),
            (TypeVar("T1", str, int), str|int),
            (TypeVar("T1", bound=int), int),
            (TypeVar("T1", bool, int), bool|int),
        )):
            result = get_types_from_typevar(typevar)
            print(f"Testing get_types_from_typevar({get_type_name(typevar)}) ==> {result}")
            assert result == expected

    def test_construct_generic_type(self):
        for cls, types, expected in cast(tuple[tuple[TypeParameter, tuple[TypeParameter, ...], TypeParameter]], (
            (list, (str,), list[str]),
            (List, (str,), List[str]),
            (Optional, (str,), Optional[str]),
            (tuple, (str,), tuple[str]),
            (tuple, (str, ...), tuple[str, ...]),
            (dict, (str, int), dict[str, int]),
            (Dict, (str, int), Dict[str, int]),
        )):

            result = construct_generic_type(cls, *types)
            print(f"Testing construct_generic_type({get_type_name(cls)}, {', '.join((get_type_name(t) for t in types))}) ==> {result}")
            assert result == expected



    def test_get_original_class(self):
        T = TypeVar("T")
        class GenericClass(Generic[T]): ...
        gc = GenericClass[str]()

        assert get_original_class(gc) == GenericClass[str]

