#!/usr/bin/env python

#############################################################################
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

"""
    
Example of usage:
class logged_class(Logger):
    def __init__(self,name,system):
        #parent must be also an instance of a Logger object
        self.call__init__(Logger,name,parent=system)
        pass
    ...

Example of logging:
In [17]: import logging  
In [18]: l = logging.getLogger("something")
In [19]: l.debug("message")
In [20]: l.error("message")
No handlers could be found for logger "something"   
In [21]: l.addHandler(logging.StreamHandler())
In [22]: l.error("message")
message

"""
from __future__ import print_function
from __future__ import absolute_import

from builtins import map
#from builtins import str
from builtins import range
from builtins import object
import time, logging, weakref, traceback, sys, os
from fandango.objects import Object, Decorator, MethodType, Struct
from pprint import pprint, pformat
from fandango.functional import *
import warnings
import functools

TRACE_LEVEL = int(os.getenv('TRACE_LEVEL') or 1)
TRACE_LEVELS = {0: "error", 
        1: "warning", 
        2: "info", 
        3: "debug", 
        4: "trace"}
TRACE_LEVEL = int(first((k for k,v in TRACE_LEVELS.items()
                if matchCl(v,TRACE_LEVEL)),TRACE_LEVEL))

FATAL, CRITICAL, ERROR, WARNING, INFO, DEBUG, TRACE = (
    logging.FATAL,
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
    logging.NOTSET,
)
LogLevels = Struct({
    "ERROR" : ERROR,
    "WARNING" : WARNING,
    "INFO" : INFO,
    "DEBUG" : DEBUG,
    "TRACE" : TRACE,
    })
LogStreams = Struct(
    ERROR = 0,
    WARNING = 1,
    INFO = 2,
    DEBUG = 3,
    TRACE = 4,
    )


def printf(*args):
    # This is a 'lambdable' version of print
    print("".join(map(str, args)))


def tprint(*args):
    print("%s: %s" % (time2str(), " ".join(map(str, args))))
    

def lprint(sequence):
    for i,l in enumerate(sequence):
        print('%05d: %s' % (i,str(l)))


def printerr(*args):
    sys.stderr.write(*args)


def except2str(e=None, max_len=int(7.5 * 80)):
    if e is None:
        e = traceback.format_exc()
    e = str(e)
    if "desc=" in e or "desc =" in e:
        r, c = "", 0
        for i in range(e.count("desc")):
            c = e.index("desc", c) + 1
            r += e[c - 15 : c + max_len - 18] + "...\n"
        result = r
    else:
        result = str(e)[-(max_len - 3) :] + "..."
    return result or e[:max_len]


def test2str(obj, meth="", args=[], kwargs={}):
    """
    Executes a method providing a verbose output.
    For usage examples see fandango.device.FolderDS.FolderAPI.__test__()
    """
    fs = str(obj) if not meth else "%s.%s" % (obj, meth)
    r = "Testing %s(*%s,**%s)\n\n" % (fs, args, kwargs)
    v = None
    try:
        f = getattr(obj, meth) if meth and isString(meth) else (meth or obj)
        v = f(*args, **kwargs)
        if isMapping(v):
            s = "\n".join(map(str, list(v.items())))
        elif isSequence(v):
            s = "\n".join(map(str, v))
        else:
            s = str(v)
    except:
        s = traceback.format_exc()
    r += "\n".join("\t%s" % l for l in s.split("\n")) + "\n\n"
    return r, v


def printtest(obj, meth="", args=[], kwargs={}):
    """
    Executes a method providing a verbose output.
    For usage examples see fandango.device.FolderDS.FolderAPI.__test__()
    """
    r, v = test2str(obj, meth, args, kwargs)
    print(r)
    return v


# def trace(msg='', level=None):
#     if level and level not in TRACE_LEVELS:
#         level = LogStreams.get(str(level).upper(),None)
#     if level is not None and level <= TRACE_LEVEL:
#         if msg:
#             tprint(TRACE_LEVELS.get(level, level), msg)
#         else:
#             return True

def tracer(msg='', obj=None, insight=4, level=None):
    """
    Generic tracer method that inspects the current object method
    to generate the trace header

    Used in ArchivingBrowser, fn.callbacks, fn.qt, fn.threads
    """
    if level and level not in TRACE_LEVELS:
        level = LogStreams.get(str(level).upper(),None)
    if level is not None:
        level = int(level)
        if level <= TRACE_LEVEL:
            if not (msg or obj):
                return True
            else:
                name, method = '', ''
                if obj is not None:
                    if isinstance(obj,str):
                        name = obj
                    else:
                        obj = getattr(obj, "name",
                            getattr(obj, "__name__", type(obj).__name__))
                if int(insight) <= level:
                    import inspect
                    method = inspect.stack()[1][0].f_code.co_name

                level = TRACE_LEVELS.get(level, level)
                tprint(level, name, method, msg)

