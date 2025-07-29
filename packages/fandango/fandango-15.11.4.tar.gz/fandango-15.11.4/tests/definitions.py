# -*- coding: utf-8 -*-

skip_tests = [
    "fandango.functional.call",
    "fandango.functional.matchMap",
    "fandango.functional.filtersmart",
    "fandango.functional.retry",
    "fandango.functional.retried",
    "fandango.functional.retrier",
    "fandango.functional.evalF",
    "fandango.functional.testF",
    "fandango.functional.evalX",
    "fandango.objects.pick",
    "fandango.objects.dump",
    "fandango.objects.Struct.default_cast",
    "fandango.objects.Struct.cast",
    "fandango.objects.Struct.cast_items",
    "fandango.objects._fget",
    "fandango.objects._fset",
    "fandango.objects._fdel",
    "fandango.objects.make_property",
    "fandango.objects.Variable",
    "fandango.objects.NamedProperty",
    "fandango.objects.ReleaseNumber",
    "fandango.objects.locked",
    "fandango.objects.self_locked",
    "fandango.objects.Decorator",
    "fandango.objects.ClassDecorator",
    "fandango.objects.Decorated",
]

# TODO: redefine test definitions according to the format defined above
tests = {
    "fandango.functional.first": {
        "numbers": {
            "docs": "Returns the first element in the sequence (list).",
            "params": ((((1, 2.0, 3, 4.0),), {}, (), {}, 1),),
        },
        "mixed": {
            "docs": "Returns the first element in the sequence (list).",
            "params": (
                (
                    (
                        (
                            "2",
                            1,
                            3,
                            "7",
                        ),
                    ),
                    {},
                    (),
                    {},
                    "2",
                ),
            ),
        },
        "iter": {
            "docs": "Returns the first element in the sequence (iterator).",
            "method": "ci/tests/test_functional.py::test_first_iter",
        },
        "generator": {
            "docs": "Returns the first element in the sequence (generator).",
            "method": "ci/tests/test_functional.py::test_first_generator",
        },
    },
    "fandango.functional.last": {
        "numbers": {
            "docs": "Returns the last element in the sequence (list).",
            "params": ((((1, 2.0, 3, 4.0),), {}, (), {}, 4.0),),
        },
        "mixed": {
            "docs": "Returns the last element in the sequence (list).",
            "params": (
                (
                    (
                        (
                            "2",
                            1,
                            3,
                            "7",
                        ),
                    ),
                    {},
                    (),
                    {},
                    "7",
                ),
            ),
        },
        "iter": {
            "docs": "Returns the last element in the sequence (iterator).",
            "method": "ci/tests/test_functional.py::test_last_iter",
        },
        "generator": {
            "docs": "Returns the last element in the sequence (generator).",
            "method": "ci/tests/test_functional.py::test_last_generator",
        },
        "generator_max": {
            "docs": "Checks if the last element of the generator is returned correctly "
            "when reaching MAX index.",
            "method": "ci/tests/test_functional.py::test_last_generator_max",
        },
        "generator_overmax": {
            "docs": "Checks if generator exceeds MAX limit and raises IndexError",
            "method": "ci/tests/test_functional.py::test_last_generator_max",
        },
    },
    "fandango.functional.max": {
        "": {
            "docs": "Checks if function returns max value",
            "params": (
                (((3, 2, 8, 4),), {}, (), {}, 8),
                (((3.2, 2.1, 8.3, 4),), {}, (), {}, 8.3),
            ),
        }
    },
    "fandango.functional.min": {
        "": {
            "docs": "Checks if function returns min value",
            "params": (
                (((5, 2, 3, 4),), {}, (), {}, 2),
                (((5.2, 2.1, 3.2, 2),), {}, (), {}, 2),
            ),
        }
    },
    "fandango.functional.avg": {
        "": {
            "docs": "Checks if function returns average value",
            "params": (
                (((1, 2, 3, 4),), {}, (), {}, 2.5),
                (((5.3, 2.1, 3.3, 8.2),), {}, (), {}, 4.725),
            ),
        },
        "iterators": {
            "docs": "Checks if function returns average value from iterators including generators",
            "method": "ci/tests/test_functional.py::test_avg_iterators",
        },
    },
    "fandango.functional.rms": {
        "": {
            "docs": "Returns the average value of the sequence.",
            "params": (
                (((1, 2, 3, 4),), {}, (), {}, 2.7386127875258306),
                (((3.0, 4, 1.0, 2),), {}, (), {}, 2.7386127875258306),
                (((7.0, 4.2, 1.0, 2.3),), {}, (), {}, 4.269953161335613),
            ),
        }
    },
    "fandango.functional.randomize": {
        "": {
            "docs": "Returns randomized version of the list. Test checks if len is the "
            "same and returned list has the same items as the input list.",
            "method": "ci/tests/test_functional.py::test_randomize",
        }
    },
    "fandango.functional.randpop": {
        "": {
            "docs": "Returns the average value of the sequence.",
            "method": "ci/tests/test_functional.py::test_randpop",
        }
    },
    # This is the same test, but for different arguments. Can we do this like that? First test will have only args, second one only kwargs. No need for additional test name.
    "fandango.functional.floor": {
        "": {
            "docs": "Returns the floor value of the number.",
            "params": (
                ((2.3,), {}, (), {}, 2),
                ((), {"x": 2.3, "unit": 1.1}, (), {}, 2.2),
            ),
        }
    },
    "fandango.functional.xor": {
        "": {
            "docs": "Checks if xor return correct value. Sometimes it returns True or "
            "False, sometimes it returns one of the arguments.",
            "params": (
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
            ),
        }
    },
    "fandango.functional.reldiff": {
        "": {
            "docs": "Checks if relative difference is correct. In case of floor being "
            "above the difference, it should return 0.",
            "params": (
                ((2, 1), {}, (), {}, 0.5),
                ((2, -1), {}, (), {}, 1.5),
                ((2, 4), {}, (), {}, -1),
                ((2.0, 1.0), {}, (), {}, 0.5),
                ((2, 1), {"floor": 0.5}, (), {}, 0.5),
                ((2, 1), {"floor": 0.7}, (), {}, 0),
                ((2, 2), {}, (), {}, 0),
            ),
        }
    },
    "fandango.functional.absdiff": {
        "": {
            "docs": "Checks if absolute difference is correct. In case of floor being "
            "above the difference, it should return 0.",
            "params": (
                ((3, 1), {}, (), {}, 2),
                ((-3, 1), {}, (), {}, 4),
                ((3, 3), {}, (), {}, 0),
                ((2.5, 2), {"floor": 0.5}, (), {}, 0.5),
                ((2.5, 2), {"floor": 0.7}, (), {}, 0),
            ),
        }
    },
    "fandango.functional.seqdiff": {
        "": {
            "docs": "Checks if differences between numbers in the list are correct. It "
            "can use both method reldiff and absdiff",
            "params": (
                (([2, 3, 4.5], [1, 1, 9]), {}, (), {}, True),
                (([2, 3, 4.5], [1, 2, 6]), {"floor": 0.7}, (), {}, False),
            ),
        }
    },
    "fandango.functional.join": {
        "": {
            "docs": "Checks if joined elements create list correctly.",
            "params": (
                ((1, "a"), {}, (), {}, [1, "a"]),
                (([1, 2, 3], [4, 5, 6]), {}, (), {}, [1, 2, 3, 4, 5, 6]),
                (([1, "b", 3], [4, "e", 6]), {}, (), {}, [1, "b", 3, 4, "e", 6]),
                (([1, 2, "c", "e"],), {}, (), {}, [1, 2, "c", "e"]),
            ),
        }
    },
    "fandango.functional.djoin": {
        "": {
            "docs": "Checks if joined elements create list or dictionary correctly. Two "
            "lists should create list. List and dict should create dict with "
            "None values for keys from list. Two dicts should create dict and "
            "if some keys are repeated, values for them should be joined",
            "params": (
                (([1, 2, 3], [4, 5, 6]), {}, (), {}, [1, 2, 3, 4, 5, 6]),
                (
                    ({"a": 1, "b": 2}, [4, "e", 6]),
                    {},
                    (),
                    {},
                    {"a": 1, "b": 2, 4: None, "e": None, 6: None},
                ),
                (
                    ([4, "e", 6], {"a": 1, "b": 2}),
                    {},
                    (),
                    {},
                    {"a": 1, "b": 2, 4: None, "e": None, 6: None},
                ),
                (
                    ({"a": 1, "b": 2}, {"c": 3, "d": 4}),
                    {},
                    (),
                    {},
                    {"a": 1, "b": 2, "c": 3, "d": 4},
                ),
                (
                    ({"a": 1, "b": 2}, {"b": 3, "c": 4}),
                    {},
                    (),
                    {},
                    {"a": 1, "b": [2, 3], "c": 3, "d": 4},
                ),
            ),
            "method": "ci/tests/test_functional.py::test_djoin",
        }
    },
    "fandango.functional.kmap": {
        "": {
            "docs": "Returns the floor value of the number.",
            "method": "ci/tests/test_functional.py::test_kmap",
        }
    },
    "fandango.functional.splitList": {
        "": {
            "docs": "Checks if list is splitted in .",
            "params": (
                (
                    (
                        [1, 2, "c", "e"],
                        3,
                    ),
                    {},
                    (),
                    {},
                    [[1, 2, "c"], ["e"]],
                ),
                (
                    (
                        [1, 2, "c", "e"],
                        1,
                    ),
                    {},
                    (),
                    {},
                    [[1], [2], ["c"], ["e"]],
                ),
            ),
        }
    },
    "fandango.functional.contains": {
        "": {
            "docs": "Checks if sequence or string contains element.",
            "params": (
                (
                    (
                        "my",
                        "this is my test",
                    ),
                    {"regexp": True},
                    (),
                    {},
                    True,
                ),
                (
                    (
                        "my",
                        "this is your test",
                    ),
                    {},
                    (),
                    {},
                    False,
                ),
                (
                    (
                        4,
                        [1, 2, 3, 7, 8],
                    ),
                    {},
                    (),
                    {},
                    None,
                ),
            ),
        }
    },
    "fandango.functional.anyone": {
        "": {
            "docs": "Returns the floor value of the number.",
            "params": (
                (([1, 2, 3],), {}, (), {}, 1),
                (([0, 0, ""],), {}, (), {}, ""),
                (([[], 0, 3],), {}, (), {}, 3),
                (([],), {}, (), {}, False),
                ((None,), {}, (), {}, False),
            ),
        }
    },
    "fandango.functional.everyone": {
        "": {
            "docs": "Checks if value returned is the first false value or last true.",
            "params": (
                (([1, 2, 3],), {}, (), {}, 3),
                (([1, 0, 3],), {}, (), {}, 0),
                (([[], 0, 3],), {}, (), {}, []),
            ),
        }
    },
    "fandango.functional.setitem": {
        "": {
            "docs": "Returns the floor value of the number.",
            "method": "ci/tests/test_functional.py::test_setitem",
        }
    },
    "fandango.functional.getitem": {
        "": {
            "docs": "Returns the floor value of the number.",
            "params": (([{"a": 1, "b": 2}, "b"], {}, (), {}, 2),),
        }
    },
    "fandango.functional.matchAll": {
        "": {
            "docs": "Checks if matchAll returns matched strings by one of the expressions.",
            "params": (
                (
                    (
                        "test",
                        "test",
                    ),
                    {},
                    (),
                    {},
                    ["test"],
                ),
                (
                    (
                        "Test",
                        "test",
                    ),
                    {},
                    (),
                    {},
                    ["test"],
                ),
                (
                    (
                        "test",
                        "Test",
                    ),
                    {},
                    (),
                    {},
                    ["Test"],
                ),
                (
                    (
                        "test",
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    ["thisISmytest"],
                ),
                (
                    (
                        "*test",
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    ["thisISmytest"],
                ),
                (
                    (
                        "^test",
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    [],
                ),
                (
                    (
                        ["my"],
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    ["thisISmytest"],
                ),
                (
                    (
                        ["*my"],
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    [],
                ),
                (
                    (
                        ["*my$"],
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    [],
                ),
                (
                    (
                        ["test", "my"],
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    ["thisISmytest"],
                ),
                (
                    (
                        ["*test", "my"],
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    [],
                ),
                (
                    (
                        ["*test", "*my*"],
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    ["thisISmytest"],
                ),
                (
                    (["*test", "*my*"], ["thisISmytest", "thisISmy"]),
                    {},
                    (),
                    {},
                    ["thisISmytest"],
                ),
                (
                    (
                        ["Test", "my", "this"],
                        ["test", "Test", "this", "my"],
                    ),
                    {},
                    (),
                    {},
                    [],
                ),
                # ((["*test", "my"], ["thisISmytest", "thisISmy"]), {}, (), {}, ["thisISmytest"]),
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
                        "seq": [
                            "thisISmytest",
                            "thisISmy",
                            "myTest",
                            "myString",
                            "testMy",
                        ],
                    },
                    (),
                    {},
                    ["testMy"],
                ),
            ),
        }
    },
    "fandango.functional.matchAny": {
        "": {
            "docs": "Checks if matchAny returns string matched by any of the expression.",
            "params": (
                (
                    (
                        "test",
                        "test",
                    ),
                    {},
                    (),
                    {},
                    "test",
                ),
                (
                    (
                        "Test",
                        "test",
                    ),
                    {},
                    (),
                    {},
                    "test",
                ),
                (
                    (
                        "test",
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    None,
                ),
                (
                    (
                        "*test",
                        "thisISmytest",
                    ),
                    {},
                    (),
                    {},
                    "thisISmytest",
                ),
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
            ),
        }
    },
    # 'fandango.functional.inCl': {
    #     '': {
    #         'docs': 'Checks if inCl returns matched strings.',
    #         'params': (
    #             (("test", "test",), {}, (), {}, "test"),
    #             (("Test", "test",), {}, (), {}, "test"),
    #             (("test", "thisISmytest",), {}, (), {}, None),
    #             (("*test", "thisISmytest",), {}, (), {}, "thisISmytest"),
    #             ((["Test", "my", "this"], "sys/tg_test/1"), {}, (), {}, None),
    #             ((["Test", "my", "this", "*tg"], "sys/tg_test/1"), {}, (), {},
    #              "sys/tg_test/1"),
    #             ((["Test", "my", "this", "*tg$"], "sys/tg_test/1"), {}, (), {}, None),
    #             ((), {"exprs": ["Test", "my", "this", "*tg"], "seq": "sys/tg_test/1"}, (),
    #              {}, "sys/tg_test/1"),
    #         )
    #     }
    # },
    "fandango.functional.searchCl": {
        "": {
            "method": "ci/tests/test_functional.py::test_serachCl",
        }
    },
    "fandango.functional.fbool": {
        "": {
            "docs": "Checks if fbool returns correct value (all(x) for sequence, "
            "cast bool otherwise.",
            "params": (
                (([2, True, 3, False],), {}, (), {}, False),
                (([2, True, 3, 7],), {}, (), {}, True),
                (([2, True, 3, {}],), {}, (), {}, False),
                ((0,), {}, (), {}, False),
                (([],), {}, (), {}, False),
                ((["test"],), {}, (), {}, True),
                (("",), {}, (), {}, False),
            ),
        }
    },
    "fandango.functional.notNone": {
        "": {
            "docs": "Checks if notNone returns arg if arg is not None, otherwise "
            "default.",
            "params": (
                ((7,), {}, (), {}, 7),
                ((["a", 2, False],), {}, (), {}, ["a", 2, False]),
                ((None,), {}, (), {}, None),
                (
                    (
                        7,
                        0,
                    ),
                    {},
                    (),
                    {},
                    7,
                ),
                (
                    (
                        ["a", 2, False],
                        0,
                    ),
                    {},
                    (),
                    {},
                    ["a", 2, False],
                ),
                (
                    (
                        None,
                        0,
                    ),
                    {},
                    (),
                    {},
                    0,
                ),
                ((7,), {"default": 0}, (), {}, 7),
                ((["a", 2, False],), {"default": 0}, (), {}, ["a", 2, False]),
                ((None,), {"default": 0}, (), {}, 0),
            ),
        }
    },
    "fandango.functional.isTrue": {
        "": {
            "docs": "Checks if fbool returns correct value (all(x) for sequence, "
            "cast bool otherwise.",
            "params": (
                # (([2, True, 3, False],), {}, (), {}, True),
                # ((7,), {}, (), {}, True),
                ((True,), {}, (), {}, True),
                ((False,), {}, (), {}, False),
                (("True",), {}, (), {}, True),
                (("False",), {}, (), {}, False),
                ((0,), {}, (), {}, False),
                (("0",), {}, (), {}, False),
                (("2",), {}, (), {}, True),
                (([],), {}, (), {}, False),
                ((None,), {}, (), {}, False),
            ),
        }
    },
    "fandango.functional.isNaN": {
        "": {
            "docs": "Checks if isNaN returns correct value",
            "params": (
                (("NaN",), {}, (), {}, True),
                ((" nan  ",), {}, (), {}, True),
                ((3,), {}, (), {}, False),
                (([],), {}, (), {}, False),
                # ((float("NaN"),), {}, (), {}, False),
            ),
        }
    },
    "fandango.functional.isNone": {
        "": {
            "docs": "Checks if isNone returns True when input argument is naive None "
            "type",
            "params": (
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
            ),
        }
    },
    "fandango.functional.isFalse": {
        "": {
            "docs": "Checks if isFalse returns True of input argument is naive bool, "
            "False otherwise",
            "params": (
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
            ),
        }
    },
    "fandango.functional.isBool": {
        "": {
            "docs": "Checks if isBool returns True if input argument is bool type or "
            "naive bool, False otherwise",
            "params": (
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
            ),
        }
    },
    "fandango.functional.isString": {
        "": {
            "docs": "Checks if isString returns True if input argument is string type, "
            "False otherwise",
            "params": (
                (("test",), {}, (), {}, True),
                (("",), {}, (), {}, True),
                ((u"sys*wąż",), {}, (), {}, True),
                ((False,), {}, (), {}, False),
                (("True",), {}, (), {}, True),
                (("  FalsE ",), {}, (), {}, True),
                ((" 0 ",), {}, (), {}, True),
                ((" NO ",), {}, (), {}, True),
                ((0,), {}, (), {}, False),
                (([],), {}, (), {}, False),
                ((None,), {}, (), {}, False),
                (("none",), {}, (), {}, True),
            ),
        }
    },
    "fandango.functional.isRegexp": {
        "": {
            "docs": "Checks if isRegexp returns True if strings seems to be regex and "
            "False otherwise",
            "params": (
                (("test",), {}, (), {}, False),
                (("test*",), {}, (), {}, True),
                ((u"sys*wąż",), {}, (), {}, True),
                ((u"syswąż",), {}, (), {}, False),
                ((u"sys/tg_test/1",), {}, (), {}, False),
                ((u"test*", "{\|"), {}, (), {}, False),
                ((u"\\test*", "{\|"), {}, (), {}, True),
                ((u"\test*", "{\|"), {}, (), {}, False),
            ),
        }
    },
    "fandango.functional.isNumber": {
        "": {
            "docs": "Checks if isNumber returns True if input argument is naive number, "
            "False otherwise",
            "params": (
                (("test",), {}, (), {}, False),
                ((3,), {}, (), {}, True),
                ((7.0,), {}, (), {}, True),
                (("0",), {}, (), {}, True),
                (("nan",), {}, (), {}, True),
                (("True",), {}, (), {}, False),
                (([],), {}, (), {}, False),
                (([3, 7],), {}, (), {}, False),
            ),
        }
    },
    "fandango.functional.isDate": {
        "": {"method": "ci/tests/test_functional.py::test_isDate"}
    },
    "fandango.functional.str2int": {
        "": {
            "docs": "Checks if str2int returns first integer found in the string",
            "params": (
                (("31",), {}, (), {}, 31),
                (("3.1",), {}, (), {}, 3),
                ((7.0,), {}, (), {}, None),
                ((None,), {}, (), {}, None),
                (("test",), {}, (), {}, None),
                (("test07test",), {}, (), {}, 7),
                (("2020-11-16 00:27:17",), {}, (), {}, 2020),
            ),
        }
    },
    "fandango.functional.str2float": {
        "": {
            "docs": "Checks if str2float returns first float found in the string",
            "params": (
                (("31",), {}, (), {}, 31),
                (("3.1",), {}, (), {}, 3.1),
                # ((7.0,), {}, (), {}, None),
                ((None,), {}, (), {}, None),
                (("test",), {}, (), {}, None),
                (("test07test",), {}, (), {}, 7),
                (("test07.5e-10test",), {}, (), {}, 7.5e-10),
                (("2020-11-16 00:27:17",), {}, (), {}, 2020),
            ),
        }
    },
    "fandango.functional.str2bool": {
        "": {
            "docs": "Checks if str2bool return True if string is not naive false and "
            "False otherwise",
            "params": (
                (("31",), {}, (), {}, True),
                (("true",), {}, (), {}, True),
                (("  Yes",), {}, (), {}, True),
                (("False",), {}, (), {}, False),
                ((" FALSE ",), {}, (), {}, False),
                (("0",), {}, (), {}, False),
                (("  None",), {}, (), {}, False),
                (("no",), {}, (), {}, False),
                (("NO  ",), {}, (), {}, False),
                # ((7.0,), {}, (), {}, True),
                # ((0,), {}, (), {}, False),
                # ((None,), {}, (), {}, None),
            ),
        }
    },
    "fandango.functional.str2bytes": {
        "": {
            "docs": "Checks if str2bool return True if string is not naive false and "
            "False otherwise",
            "params": (
                (("03",), {}, (), {}, [48, 51]),
                (("abba",), {}, (), {}, [97, 98, 98, 97]),
                (("test",), {}, (), {}, [116, 101, 115, 116]),
                ((u"wąż",), {}, (), {}, [119, 261, 380]),
                # ((u"wąż",), {}, (), {}, [119, 196, 133, 197, 188]),
                # ((7.0,), {}, (), {}, [55, 46, 48]),
                # ((0,), {}, (), {}, [48]),
                # ((None,), {}, (), {}, [78, 111, 110, 101]),
            ),
        }
    },
    "fandango.functional.str2type": {
        "": {
            "docs": "Checks if str2bool return True if string is not naive false and "
            "False otherwise",
            "params": (
                (("31",), {}, (), {}, 31),
                (("0o31",), {}, (), {}, 25),
                (("3.7",), {}, (), {}, 3.7),
                (("No",), {}, (), {}, False),
                (("TRUE",), {}, (), {}, True),
                (("1",), {}, (), {}, 1),
                ((None,), {}, (), {}, None),
                (("abba",), {}, (), {}, "abba"),
                ((u"wąż",), {}, (), {}, u"wąż"),
                (("3+5",), {}, (), {}, 8),
                (("[1, 2, 4, 3]",), {}, (), {}, [1, 2, 4, 3]),
                (("1 2 4 3",), {"use_eval": False}, (), {}, [1, 2, 4, 3]),
                # (("[1, 2, 4, 3]",), {"use_eval": False}, (), {}, [1, 2, 4, 3]),
                # ((u"wąż".encode("utf8"),), {}, (), {}, u"wąż"),
                ((7,), {}, (), {}, 7),
                ((7.3,), {}, (), {}, 7.3),
                (("2020-11-16 00:27:17",), {}, (), {}, "2020-11-16 00:27:17"),
            ),
        }
    },
    "fandango.functional.rtf2plain": {
        "": {
            "docs": "Checks if str2bool return True if string is not naive false and "
            "False otherwise",
            "params": (
                (
                    ("<html><title>this is a title</title></html>",),
                    {},
                    (),
                    {},
                    "this is a title",
                ),
                # (("abba",), {}, (), {}, [97, 98, 98, 97]),
                # (("test",), {}, (), {}, [116, 101, 115, 116]),
                # (("wąż",), {}, (), {}, [119, 196, 133, 197, 188]),
                # ((u"wąż",), {}, (), {}, [119, 196, 133, 197, 188]),
                # ((7.0,), {}, (), {}, [55, 46, 48]),
                # ((0,), {}, (), {}, [48]),
                # ((None,), {}, (), {}, [78, 111, 110, 101]),
            ),
        }
    },
}
