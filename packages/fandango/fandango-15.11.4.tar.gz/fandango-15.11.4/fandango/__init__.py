#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
#############################################################################
##
## project :     Functional tools for Tango Control System
##
## $Author:      Sergi Rubio Manrique, srubio@cells.es $
##
## $Revision:    2008 $
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
####################################################################@########
"""
#from __future__ import print_function
#from __future__ import absolute_import

try:
#    from builtins import str
    from builtins import map
except:
    pass


__doc__ = """
@package fandango

@mainpage fandango "Functional tools for Tango" Reference
Several modules included are used in Tango Device Server projects, 
like @link dynamic @endlink and PyPLC. @n

@brief This module(s) include some PyTango additional classes and methods that 
are not implemented in the C++/Python API's; 
it replaces the previous PyTango_utils module
"""

import os, traceback, sys

__test__ = [] #['tango']
py3 = sys.version_info.major >= 3
__options__ = os.environ.get('FANDANGO','').split()

global MBS
MBS = 0,[]
try:
    import psutil
    def get_mbs():
        global MBS
        old = MBS
        MBS = psutil.Process(os.getpid()).memory_info().rss/1e6, sys.modules.copy()
        return "%.2f/%.2f: %s" % (MBS[0]-old[0],MBS[0],[m for m in sys.modules 
                if m not in old[1] and not any(s in m for s in ('fandango.','tango.','PyTango.'))])
except:
    get_mbs = lambda x:''

PATH = os.path.dirname(__file__)

if '--mem' in __options__: print('raw',get_mbs())

# CLEAN DEPRECATED FILES
deprecated = 'tango','device','interface'
deprecated = [os.path.join(PATH,f+'.'+x)
        for f in deprecated for x in ('py','pyc','pyo','py~')]
for p in deprecated:
    if os.path.exists(p):
        try:
            os.remove(p)
            print("%s removed ..." % p)
        except Exception as e:
            print(e)
            print("fandango, CLEAN OLD FILES ERROR!:")
            print("An old file still exists at:\n\t%s" % p)
            print("Import fandango as sysadmin and try again")
            print("")
            sys.exit(-1)

try:
    from . import functional
    from .functional import *
except Exception as e:
    print("Unable to import functional module: %s" % e)

if '--mem' in __options__: print('functional',get_mbs())

try:
    # LOAD VERSION NUMBER
    from . import objects
    from .objects import ReleaseNumber
    from .objects import Object, Singleton, SingletonMap, Struct, NamedProperty
    from .objects import dirModule, findModule, loadModule, dirClasses, obj2dict, copy
    from .objects import load_module, find_module
    from .objects import Decorator, ClassDecorator, BoundDecorator
    from .objects import decorate, decorates
    from .objects import Cached, Variable
    from .objects import getModuleName, getCode, decorate
    
    vf = open(PATH + "/VERSION")
    RELEASE = ReleaseNumber(list(map(int, vf.read().strip().split("."))))
    vf.close()

except Exception as e:
    print(traceback.format_exc())
    print("Unable to load RELEASE number: %s" % e)
    
if '--mem' in __options__: print('objects',get_mbs())

try:
    from .log import (printf, Logger, LogFilter, shortstr, except2str, trace,
            FakeLogger, pprint, Debugged, InOutLogged, Logged, tprint, lprint)
except Exception as e:
    print("Unable to import log module: %s" % e)

if '--mem' in __options__: print('log',get_mbs())

try:
    from .excepts import (
        trial,
        getLastException,
        getPreviousExceptions,
        ExceptionContext,
        ExceptionDecorator,
        ExceptionWrapper,
        Catched,
        CatchedArgs,
        get_current_stack,
        exc2str,
    )
except:
    print("Unable to import excepts module")

if '--mem' in __options__: print('excepts',get_mbs())

try:
    from .linos import (
        shell_command,
        ping,
        sysargs_to_dict,
        listdir,
        sendmail,
        MyMachine,
        get_fqdn,
    )
except:
    print("Unable to import linos module: %s\n" % traceback.format_exc())

if '--mem' in __options__: print('linos',get_mbs())

try:
    from .arrays import CSVArray, TimedQueue
except:
    print("Unable to import arrays module")

if '--mem' in __options__: print('arrays',get_mbs())

try:
    from .doc import *
except:
    print("Unable to import doc module")

try:
    from .dicts import (
        CaselessDict,
        ReversibleDict,
        CaselessDefaultDict,
        Enumeration,
        SortedDict,
        CaselessList,
        defaultdict,
        defaultdict_fromkey,
        reversedict,
        collections,
        deque,
        json2dict,
        dict2json,
    )
except:
    print("Unable to import dicts module")
    traceback.print_exc()

if '--mem' in __options__: print('dicts',get_mbs())

try:
    from .threads import WorkerProcess, WorkerThread, SingletonWorker, wait, timed_range
    from .threads import get_tango_thread_context, ThreadDict, DefaultThreadDict
except:
    print("Unable to import threads module: {}".format(traceback.format_exc()))

if '--mem' in __options__: print('threads',get_mbs())

try:
    from .debug import Timed, timeit
except Exception as e:
    print("Unable to import debug module")

if '--mem' in __options__: print('debug',get_mbs())

# TANGO related modules
try:
    from .tango import defaults
    from .tango import methods
    from .tango import (
        finder,
        get_device,
        get_database,
        get_database_device,
        get_all_devices,
        get_device_info,
        get_alias_for_device,
        get_device_for_alias,
        get_tango_host,
        add_new_device,
        find_devices,
        find_attributes,
        find_properties,
        get_matching_devices,
        get_matching_attributes,
        get_device_property,
        put_device_property,
        get_device_commands,
        get_device_attributes,
        cast_tango_type,
        parse_tango_model,
        check_attribute,
        read_attribute,
        read_attributes,
        check_device,
        except2str,
        TangoEval,
        ProxiesDict,
        getTangoValue,
        TangoCommand,
        fakeEvent,
        fakeEventType,
        get_attribute_events,
        check_attribute_events,
    )

    if '--mem' in __options__: print('tango.methods',get_mbs())

    try:
        from .device import Dev4Tango #, DevChild, TangoCommand
    except Exception as e:
        raise Exception("fandango.device: %s" % e)

    if '--mem' in __options__: print('tango.devices',get_mbs())

    try:
        from .servers import ServersDict, Astor, ProxiesDict, ComposersDict
    except Exception as e:
        raise Exception("fandango.servers: %s" % e)

    if '--mem' in __options__: print('tango.servers',get_mbs())

    try:
        from .callbacks import (
            EventSource,
            EventThread,
            EventListener,
            CachedAttributeProxy,
            TangoListener,
            TangoAttribute,
        )
    except Exception as e:
        raise Exception("fandango.callbacks: %s" % e)

    try:
        from .interface import FullTangoInheritance, NewTypeInheritance
    except Exception as e:
        raise Exception("fandango.interface: %s" % e)

    try:
        from .dynamic import (
            DynamicDS,
            DynamicDSClass,
            DynamicAttribute,
            DynamicDSTypes,
            CreateDynamicCommands,
            DynamicServer,
        )
    except Exception as e:
        raise Exception("fandango.dynamic: %s" % e)

    if '--mem' in __options__: print('tango.dynamic',get_mbs())

except Exception as e:
    print("Unable to import fandango.*tango modules")
    if '-v' in __options__:
        print(traceback.format_exc())

# OTHER fancy modules
if False:  # Disabled to avoid extra dependencies!!
    try:
        from . import web
    except:
        print("Unable to import fandango.web module")
    try:
        from . import qt
    except:
        print("Unable to import fandango.qt module")
    try:
        from .db import FriendlyDB
    except:
        print("Unable to import db module")

__all__ = [
    "dicts",
    "excepts",
    "log",
    "objects",
    "db",
    "device",
    "web",
    "threads",
    "dynamic",
    "callbacks",
    "arrays",
    "servers",
    "linos",
    "functional",
    "interface",
    "qt",
    "debug",
]

if '--mem' in __options__: print('fandango',get_mbs())
