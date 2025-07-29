#!/usr/bin/env python
"""
#############################################################################
##
## file :       dicts.py
##
## description : see below
##
## project :     Tango Control System
##
## $Author: Sergi Rubio Manrique, srubio@cells.es $
##
## $Revision: 2008 $
##
## copyleft :    ALBA Synchrotron Controls Section, CELLS
##               Bellaterra
##               Spain
##
#############################################################################
##
## This file is part of Tango Control System
##
## Tango Control System is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## Tango Control System is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
###########################################################################
@package dicts

Some extensions to python dictionary
ThreadDict: Thread safe dictionary with redefinable read/write methods and a backgroud thread for hardware update.
defaultdict_fromkey: Creates a dictionary with a default_factory function that creates new elements using key as argument.
CaselessDict: caseless dictionary
CaselessDefaultDict: a join venture between caseless and default dict from key

@deprecated
@note see in tau.core.utils.containers

by Sergi Rubio, 
srubio@cells.es, 
2008 
"""
from __future__ import print_function
from __future__ import division

from builtins import next
from builtins import map
from builtins import zip
#from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
from future.utils import raise_

import time, traceback, os
import collections
from collections import defaultdict, deque

try:
    from collections import OrderedDict
    from collections import namedtuple
    from collections import ChainMap
except:
    pass

from .objects import self_locked
from .functional import *

ENC = "latin-1"


def dict2json(
    dct, filename=None, throw=False, recursive=True, encoding=ENC, as_dict=False
):
    """
    It will check that all objects in dict are serializable.
    Thus, returning a dictionary with the json serialization of each object.
    If throw is False, a corrected dictionary will be returned in case of error.
    If filename is given, dict will be saved as a .json file.
    ElIf as_dict is True, then a python dictionary is returned instead of json.
    """
    import json

    result = {}
    for k, v in list(dct.items()):
        try:
            if py3:
                json.dumps(v)
            else:
                json.dumps(v, encoding=encoding)
            result[k] = v
        except Exception as e:
            if throw:
                raise e
            if isString(v):
                result[k] = ""
            elif isSequence(v):
                try:
                    result[k] = list(v)
                    json.dumps(result[k])
                except:
                    result[k] = []
            elif isMapping(v, strict=True) and recursive:
                result[k] = dict2json(v, None, False, True, encoding=encoding)
    if filename:
        if py3:
            json.dump(result, open(filename, "w"))
        else:
            json.dump(result, open(filename, "w"), encoding=encoding)
    elif not as_dict:
        result = json.dumps(result)

    return result if not filename else filename


def decode(s, encoding=ENC):
    """
    decodes json string using encoding
    not needed with python3 jsons

    dec = lambda s: str(s.decode(encoding) if isinstance(s,unicode) else s)
    """
    try:
        if isinstance(s, str):
            s = s.encode(encoding)
            return str(s)
        else:
            return str(s)
    except Exception as e:
        print("dec(%s) failed!" % (s))
        traceback.print_exc()
        raise e


def json2dict(jstr, encoding=ENC):
    """
    Converts unicode to str recursively.

    :param jstr: may be json string, filename or dictionary

    in the last case, this method is equivalent to fandango.unicode2str(obj)
    """
    import json

    kw = {'encoding':encoding} if not py3 else {}

    if not hasattr(jstr, "items"):
        if "{" not in jstr and os.path.exists(jstr):
            f = open(jstr)
            jstr = json.load(f, **kw)
            f.close()
        else:
            jstr = json.loads(jstr, **kw)

    d = {}
    dec = (lambda s,**kw:s) if py3 else decode

    for k, v in list(jstr.items()):
        k = dec(k)
        if isString(v):
            d[k] = dec(v)
        elif isinstance(v, (list, tuple)):
            d[k] = [(dec(i) if isString(i) else i) for i in v]
        elif hasattr(v, "items"):
            d[k] = json2dict(v, **kw)
        else:
            d[k] = v
    return d


