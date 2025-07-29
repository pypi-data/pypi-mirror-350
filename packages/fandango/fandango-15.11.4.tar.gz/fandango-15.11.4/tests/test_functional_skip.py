#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   test_functional_skip.py.tmp test template generated
#   from /home/srubio/src/fandango.git/fandango/functional.py
#

import traceback

import pytest

pytest.skip("This module has it's tests not implemented yet!", allow_module_level=True)

"""
dictionary with 
{'method1' : [
    (args1,kwargs1,result),
    (args2,kwargs2,result),
    ...],
}

'method' could be a method, or a class obtained calling "eval()"
result may be a value or a callable
    
"""
test_data = {
    "first": [
        (((1, 2, 3),), {}, 1),
        (((a for a in [1, 2, 3]),), {}, 1),
    ],
    "last": [
        (((1, 2, 3),), {}, 3),
        (((a for a in [1, 2, 3]),), {}, 3),
    ],
    "avg": [
        (((1, 2, 3, 4),), {}, 2.5),
    ],
    "rms": [
        (((1, 2, 3, 4),), {}, 2.7386127875258306),
    ],
}

import fandango.functional


def test_djoin():
    """
    This method merges dictionaries and/or lists
    """
    # assert fandango.functional.djoin


def test_kmap():
    __test_kmap = """ [{'args': [<method 'lower' of 'str' objects>, 'BCA', 'YZX', False], 'result': [('A', 'x'), ('B', 'y'), ('C', 'z')]}] """
    # assert fandango.functional.kmap


def test_setitem():
    # assert fandango.functional.setitem
    pass


def test_getitem():
    # assert fandango.functional.getitem
    pass


def test_setlocal():
    # assert fandango.functional.setlocal
    pass


def test_matchMap():
    """
    from a mapping type (dict or tuples list) with strings as keys it returns the value from the matched key or raises KeyError exception
    """
    # assert fandango.functional.matchMap


def test_matchTuples():
    """
    mapping is a (regexp,[regexp]) tuple list where it is verified that value matches any from the matched key
    """
    # assert fandango.functional.matchTuples


def test_matchCl():
    """
    Returns a caseless match between expression and given string
    """
    # assert fandango.functional.matchCl


def test_searchCl():
    """
    Returns a caseless regular expression search between
    expression and given string
    """
    # assert fandango.functional.searchCl


def test_replaceCl():
    """
    Replaces caseless expression exp by repl in string seq
    repl can be string or callable(matchobj) ; to reuse matchobj.group(x) if needed in the replacement string
    lower argument controls whether replaced string should be always lower case or not
    """
    # assert fandango.functional.replaceCl


def test_splitCl():
    """
    Split an string by occurences of exp
    """
    # assert fandango.functional.splitCl


def test_sortedRe():
    """
    Returns a list sorted using regular expressions.
        order = list of regular expressions to match ('[a-z]','[0-9].*','.*')
    """
    # assert fandango.functional.sortedRe


def test_toCl():
    """
    Replaces * by .* and ? by . in the given expression.
    """
    # assert fandango.functional.toCl


def test_toRegexp():
    """
    Case sensitive version of the previous one, for backwards compatibility
    """
    # assert fandango.functional.toRegexp


def test_filtersmart():
    """
    filtersmart(sequence,filters=['any_filter','+all_filter','!neg_filter'])

    appies a list of filters to a sequence of strings,
    behavior of filters depends on first filter character:
        '[a-zA-Z0-9] : an individual filter matches all strings that contain it, one matching filter is enough
        '!' : negate, discards all matching values
        '+' : complementary, it must match all complementaries and at least a 'normal filter' to be valid
        '^' : matches string since the beginning (startswith instead of contains)
        '$' : matches the end of strings
        ',' : will be used as filter separator if a single string is provided
    """
    # assert fandango.functional.filtersmart


def test_Piped():
    """
    This class gives a "Pipeable" interface to a python method:
        cat | Piped(method,args) | Piped(list)
        list(method(args,cat))
    e.g.:
    class grep:
        #keep only lines that match the regexp
        def __init__(self,pat,flags=0):
            self.fun = re.compile(pat,flags).match
        def __ror__(self,input):
            return ifilter(self.fun,input) #imap,izip,count,ifilter could ub useful
    cat('filename') | grep('myname') | printlines
    """
    # assert fandango.functional.Piped


def test_iPiped():
    """
    Used to pipe methods that already return iterators
    e.g.: hdb.keys() | iPiped(filter,partial(fandango.inCl,'elotech')) | plist
    """
    # assert fandango.functional.iPiped