def parseTangoLogLevel(level=None):
    if not level:
        level = first([int(a[2]) for a in sys.argv if clmatch('-v[0-9]+$',a)],None)
    if level is None:
        return None # No Tango Level specified
    elif level >= 8:
        return 'TRACE'
    elif level >=4:
        return 'DEBUG'
    elif level >=2:
        return 'INFO'
    elif level >=1:
        return 'WARNING'
    else:
        return 'ERROR'

class FakeLogger(object):
    """
    This class just simulates a Logger using prints with date and header,
    it doesn't allow any customization
    """

    _instances = []

    def __init__(self, header="", keep=False):
        self.LogLevel = 1
        self.header = "%s: " % header if header else ""
        if keep:
            self._instances.append(self)

    def setLogLevel(self, s):
        self.LogLevel = str(s).lower() != "DEBUG"

    def trace(self, s):
        if not self.LogLevel:
            print(time2str() + " " + "TRACE\t" + self.header + s)

    def debug(self, s):
        if not self.LogLevel:
            print(time2str() + " " + "DEBUG\t" + self.header + s)

    def info(self, s):
        print(time2str() + " " + "INFO\t" + self.header + s)

    def warning(self, s):
        print(time2str() + " " + "WARNING\t" + self.header + s)

    def error(self, s):
        print(time2str() + " " + "ERROR\t" + self.header + s)


