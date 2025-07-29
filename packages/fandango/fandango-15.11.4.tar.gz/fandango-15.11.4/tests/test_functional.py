# -*- coding: utf-8 -*-
from builtins import range
import datetime, os, time
from collections import namedtuple, OrderedDict

import pytest, pytz

import fandango


def test_first_iter():
    """Checks if the first element of the iterator is returned correctly."""
    params = (
        ((iter([8, 2, 7, 2]),), {}, (), {}, 8),
        (((y for y in [3, 2, 1, 5]),), {}, (), {}, 3),
    )
    for args, kwargs, init_args, init_kwargs, result in params:

        assert fandango.functional.first(*args, **kwargs) == result


def test_last_iter():
    """
    Checks if the last element of the iterator is returned correctly.
    """
    params = (
        ((iter([8, 3, 7, 2]),), {}, (), {}, 2),
        (((y for y in [3, 2, 1, 5]),), {}, (), {}, 5),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.last(*args, **kwargs) == result


# @pytest.mark.skip("djoin returns list but also changes input list")
def test_last_generator_max():
    """
    Checks if the last element of the generator is returned correctly when reaching MAX
    index.
    """
    params = (
        (((y for y in range(5)),), {"MAX": 10}, (), {}, 4),
        (((y for y in range(1000)),), {}, (), {}, 999),
        (((y for y in range(10)),), {"MAX": 10}, (), {}, 9),
        (((y for y in range(1001)),), {}, (), {}, 1000),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.last(*args, **kwargs) == result


def test_last_generator_overmax():
    """
    Checks if the last element of the generator is returned correctly when reaching MAX
    index.
    """
    params = (
        (((y for y in range(1001)),), {"MAX": 1000}, (), {}, ()),
        (((y for y in range(11)),), {"MAX": 10}, (), {}, ()),
    )
    for args, kwargs, init_args, init_kwargs, result in params:

        with pytest.raises(IndexError):
            fandango.functional.last(*args, **kwargs)


def test_avg_iterators():
    """Checks if function returns average value from iterators including generators"""
    params = (
        (((y for y in range(10)),), {}, (), {}, 4.5),
        ((iter([5.3, 2.1, 3.3, 8.2]),), {}, (), {}, 4.725),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.avg(*args, **kwargs) == result


def test_randomize():
    """
    Checks if returned randomized list contains the same elements as input list.
    """
    params = (
        ((list(range(100)),), {}, (), {}, None),
        (([3.0, "a", "b", {"c": 2}],), {}, (), {}, None),
    )

    def helper_compar_fun(list1, list2):
        """
        Compare two lists and returns True if they contain the same elements,
        otherwise False (works with not hashable)
        """
        list_compared = list(list2)
        for element in list1:
            try:
                list_compared.remove(element)
            except ValueError:
                return False
        return not list_compared

    for args, kwargs, init_args, init_kwargs, result in params:
        randomized_list = fandango.functional.randomize(*args, **kwargs)
        assert helper_compar_fun(args[0], randomized_list)


def test_randpop():
    """
    Checks if list after poping one random elements has correct length
    and old list contains poped element.
    """
    params = (
        ((list(range(100)),), {}, (), {}, None),
        (([3.0, "a", "b", {"c": 2}],), {}, (), {}, None),
    )

    for args, kwargs, init_args, init_kwargs, result in params:
        list_input_length = len(*args)
        list_input = list(args[0])
        random_elem = fandango.functional.randpop(*args, **kwargs)
        assert random_elem in list_input
        assert len(*args) == list_input_length - 1


def test_join_generator():
    """
    Checks if joined generators create list containing all elements
    """
    params = (
        (
            (
                (y for y in [3, 2, 1]),
                (y for y in [8, 7]),
            ),
            {},
            (),
            {},
            [3, 2, 1, 8, 7],
        ),
        (((y for y in [3, 2, 1]),), {}, (), {}, [3, 2, 1]),
    )

    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.join(*args, **kwargs) == result


# @pytest.mark.skip("djoin returns list but also changes input list")
def test_djoin_unchanged_input():
    """
    Checks if djoin doesn't change input list or dict
    """
    params = (
        (({"a": 1, "b": 2}, [4, 5, 6]), {}, (), {}, ()),
        (([4, 5, 6], {"a": 1, "b": 2}), {}, (), {}, ()),
        (({"a": 1, "b": 2}, {"c": 4, "d": 5}), {}, (), {}, ()),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        lists_before = [list(elem) for elem in args if isinstance(elem, list)]
        dicts_before = [dict(elem) for elem in args if isinstance(elem, dict)]
        fandango.functional.djoin(*args, **kwargs) == result
        lists_after = [elem for elem in args if isinstance(elem, list)]
        dicts_after = [elem for elem in args if isinstance(elem, dict)]
        assert lists_before == lists_after and dicts_before == dicts_after


def test_kmap():
    """
    Checks if items are properly maped to input function and optionally sorted.
    """
    params = (
        (
            [str.lower, "BCA"],
            {},
            (),
            {},
            [
                ("A", "a"),
                (
                    "B",
                    "b",
                ),
                ("C", "c"),
            ],
        ),
        (
            [str.lower, "BCA"],
            {
                "values": "XYZ",
            },
            (),
            {},
            [
                ("A", "z"),
                (
                    "B",
                    "x",
                ),
                ("C", "y"),
            ],
        ),
        (
            [str.lower, "BCA"],
            {"sort": False},
            (),
            {},
            [
                (
                    "B",
                    "b",
                ),
                ("C", "c"),
                ("A", "a"),
            ],
        ),
        (
            [str.lower, "BCA"],
            {"values": "XYZ", "sort": False},
            (),
            {},
            [
                (
                    "B",
                    "x",
                ),
                ("C", "y"),
                ("A", "z"),
            ],
        ),
    )

    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.kmap(*args, **kwargs) == result


def test_setitem():
    """
    Checks if item is properly added to the dictionary.
    """
    params = (
        ([{"a": 1, "b": 2}, "c", 3], {}, (), {}, {"a": 1, "b": 2, "c": 3}),
        ([{"a": 1, "b": 2}, "b", 3], {}, (), {}, {"a": 1, "b": 3}),
    )

    for args, kwargs, init_args, init_kwargs, result in params:
        fandango.functional.setitem(*args, **kwargs)
        assert args[0] == result


def test_matchCl():
    """
    Checks if matchCl correctly finds match.
    """
    params = (
        (["sys*", "sys/TG_TEST/1"], {}, (), {}, "sys/tg_test/1"),
        (["sys*test*", "sys/TG_TEST/1"], {}, (), {}, "sys/tg_test/1"),
        (["sys*test*", "sys/TG_TEST/1"], {"extend": True}, (), {}, "sys/tg_test/1"),
        (["sys*test", "sys/TG_TEST/1"], {}, (), {}, "sys/tg_test"),
        (["sys*test", "sys/TG_TEST/1"], {"terminate": True}, (), {}, None),
        (["sys*test*1", "sys/TG_TEST/1"], {"terminate": True}, (), {}, "sys/tg_test/1"),
        (["*test*&*sys*&!*tango*", "myTESTissys"], {"extend": True}, (), {}, True),
        (
            ["*test*&*sys*&!*tango*", "myTESTissysTANGO"],
            {"extend": True},
            (),
            {},
            False,
        ),
        (["*test*&*sys*&~*tango*", "myTESTissys"], {"extend": True}, (), {}, True),
        (
            ["*test*&*sys*&~*tango*", "myTESTissystango"],
            {"extend": True},
            (),
            {},
            False,
        ),
        (
            ["tango://*:\d+/*/*/*", "tango://example.com:10000/sys/TG_TEST/1"],
            {},
            (),
            {},
            "tango://example.com:10000/sys/tg_test/1",
        ),
        (
            ["tango://*:[0-9]+/*/*/*", "tango://tango.com:10000/sys/TG_TEST/1"],
            {},
            (),
            {},
            "tango://tango.com:10000/sys/tg_test/1",
        ),
        (
            ["tango://*:[0-9]+/*/*/*", "tango://tango.com:10000/sys/TG_TEST"],
            {},
            (),
            {},
            None,
        ),
        ([u"sys*wąż", u"sys/tg_test/wąż"], {}, (), {}, u"sys/tg_test/wąż"),
        (["^sys*test*", "sys/tg_test/1"], {}, (), {}, "sys/tg_test/1"),
        (["*test", "sys/tg_test/1"], {}, (), {}, "sys/tg_test"),
        (["test*", "sys/tg_test/1"], {}, (), {}, None),
        (["test", "sys/tg_test/1"], {}, (), {}, None),
        (["^test*", "sys/tg_test/1"], {}, (), {}, None),
        (["sys*test/1$", "sys/tg_test/1"], {}, (), {}, "sys/tg_test/1"),
        (["sys*test/$", "sys/tg_test/1"], {}, (), {}, None),
        (
            ["^sys*test/1", "sys/tg_test/1"],
            {"terminate": True},
            (),
            {},
            "sys/tg_test/1",
        ),
        (["^sys*test/", "sys/tg_test/1"], {"terminate": True}, (), {}, None),
        (["^sys*test/1$", "sys/tg_test/1"], {}, (), {}, "sys/tg_test/1"),
    )

    for args, kwargs, init_args, init_kwargs, result in params:
        if result in [True, False, None]:
            assert fandango.functional.matchCl(*args, **kwargs) == result
        else:
            assert fandango.functional.matchCl(*args, **kwargs).group() == result


def test_searchCl():
    """
    Checks if searchCl correctly finds search.
    """
    params = (
        (["sys*", "sys/TG_TEST/1"], {}, (), {}, "sys/tg_test/1"),
        (["sys*test*", "sys/TG_TEST/1"], {}, (), {}, "sys/tg_test/1"),
        (["sys*test*", "sys/TG_TEST/1"], {"extend": True}, (), {}, "sys/tg_test/1"),
        (["sys*test", "sys/TG_TEST/1"], {}, (), {}, "sys/tg_test"),
        (["sys*test", "sys/TG_TEST/1"], {"terminate": True}, (), {}, None),
        (["sys*test*1", "sys/TG_TEST/1"], {"terminate": True}, (), {}, "sys/tg_test/1"),
        (["*test*&*sys*&!*tango*", "myTESTissys"], {"extend": True}, (), {}, True),
        (
            ["*test*&*sys*&!*tango*", "myTESTissysTANGO"],
            {"extend": True},
            (),
            {},
            False,
        ),
        (["*test*&*sys*&~*tango*", "myTESTissys"], {"extend": True}, (), {}, True),
        (
            ["*test*&*sys*&~*tango*", "myTESTissystango"],
            {"extend": True},
            (),
            {},
            False,
        ),
        (
            ["tango://*:\d+/*/*/*", "tango://example.com:10000/sys/TG_TEST/1"],
            {},
            (),
            {},
            "tango://example.com:10000/sys/tg_test/1",
        ),
        (
            ["tango://*:[0-9]+/*/*/*", "tango://tango.com:10000/sys/TG_TEST/1"],
            {},
            (),
            {},
            "tango://tango.com:10000/sys/tg_test/1",
        ),
        (
            ["tango://*:[0-9]+/*/*/*", "tango://tango.com:10000/sys/TG_TEST"],
            {},
            (),
            {},
            None,
        ),
        ([u"sys*wąż", u"sys/tg_test/wąż"], {}, (), {}, u"sys/tg_test/wąż"),
        (["^sys*test*", "sys/tg_test/1"], {}, (), {}, "sys/tg_test/1"),
        (["*test", "sys/tg_test/1"], {}, (), {}, "sys/tg_test"),
        (["test*", "sys/tg_test/1"], {}, (), {}, "test/1"),
        (["test", "sys/tg_test/1"], {}, (), {}, "test"),
        (["^test*", "sys/tg_test/1"], {}, (), {}, None),
        (["sys*test/1$", "sys/tg_test/1"], {}, (), {}, "sys/tg_test/1"),
        (["sys*test/$", "sys/tg_test/1"], {}, (), {}, None),
        (
            ["^sys*test/1", "sys/tg_test/1"],
            {"terminate": True},
            (),
            {},
            "sys/tg_test/1",
        ),
        (["^sys*test/", "sys/tg_test/1"], {"terminate": True}, (), {}, None),
        (["^sys*test/1$", "sys/tg_test/1"], {}, (), {}, "sys/tg_test/1"),
    )

    for args, kwargs, init_args, init_kwargs, result in params:
        if result in [True, False, None]:
            assert fandango.functional.searchCl(*args, **kwargs) == result
        else:
            assert fandango.functional.searchCl(*args, **kwargs).group() == result


def test_set_default_time_format():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (
        (["%Y-%m-%d %H:%M:%S"], {}, (), {}, ()),
        (["%Y-%m-%dT%H:%M:%S"], {}, (), {}, ()),
        (["%Y/%m/%d %H %M %S"], {}, (), {}, ()),
    )
    old_time_format = fandango.functional.DEFAULT_TIME_FORMAT
    for args, kwargs, init_args, init_kwargs, result in params:
        fandango.functional.set_default_time_format(*args, **kwargs)
        assert args[0] == fandango.functional.DEFAULT_TIME_FORMAT
    fandango.functional.DEFAULT_TIME_FORMAT = old_time_format


@pytest.mark.freeze_time("2020-11-16 00:27:17")
def test_now():
    """
    Checks if now returns proper timestamp according to current time.
    """
    params = (((), {}, (), {}, (1605486437.0)),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.now(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-11-16 00:27:17")
def test_time2tuple():
    """
    Checks if time2tuple returns date properly.
    """
    params = (
        ((), {}, (), {}, (2020, 11, 16, 1, 27, 17, 0, 321, 0)),
        ((), {"utc": True}, (), {}, (2020, 11, 16, 0, 27, 17, 0, 321, 0)),
        ((), {"epoch": 1596109800}, (), {}, (2020, 7, 30, 13, 50, 00, 3, 212, 1)),
        (
            (),
            {"epoch": 1596109800, "utc": True},
            (),
            {},
            (2020, 7, 30, 11, 50, 00, 3, 212, 0),
        ),
        ((), {"epoch": -3600}, (), {}, (2020, 11, 16, 2, 27, 17, 0, 321, 0)),
        (
            (),
            {"epoch": -3600, "utc": True},
            (),
            {},
            (2020, 11, 16, 1, 27, 17, 0, 321, 0),
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2tuple(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00")
def test_time2tuple_dst():
    """
    Checks if time2tuple returns date properly in case of date during summer (dst)
    """
    params = (
        ((), {}, (), {}, (2020, 7, 30, 13, 50, 00, 3, 212, 1)),
        ((), {"utc": True}, (), {}, (2020, 7, 30, 11, 50, 00, 3, 212, 0)),
        ((), {"epoch": 1605486437}, (), {}, (2020, 11, 16, 1, 27, 17, 0, 321, 0)),
        (
            (),
            {"epoch": 1605486437, "utc": True},
            (),
            {},
            (2020, 11, 16, 0, 27, 17, 0, 321, 0),
        ),
        ((), {"epoch": -3600}, (), {}, (2020, 7, 30, 14, 50, 00, 3, 212, 1)),
        (
            (),
            {"epoch": -3600, "utc": True},
            (),
            {},
            (2020, 7, 30, 12, 50, 00, 3, 212, 0),
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2tuple(*args, **kwargs) == result


def test_tuple2time():
    """
    Checks if tuple2time returns timestamp properly for given dates (dst is also taken
    into account).
    """
    params = (
        (((2020, 7, 30, 13, 50, 00, 3, 212, 1),), {}, (), {}, 1596109800.0),
        (((2020, 7, 30, 12, 50, 00, 3, 212, 0),), {}, (), {}, 1596109800.0),
        (((2020, 7, 30, 13, 50, 00, 3, 212, -1),), {}, (), {}, 1596109800.0),
        (((2020, 11, 16, 2, 27, 17, 0, 321, 1),), {}, (), {}, 1605486437.0),
        (((2020, 11, 16, 1, 27, 17, 0, 321, 0),), {}, (), {}, 1605486437.0),
        (((2020, 11, 16, 1, 27, 17, 0, 321, -1),), {}, (), {}, 1605486437.0),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.tuple2time(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 13:50:00.01")
def test_date2time():
    """
    Checks if date2time returns timestamp properly.
    """
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    params = (
        ((datetime.datetime.now(),), {}, (), {}, 1596109800.01),
        ((datetime.datetime.utcnow(),), {}, (), {}, 1596109800.01),
        ((datetime.datetime.now(tz=pytz.utc),), {}, (), {}, 1596113400.01),
        (
            (datetime.datetime.fromtimestamp(1596109800.01, tz=pytz.utc),),
            {},
            (),
            {},
            1596106200.01,
        ),
        ((datetime.datetime.fromtimestamp(1596109800.01),), {}, (), {}, 1596102600.01),
        ((datetime.datetime.now(),), {"us": False}, (), {}, 1596109800),
        ((datetime.datetime.utcnow(),), {"us": False}, (), {}, 1596109800),
        ((datetime.datetime.now(tz=pytz.utc),), {"us": False}, (), {}, 1596113400),
        (
            (datetime.datetime.fromtimestamp(1596109800, tz=pytz.utc),),
            {"us": False},
            (),
            {},
            1596106200,
        ),
        (
            (datetime.datetime.fromtimestamp(1596109800),),
            {"us": False},
            (),
            {},
            1596102600,
        ),
        ((datetime.timedelta(days=1),), {}, (), {}, 60 * 60 * 24),
        ((datetime.timedelta(seconds=1.01),), {}, (), {}, 1.01),
        ((datetime.timedelta(weeks=1, seconds=1.01),), {}, (), {}, 604801.01),
        ((datetime.timedelta(seconds=1.01),), {"us": False}, (), {}, 1.01),
        (
            (datetime.timedelta(weeks=1, seconds=1.01),),
            {"us": False},
            (),
            {},
            604801.01,
        ),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.date2time(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 13:50:00.01")
def test_date2str():
    """
    Checks if date2str returns string with date properly.
    """
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    params = (
        ((datetime.datetime.now(),), {}, (), {}, "2020-07-30 13:50:00"),
        ((datetime.datetime.utcnow(),), {}, (), {}, "2020-07-30 13:50:00"),
        ((datetime.datetime.now(tz=pytz.utc),), {}, (), {}, "2020-07-30 14:50:00"),
        (
            (datetime.datetime.fromtimestamp(1596109800.01, tz=pytz.utc),),
            {},
            (),
            {},
            "2020-07-30 12:50:00",
        ),
        (
            (datetime.datetime.fromtimestamp(1596109800.01),),
            {},
            (),
            {},
            "2020-07-30 11:50:00",
        ),
        (
            (datetime.datetime.fromtimestamp(1605486437.01, tz=pytz.utc),),
            {},
            (),
            {},
            "2020-11-16 00:27:17",
        ),
        (
            (datetime.datetime.fromtimestamp(1605486437.01),),
            {},
            (),
            {},
            "2020-11-16 00:27:17",
        ),
        (
            (datetime.datetime.now(),),
            {"us": True},
            (),
            {},
            "2020-07-30 13:50:00.010000",
        ),
        (
            (datetime.datetime.utcnow(),),
            {"us": True},
            (),
            {},
            "2020-07-30 13:50:00.010000",
        ),
        (
            (datetime.datetime.now(tz=pytz.utc),),
            {"us": True},
            (),
            {},
            "2020-07-30 14:50:00.010000",
        ),
        (
            (datetime.datetime.fromtimestamp(1596109800, tz=pytz.utc),),
            {"us": True},
            (),
            {},
            "2020-07-30 12:50:00",
        ),
        (
            (datetime.datetime.fromtimestamp(1596109800),),
            {"us": True},
            (),
            {},
            "2020-07-30 11:50:00",
        ),
        ((datetime.timedelta(days=1),), {}, (), {}, "1970-01-02 01:00:00"),
        ((datetime.timedelta(seconds=1.01),), {}, (), {}, "1970-01-01 01:00:01"),
        (
            (datetime.timedelta(weeks=1, seconds=1.01),),
            {},
            (),
            {},
            "1970-01-08 01:00:01",
        ),
        (
            (datetime.timedelta(seconds=1.01),),
            {"us": True},
            (),
            {},
            "1970-01-01 01:00:01",
        ),
        (
            (datetime.timedelta(weeks=1, seconds=1.01),),
            {"us": True},
            (),
            {},
            "1970-01-08 01:00:01",
        ),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.date2str(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00")
def test_time2date():
    """
    Checks if time2date returns proper when epoch is not given, is given positive and
    is given negative.
    """
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    params = (
        ((), {}, (), {}, datetime.datetime.now()),
        ((1596109800,), {}, (), {}, datetime.datetime.now()),
        ((1596109800,), {}, (), {}, datetime.datetime.fromtimestamp(1596109800)),
        ((-3600,), {}, (), {}, datetime.datetime.fromtimestamp(1596113400)),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2date(*args, **kwargs) == result
        # assert fandango.functional.time2date(*args, **kwargs).timetuple() == result


@pytest.mark.freeze_time("2020-11-16 00:27:17")
def test_utcdiff_warsaw():
    """
    Check if time difference in seconds between local time and utc is right for Warsaw
    timezone.
    """
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    params = (((), {}, (), {}, 3600),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.utcdiff(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-11-16 00:27:17")
def test_utcdiff_moscow():
    """
    Check if time difference in seconds between local time and utc is right for Moscow
    timezone.
    """
    os.environ["TZ"] = "Europe/Moscow"
    time.tzset()
    params = (((), {}, (), {}, 10800),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.utcdiff(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00")
def test_utcdiff_warsaw_dst():
    """
    Check if time difference in seconds between local time and utc is right for Warsaw
    timezone during summer (dst).
    """
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    params = (((), {}, (), {}, 7200),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.utcdiff(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00")
def test_utcdiff_moscow_dst():
    """
    Check if time difference in seconds between local time and utc is right for Moscow
    timezone during summer (dst).
    """
    os.environ["TZ"] = "Europe/Moscow"
    time.tzset()
    params = (((), {}, (), {}, 10800),)
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.utcdiff(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00.01")
def test_time2str_epoch_none():
    """
    Checks if time2str returns proper string when epoch is not given (should use actual time).
    """
    params = (
        ((), {}, (), {}, "2020-07-30 13:50:00"),
        ((), {"cad": "%Y/%m/%d %H/%M/%S"}, (), {}, "2020/07/30 13/50/00"),
        ((), {"us": True}, (), {}, "2020-07-30 13:50:00.009999"),
        ((), {"bt": False}, (), {}, "2020-07-30 13:50:00"),
        ((), {"utc": True}, (), {}, "2020-07-30 11:50:00"),
        ((), {"iso": True}, (), {}, "2020-07-30T13:50:00"),
        ((), {"cad": "%Y/%m/%d %H/%M/%S", "iso": True}, (), {}, "2020/07/30T13/50/00"),
        ((), {"cad": "%Y/%m/%d-%H/%M/%S", "iso": True}, (), {}, "2020/07/30-13/50/00"),
        (
            (),
            {"us": True, "utc": True, "iso": True},
            (),
            {},
            "2020-07-30T11:50:00.009999",
        ),
        (
            (),
            {"cad": "%Y/%m/%d %H/%M/%S", "us": True, "utc": True, "iso": True},
            (),
            {},
            "2020/07/30T11/50/00.009999",
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2str(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-11-16 00:27:17.01")
def test_time2str_epoch_pos():
    """
    Checks if time2str returns proper string when epoch is positive.
    """
    params = (
        ((1605486437.01,), {}, (), {}, "2020-11-16 01:27:17"),
        ((1605486437.01,), {"cad": "%Y/%m/%d %H/%M/%S"}, (), {}, "2020/11/16 01/27/17"),
        ((1605486437.01,), {"us": True}, (), {}, "2020-11-16 01:27:17.009999"),
        ((1605486437.01,), {"bt": False}, (), {}, "2020-11-16 01:27:17"),
        ((1605486437.01,), {"utc": True}, (), {}, "2020-11-16 00:27:17"),
        ((1605486437.01,), {"iso": True}, (), {}, "2020-11-16T01:27:17"),
        (
            (1605486437.01,),
            {"cad": "%Y/%m/%d %H/%M/%S", "iso": True},
            (),
            {},
            "2020/11/16T01/27/17",
        ),
        (
            (1605486437.01,),
            {"cad": "%Y/%m/%d-%H/%M/%S", "iso": True},
            (),
            {},
            "2020/11/16-01/27/17",
        ),
        (
            (1605486437.01,),
            {"us": True, "utc": True, "iso": True},
            (),
            {},
            "2020-11-16T00:27:17.009999",
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2str(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00.01")
def test_time2str_epoch_neg():
    """
    Checks if time2str returns proper string when epoch is negative.
    """
    params = (
        ((-3600.02,), {}, (), {}, "2020-07-30 12:49:59"),
        ((-3600.02,), {"cad": "%Y/%m/%d %H/%M/%S"}, (), {}, "2020/07/30 12/49/59"),
        ((-3600.02,), {"us": True}, (), {}, "2020-07-30 12:49:59.990000"),
        ((-3600.02,), {"bt": False}, (), {}, "2020-07-30 14:50:00"),  # ??
        ((-3600.02,), {"utc": True}, (), {}, "2020-07-30 10:49:59"),
        ((-3600.02,), {"iso": True}, (), {}, "2020-07-30T12:49:59"),
        (
            (-3600.02,),
            {"cad": "%Y/%m/%d %H/%M/%S", "iso": True},
            (),
            {},
            "2020/07/30T12/49/59",
        ),
        (
            (-3600.02,),
            {"cad": "%Y/%m/%d-%H/%M/%S", "iso": True},
            (),
            {},
            "2020/07/30-12/49/59",
        ),
        (
            (-3600.02,),
            {"us": True, "utc": True, "iso": True},
            (),
            {},
            "2020-07-30T10:49:59.990000",
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2str(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00.01")
def test_str2time_seq_now():
    """
    Checks if str2time returns proper timestamp (actual) when no arguments are given.
    """
    params = (
        ((), {}, (), {}, 1596109800.01),
        (("NOW",), {}, (), {}, 1596109800.01),
        (("3600",), {}, (), {}, 3600),
        (("1h",), {}, (), {}, 3600),
        (("-1h",), {}, (), {}, -3600),
        # (("1h 30m",), {}, (), {}, 3600),
        # (("NOW-3600",), {}, (), {}, -3600),
        # (("-1h",), {"relative": True}, (), {}, -3600),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2time(*args, **kwargs) == result


def test_str2time_seq():
    """
    Checks if str2time returns proper timestamps according to sequence given.
    """
    params = (
        (("2020-07-30 12:49:59",), {}, (), {}, 1596106199.0),
        (("2020/07/30 12:49:59",), {}, (), {}, 1596106199.0),
        (("30/07/2020",), {}, (), {}, 1596060000.0),
        (("2020-07-30 12:49:59.990000",), {}, (), {}, 1596106199.99),
        (("2020-07-30 14:50:00",), {"throw": False}, (), {}, 1596113400.0),
        (("2020/07/30 14/50/00",), {"throw": False}, (), {}, None),
        (("2020-07-30 10:49:59",), {"relative": True}, (), {}, 1596098999.0),
        (("2020-07-30T12:49:59",), {}, (), {}, 1596106199.0),
        (
            ("2020-07-30T10:49:59.990000",),
            {"throw": False, "relative": True},
            (),
            {},
            1596098999.99,
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2time(*args, **kwargs) == result


def test_str2time_cad():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (
        (("2020/07/30 12/49/59",), {"cad": "%Y/%m/%d %H/%M/%S"}, (), {}, 1596106199.0),
        (("2020-07-30 12:49:59.990000",), {}, (), {}, 1596106199.99),
        (
            ("2020/07/30 14/50/00",),
            {"cad": "%Y/%m/%d %H/%M/%S", "throw": False},
            (),
            {},
            1596113400.0,
        ),
        (
            ("2020-07-30 14:50:00",),
            {"cad": "%Y/%m/%d %H/%M/%S", "throw": False},
            (),
            {},
            None,
        ),
        (("2020-07-30 10:49:59",), {"relative": True}, (), {}, 1596098999.0),
        (("2020-07-30T12:49:59",), {}, (), {}, 1596106199.0),
        (
            ("2020-07-30T10:49:59.990000",),
            {"throw": False, "relative": True},
            (),
            {},
            1596098999.99,
        ),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.str2time(*args, **kwargs) == result


def test_str2time_raise():
    """
    Checks if str2time raises error properly when wrong arguments are given
    """
    params = (
        (("asdf",), {}, (), {}, ()),
        ((100,), {}, (), {}, ()),
        (("2020-07-30 14:50:00",), {"cad": "%Y/%m/%d %H/%M/%S"}, (), {}, ()),
        (("2020-07-",), {"relative": True}, (), {}, ()),
        (("2020-0730T10:49:59.990000",), {"relative": True}, (), {}, ()),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        with pytest.raises(Exception, match="PARAMS_ERROR"):
            fandango.functional.str2time(*args, **kwargs)


@pytest.mark.freeze_time("2020-07-30 13:50:00")
def test_time2gmt():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (
        # ((), {}, (), {}, 1596109800),
        ((1605486437,), {}, (), {}, 1605482837),
        ((-3600,), {}, (), {}, -7200),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.time2gmt(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-11-16 00:27:17")
def test_timezone_warsaw():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (((), {}, (), {}, 1),)
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.timezone(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 13:50:00")
def test_timezone_warsaw_dst():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (
        # ((), {}, (), {}, 2),
    )
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.timezone(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-11-16 00:27:17")
def test_timezone_moscow():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (((), {}, (), {}, 3),)
    os.environ["TZ"] = "Europe/Moscow"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.timezone(*args, **kwargs) == result


@pytest.mark.freeze_time("2020-07-30 11:50:00.01")
def test_timezone_moscow_dst():
    """
    Checks if default format, which is global variable, is set properly.
    """
    params = (((), {}, (), {}, 3),)
    os.environ["TZ"] = "Europe/Moscow"
    time.tzset()
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.timezone(*args, **kwargs) == result


def test_ctime2time():
    """
    Checks if default format, which is global variable, is set properly.
    """
    TimeStruct = namedtuple("TimeStruct", "tv_sec tv_usec")
    time_struct = TimeStruct(100, 50)
    params = (
        ((time_struct,), {}, (), {}, 100.00005),
        ((0,), {}, (), {}, -1),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.ctime2time(*args, **kwargs) == result


def test_isNaN_float():
    """
    Checks if isNaN returns correct value for special floats (nan and inf).
    """
    params = (
        ((float("NaN"),), {}, (), {}, True),
        ((float("inf"),), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isNaN(*args, **kwargs) == result


def test_isDate():
    """
    Checks if isDate returns True if input argument is a date, False otherwise.
    """
    os.environ["TZ"] = "Europe/Warsaw"
    time.tzset()
    params = (
        # (("2020-11-16 00:27:17",), {}, (), {}, True),
        (("1970-01-01 1:0:0",), {}, (), {}, True),
        (("test",), {}, (), {}, False),
        ((7.0,), {}, (), {}, False),
        (("0",), {}, (), {}, True),
        (("nan",), {}, (), {}, False),
        (("True",), {}, (), {}, False),
        (([],), {}, (), {}, False),
        (([3, 7],), {}, (), {}, False),
        # ((), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isDate(*args, **kwargs) == result


def test_isGenerator():
    """
    Checks if isGenerator returns True if input argument is generator, False otherwise.
    """
    params = (
        (((y for y in range(10)),), {}, (), {}, True),
        ((iter([5.3, 2.1, 3, 8.2]),), {}, (), {}, False),
        (([5, 2.1, 3, 8.2],), {}, (), {}, False),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
        ((False,), {}, (), {}, False),
        (("string",), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isGenerator(*args, **kwargs) == result


def test_isSequence():
    """
    Checks if isSequence returns True for input argument if it is considered as list,
    set, tuple and by default generator, otherwise False.
    """
    params = (
        ((None,), {}, (), {}, False),
        ((False,), {}, (), {}, False),
        (("string",), {}, (), {}, False),
        (([],), {}, (), {}, True),
        (([5, 2.1, 3, 8.2],), {}, (), {}, True),
        (({5, 2.1, 3, 8.2},), {}, (), {}, True),
        (((5, 2.1, 3, 8.2),), {}, (), {}, True),
        (({"a": 1, "b": 3},), {}, (), {}, False),
        ((OrderedDict([(4, 3), (1, 2)]),), {}, (), {}, False),
        (((y for y in range(10)),), {}, (), {}, True),
        (((y for y in range(10)), False), {}, (), {}, False),
        (((y for y in range(10)),), {'iterators': True}, (), {}, True),
        ((iter([5, 2.1, 3, 8.2]),), {}, (), {}, True),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isSequence(*args, **kwargs) == result


def test_isDictionary():
    """
    Checks if isDictionary returns True for input argument if it is considered as
    dictionary.
    """
    params = (
        (((y for y in range(10)),), {}, (), {}, False),
        ((iter([5, 2.1, 3, 8.2]),), {}, (), {}, False),
        (([5, 2.1, 3, 8.2],), {}, (), {}, False),
        (({5, 2.1, 3, 8.2},), {}, (), {}, False),
        (((5, 2.1, 3, 8.2),), {}, (), {}, False),
        (({"a": 1, "b": 3},), {}, (), {}, True),
        ((OrderedDict([(4, 3), (1, 2)]),), {}, (), {}, True),
        ((([5], 2.1, 3, 8.2),), {}, (), {}, True),
        ((([5], [2.1], [3], [8.2]),), {}, (), {}, True),
        ((([[5]], [2.1], [3], [8.2]),), {}, (), {}, False),
        ((([5], [2.1], [[3]], [8.2]),), {}, (), {}, True),
        (((["str"], [2.1], [3], [8.2]),), {}, (), {}, True),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
        ((False,), {}, (), {}, False),
        (("string", True), {}, (), {}, False),
        (({"a": 1, "b": 3}, True), {}, (), {}, True),
        ((OrderedDict([(4, 3), (1, 2)]), True), {}, (), {}, True),
        ((([5], 2.1, 3, 8.2), True), {}, (), {}, False),
        ((([5], [2.1], [3], [8.2]), True), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isDictionary(*args, **kwargs) == result


def test_isMapping():
    """
    Checks if isMaping returns True for input argument if it is considered as
    dictionary, if strict is False (default) it also consider nested lists but first
    element cannot be iterable.
    """
    params = (
        (((y for y in range(10)),), {}, (), {}, False),
        ((iter([5, 2.1, 3, 8.2]),), {}, (), {}, False),
        (([5, 2.1, 3, 8.2],), {}, (), {}, False),
        (({5, 2.1, 3, 8.2},), {}, (), {}, False),
        (((5, 2.1, 3, 8.2),), {}, (), {}, False),
        (({"a": 1, "b": 3},), {}, (), {}, True),
        ((OrderedDict([(4, 3), (1, 2)]),), {}, (), {}, True),
        ((([5], 2.1, 3, 8.2),), {}, (), {}, True),
        ((([5], [2.1], [3], [8.2]),), {}, (), {}, True),
        ((([[5]], [2.1], [3], [8.2]),), {}, (), {}, False),
        ((([5], [2.1], [[3]], [8.2]),), {}, (), {}, True),
        (((["str"], [2.1], [3], [8.2]),), {}, (), {}, True),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
        ((False,), {}, (), {}, False),
        (("string", True), {}, (), {}, False),
        (({"a": 1, "b": 3}, True), {}, (), {}, True),
        ((OrderedDict([(4, 3), (1, 2)]), True), {}, (), {}, True),
        ((([5], 2.1, 3, 8.2), True), {}, (), {}, False),
        ((([5], [2.1], [3], [8.2]), True), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isMapping(*args, **kwargs) == result


def test_isHashable():
    """
    Checks if isHashable returns True for input argument if it is hashable
    """
    params = (
        (((y for y in range(10)),), {}, (), {}, True),
        ((iter([5, 2.1, 3, 8.2]),), {}, (), {}, True),
        (([5, 2.1, 3, 8.2],), {}, (), {}, False),
        (({5, 2.1, 3, 8.2},), {}, (), {}, False),
        (((5, 2.1, 3, 8.2),), {}, (), {}, True),
        (((5, [2.1], 3, 8.2),), {}, (), {}, False),
        (((5, (2.1), 3, 8.2),), {}, (), {}, True),
        (((5, ([2.1]), 3, 8.2),), {}, (), {}, False),
        (({"a": 1, "b": 3},), {}, (), {}, False),
        ((OrderedDict([(4, 3), (1, 2)]),), {}, (), {}, False),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, True),
        ((False,), {}, (), {}, True),
        (("string",), {}, (), {}, True),
        ((3,), {}, (), {}, True),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isHashable(*args, **kwargs) == result


def test_isIterable():
    """
    Checks if isIterable returns True for input argument if it is iterable
    """
    params = (
        (((y for y in range(10)),), {}, (), {}, True),
        ((iter([5, 2.1, 3, 8.2]),), {}, (), {}, True),
        (([5, 2.1, 3, 8.2],), {}, (), {}, True),
        (({5, 2.1, 3, 8.2},), {}, (), {}, True),
        (((5, 2.1, 3, 8.2),), {}, (), {}, True),
        (({"a": 1, "b": 3},), {}, (), {}, True),
        ((OrderedDict([(4, 3), (1, 2)]),), {}, (), {}, True),
        (([],), {}, (), {}, True),
        ((None,), {}, (), {}, False),
        ((False,), {}, (), {}, False),
        (("string",), {}, (), {}, False),
        ((3,), {}, (), {}, False),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isIterable(*args, **kwargs) == result


def test_isNested():
    """
    Checks if isNested returns True for input argument if it is nested
    """
    params = (
        # (((y for y in range (10)),), {}, (), {}, False),
        # ((iter([5, 2.1, 3, 8.2]),), {}, (), {}, False),
        # (([(y for y in range (10))],), {}, (), {}, False),
        ((3,), {}, (), {}, False),
        (([],), {}, (), {}, False),
        ((None,), {}, (), {}, False),
        ((False,), {}, (), {}, False),
        (("string",), {}, (), {}, False),
        (([5, 2.1, 3], True), {}, (), {}, False),
        (([[5]],), {}, (), {}, True),
        (([[5], 2.1, 3],), {}, (), {}, True),
        (([5, [2.1], 3],), {}, (), {}, False),
        (([[5], 2.1, 3], True), {}, (), {}, True),
        (([5, [2.1], 3], True), {}, (), {}, False),
        (({"a": 1, "b": 3},), {}, (), {}, False),
        (({"a": [1, 2], "b": 3},), {}, (), {}, True),
        (({"a": 1, "b": [3, 2]},), {}, (), {}, False),
        (([(y for y in range(10)), 2.1],), {}, (), {}, True),
        (([(y for y in range(10)), 2.1], True), {}, (), {}, True),
        (([iter([5, 2.1, 3])],), {}, (), {}, True),
        (([iter([5, 2.1, 3]), 2.1],), {}, (), {}, True),
        (([iter([5, 2.1, 3]), 2.1], True), {}, (), {}, True),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.isNested(*args, **kwargs) == result


def test_shape():
    """
    Checks if shape returns actual size of nested sequence in list
    """
    params = (
        ((3,), {}, (), {}, []),
        (([],), {}, (), {}, [0]),
        (([5, 2.1, 3],), {}, (), {}, [3]),
        (([[5]],), {}, (), {}, [1, 1]),
        (([[5], 2.1, 3],), {}, (), {}, [3, 1]),
        (([5, [2.1], 3],), {}, (), {}, [3]),
        (([[[5, 3, 4, 7], 2], 2.1, 3],), {}, (), {}, [3, 2, 4]),
    )
    for args, kwargs, init_args, init_kwargs, result in params:
        assert fandango.functional.shape(*args, **kwargs) == result