def test_zPiped():
    """
    Returns a callable that applies elements of a list of tuples to a set of functions
    e.g. [(1,2),(3,0)] | zPiped(str,bool) | plist => [('1',True),('3',False)]
    """
    # assert fandango.functional.zPiped


def test_isDate():

    # assert fandango.functional.isDate
    pass


def test_isGenerator():

    # assert fandango.functional.isGenerator
    pass


def test_isSequence():
    """
    It excludes Strings, dictionaries but includes generators
    """
    # assert fandango.functional.isSequence


def test_isDictionary():
    """
    It includes dict-like and also nested lists if strict is False
    """
    # assert fandango.functional.isDictionary


def test_isHashable():
    # assert fandango.functional.isHashable
    pass


def test_isIterable():
    """
    It includes dicts and listlikes but not strings
    """
    # assert fandango.functional.isIterable


def test_isNested():
    # assert fandango.functional.isNested
    pass


def test_shape():
    """
    Returns the N dimensions of a python sequence
    """
    # assert fandango.functional.shape


def test_doc2str():

    # assert fandango.functional.doc2str
    pass


def test_html2text():

    # assert fandango.functional.html2text
    pass


def test_unicode2str():
    """
    Converts an unpacked unicode object (json) to
    nested python primitives (map,list,str)
    """
    # assert fandango.functional.unicode2str


def test_toString():

    # assert fandango.functional.toString
    pass


def test_toStringList():

    # assert fandango.functional.toStringList
    pass


def test_str2list():
    """
    Convert a single string into a list of strings

    Arguments allow to split by regexp and to keep or not the separator character
    sep_offset = 0 : do not keep
    sep_offset = -1 : keep with posterior
    sep_offset = 1 : keep with precedent
    """
    # assert fandango.functional.str2list


def test_code2atoms():
    """
    Obtain individual elements of a python code
    """
    # assert fandango.functional.code2atoms


def test_shortstr():
    """
    Obtain a shorter string
    """
    # assert fandango.functional.shortstr


def test_text2list():
    """
    Return only non empty words of a text
    """
    # assert fandango.functional.text2list


def test_str2lines():
    """
    Convert string into a multiline text of the same length
    """
    # assert fandango.functional.str2lines


def test_list2lines():
    """
    Joins every element of the list ending in multiline character,
    if joiner, returns the result as a single string.
    if comment, it will escape the comments until the end of the line
    """
    # assert fandango.functional.list2lines


def test_list2str():

    # assert fandango.functional.list2str
    pass


def test_text2tuples():

    # assert fandango.functional.text2tuples
    pass


def test_tuples2text():

    # assert fandango.functional.tuples2text
    pass


def test_dict2str():

    # assert fandango.functional.dict2str
    pass


def test_str2dict():
    """
    convert "name'ksep'value'vsep',..." to {name:value,...}
    argument may be string or sequence of strings
    if s is a mapping type it will be returned
    """
    # assert fandango.functional.str2dict


def test_obj2str():

    # assert fandango.functional.obj2str
    pass


def test_negbin():
    """
    Given a binary number as an string, it returns all bits negated
    """
    # assert fandango.functional.negbin


def test_char2int():
    """
    ord(c)
    """
    # assert fandango.functional.char2int


def test_int2char():
    """
    unichr(n)
    """
    # assert fandango.functional.int2char


def test_int2hex():

    # assert fandango.functional.int2hex
    pass


def test_int2bin():

    # assert fandango.functional.int2bin
    pass


def test_hex2int():

    # assert fandango.functional.hex2int
    pass


def test_bin2unsigned():

    # assert fandango.functional.bin2unsigned
    pass


def test_signedint2bin():
    """
    It converts an integer to an string with its binary representation
    """
    # assert fandango.functional.signedint2bin


def test_bin2signedint():
    """
    Converts an string with a binary number into a signed integer
    """
    # assert fandango.functional.bin2signedint


def test_int2bool():
    """
    Converts an integer to a binary represented as a boolean array
    """
    # assert fandango.functional.int2bool


def test_bool2int():
    """
    Converts a boolean array to an unsigned integer
    """
    # assert fandango.functional.bool2int


def test_set_default_time_format():
    """
    Usages:

        fandango.set_default_time_format('%Y-%m-%d %H:%M:%S')

        or

        fandango.set_default_time_format(fandango.ISO_TIME_FORMAT)
    """
    # assert fandango.functional.set_default_time_format


def test_now():

    # assert fandango.functional.now
    pass


def test_time2tuple():

    # assert fandango.functional.time2tuple
    pass


def test_tuple2time():

    # assert fandango.functional.tuple2time
    pass


def test_date2time():

    # assert fandango.functional.date2time
    pass