class Logger(Object):
    """
    This type provides logging methods (debug,info,error,warning) 
    to all classes inheriting it.
    To use it you must inherit from it and add it within your __init__ method:
    
    klass MyTangoDevice(LatestDeviceImpl,Logger):
          def __init__(self,cl, name):
      
        PyTango.LatestDeviceImpl.__init__(self,cl,name)
        self.call__init__(Logger,name,format='%(levelname)-8s %(asctime)s'
          ' %(name)s: %(message)s')
    
    Constructor arguments allow to customize the output format:
     * name='fandango.Logger' #object name to appear at the beginning
     * parent=None
     * format='%(levelname)-8s %(asctime)s %(name)s: %(message)s'\
     * use_tango_logs=True #Use Tango Logger if available
     * use_print=True #Use printouts instead of linux logger (use_tango_logs
        will override this option)
     * level='INFO' #default log level
     * max_len=0 #max length of log strings
    """

    root_inited = False
    Error = ERROR
    Warning = WARNING
    Info = INFO
    Debug = DEBUG
    DefaultLogLevel = WARNING

    def __init__(
        self,
        name="fandango.Logger",
        parent=None,
        format="%(levelname)-8s %(asctime)s %(name)s: %(message)s",
        use_tango_logs=True,
        use_print=True,
        level="WARNING",
        max_len=0,
        **kwargs
        ):
        self.max_len = max_len
        self.call__init__(Object)
        self.levelAliases = LogLevels.copy()
        self.stash = []

        self.log_name = name
        if parent is not None:
            self.full_name = "%s.%s" % (parent.full_name, name)
        else:
            self.full_name = name

        if not self.full_name:
            raise Exception('logger name required!')

        self.log_obj = logging.getLogger(self.full_name)
        self.log_obj.setLevel(getattr(logging,str(level),logging.WARNING))
        self.log_handlers = []

        use_tango_logs = kwargs.get('use_tango',use_tango_logs) #backwards compat
        self.use_tango_logs = use_tango_logs and hasattr(self, "debug_stream")
        self._ForcePrint = use_print

        self.parent = None
        self.children = []
        if parent is not None:
            self.parent = weakref.ref(parent)
            parent.addChild(self)
        self.setLogLevel(level)

        if not Logger.root_inited:
            # print('log format is ',format)
            self.initRoot(format)
            Logger.root_inited = True

    def __del__(self):
        parent = self.getParent()
        if parent is not None:
            parent.delChild(self)

    def initRoot(
        self,
        _format="%(threadName)-12s %(levelname)-8s "
        "%(asctime)s %(name)s: %(message)s",
    ):
        ## WARNING!: This setting affects other packages like opcua
        logging.basicConfig(level=self.DefaultLogLevel, format=_format)
        # logging.basicConfig(level=logging.DEBUG,
        # format='%(threadName)-12s %(levelname)-8s '
        #'%(asctime)s %(name)s: %(message)s')

    def setLogPrint(self, force):
        """This method enables/disables a print to be
        executed for each log call"""
        self._ForcePrint = force

    def getTimeString(self, t=None):
        if t is None:
            t = time.time()
        cad = "%Y-%m-%d %H:%M:%S"
        s = time.strftime(cad, time.localtime(t))
        ms = int((t - int(t)) * 1e3)
        return "%s.%d" % (s, ms)

    def logPrint(self, prio, msg, head=True):
        name = self.log_name or ""
        l = self.levelAliases.get(prio, prio)
        if l < self.log_obj.level:
            return
        head = "%s %7s %s: " % (name, prio, self.getTimeString()) if head else ""
        print(head + str(msg).replace("\r", ""))

    def setLogLevel(self, level=None):
        """
        This method allows to change the logging level.
        If level is empty, goes back to previous logging level.
        """
        if level is None:
            self.setLogLevel(self.stash.pop(-1) if self.stash else self.DefaultLogLevel)
            return
        self.stash.append(self.getLogLevel())
        self.stash = self.stash[-5:] #keeps only last 5 levels
        if type(level) == type(logging.NOTSET):
            self.log_obj.setLevel(level)
        else:
            l = self.getLogLevel(level)
            if l is None:
                self.warning('log.Logger: Logging level cannot be set to "%s"' % level)
            elif l != self.log_obj.level:
                self.debug('log.Logger(%s): Logging  level set to "%s" = %s'
                    % (self.log_obj.level, level, l))
                self.log_obj.setLevel(l)

        return level

    setLevel = setLogLevel

    def setLevelAlias(self, alias, level):
        """setLevelAlias(alias,level), allows to setup predefined
        levels for different tags"""
        self.levelAliases[alias] = level

    def getLogLevel(self, alias=None):
        """
        If no argument is passed, it returns current LogLevel
        If alias, it returns LogLevel for alias instead of current value
        """
        if alias is None:
            l = self.log_obj.level
            for k, v in list(self.levelAliases.items()):
                if v == l:
                    l = k
            return l
        else:
            if not isString(alias):
                try:
                    return next(
                        (k for k, v in self.levelAliases.items() if v == alias)
                    )
                except:
                    return None
            elif alias.lower() in ("debug", "info", "warning", "error"):
                return logging.__dict__.get(alias.upper())
            else:
                try:
                    return next(
                        (
                            v
                            for k, v in self.levelAliases.items()
                            if k.lower() == alias.lower()
                        )
                    )
                except:
                    return None
        return

    def checkLogLevel(self, level):
        """
        returns True if the current log level is equal or lower than arg
        """
        if not isinstance(level,int):
            level = self.getLogLevel(level)
        return LogLevels[self.getLogLevel()] <= (notNone(level,0))

    def getRootLog(self):
        return logging.getLogger()

    def getTangoLog(self):
        if not self.use_tango_logs:
            return None
        if getattr(self, "__tango_log", None):
            return self.__tango_log
        try:
            # import PyTango
            # if PyTango.Util.instance().is_svr_starting(): return None
            self.get_name()
            # Will trigger exception if Tango object is not ready
            self.__tango_log = self
        except:
            print(traceback.format_exc())
            self.warning("Unable to setup tango logging for %s" % self.log_name)
            self.__tango_log = None
        return self.__tango_log

    def getParent(self):
        if self.parent is None:
            return None
        return self.parent()

    def getChildren(self):
        children = []
        for ref in self.children:
            child = ref()
            if child is not None:
                children.append(child)
        return children

    def addChild(self, child):
        ref = weakref.ref(child)
        if not ref in self.children:
            self.children.append(ref)

    def delChild(self, child):
        ref = weakref.ref(child)
        if ref in self.children:
            self.children.remove(ref)

    #def __eq__(self, other):
        #return self is other

    def addLogHandler(self, handler):
        self.log_obj.addHandler(handler)
        self.log_handlers.append(handler)

    def copyLogHandlers(self, other):
        for handler in other.log_handlers:
            self.addLogHandler(handler)

    def output(self, msg, *args, **kw):
        self.log_obj.log(Logger.Output, msg, *args, **kw)

    def debug(self, msg, *args, **kw):
        if self.log_obj.level <= DEBUG:
            self.sendToStream(msg, "debug", 3, *args, **kw)

    def trace(self, msg, *args, **kw):
        if self.log_obj.level <= DEBUG:
            self.sendToStream(msg, "debug", 3, *args, **kw)

    def info(self, msg, *args, **kw):
        if self.log_obj.level <= INFO:
            self.sendToStream(msg, "info", 2, *args, **kw)

    def warning(self, msg, *args, **kw):
        if self.log_obj.level <= WARNING:
            self.sendToStream(msg, "warning", 1, *args, **kw)

    def error(self, msg, *args, **kw):
        if self.log_obj.level <= ERROR:
            self.sendToStream(msg, "error", 0, *args, **kw)

    def sendToStream(self, msg, level, prio, *args, **kw):
        # stream should be a number in trace=4,debug=3,info=2,warning=1,error=0
        try:
            prio = min(prio, 3) #trace=4 overriden by debug=3
            msg = shortstr(msg, self.max_len) if self.max_len else str(msg)
            msg = msg.replace("\r", "").replace("%", "%%")
            obj = self.getTangoLog()
            if obj:
                stream = (
                    obj.error_stream,
                    obj.warn_stream,
                    obj.info_stream,
                    obj.debug_stream,
                )[prio]
                stream(msg, *args, **kw)
            elif self._ForcePrint:
                self.logPrint(level.upper(), msg)
            else:
                stream = (
                    self.log_obj.error,
                    self.log_obj.warning,
                    self.log_obj.info,
                    self.log_obj.debug,
                )[prio]
                stream(msg, *args, **kw)
        except Exception as e:
            print(
                "Exception in Logger.%s! \nmsg:%s\ne:%s\nargs:%s\nkw:%s"
                % (level, msg, e, str(args), str(kw))
            )
            print(traceback.format_exc())

    def deprecated(self, msg, *args, **kw):
        filename, lineno, func = self.log_obj.findCaller()
        depr_msg = warnings.formatwarning(msg, DeprecationWarning, filename, lineno)
        self.log_obj.warning(depr_msg, *args, **kw)

    def flushOutput(self):
        self.syncLog()

    def syncLog(self):
        logger = self
        synced = []
        while logger is not None:
            for handler in logger.log_handlers:
                if handler in synced:
                    continue
                try:
                    sync = getattr(handler, "sync")
                except:
                    continue
                sync()
                synced.append(handler)
            logger = logger.getParent()

    def changeLogName(self, name):
        """Change the log name."""
        p = self.getParent()
        if p is not None:
            self.full_name = "%s.%s" % (p.full_name, name)
        else:
            self.full_name = name

        if not self.full_name:
            raise Exception('logger name required!')

        self.log_obj = logging.getLogger(self.full_name)
        for handler in self.log_handlers:
            self.log_obj.addHandler(handler)

        for child in self.getChildren():
            self.changeLogName(child.log_name)


