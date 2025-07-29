from __future__ import print_function
from builtins import str
from builtins import range
from builtins import object
import datetime
import imp
import time
import sys
import pytest
from freezegun import freeze_time
from fandango import objects

import fandango
import os


def test_dirModule():
    """
    Checks if dirModule correctly list all functions in dependency module.
    """
    from tests.dependencies import dummy_module

    assert sorted(objects.dirModule(dummy_module)) == sorted(
        ["dummy_function", "DummyClass"]
    )


def test_findModule():
    """
    Checks if findModule correctly returns path to the module.
    """

    imp.find_module("fandango")[1]
    params = (
        (
            ("tests.dependencies.dummy_module",),
            {},
            (),
            {},
            os.getcwd() + "/tests/dependencies/dummy_module.py",
        ),
        (("fandango",), {}, (), {}, imp.find_module("fandango")[1]),
        (
            ("fandango.functional",),
            {},
            (),
            {},
            imp.find_module("fandango")[1] + "/functional.py",
        ),
        (("sys",), {}, (), {}, "sys"),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.objects.findModule(*args, **kwargs) == result


def test_NewClass():
    """
    Checks if NewClass creates new class.
    """

    params = (
        (
            ("MyClass",),
            {"classdict": {"__repr__": lambda _: "halo"}},
            (),
            {},
            {"name": "MyClass", "repr": "halo"},
        ),
        # (("MyClass",), {}, (), {}, "MyClass"),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        cls = fandango.objects.NewClass(*args, **kwargs)
        assert repr(cls()) == result["repr"]
        assert cls.__name__ == result["name"]


def test_Singleton():
    from fandango.objects import Singleton

    test_a = Singleton("test1")
    test_b = Singleton("test2")
    assert test_a == test_b
    assert test_a is test_b
    assert isinstance(Singleton.get_singleton("test1"), Singleton)
    test_a.clear_singleton()
    test_c = Singleton("test1")
    assert test_a != test_c
    assert not test_a is test_c


def test_Singleton_inherited():
    from fandango.objects import Singleton

    class MyClass(Singleton):
        counter = 0

    test_mc1 = MyClass("test1")
    test_mc2 = MyClass("test2")
    test_sm = Singleton("test1")

    assert test_mc1 != test_sm
    assert not test_mc1 is test_sm
    assert test_mc1 == test_mc2
    assert test_mc1 is test_mc2

    assert test_mc1.get_singleton() == test_mc2.get_singleton()
    assert MyClass.get_singleton() != Singleton.get_singleton()
    assert test_mc1.get_singleton() is test_mc2.get_singleton()
    assert not MyClass.get_singleton() is Singleton.get_singleton()

    assert isinstance(test_mc1, MyClass)
    assert isinstance(test_mc1.get_singleton("test1"), MyClass)
    assert isinstance(test_mc1.get_singleton("test1"), Singleton)

    assert test_mc1.counter == test_mc2.counter
    test_mc1.counter += 1
    assert test_mc1.counter == test_mc2.counter
    with pytest.raises(AttributeError):
        test_sm.counter


def test_Singleton_mixin():
    from fandango.objects import Singleton

    class MyClass1(object):
        counter1 = 0

    class MyClass2(MyClass1, Singleton):
        counter2 = 0

    test_a = MyClass2("test1")
    test_b = MyClass2("test2")

    assert test_a == test_b
    assert test_a is test_b

    assert test_a.get_singleton() == test_b.get_singleton()

    assert test_a.counter1 == test_b.counter1
    assert test_a.counter2 == test_b.counter2
    test_a.counter1 += 1
    test_a.counter2 += 2
    assert test_a.counter1 == test_b.counter1
    assert test_a.counter2 == test_b.counter2


# skip this
# def test_Singleton_mixin_str():
#     from fandango.objects import Singleton
#
#     class MyClass(str, Singleton):
#         counter = 0
#
#     test_a = MyClass("test1")
#     test_b = MyClass("test2")
#     assert test_a == test_b
#     assert test_a.get_singleton() == test_b.get_singleton()
#     assert test_a.counter == test_b.counter
#     test_a.counter += test_a.counter
#     assert test_a.counter == test_b.counter


# def test_SingletonMap():
#     from fandango.objects import SingletonMap
#     test_a = SingletonMap("test1")
#     test_b = SingletonMap("test1")
#     test_c = SingletonMap("test2")
#     test_d = SingletonMap("test2")
#     assert test_a == test_b
#     assert test_a != test_c
#     assert test_c == test_d
#     # assert test_a.get_singleton() == test_b.get_singleton()
#     # assert test_a.get_singleton() != test_c.get_singleton()
#     # assert test_c.get_singleton() == test_d.get_singleton()
#     assert test_a.get_singleton("test1") == test_b.get_singleton("test1")
#     assert test_a.get_singleton("test1") != test_c.get_singleton("test2")
#     assert test_a.get_singleton("test2") == test_c.get_singleton("test2")


def test_SingletonMap_multiple_args():
    from fandango.objects import SingletonMap

    test_a = SingletonMap("test1", True)
    test_b = SingletonMap("test1", True)
    test_c = SingletonMap("test1", False)
    test_d = SingletonMap(False, "test1")
    test_e = SingletonMap("test1", True, test1_arg=False, test2_arg=True)
    test_f = SingletonMap("test1", True, test1_arg=False, test2_arg=True)
    test_g = SingletonMap("test1", True, test2_arg=True, test1_arg=False)
    test_h = SingletonMap("test1", True, test1_arg=False, test2_arg=True)

    assert test_a == test_b
    assert test_a != test_c
    assert test_c != test_d
    assert test_a != test_e
    assert test_e == test_f
    assert test_e == test_g
    assert test_a is test_b
    assert not test_a is test_c
    assert not test_c is test_d
    assert not test_a is test_e
    assert test_e is test_f
    assert test_e is test_g

    assert SingletonMap.get_singleton("test1", True) == test_a.get_singleton(
        "test1", True
    )
    assert SingletonMap.get_singleton("test1", True) == test_c.get_singleton(
        "test1", True
    )
    assert SingletonMap.get_singleton("test1", True) != SingletonMap.get_singleton(
        "test1", False
    )
    assert SingletonMap.get_singleton("test1", False) != SingletonMap.get_singleton(
        False, "test1"
    )
    assert SingletonMap.get_singleton("test1", True) != SingletonMap.get_singleton(
        "test1"
    )

    assert isinstance(SingletonMap.get_singleton("test1", True), SingletonMap)
    a = SingletonMap.get_singletons()
    for args, instance in list(SingletonMap.get_singletons().items()):
        assert isinstance(instance, SingletonMap)
        assert args.startswith("SingletonMap")
        assert "test1" in args or "test2" in args
        assert "*[" in args and "**[" in args

    SingletonMap.clear_singleton("test1", True)
    test_i = SingletonMap("test1", True)
    test_j = SingletonMap("test1", True, test1_arg=False, test2_arg=True)
    assert test_a != test_i
    assert test_e == test_j
    assert not test_a is test_i
    assert test_e is test_j

    SingletonMap.clear_singletons()
    test_k = SingletonMap("test1", True)
    test_l = SingletonMap("test1", True, test1_arg=False, test2_arg=True)
    assert test_a != test_k
    assert test_e != test_l
    assert not test_a is test_k
    assert not test_e is test_l

    assert (
        SingletonMap.parse_instance_key("test1", True)
        == "SingletonMap(*['test1', True],**[])"
    )
    assert test_k.get_instance_key() == "SingletonMap(*['test1', True],**[])"


def test_SingletonMap_inherited():
    from fandango.objects import SingletonMap

    class MyClass(SingletonMap):
        counter = 0

    test_mc1 = MyClass("test1", True)
    test_mc2 = MyClass(True, "test1")
    test_sm1 = SingletonMap("test1", True)
    test_sm2 = SingletonMap(True, "test1")

    assert test_mc1 != test_mc2
    assert test_sm1 != test_sm2
    assert test_mc1 != test_sm1
    assert test_mc2 != test_sm2
    assert not test_mc1 is test_mc2
    assert not test_sm1 is test_sm2
    assert not test_mc1 is test_sm1
    assert not test_mc2 is test_sm2

    assert test_mc1.get_singleton() == test_mc2.get_singleton()
    assert MyClass.get_singleton() != SingletonMap.get_singleton()
    assert isinstance(test_mc1, MyClass)
    assert isinstance(test_mc1.get_singleton("test1", True), MyClass)
    assert isinstance(test_mc1.get_singleton("test1", True), SingletonMap)

    assert test_mc1.counter == test_mc2.counter
    test_mc1.counter += 1
    assert test_mc1.counter != test_mc2.counter
    with pytest.raises(AttributeError):
        test_sm1.counter


def test_Struct():
    from fandango.objects import Struct

    test_s = Struct(name="DMC", value="1.21", unit="watts", unit_prefix="G")

    test_s2 = Struct(["speed"])
    assert list(test_s2.items()) == [("speed", None)]
    test_s3 = Struct(
        "speed", "year", name="DMC", value="1.21", unit="watts", unit_prefix="G"
    )
    assert list(test_s3.items()) == [("speed", None), ("year", None)]
    # test_s.setCastMethod(lambda k,v: str2type) no such method like in example
    # test_s.set_cast_method(lambda k,v: str2type) it does not exist
    assert test_s.name == "DMC"
    assert test_s.value == "1.21"
    assert test_s["unit"] == "watts"
    assert test_s["unit_prefix"] == "G"

    assert test_s.get("unit") == "watts"
    assert test_s.get("model") == None
    assert test_s.get("model", "DeLorean") == "DeLorean"
    with pytest.raises(AttributeError):
        test_s.model

    test_s.update(model="DeLorean", unit_prefix="giga")
    assert test_s.model == "DeLorean"
    assert test_s.unit_prefix == "giga"

    assert test_s.pop("model") == "DeLorean"
    with pytest.raises(AttributeError):
        test_s.model

    test_s.set("model", "DeLorean")
    assert test_s.model == "DeLorean"

    assert ("model" in test_s) == True
    assert ("drive" in test_s) == False

    assert list(test_s.keys()) == ["model", "unit_prefix", "unit", "value", "name"]
    assert list(test_s.values()) == ["DeLorean", "giga", "watts", "1.21", "DMC"]
    assert list(test_s.items()) == [
        ("model", "DeLorean"),
        ("unit_prefix", "giga"),
        ("unit", "watts"),
        ("value", "1.21"),
        ("name", "DMC"),
    ]
    assert test_s.dict() == {
        "model": "DeLorean",
        "unit_prefix": "giga",
        "unit": "watts",
        "value": "1.21",
        "name": "DMC",
    }
    assert test_s.get_key("1.21") == "value"

    assert (
        test_s.to_str()
        == "fandango.Struct({'model': DeLorean,'unit_prefix': giga,'unit': watts,'value': 1.21,'name': DMC,})"
    )
    assert test_s.to_str(["name", "model"]) == "DMC,DeLorean"
    assert test_s.to_str(["value", "unit_prefix", "unit"], "") == "1.21gigawatts"
    assert test_s.to_str(["value", "unit_prefix", "unit"], sep="") == "1.21gigawatts"

    assert test_s.default_cast("value") == 1.21
    assert test_s.default_cast("value", "1.2") == 1.2
    assert test_s.default_cast("10e9") == 10e9
    assert test_s.default_cast(["1.21, 10e9"]) == ["1.21, 10e9"]
    assert test_s.cast("value") == 1.21
    assert test_s.cast("10e9") == 10e9
    assert (
        test_s.cast("giga", method=lambda k, v: test_s.value + k + test_s.unit)
        == "1.21gigawatts"
    )
    # cast does not take key from the object:
    # assert test_s.cast("unit_prefix", method=lambda k, v: test_s.value+k+test_s.unit) == "1.21gigawatts"
    # cast and cast_item have similar docs

    test_s_casted_keys = test_s.cast_items()
    # not ordered dict, can be unstable?
    assert test_s_casted_keys == [
        ("model", "DeLorean"),
        ("unit_prefix", "giga"),
        ("unit", "watts"),
        ("value", 1.21),
        ("name", "DMC"),
    ]
    assert test_s_casted_keys == list(test_s.items())
    assert test_s.value == 1.21  # update occured

    test_s.update(value="1.21")
    assert test_s.value == "1.21"

    test_s_casted_keys = test_s.cast_items(update=False)
    assert test_s_casted_keys == [
        ("model", "DeLorean"),
        ("unit_prefix", "giga"),
        ("unit", "watts"),
        ("value", 1.21),
        ("name", "DMC"),
    ]
    assert test_s_casted_keys != list(test_s.items())
    assert test_s.value == "1.21"


def test_Cached_expire():
    from fandango.objects import Cached

    @Cached(depth=5, expire=3)
    def return_time():
        return datetime.datetime.now()

    start_time = datetime.datetime(2020, 1, 7, 13, 4, 50)
    with freeze_time(start_time) as frozen_time:
        cached_time = return_time()
        assert start_time == cached_time
        assert datetime.datetime.now() == cached_time

        # first tick
        frozen_time.tick()
        cached_time = return_time()
        assert start_time == cached_time
        assert datetime.datetime.now() != cached_time

        # second tick
        frozen_time.tick()
        cached_time = return_time()
        assert start_time == cached_time
        assert datetime.datetime.now() != cached_time

        # third tick
        frozen_time.tick()
        cached_time = return_time()
        assert start_time != cached_time
        assert datetime.datetime.now() == cached_time


def test_Cached_depth():
    from fandango.objects import Cached

    @Cached(depth=5, expire=3)
    def return_time(fake_arg):
        return datetime.datetime.now()

    start_time = datetime.datetime(2020, 1, 7, 13, 4, 50)
    with freeze_time(start_time) as frozen_time:
        cached_time = return_time(0)
        assert start_time == cached_time
        assert datetime.datetime.now() == cached_time

        # first tick
        frozen_time.tick()
        for i in range(10):
            # assert start_time == cached_time
            cached_time = return_time(i + 1)

        assert start_time != cached_time
        assert datetime.datetime.now() != cached_time


def main():
    for f in list(globals().values()):
        if str(getattr(f, "__name__", "")).startswith("test_"):
            with _Tester(f.__name__) as t:
                print(f())
    return True


if __name__ == "__main__":
    main()
