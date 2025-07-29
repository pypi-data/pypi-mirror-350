# -*- coding: utf-8 -*-

import fandango


def test_absdiff():
    """Checks if absolute difference is correct. In case of floor being above the difference, it should return 0."""
    params = (
        ((3, 1), {}, (), {}, 2),
        ((-3, 1), {}, (), {}, 4),
        ((3, 3), {}, (), {}, 0),
        ((2.5, 2), {"floor": 0.5}, (), {}, 0.5),
        ((2.5, 2), {"floor": 0.7}, (), {}, 0),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.absdiff(*args, **kwargs) == result


def test_anyone():
    """Returns the floor value of the number."""
    params = (
        (([1, 2, 3],), {}, (), {}, 1),
        (([0, 0, ""],), {}, (), {}, ""),
        (([[], 0, 3],), {}, (), {}, 3),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.anyone(*args, **kwargs) == result


def test_avg():
    """Checks if function returns average value"""
    params = (
        (((1, 2, 3, 4),), {}, (), {}, 2.5),
        (((5.3, 2.1, 3.3, 8.2),), {}, (), {}, 4.725),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.avg(*args, **kwargs) == result


def test_contains():
    """Checks if sequence or string contains element."""
    params = (
        (("my", "this is my test"), {"regexp": True}, (), {}, True),
        (("my", "this is your test"), {}, (), {}, False),
        ((4, [1, 2, 3, 7, 8]), {}, (), {}, None),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.contains(*args, **kwargs) == result


def test_everyone():
    """Checks if value returned is the first false value or last true."""
    params = (
        (([1, 2, 3],), {}, (), {}, 3),
        (([1, 0, 3],), {}, (), {}, 0),
        (([[], 0, 3],), {}, (), {}, []),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.everyone(*args, **kwargs) == result


def test_fbool():
    """Checks if fbool returns correct value (all(x) for sequence, cast bool otherwise."""
    params = (
        (([2, True, 3, False],), {}, (), {}, False),
        (([2, True, 3, 7],), {}, (), {}, True),
        (([2, True, 3, {}],), {}, (), {}, False),
        ((0,), {}, (), {}, False),
        (([],), {}, (), {}, False),
        ((["test"],), {}, (), {}, True),
        (("",), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.fbool(*args, **kwargs) == result


def test_first_numbers():
    """Returns the first element in the sequence (list)."""
    params = ((((1, 2.0, 3, 4.0),), {}, (), {}, 1),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.first(*args, **kwargs) == result


def test_first_mixed():
    """Returns the first element in the sequence (list)."""
    params = (((("2", 1, 3, "7"),), {}, (), {}, "2"),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.first(*args, **kwargs) == result


def test_floor():
    """Returns the floor value of the number."""
    params = (((2.3,), {}, (), {}, 2), ((), {"x": 2.3, "unit": 1.1}, (), {}, 2.2))
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.floor(*args, **kwargs) == result


def test_getitem():
    """Returns the floor value of the number."""
    params = (([{"a": 1, "b": 2}, "b"], {}, (), {}, 2),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.getitem(*args, **kwargs) == result


def test_isBool():
    """Checks if isBool returns True if input argument is bool type or naive bool, False otherwise"""
    params = (
        (([False, False, False],), {}, (), {}, False),
        ((7,), {}, (), {}, False),
        ((True,), {}, (), {}, True),
        ((False,), {}, (), {}, True),
        (("True",), {}, (), {}, True),
        (("  FalsE ",), {}, (), {}, True),
        ((" yes ",), {}, (), {}, True),
        ((" NO ",), {}, (), {}, True),
        ((0,), {}, (), {}, True),
        ((1,), {}, (), {}, True),
        (("0",), {}, (), {}, True),
        (("1",), {}, (), {}, True),
        ((None,), {}, (), {}, False),
        (("none",), {}, (), {}, False),
        (("null",), {}, (), {}, False),
        (([False, False, False], False), {}, (), {}, False),
        ((7, False), {}, (), {}, False),
        ((True, False), {}, (), {}, True),
        ((False, False), {}, (), {}, True),
        (("True", False), {}, (), {}, True),
        (("  FalsE ", False), {}, (), {}, True),
        ((" yes ", False), {}, (), {}, True),
        ((" NO ", False), {}, (), {}, True),
        ((0, False), {}, (), {}, True),
        ((1, False), {}, (), {}, True),
        (("0", False), {}, (), {}, False),
        (("1", False), {}, (), {}, False),
        ((None, False), {}, (), {}, False),
        (("none",), {}, (), {}, False),
        (("null",), {}, (), {}, False),
        (("0",), {"is_zero": False}, (), {}, False),
        (("1",), {"is_zero": False}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isBool(*args, **kwargs) == result


def test_isFalse():
    """Checks if isFalse returns True of input argument is naive bool, False otherwise"""
    params = (
        (([2, True, 3, False],), {}, (), {}, False),
        ((7,), {}, (), {}, False),
        ((True,), {}, (), {}, False),
        ((False,), {}, (), {}, True),
        (("True",), {}, (), {}, False),
        (("  FalsE ",), {}, (), {}, True),
        ((" 0 ",), {}, (), {}, True),
        ((" NO ",), {}, (), {}, True),
        ((0,), {}, (), {}, True),
        (([],), {}, (), {}, True),
        ((None,), {}, (), {}, True),
        (("none",), {}, (), {}, True),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isFalse(*args, **kwargs) == result


def test_isNaN():
    """Checks if isNaN returns correct value"""
    params = (
        (("NaN",), {}, (), {}, True),
        ((" nan  ",), {}, (), {}, True),
        ((3,), {}, (), {}, False),
        (([],), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isNaN(*args, **kwargs) == result


def test_isNone():
    """Checks if isNone returns True when input argument is naive None type"""
    params = (
        ((None,), {}, (), {}, True),
        (("  None ",), {}, (), {}, True),
        (("none",), {}, (), {}, True),
        (("NaN",), {}, (), {}, True),
        ((" nan  ",), {}, (), {}, True),
        (("null",), {}, (), {}, True),
        ((" NULL  ",), {}, (), {}, True),
        (([2, True, 3, False],), {}, (), {}, False),
        ((7,), {}, (), {}, False),
        ((3,), {}, (), {}, False),
        (([],), {}, (), {}, False),
        (([None, None],), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isNone(*args, **kwargs) == result


def test_isNumber():
    """Checks if isNumber returns True if input argument is naive number, False otherwise"""
    params = (
        (("test",), {}, (), {}, False),
        ((3,), {}, (), {}, True),
        ((7.0,), {}, (), {}, True),
        (("0",), {}, (), {}, True),
        (("nan",), {}, (), {}, True),
        (("True",), {}, (), {}, False),
        (([],), {}, (), {}, False),
        (([3, 7],), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isNumber(*args, **kwargs) == result


def test_isRegexp():
    """Checks if isRegexp returns True if strings seems to be regex and False otherwise"""
    params = (
        (("test",), {}, (), {}, False),
        (("test*",), {}, (), {}, True),
        (("sys*wąż",), {}, (), {}, True),
        (("syswąż",), {}, (), {}, False),
        (("sys/tg_test/1",), {}, (), {}, False),
        (("test*", "{\\|"), {}, (), {}, False),
        (("\\test*", "{\\|"), {}, (), {}, True),
        (("\test*", "{\\|"), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isRegexp(*args, **kwargs) == result


def test_isString():
    """Checks if isString returns True if input argument is string type, False otherwise"""
    params = (
        (("test",), {}, (), {}, True),
        (("",), {}, (), {}, True),
        (("sys*wąż",), {}, (), {}, True),
        ((False,), {}, (), {}, False),
        (("True",), {}, (), {}, True),
        (("  FalsE ",), {}, (), {}, True),
        ((" 0 ",), {}, (), {}, True),
        ((" NO ",), {}, (), {}, True),
        ((0,), {}, (), {}, False),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
        (("none",), {}, (), {}, True),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isString(*args, **kwargs) == result


def test_isTrue():
    """Checks if fbool returns correct value (all(x) for sequence, cast bool otherwise."""
    params = (
        ((True,), {}, (), {}, True),
        ((False,), {}, (), {}, False),
        (("True",), {}, (), {}, True),
        (("False",), {}, (), {}, False),
        ((0,), {}, (), {}, False),
        (("0",), {}, (), {}, False),
        (("2",), {}, (), {}, True),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isTrue(*args, **kwargs) == result


def test_join():
    """Checks if joined elements create list correctly."""
    params = (
        ((1, "a"), {}, (), {}, [1, "a"]),
        (([1, 2, 3], [4, 5, 6]), {}, (), {}, [1, 2, 3, 4, 5, 6]),
        (([1, "b", 3], [4, "e", 6]), {}, (), {}, [1, "b", 3, 4, "e", 6]),
        (([1, 2, "c", "e"],), {}, (), {}, [1, 2, "c", "e"]),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.join(*args, **kwargs) == result


def test_last_numbers():
    """Returns the last element in the sequence (list)."""
    params = ((((1, 2.0, 3, 4.0),), {}, (), {}, 4.0),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.last(*args, **kwargs) == result


def test_last_mixed():
    """Returns the last element in the sequence (list)."""
    params = (((("2", 1, 3, "7"),), {}, (), {}, "7"),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.last(*args, **kwargs) == result


def test_matchAll():
    """Checks if matchAll returns matched strings by one of the expressions."""
    params = (
        (("test", "test"), {}, (), {}, ["test"]),
        (("Test", "test"), {}, (), {}, ["test"]),
        (("test", "Test"), {}, (), {}, ["Test"]),
        (("test", "thisISmytest"), {}, (), {}, ["thisISmytest"]),
        (("*test", "thisISmytest"), {}, (), {}, ["thisISmytest"]),
        (("^test", "thisISmytest"), {}, (), {}, []),
        ((["my"], "thisISmytest"), {}, (), {}, ["thisISmytest"]),
        ((["*my"], "thisISmytest"), {}, (), {}, []),
        ((["*my$"], "thisISmytest"), {}, (), {}, []),
        ((["test", "my"], "thisISmytest"), {}, (), {}, ["thisISmytest"]),
        ((["*test", "my"], "thisISmytest"), {}, (), {}, []),
        ((["*test", "*my*"], "thisISmytest"), {}, (), {}, ["thisISmytest"]),
        (
            (["*test", "*my*"], ["thisISmytest", "thisISmy"]),
            {},
            (),
            {},
            ["thisISmytest"],
        ),
        ((["Test", "my", "this"], ["test", "Test", "this", "my"]), {}, (), {}, []),
        (
            ("my*", ["thisISmytest", "thisISmy", "myTest", "myString"]),
            {},
            (),
            {},
            ["myTest", "myString"],
        ),
        (
            (
                ["test*", "*my"],
                ["thisISmytest", "thisISmy", "myTest", "myString", "testMy"],
            ),
            {},
            (),
            {},
            ["testMy"],
        ),
        (
            (),
            {
                "exprs": ["test*", "*my"],
                "seq": ["thisISmytest", "thisISmy", "myTest", "myString", "testMy"],
            },
            (),
            {},
            ["testMy"],
        ),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.matchAll(*args, **kwargs) == result


def test_matchAny():
    """Checks if matchAny returns string matched by any of the expression."""
    params = (
        (("test", "test"), {}, (), {}, "test"),
        (("Test", "test"), {}, (), {}, "test"),
        (("test", "thisISmytest"), {}, (), {}, None),
        (("*test", "thisISmytest"), {}, (), {}, "thisISmytest"),
        ((["Test", "my", "this"], "sys/tg_test/1"), {}, (), {}, None),
        ((["Test", "my", "this", "tg"], "sys/tg_test/1"), {}, (), {}, None),
        ((["Test", "my", "this", "*tg"], "sys/tg_test/1"), {}, (), {}, None),
        ((["Test", "my", "this", "*tg$"], "sys/tg_test/1"), {}, (), {}, None),
        ((["Test", "my", "this", "tg*"], "sys/tg_test/1"), {}, (), {}, None),
        ((["Test", "my", "this", "^tg*"], "sys/tg_test/1"), {}, (), {}, None),
        (
            (["Test", "my", "this", "*tg*"], "sys/tg_test/1"),
            {},
            (),
            {},
            "sys/tg_test/1",
        ),
        ((["Test", "my", "this", "tg*"], "sys/tg_test/my"), {}, (), {}, None),
        (
            (["Test", "*my", "this", "tg*"], "sys/tg_test/my"),
            {},
            (),
            {},
            "sys/tg_test/my",
        ),
        (
            (),
            {"exprs": ["Test", "my", "this", "*tg*"], "seq": "sys/tg_test/1"},
            (),
            {},
            "sys/tg_test/1",
        ),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.matchAny(*args, **kwargs) == result


def test_max():
    """Checks if function returns max value"""
    params = (
        (((3, 2, 8, 4),), {}, (), {}, 8),
        (((3.2, 2.1, 8.3, 4),), {}, (), {}, 8.3),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.max(*args, **kwargs) == result


def test_min():
    """Checks if function returns min value"""
    params = ((((5, 2, 3, 4),), {}, (), {}, 2), (((5.2, 2.1, 3.2, 2),), {}, (), {}, 2))
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.min(*args, **kwargs) == result


def test_notNone():
    """Checks if notNone returns arg if arg is not None, otherwise default."""
    params = (
        ((7,), {}, (), {}, 7),
        ((["a", 2, False],), {}, (), {}, ["a", 2, False]),
        ((None,), {}, (), {}, None),
        ((7, 0), {}, (), {}, 7),
        ((["a", 2, False], 0), {}, (), {}, ["a", 2, False]),
        ((None, 0), {}, (), {}, 0),
        ((7,), {"default": 0}, (), {}, 7),
        ((["a", 2, False],), {"default": 0}, (), {}, ["a", 2, False]),
        ((None,), {"default": 0}, (), {}, 0),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.notNone(*args, **kwargs) == result


def test_reldiff():
    """Checks if relative difference is correct. In case of floor being above the difference, it should return 0."""
    params = (
        ((2, 1), {}, (), {}, 0.5),
        ((2, -1), {}, (), {}, 1.5),
        ((2, 4), {}, (), {}, -1),
        ((2.0, 1.0), {}, (), {}, 0.5),
        ((2, 1), {"floor": 0.5}, (), {}, 0.5),
        ((2, 1), {"floor": 0.7}, (), {}, 0),
        ((2, 2), {}, (), {}, 0),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.reldiff(*args, **kwargs) == result


def test_rms():
    """Returns the average value of the sequence."""
    params = (
        (((1, 2, 3, 4),), {}, (), {}, 2.7386127875258306),
        (((3.0, 4, 1.0, 2),), {}, (), {}, 2.7386127875258306),
        (((7.0, 4.2, 1.0, 2.3),), {}, (), {}, 4.269953161335613),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.rms(*args, **kwargs) == result


def test_rtf2plain():
    """Checks if str2bool return True if string is not naive false and False otherwise"""
    params = (
        (
            ("<html><title>this is a title</title></html>",),
            {},
            (),
            {},
            "this is a title",
        ),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.rtf2plain(*args, **kwargs) == result


def test_seqdiff():
    """Checks if differences between numbers in the list are correct. It can use both method reldiff and absdiff"""
    params = (
        (([2, 3, 4.5], [1, 1, 9]), {}, (), {}, True),
        (([2, 3, 4.5], [1, 2, 6]), {"floor": 0.7}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.seqdiff(*args, **kwargs) == result


def test_splitList():
    """Checks if list is splitted in ."""
    params = (
        (([1, 2, "c", "e"], 3), {}, (), {}, [[1, 2, "c"], ["e"]]),
        (([1, 2, "c", "e"], 1), {}, (), {}, [[1], [2], ["c"], ["e"]]),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.splitList(*args, **kwargs) == result


def test_str2bool():
    """Checks if str2bool return True if string is not naive false and False otherwise"""
    params = (
        (("31",), {}, (), {}, True),
        (("true",), {}, (), {}, True),
        (("  Yes",), {}, (), {}, True),
        (("False",), {}, (), {}, False),
        ((" FALSE ",), {}, (), {}, False),
        (("0",), {}, (), {}, False),
        (("  None",), {}, (), {}, False),
        (("no",), {}, (), {}, False),
        (("NO  ",), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2bool(*args, **kwargs) == result


def test_str2bytes():
    """Checks if str2bool return True if string is not naive false and False otherwise"""
    params = (
        (("03",), {}, (), {}, [48, 51]),
        (("abba",), {}, (), {}, [97, 98, 98, 97]),
        (("test",), {}, (), {}, [116, 101, 115, 116]),
        (("wąż",), {}, (), {}, [119, 261, 380]),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2bytes(*args, **kwargs) == result


def test_str2float():
    """Checks if str2float returns first float found in the string"""
    params = (
        (("31",), {}, (), {}, 31),
        (("3.1",), {}, (), {}, 3.1),
        ((None,), {}, (), {}, None),
        (("test",), {}, (), {}, None),
        (("test07test",), {}, (), {}, 7),
        (("test07.5e-10test",), {}, (), {}, 7.5e-10),
        (("2020-11-16 00:27:17",), {}, (), {}, 2020),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2float(*args, **kwargs) == result


def test_str2int():
    """Checks if str2int returns first integer found in the string"""
    params = (
        (("31",), {}, (), {}, 31),
        (("3.1",), {}, (), {}, 3),
        ((7.0,), {}, (), {}, None),
        ((None,), {}, (), {}, None),
        (("test",), {}, (), {}, None),
        (("test07test",), {}, (), {}, 7),
        (("2020-11-16 00:27:17",), {}, (), {}, 2020),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2int(*args, **kwargs) == result


def test_str2type():
    """Checks if str2bool return True if string is not naive false and False otherwise"""
    params = (
        (("31",), {}, (), {}, 31),
        (("0o31",), {}, (), {}, 25),
        (("3.7",), {}, (), {}, 3.7),
        (("No",), {}, (), {}, False),
        (("TRUE",), {}, (), {}, True),
        (("1",), {}, (), {}, 1),
        ((None,), {}, (), {}, None),
        (("abba",), {}, (), {}, "abba"),
        (("wąż",), {}, (), {}, "wąż"),
        (("3+5",), {}, (), {}, 8),
        (("[1, 2, 4, 3]",), {}, (), {}, [1, 2, 4, 3]),
        (("1 2 4 3",), {"use_eval": False}, (), {}, [1, 2, 4, 3]),
        ((7,), {}, (), {}, 7),
        ((7.3,), {}, (), {}, 7.3),
        (("2020-11-16 00:27:17",), {}, (), {}, "2020-11-16 00:27:17"),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2type(*args, **kwargs) == result


def test_xor():
    """Checks if xor return correct value. Sometimes it returns True or False, sometimes it returns one of the arguments."""
    params = (
        (("a", "b"), {}, (), {}, False),
        (("", "b"), {}, (), {}, "b"),
        (("", ""), {}, (), {}, ""),
        ((4, 2), {}, (), {}, False),
        ((4, 0), {}, (), {}, 4),
        ((0, 0), {}, (), {}, 0),
        ((4.0, 0.1), {}, (), {}, False),
        ((4, 0), {}, (), {}, 4),
        (([], "c"), {}, (), {}, "c"),
        (([], ""), {}, (), {}, ""),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.xor(*args, **kwargs) == result