class defaultdict_fromkey(defaultdict):
    """Creates a dictionary with a default_factory function that creates new elements using key as argument.
    Usage : new_dict = defaultdict_fromkey(method); where method like (lambda key: return new_obj(key))
    Each time that new_dict[key] is called with a key that doesn't exist, method(key) is used to create the value
    Copied from PyAlarm device server
    @deprecated now in tau.core.utils.containers
    """

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        try:
            self[key] = value = self.default_factory(key)
        except Exception as e:
            try:
                self[key] = value = self.default_factory()
            except:
                raise e
        return value


class CaselessList(list):
    """
    Python list with caseless index,contains,remove methods
    """

    def _lowstreq(self, a, b):
        return (a == b) or (
            hasattr(a, "lower") and hasattr(b, "lower") and a.lower() == b.lower()
        )

    def __contains__(self, item):
        for k in self:
            if self._lowstreq(k, item):
                return True
        return False

    def index(self, item):
        for i, k in enumerate(self):
            if self._lowstreq(k, item):
                return i
        return None

    def __contains__(self, item):
        return self.index(item) is not None

    def remove(self, item):
        list.pop(self, self.index(item))


class CustomDict(dict):
    """ Dictionary that replaces key using alternate customkey function
    """
    customkey = staticmethod(str)
    
    def __init__(self, other=None, customkey = None):
        super(CustomDict,self).__init__()
        if customkey is not None:
            self.customkey = customkey
        other and self.update(other)
    
    def __getitem__(self, key):
        return super(CustomDict,self).__getitem__(self.customkey(key))
    
    def get(self, key, def_val = None):
        # this is NOT equivalent to __getitem__
        return super(CustomDict,self).get(self.customkey(key), def_val)
    
    getitem = get

    def __setitem__(self, key, value):
        super(CustomDict,self).__setitem__(self.customkey(key), value)
        
    setitem = put = __setitem__

    def __contains__(self, key):
        return super(CustomDict,self).__contains__(self.customkey(key))

    has_key = __contains__

    def setdefault(self, key, def_val=None):
        return super(CustomDict,self).setdefault(self.customkey(key), def_val)

    def update(self, other):
        if hasattr(other,'items'):
            other = other.items()
        for k,v in other:
            super(CustomDict,self).__setitem__(self.customkey(k), v)

    @classmethod
    def fromkeys(klass, iterable, value=None):
        return klass(((k,value) for k in iterable))

    def pop(self, key, def_val=None):
        return super(CustomDict,self).pop(self.customkey(key), def_val)

    def __delitem__(self, key):
        super(CustomDict,self).__delitem__(self.customkey(key))

        
class CaselessDict(CustomDict):
    """Dictionary with caseless key resolution
    """
    customkey = staticmethod(lowstr)

    @classmethod
    def __test__(klass):
        # python3 -c "import fandango; fandango.dicts.CaselessDict.__test__()"
        def test(t,env): print('%s: %s => %s' % (klass,t,eval(t,globals(),env)))
        cd = klass.fromkeys(('a','B','c'),1)
        test('cd',locals())
        test('cd["b"] == cd["B"]',locals())
        test('(cd.put("D",4),cd)',locals())
        test('CaselessDict(cd)',locals())
        test('CaselessDict(cd.items())',locals())
        test('cd.pop("d")',locals())
        test('cd',locals())

class CaselessDefaultDict(defaultdict_fromkey, CaselessDict):
    """a join venture between caseless and defaultdict_fromkey
    This class merges the two previous ones.
    This declaration equals to:
        CaselessDefaultDict = type('CaselessDefaultType',(CaselessDict,defaultdict_fromkey),{})
    """
    
    def __init__(self,factory=None,other=None):
        defaultdict_fromkey.__init__(self,factory)
        CaselessDict.__init__(self,other)

    def __getitem__(self, key):
        return defaultdict_fromkey.__getitem__(self, self.customkey(key))
    
    @classmethod
    def fromkeys(klass, iterable, factory = None):
        r = klass(factory)
        [r[k] for k in iterable]
        return r

    @classmethod
    def __test__(klass):
        # python3 -c "import fandango; fandango.dicts.CaselessDict.__test__()"
        import random
        def test(t,env): 
            print('%s: %s => %s' % (klass.__name__,t,eval(t,globals(),env)))
        #cd = klass.fromkeys(('a','B','c'),random.random)
        factory = lambda k: 1+'abcd'.index(k.lower())+random.random()
        cd = klass(factory)
        test('cd',locals())
        test('cd["a"], "cd" in locals()',locals())
        test('cd["b"] == cd["B"]',locals())
        test('(cd.put("D",4),cd)',locals())
        test('CaselessDict(cd)',locals())
        test('CaselessDict(cd.items())',locals())
        test('klass.fromkeys(["a","C"],factory)',locals())
        test('cd.pop("d")',locals())
        test('cd',locals())