class LogFilter(logging.Filter):
    def __init__(self, level):
        self.filter_level = level
        logging.Filter.__init__(self)

    def filter(self, record):
        ok = record.levelno == self.filter_level
        return ok


__doc__ += """
fandango.logger submodule provides a default Logger instance
and its info/debug/warning/error/trace methods directly available
as module methods.

  import fandango.log
  fandango.log.info('just a test')
  fandango.Logger.INFO    2016-02-19 11:49:55.609 just a test
"""

_LogLevel = TRACE_LEVELS[TRACE_LEVEL].upper()
for a in sys.argv:
    if a.startswith("--log-level="):
        _LogLevel = a.split("=")[-1].upper()

_Logger = Logger(level=_LogLevel)
info = _Logger.info
debug = _Logger.debug
warning = _Logger.warning
error = _Logger.error
trace = _Logger.trace
set_shell_log_level = _Logger.setLogLevel

def get_object_log(o):
    return getattr(o,'log',None) if not isinstance(o,Logger) else o

def Logged(level):
    def fff(f):
        @functools.wraps(f)
        def ff(*args, **kwargs):
            if isinstance(f,MethodType):
                o = f.im_self or f.im_class
            else:
                o = args[0]
            o = get_object_log(o)
            if o is not None:
                prev = o.getLogLevel()
                o.setLogLevel(level)
                if level in (DEBUG,'DEBUG',3,4):
                    o.debug('In %s(%s,%s)' % (f,shortstr(args),kwargs))
            r = f(*args,**kwargs)
            if o is not None:
                if level in (DEBUG,'DEBUG',3,4):
                    o.debug('Out of %s(...) = %s' % (f,shortstr(r)))
                o.setLogLevel(prev)
            return r
        return ff
    return fff
    
Debugged = Logged(DEBUG)
#def Debugged(f):
    #@functools.wraps(f)
    #def ff(*args, **kwargs):
        #o = get_object_log(args[0])
        #o and o.setLogLevel('DEBUG') #put
        #r = f(*args,**kwargs)
        #o and o.setLogLevel() #pop
        #return r
    #return ff

class InOutLogged(Decorator):
    """
    This class provides an easy way to trace whenever python enter/leaves
    a function.
    """

    def __call__(self, *args, **kwargs):
        debug(
            "In %s(%s,%s)"
            % (
                self.f.__name__,
                args,
                kwargs,
            )
        )
        r = self.f(*args, **kwargs)
        debug("Out of " + self.f.__name__)
        return r


try:
    from . import doc
    __doc__ = doc.get_fn_autodoc(__name__, vars())
except:
    pass