def test_date2str():

    # assert fandango.functional.date2str
    pass


def test_time2date():

    # assert fandango.functional.time2date
    pass


def test_utcdiff():

    # assert fandango.functional.utcdiff
    pass


def test_time2str():
    """
    cad: introduce your own custom format (see below)
    use DEFAULT_TIME_FORMAT to set a default one
    us=False; True to introduce ms precission
    bt=True; negative epochs are considered relative from now
    utc=False; if True it converts to UTC
    iso=False; if True, 'T' will be used to separate date and time

    cad accepts the following formats:

    %a 	Locale’s abbreviated weekday name.
    %A 	Locale’s full weekday name.
    %b 	Locale’s abbreviated month name.
    %B 	Locale’s full month name.
    %c 	Locale’s appropriate date and time representation.
    %d 	Day of the month as a decimal number [01,31].
    %H 	Hour (24-hour clock) as a decimal number [00,23].
    %I 	Hour (12-hour clock) as a decimal number [01,12].
    %j 	Day of the year as a decimal number [001,366].
    %m 	Month as a decimal number [01,12].
    %M 	Minute as a decimal number [00,59].
    %p 	Locale’s equivalent of either AM or PM. 	(1)
    %S 	Second as a decimal number [00,61]. 	(2)
    %U 	Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
    All days in a new year preceding the first Sunday are considered to be in week 0. 	(3)
    %w 	Weekday as a decimal number [0(Sunday),6].
    %W 	Week number of the year (Monday as the first day of the week) as a decimal number [00,53].
    All days in a new year preceding the first Monday are considered to be in week 0. 	(3)
    %x 	Locale’s appropriate date representation.
    %X 	Locale’s appropriate time representation.
    %y 	Year without century as a decimal number [00,99].
    %Y 	Year with century as a decimal number.
    %Z 	Time zone name (no characters if no time zone exists).
    %% 	A literal '%' character.
    """
    # assert fandango.functional.time2str


def test_str2time():
    """
    :param seq: Date must be in ((Y-m-d|d/m/Y) (H:M[:S]?)) format or -N [d/m/y/s/h]

    See RAW_TIME and TIME_UNITS to see the units used for pattern matching.

    The conversion itself is done by time.strptime method.

    :param cad: You can pass a custom time format
    """
    # assert fandango.functional.str2time


def test_time2gmt():

    # assert fandango.functional.time2gmt
    pass


def test_timezone():

    # assert fandango.functional.timezone
    pass


def test_ctime2time():

    # assert fandango.functional.ctime2time
    pass


def test_mysql2time():

    # assert fandango.functional.mysql2time
    pass


def test_iif():
    """
    if condition is boolean return (falsepart,truepart)[condition]
    if condition is callable returns truepart if condition(tp) else falsepart
    if forward is True condition(truepart) is returned instead of truepart
    if forward is callable, forward(truepart) is returned instead
    """
    # assert fandango.functional.iif


def test_ifThen():
    """
    This function allows to execute a callable on an object only if it
    has a valid value. ifThen(value,callable) will return callable(value)
    only if value is not in falsables.

    It is a List-like method, it can be combined with fandango.excepts.trial
    """
    # assert fandango.functional.ifThen


def test_call():
    """
    Calls a method from local scope parsing a pipe-like argument list
    """
    # assert fandango.functional.call


def test_retry():

    # assert fandango.functional.retry
    pass


def test_retried():
    """ """
    # assert fandango.functional.retried


def test_evalF():
    """
    Returns a function that executes the formula passes as argument.
    The formula should use x,y,z as predefined arguments, or use args[..] array instead

    e.g.:
    map(evalF("x>2"),range(5)) : [False, False, False, True, True]

    It is optimized to be efficient (but still 50% slower than a pure lambda)
    """
    # assert fandango.functional.evalF


def test_testF():
    """
    it returns how many times f(*args) can be executed in t seconds
    """
    # assert fandango.functional.testF


def test_evalX():
    """
    evalX is an enhanced eval function capable of evaluating multiple types
    and import modules if needed.

    The _locals/modules/instances dictionaries WILL BE UPDATED with the result
    of the code! (if '=' or import are used)

    It is used by some fandango classes to send python code to remote threads;
    that will evaluate and return the values as pickle objects.

    target may be:
         - dictionary of built-in types (pickable):
                {'__target__':callable or method_name,
                '__args__':[],'__class_':'',
                '__module':'','__class_args__':[]}
         - string to eval: eval('import $MODULE' or '$VAR=code()' or 'code()')
         - list if list[0] is callable: value = list[0](*list[1:])
         - callable: value = callable()
    """
    # assert fandango.functional.evalX