##################################################################################################


class SortedDict(dict):
    """This class implements a dictionary that returns keys in the same order they were inserted."""

    def __init__(self, other=None):
        dict.__init__(self)
        self._keys = []
        if other is not None:
            self.update(other)
        return

    def sort(self, key):
        """
        This method modifies the sorting of the dictionary overriding the existing sort key.
        :param key: it can be a sequence containing all the keys already existing in the dictionary
                    or a callable providing a sorting key algorithm.
        """
        import operator

        if callable(key): #if hasattr(key, "__call__"):
            self._keys = sorted(self._keys, key=key)
        else:
            for k in self._keys:
                if k not in self._keys:
                    raise KeyError(k)
            self._keys = list(key)
        return self._keys[:]

    def __setitem__(self, k, v):
        if k not in self._keys:
            self._keys.append(k)
        dict.__setitem__(self, k, v)

    def update(self, other):
        if hasattr(other, "items"):
            other = list(other.items())
        for k, v in other:
            self.__setitem__(k, v)

    @staticmethod
    def fromkeys(S, v=None):
        return SortedDict((s, v) for s in S)

    def insert(self, index, key, value):
        """Insert key,value at given position"""
        if key in self:
            self.pop(key)
        self._keys.insert(index, key)
        dict.__setitem__(self, key, value)

    def pop(self, k, d=None):
        """Removes key and returns its (self[key] or d or None)"""
        if k not in self:
            return d
        self._keys.remove(k)
        return dict.pop(self, k)

    def popitem(self):
        """Removes and returns last key,value pair"""
        k = self._keys[-1]
        v = self[k]
        self.pop(k)
        return k, v

    def clear(self):
        self._keys = []
        return dict.clear(self)

    def keys(self):
        return self._keys[:]

    def values(self):
        return [self[k] for k in self._keys]

    def items(self):
        return [(k, self[k]) for k in self._keys]

    def __iter__(self):
        return (i for i in self._keys)

    def iteritems(self):
        return ((k, self[k]) for k in self._keys)

    def iterkeys(self):
        return (i for i in self._keys)

    def itervalues(self):
        return (self[k] for k in self._keys)


class CaselessSortedDict(SortedDict, CaselessDict):
    """This class implements a dictionary that returns keys in the same order they were inserted."""

    def __init__(self, other=None):
        dict.__init__(self)
        self._keys = []
        if other is not None:
            CaselessDict.__init__(self, other)
        return

    @staticmethod
    def caseless(key):
        return str(key).lower()

    def sort(self, key):
        """
        This method modifies the sorting of the dictionary overriding the existing sort key.
        :param key: it can be a sequence containing all the keys already existing in the dictionary
                    or a callable providing a sorting key algorithm.
        """
        import operator

        if callable(key):
            self._keys = sorted(self._keys, key=key)
        else:
            for k in self._keys:
                if k not in self._keys:
                    raise KeyError(k)
            self._keys = list(key)
        return self._keys[:]

    def __setitem__(self, k, v):
        k = self.caseless(k)
        if k not in self._keys:
            self._keys.append(k)
        dict.__setitem__(self, k, v)

    def update(self, other):
        if hasattr(other, "items"):
            other = list(other.items())
        for k, v in other:
            self.__setitem__(k, v)

    @staticmethod
    def fromkeys(S, v=None):
        S = list(map(self.caseless, S))
        return SortedDict((s, v) for s in S)

    def pop(self, k, d=None):
        """Removes key and returns its (self[key] or d or None)"""
        k = self.caseless(k)
        if k not in self:
            return d
        self._keys.remove(k)
        return dict.pop(self, k)


