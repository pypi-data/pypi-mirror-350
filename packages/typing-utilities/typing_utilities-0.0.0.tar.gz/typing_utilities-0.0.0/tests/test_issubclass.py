# pyright: basic
from typing import Any, Type, Iterable, TypeVar, cast
from collections import abc, deque, defaultdict, OrderedDict, ChainMap
from types import NoneType
from pytest import raises as assert_raises, fixture
from typingutils import issubclass_typing, get_type_name, get_type_name, TypeParameter, UnionParameter

from tests.other_impl.issubclass import comparison_generator
from tests.testcase_generators.issubclass import create_testcases_for_issubclass
from tests.generic_classes import DerivedClass1, DerivedClass2, ParentClass, BaseClass


subclass_assertions: list[tuple[TypeParameter | tuple[TypeParameter, ...], tuple[TypeParameter | UnionParameter, ...]]] = [
    (type, (
        object,
        Type,
        Type[Any],
        type,
        type[Any])),
    (NoneType, (
        object,
        NoneType,
        Type[Any],
        type[Any])),
    (list, (
        object,
        abc.Collection)),
    (deque, (
        object,
        Type[Any],
        type[Any],
        deque,
        abc.Collection)),
    (dict, (
        object,
        Type[Any],
        type[Any],
        dict,
        abc.Mapping,
        abc.Collection)),
    (defaultdict, (
        object,
        Type[Any],
        type[Any],
        dict,
        defaultdict,
        abc.Mapping,
        abc.MutableMapping,
        abc.Collection)),
    (OrderedDict, (
        object,
        Type[Any],
        type[Any],
        dict,
        OrderedDict,
        abc.Mapping,
        abc.MutableMapping,
        abc.Collection)),
    (ChainMap, (
        object,
        Type[Any],
        type[Any],
        ChainMap,
        abc.Mapping,
        abc.MutableMapping,
        abc.Collection)),
    (set, (
        object,
        Type[Any],
        type[Any],
        set,
        abc.Set,
        abc.Collection)),
    (frozenset, (
        object,
        Type[Any],
        type[Any],
        abc.Set,
        abc.Collection)),
    (tuple, (
        object,
        Type[Any],
        type[Any],
        tuple)),
    (tuple[str], (
        object,
        Type[Any],
        type[Any],
        tuple[Any],
        tuple)),
    ((str, int, float, bool), (
        object,
        Type[Any],
        type[Any],
        (str, int, float, bool)
    )),
    (DerivedClass2, (
        ParentClass,
        BaseClass
    )),
]

all_types = set([ type_ for _, types in subclass_assertions for type_ in types ])

@fixture(scope = "class")
def comparisons():
    impl: dict[str, list[str]] = defaultdict(lambda: [])
    yield impl

    print("\n")

    for key in impl:
        count = 0
        for comparison in impl[key]:
            print(comparison)
            count +=1

        print(f"Comparison with {key}: {count} differences\n")


