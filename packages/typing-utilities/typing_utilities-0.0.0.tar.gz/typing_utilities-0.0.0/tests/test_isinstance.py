# pyright: basic
from typing import (
    Any, Sequence, MutableSequence, List, Mapping, MutableMapping, Dict, Deque,
    Set, Tuple, DefaultDict, OrderedDict as OrderedDict_, FrozenSet, Type, Iterable, cast
)
from collections import abc, deque, defaultdict, OrderedDict, Counter, ChainMap
from datetime import date, time, datetime
from decimal import Decimal
from types import NoneType
from pytest import raises as assert_raises, fixture

from typingutils import TypeParameter, UnionParameter, AnyType, get_type_name, isinstance_typing, is_type
from tests.other_impl.isinstance import comparison_generator

instance_assertions: list[tuple[object | tuple[object], tuple[TypeParameter | UnionParameter, ...], bool]] = [
    (type, (
        object,
        Type[Any],
        type[Any]
        ), False),
    (None, (
        object,
        NoneType,
        Type[Any],
        type[Any]), True),
    ("abcdefg", (
        object,
        Type[Any],
        type[Any],
        str,
        abc.Collection,
        abc.Collection[Any],
        abc.Sequence,
        abc.Sequence[Any],
        Sequence,
        Sequence[Any]), True),
    (123, (
        object,
        Type[Any],
        type[Any],
        int), True),
    (10.12345, (
        object,
        Type[Any],
        type[Any],
        float), True),
    (Decimal(10.12345), (
        object,
        Type[Any],
        type[Any],
        Decimal), True),
    ((True, False), (
        object,
        Type[Any],
        type[Any],
        bool,
        int), True),
    (date(2000, 1, 1), (
        object,
        Type[Any],
        type[Any],
        date), True),
    (time(10, 0, 0), (
        object,
        Type[Any],
        type[Any],
        time), True),
    (datetime(2000, 1, 1, 10, 0, 0), (
        object,
        Type[Any],
        type[Any],
        datetime,
        date), True),
    (([], ["a", "b", "c"]), (
        object,
        Type[Any],
        type[Any],
        list,
        List,
        abc.Collection,
        abc.Collection[Any],
        abc.Sequence,
        abc.Sequence[Any],
        abc.MutableSequence,
        abc.MutableSequence[Any],
        Sequence,
        Sequence[Any],
        MutableSequence,
        MutableSequence[Any]), True),
    (deque((1,2,3), maxlen=10), (
        object,
        Type[Any],
        type[Any],
        deque,
        Deque,
        abc.Collection,
        abc.Collection[Any],
        abc.Sequence,
        abc.Sequence[Any],
        abc.MutableSequence,
        abc.MutableSequence[Any],
        Sequence,
        Sequence[Any],
        MutableSequence,
        MutableSequence[Any]), True),
    (({}, { "a": 1}), (
        object,
        Type[Any],
        type[Any],
        dict,
        dict[Any, Any],
        Dict,
        Dict[Any, Any],
        abc.Mapping,
        abc.Mapping[Any, Any],
        abc.MutableMapping,
        abc.MutableMapping[Any, Any],
        abc.Collection,
        abc.Collection[Any],
        Mapping,
        Mapping[Any, Any],
        MutableMapping,
        MutableMapping[Any, Any]), True),
    (defaultdict(list), (
        object,
        Type[Any],
        type[Any],
        dict,
        dict[Any, Any],
        defaultdict,
        defaultdict[Any, Any],
        Dict,
        Dict[Any, Any],
        DefaultDict,
        DefaultDict[Any, Any],
        abc.Mapping,
        abc.Mapping[Any, Any],
        abc.MutableMapping,
        abc.MutableMapping[Any, Any],
        abc.Collection,
        abc.Collection[Any],
        Mapping,
        Mapping[Any, Any],
        MutableMapping,
        MutableMapping[Any, Any]), True),
    (OrderedDict(), (
        object,
        Type[Any],
        type[Any],
        dict,
        dict[Any, Any],
        Dict,
        Dict[Any, Any],
        OrderedDict,
        OrderedDict[Any, Any],
        OrderedDict_,
        OrderedDict_[Any, Any],
        abc.Mapping,
        abc.Mapping[Any, Any],
        abc.MutableMapping,
        abc.MutableMapping[Any, Any],
        abc.Collection,
        abc.Collection[Any],
        Mapping,
        Mapping[Any, Any],
        MutableMapping,
        MutableMapping[Any, Any]), True),
    (ChainMap(), (
        object,
        Type[Any],
        type[Any],
        ChainMap,
        ChainMap[Any, Any],
        abc.Mapping,
        abc.Mapping[Any, Any],
        abc.MutableMapping,
        abc.MutableMapping[Any, Any],
        abc.Collection,
        abc.Collection[Any],
        Mapping,
        Mapping[Any, Any],
        MutableMapping,
        MutableMapping[Any, Any]), True),
    ({ 1, 2, 3}, (
        object,
        Type[Any],
        type[Any],
        set,
        set[Any],
        abc.Set,
        abc.Set[Any],
        abc.Collection,
        abc.Collection[Any],
        Set,
        Set[Any]), True),
    (frozenset((1,2,3)), (
        object,
        Type[Any],
        type[Any],
        abc.Set,
        abc.Set[Any],
        abc.Collection,
        abc.Collection[Any],
        FrozenSet,
        FrozenSet[Any]), True),
    ((), (
        object,
        Type[Any],
        type[Any],
        tuple,
        Tuple,
        Tuple[Any],
        Sequence,
        Sequence[Any]), True)
]