##################################################################################################


def reversedict(dct, key=None, default=None):
    # it just exchanges keys/values in a dictionary
    if key is None:
        return dict((v, k) for k, v in list(dct.items()))
    for k, v in list(dct.items()):
        if v == key:
            return k
    return default


class ReversibleDict(object):  # dict):
    """Dictionary that searches in both directions within a list of tuples acting like a nested dictionary.
     * Negative indexes and levels are used to reverse the direction of key,values retrieval (i>=0: left-to-right; i<0: rigth-to-left)
     * Both directions are not exclusive!!! ... search direction is managed by the tuple index sign (+/-)
     * The _level is always positive, and could relate to both sides of the tuple [+level,-(level-1)][i<0]
     * When no sublevel is entered, keys() returns both sides of each tuple
     * Due to this behaviour may be: len(self) < len(self.items())
     * It inherits from dictionary just to be recognized by isinstance!
     * keys()[x] != values()[x] ... use .items() or iteritems() when you need to match it
     * There's no check for duplicate keys, if there's a duplicate key then the first match is returned

    :TODO : A nice search algorithm in sorted tables would speed up retrieving a lot

    dict methods implemeted:
        __contains__,__delitem__,__getitem__,__iter__,__len__,__repr__,__setitem__,__str__
        get,has_key,items,iteritems,iterkeys,itervalues,keys,pop,values
    NotImplemented: clear,copy,fromkeys,setdefault,update,popitem
    """

    DEFAULT = None
    SORTKEY = lambda s: ord(s[0]) % 3

    def __init__(
        self, table=None, subset=None, index=None, level=0, sorted=False, trace=False
    ):
        """
        :param table: The table must be a list of tuples having all the same length and must be sorted!
        :param subset: it will be a list of lines to be searched, the rest will be ignored; used for nesting
        :param index: the index in tuples to be searched, if None both begin (0) and end (-1) are searched
        :param level: always a positive value
        """
        table, subset, index = (
            table or [],
            subset or (),
            index or [],
        )  # There are strange problems if persistent types are used as __init__ arguments!?!
        if isinstance(table, ReversibleDict):
            table = table.data()
        elif hasattr(table, "items"):
            table = [t for t in list(table.items())]  # Updating from a dictionary
        # Attributes persistent
        self._depth = table and len(table[0]) or 0
        self._table = table or []
        self._sorted = index or sorted
        self.trace(trace)
        if sorted and not index:
            self._index = self.sort(True)
        else:
            self._index = index
        # Attributes that changed in sub-instances
        self._level = level  # It's always positive!
        self._subset = subset

    def update(self, other):
        if not other:
            return
        if hasattr(other, "iteritems"):
            [self.set(*t) for t in other.items()]
        else:
            [self.set(*t) for t in other]

    # def __new__(klass,*args):
    # return klass(*args)

    def __len__(self):
        """It returns the number of raw lines, not keys or values"""
        return len(self._subset or self._table)

    def range(self, full=True):
        """And appropiated iterator to check all lines in the table"""
        return self._subset or list(
            range(full and -len(self._table) or 0, len(self._table))
        )

    def __repr__(self):
        return "{" + ",\n".join("\t%s%s:%s" % (k, "", v) for k, v in self.items()) + "}"

    def __str__(self):
        return self.__repr__()

    def trace(self, val=None):
        if val in (True, False):
            self._trace = val
        return self._trace

    def sort(self, update=False):
        """creates indexes of the keys at each level using the self.SORTKEY method
        for each level there's a dictionary {SORTKEY(s):[lines where SORTKEY(key)==SORTKEY(s)]}
        SORTKEY is used instead of key to improve retrieve times.
        """
        if update:
            self._index = {}
            for l in range(self._depth):
                self._index[l] = self._index[-(l + 1)] = defaultdict(set)
                for i in self.range():
                    self._index[l][self.SORTKEY(self._table[i][l])].add(i)
            self._sorted = True
        return self._index

    def prune(self, filters=[]):
        """This method should do a cleanup of all repeated key-chains in both directions (or delete anything matched by filters)"""
        raise Exception("NotImplemented")

    def depth(self):
        return self._depth

    def data(self):
        return self._table

    def size(self):
        return len(self._table)

    def sorted(self):
        return self._sorted

    def nextlevel(self, i=None):
        if i is not None and i < 0:
            return self.level(i) - 1
        else:
            return self._level + 1  # (1 if direction>=0 else -1) #Level always positive

    def prevlevel(self, i=None):
        if i is not None and i < 0:
            return self.level(i) + 1
        else:
            return (
                self._level - 1
            )  # (1 if directionl>=0 else -1) #Level always positive

    # def iterlevel(self):
    # """ Returns (level,) or if level is None then it will try left-to-right and right-to-left first levels """
    # return ((0,-1) if self._level is None else (self._level,))

    def level(self, i=None):
        """The direction depends on the sign of the tuple index"""
        if i is not None and i < 0:
            return -(self._level + 1)
        else:
            return self._level

    def last(self):
        return self.nextlevel() == self.depth() - 1

    def __iter__(self):
        """It returns distinct keys"""
        previous = set()
        for i in self.range():
            k = self._table[i][self.level(i)]
            if k in previous:
                continue
            previous.add(k)
            yield k
        pass

    def iterkeys(self):
        return self.__iter__()

    def keys(self):
        return set([k for k in self.__iter__()])

    def keysets(self, key=None):
        """It returns a dictionary of {key:[index set]} at actual level.
        The sign +/- of the index refers to left-to-right/right-to-left order
        The level/direcition is not initialized until a key is found by this method.
        """
        keys = defaultdict(set)
        if key is None:  # Don't check it at every loop!
            for i in self.range():
                [keys[self._table[i][self.level(i)]].add(i) for i in self.range()]
        else:  # Searching for a given key
            for i in self.range():
                j = self.level(i)
                if self._table[i][j] != key:
                    continue
                keys[self._table[i][j]].add(i)
        return keys

    def itervalues(self):
        """It returns values for actual keys"""
        if self.level() == self.depth() - 1:
            for i in self.range():
                yield self._table[i][self.level(i)]
        else:
            for ks in list(self.keysets().values()):
                yield ReversibleDict(
                    table=self._table,
                    index=self._index,
                    subset=ks,
                    level=self.nextlevel(),
                    trace=self._trace,
                )
        pass

    def values(self):
        return [v for v in self.values()]

    def iteritems(self):
        """returns key,value pairs at self.level()"""
        if self.nextlevel() == self.depth() - 1:
            for i in self.range():
                yield self._table[i][self.level(i)], self._table[i][
                    self.nextlevel(i)
                ]  # Last key,value pair
        else:
            for k, ks in list(self.keysets().items()):
                yield k, ReversibleDict(
                    table=self._table,
                    index=self._index,
                    subset=ks,
                    level=self.nextlevel(),
                    trace=self._trace,
                )
        pass

    def items(self):
        return [t for t in self.items()]

    def line(self, i):
        """It returns an arranged tuple slice of the selected index of the table
        :param i: it must be the RAW (positive or negative) index of the line
        """
        if i > self.size():
            i = i - 2 * self.size()  # converting to a negative index
        rightleft = i < 0  # left-to-right or right-to-left order
        t = self._table[i]
        if not self._level:
            return tuple(reversed(t)) if rightleft else t
        else:
            level = self.level(i)
            if rightleft:
                return (t[level],) + tuple(reversed(t[-self._depth : level]))
            else:
                return t[level : self._depth]

    def iterlines(self):
        """Instead of returning key,value pairs it returns a tuple with self.depth() values"""
        for i in self.range(full=False):
            yield self.line(i)

    def lines(self):
        """Instead of returning key,value pairs it returns a tuple with self.depth() values"""
        return [i for i in self.iterlines()]

    def has_key(self, key):
        """Implemented separately of __getitem__ to be more efficient."""
        for i in self.range(full=True):
            if self._table[i][self.level(i)] == key:
                return True
        return False

    def __contains__(self, key):
        return key in self

    def get(self, *keys):
        """Arguments are keys separated by commas, it is a recursive call to __getitem__"""
        if len(keys) > self._depth:
            return self.DEFAULT
        try:
            v = self[keys[0]]
            if isinstance(v, ReversibleDict):
                return v.get(*keys[1:])
            else:
                return v
        except:
            return self.DEFAULT

    def __getitem__(self, key, raw=False):
        """It scans the dict table in both directions, returning value or a ReversibleDict instance"""
        ks = self.keysets(key=key)
        if not ks.get(key, []):
            raise_(Exception, "KeyNotFound(%s)" % str(key))
        if self.nextlevel() == self.depth() - 1:
            i = ks[key].pop()
            return self._table[i][
                self.nextlevel(i)
            ]  # Returning a first/last element of tuple
        else:
            return ReversibleDict(
                table=self._table,
                subset=ks[key],
                index=self._index,
                level=self.nextlevel(),
                trace=self._trace,
            )  # Returning a ReversibleDict with the subset of tuples that matched previous searches.

    def set(self, *keys):
        """Arguments are values separated by commas, it is a recursive call to __setitem__"""
        if len(keys) == 1 and any(isinstance(keys[0], t) for t in (list, tuple, set)):
            keys = tuple(keys[0])
        self[keys[0]] = keys[1:]

    def __setitem__(self, key, value):
        """It may accept two ways:
        * Entering a tuple of length = depth-level
        * Entering directly the last value (level = depth-1); it will override existing ones!!!
        * Order will depend of the previously inserted tuples for the same key
        * If key doesn't exist it will be added as a left-to-right tuple
        """
        # print 'In ReversibleDict.__setitem__(%s,%s), level is %s'%(key,value,self.level())

        # Checking all the conditions for the arguments
        if not hasattr(value, "__iter__") or isinstance(value, str):
            value = (value,)
        elif not isinstance(value, tuple):
            value = tuple(value)
        if not len(value):
            raise Exception("EmptyTuple!")
        elif self._table and (len(value)) != self.depth() - self.level() - 1:
            raise_(
                Exception,
                "WrongTupleSize(%s!=%s)"
                % (len(value), self.depth() - self.level() - 1),
            )

        if self._trace:
            print("In ReversibleDict[%s] = %s" % (key, value))
        # Creating a new table if the dict was empty
        if not self._table:
            self._table.append((key,) + value)
            self._depth = 1 + len(value)
            if self._trace:
                print("Creating a table ...")
        # Check if the key already exist
        elif key in self:
            if self._trace:
                print("Updating a key ...")
            i = next(iter(self.keysets(key)[key]))
            if self.last():  # If it's a final leaf the value is overriden
                self._table[i] = (
                    (self._table[i][: self.nextlevel(i)] + value)
                    if i >= 0
                    else (value + self._table[i][self.level(i) :])
                )
            else:  # If not the tuple is passed to the next dictionary
                return self[key].__setitem__(value[0], value[1:])
                # if i>=0:
                # else: return self[key].__setitem__(value[-1],value[:-1])

        # The key exists but in reversed order (only for root dictionary)
        elif self.level() in (0, -1) and value[-1] in self:
            if self._trace:
                print("Inserting reversed key ...")
            self[value[-1]] = tuple(reversed(value[:-1])) + (key,)

        # Adding new keys
        elif self.level():
            i = next(iter(self._subset))
            # print 'adding new key %s at level %s, i = %s' % (key,self.level(i),i)
            if i >= 0:
                self._table.append(self._table[i][: self.level(i)] + (key,) + value)
            else:
                self._table.append(
                    tuple(reversed(value))
                    + (key,)
                    + self._table[i][self.level(i) + 1 :]
                )  # +1 because slices are not symmetric!
            if self._trace:
                print("Adding a new key ...")
        else:
            if self._trace:
                print("Adding a new line ...")
            self._table.append((key,) + value)

    def __del__(self):
        del self._table

    def __delitem__(self, k):
        raise Exception("NotImplemented!")

    def setdefault(self, key, def_val=None):
        raise Exception("NotImplemented!")

    def fromkeys(self, iterable, value=None):
        raise Exception("NotImplemented!")

    def pop(self, key, def_val=None):
        raise Exception("NotImplemented!")