class TestClass:

    issubclass_testcases = list(create_testcases_for_issubclass())

    def test_multiple_bases(self, comparisons: dict[str, list[str]]):
        assert issubclass_typing(DerivedClass2, ParentClass)
        assert issubclass_typing(DerivedClass2, BaseClass)
        assert not issubclass_typing(DerivedClass2, DerivedClass1)

    def test_issubclass_typing(self, comparisons: dict[str, list[str]]):
        tested_base: set[type[Any]] = set()
        tested_comparison: set[type[Any]] = set()

        for testcase in self.issubclass_testcases:
            if testcase.base not in tested_base:
                tested_base.add(testcase.base)
                result = issubclass_typing(testcase.base, testcase.base)
                print(f"Testing issubclass_typing({get_type_name(testcase.base)}, {get_type_name(testcase.base)}) ==> {result}")
                assert result

                for impl, result_comparison in comparison_generator(testcase.base, testcase.base):
                    if result_comparison is not None:
                        if result != result_comparison:
                            comparisons[impl].append(f"Comparing {impl}.issubclass({get_type_name(testcase.base)}, {get_type_name(testcase.base)}) ==> {result_comparison} != {result}")

            if testcase.comparison not in tested_comparison:
                tested_comparison.add(testcase.comparison)

                result = issubclass_typing(testcase.comparison, testcase.base)

                if testcase.expected_equality:
                    print(f"Testing issubclass_typing({get_type_name(testcase.comparison)}, {get_type_name(testcase.base)}) ==> {result}")
                    assert result
                else:
                    print(f"Testing !issubclass_typing({get_type_name(testcase.comparison)}, {get_type_name(testcase.base)}) ==> {result}")
                    assert not result

                for impl, result_comparison in comparison_generator(testcase.comparison, testcase.base):
                    if result_comparison is not None:
                        if result != result_comparison:
                            comparisons[impl].append(f"Comparing {impl}.issubclass({get_type_name(testcase.comparison)}, {get_type_name(testcase.base)}) ==> {result_comparison} != {result}")


    def test_explicit_assertions(self, comparisons: dict[str, list[str]]):
        for test_types, types in subclass_assertions:
            for test_type in cast(Iterable[type], test_types if isinstance(test_types, tuple) else (test_types,)):
                for type_ in types:
                    result = issubclass_typing(test_type, type_)


                    print(f"Testing issubclass_typing({get_type_name(test_type)}, {get_type_name(type_)}) ==> {result}")
                    assert result

                    for impl, result_comparison in comparison_generator(test_type, type_):
                        if result_comparison is not None:
                            if result != result_comparison:
                                comparisons[impl].append(f"Comparing {impl}.issubclass({get_type_name(test_type)}, {get_type_name(type_)}) ==> {result_comparison} != {result}")


    def test_tuple_bases(self, comparisons: dict[str, list[str]]):
        for cls, base, expected in cast(tuple[tuple[TypeParameter, TypeParameter|tuple[TypeParameter], bool]], (
            (str, [str, int, bool], True),
            (str, (str, int, bool), True),
            (str, (int, bool), False),
        )):
            result = issubclass_typing(cls, base)
            print(f"Testing issubclass_typing({get_type_name(cls)}, {get_type_name(base)}) ==> {result}")
            assert result == expected

            for impl, result_comparison in comparison_generator(cls, base):
                if result_comparison is not None:
                    if result != result_comparison:
                        comparisons[impl].append(f"Comparing {impl}.issubclass({get_type_name(cls)}, {get_type_name(base)}) ==> {result_comparison} != {result}")


    def test_union_bases(self, comparisons: dict[str, list[str]]):
        for cls, base, expected in cast(tuple[tuple[TypeParameter, TypeParameter|tuple[TypeParameter], bool]], (
            (str, int | bool, False),
            (str, str | float, True),
        )):
            result = issubclass_typing(cls, base)
            print(f"Testing issubclass_typing({get_type_name(cls)}, {get_type_name(base)}) ==> {result}")
            assert result == expected

            for impl, result_comparison in comparison_generator(cls, base):
                if result_comparison is not None:
                    if result != result_comparison:
                        comparisons[impl].append(f"Comparing {impl}.issubclass({get_type_name(cls)}, {get_type_name(base)}) ==> {result_comparison} != {result}")


    def test_typevars(self, comparisons: dict[str, list[str]]):
        for cls, base, expected in (
            (dict[str, int], dict[TypeVar("T1"), TypeVar("T2")], True),
            (dict[str, int], dict[TypeVar("T1", bound=str), TypeVar("T2", bound=int)], True),
            (dict[str, int], dict[TypeVar("T1", bound=bool), TypeVar("T2", bound=int)], False),
            (str, TypeVar("T"), True),
            (str, TypeVar("T", int, str), True),
            (str, TypeVar("T", bound=str), True),
            (str, TypeVar("T", bound=int), False),
        ):

            result = issubclass_typing(cls, base)
            print(f"Testing issubclass_typing({get_type_name(cls)}, {get_type_name(base)}) ==> {result}")
            if result != expected:
                issubclass_typing(cls, base)
            assert result == expected

            for impl, result_comparison in comparison_generator(cls, base):
                if result_comparison is not None:
                    if result != result_comparison:
                        comparisons[impl].append(f"Comparing {impl}.issubclass({get_type_name(cls)}, {get_type_name(base)}) ==> {result_comparison} != {result}")