all_types = set( type_ for _, types, _ in instance_assertions for type_ in types )
all_instances = tuple( (instance, is_inst) for instances, _, is_inst in instance_assertions for instance in cast(Iterable[object], instances if isinstance(instances, tuple) else (instances,)) )


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

    def test_all_types(self, comparisons: dict[str, list[str]]):
        for type_ in all_types:
            result = is_type(type_)

            if type_ is object:
                assert not result
            else:
                assert result

            result = isinstance_typing(type_, type_)

            if type_ is object:
                assert result # object is always an instance of object
            else:
                assert not result

            for impl, result_comparison in comparison_generator(type_, type_):
                if result_comparison is not None:
                    if result != result_comparison:
                        comparisons[impl].append(f"Comparing {impl}.isinstance({type_}, {get_type_name(type_)}) ==> {result_comparison} != {result}")


    def test_all_instances(self, comparisons: dict[str, list[str]]):
        for instance, is_inst in all_instances:
            result = isinstance_typing(instance)

            if is_inst:
                print(f"Testing isinstance_typing({instance}) ==> {result}")
                assert result
            else:
                print(f"Testing !isinstance_typing({instance}) ==> {result}")
                assert not result



    def test_explicit_assertions(self, comparisons: dict[str, list[str]]):
        for instances, types, is_inst in instance_assertions:
            negations = all_types.difference(types)

            for instance in cast(Iterable[object], instances if isinstance(instances, tuple) else (instances,)):
                for type_ in types:
                    result = isinstance_typing(instance, type_)

                    print(f"Testing isinstance_typing({instance}, {get_type_name(type_)}) ==> {result}")
                    assert result is not None
                    assert result == True

                    for impl, result_comparison in comparison_generator(instance, type_):
                        if result_comparison is not None:
                            if result != result_comparison:
                                comparisons[impl].append(f"Comparing {impl}.isinstance({instance}, {get_type_name(type_)}) ==> {result_comparison} != {result}")


                for type_ in negations:
                    result = isinstance_typing(instance, type_)
                    print(f"Testing !isinstance_typing({instance}, {get_type_name(type_)}) ==> {result}")

                    assert result is not None
                    assert result == False

                    for impl, result_comparison in comparison_generator(instance, type_):
                        if result_comparison is not None:
                            if result != result_comparison:
                                comparisons[impl].append(f"Comparing {impl}.isinstance({instance}, {get_type_name(type_)}) ==> {result_comparison} = {result}")


    def test_multiple(self, comparisons: dict[str, list[str]]):
        for obj, cls, expected in cast(tuple[tuple[object, Tuple[TypeParameter|UnionParameter, ...], bool]], (
            ("abc", (str, int, bool), True),
            ("abc", (float, int, bool), False),
            ("abc", (float, int, bool), False),
            ("abc", (float, str|int, bool), True),
        )):

            result = isinstance_typing(obj, cls)
            print(f"Testing isinstance_typing({obj}, {cls}) ==> {result}")
            assert result == expected

            for impl, result_comparison in comparison_generator(obj, cls):
                if result_comparison is not None:
                    if result != result_comparison:
                        comparisons[impl].append(f"Comparing {impl}.isinstance({obj}, {get_type_name(cast(AnyType, cls))}) ==> {result_comparison} != {result}")