##################################################################################################

"""
enumeration.py: borrowed from tcoutinho@cells.es tau.core.utils library

  Enumeration module.
  In C, enums allow you to declare a bunch of constants with unique values,
  without necessarily specifying the actual values (except in cases where you
  need to). Python has an accepted idiom that's fine for very small numbers of
  constants (A, B, C, D = range(4)) but it doesn't scale well to large numbers,
  and it doesn't allow you to specify values for some constants while leaving
  others unspecified. This approach does those things, while verifying that all
  values (specified and unspecified) are unique. Enum values then are attributes
  of an Enumeration class (Insect.BEETLE, Car.PASSAT, etc.).

"""

import types


class EnumException(Exception):
    pass


class Enumeration(object):
    """@DEPRECATED: Use python Enum type instead!

    Enumeration class intended to provide the 'enum' feature present in many
    programming languages.
    Usage:
    car = ThingWithType(fruit.Lemon)
    print whatkind(fruit.type, Lemon)
    bug = ThingWithType(Insect.BEETLE)
    print whatkind(bug.type, Insect)

    Notice that car's and bug's attributes don't include any of the
    enum machinery, because that machinery is all CLASS attributes and
    not INSTANCE attributes. So you can generate thousands of cars and
    bugs with reckless abandon, never worrying that time or memory will
    be wasted on redundant copies of the enum stuff.

    print car.__dict__
    print bug.__dict__
    pprint.pprint(Cars.__dict__)
    pprint.pprint(Insect.__dict__)
    """

    def __init__(self, name, enumList):
        self.__doc__ = name
        lookup = {}
        reverseLookup = {}
        caseless = CaselessDict()
        uniqueNames = []
        self._uniqueValues = uniqueValues = []
        self._uniqueId = 0
        for x in enumList:
            if isinstance(x,tuple):
                x, i = x
                if not isString(x): #if type(x) != bytes:
                    raise EnumException("enum name is not a string: %s" % str(x))
                if type(i) != int:
                    raise EnumException("enum value is not an integer: %s" % str(i))
                if x in uniqueNames:
                    raise EnumException("enum name is not unique: %s" % str(x))
                if i in uniqueValues:
                    raise EnumException("enum value is not unique for %s" % str(x))
                uniqueNames.append(x)
                uniqueValues.append(i)
                lookup[x] = i
                reverseLookup[i] = x
                caseless[x] = i
        for x in enumList:
            if type(x) != tuple:
                if not isString(x): #if type(x) != bytes:
                    raise EnumException("enum name is not a string: %s" % str(x))
                if x in uniqueNames:
                    raise EnumException("enum name is not unique: %s" % str(x))
                uniqueNames.append(x)
                i = self.generateUniqueId()
                uniqueValues.append(i)
                lookup[x] = i
                reverseLookup[i] = x
                caseless[x] = i
        self.lookup = lookup
        self.reverseLookup = reverseLookup
        self.caseless = caseless

    def generateUniqueId(self):
        while self._uniqueId in self._uniqueValues:
            self._uniqueId += 1
        n = self._uniqueId
        self._uniqueId += 1
        return n

    def get(self, k, default=None):
        return self.__getitem__(k) if k in self else default

    def __contains__(self, i):
        return i in self.reverseLookup or i in self.caseless

    def __getitem__(self, i):
        if type(i) == int:
            return self.whatis(i)
        elif isinstance(i,(str,bytes,unicode)):
            return self.caseless[i]

    def __getattr__(self, attr):
        if attr not in self.lookup:
            raise AttributeError
        return self.lookup[attr]

    def whatis(self, value):
        return self.reverseLookup[value]


from . import doc

__doc__ = doc.get_fn_autodoc(__name__, vars())
