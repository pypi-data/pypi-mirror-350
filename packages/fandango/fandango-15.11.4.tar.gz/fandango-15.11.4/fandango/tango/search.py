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
provides tango utilities for fandango, like database search methods and 
emulated Attribute Event/Value types

This module is a light-weight set of utilities for PyTango.
Classes dedicated for device management will go to fandango.device
Methods for Astor-like management will go to fandango.servers

.. contents::

.

"""
from __future__ import print_function

from builtins import filter
#from builtins import str
from builtins import map
import fandango.objects as objects
from fandango.linos import get_fqdn
from .defaults import *  ## Regular expressions defined here!
from .methods import *

__test__ = {}

###############################################################################
##@name Methods for searching the database with regular expressions
# @{

# This variable controls how often the Tango Database will be queried
TANGO_KEEPTIME = 60


class get_all_devices(objects.SingletonMap):
    """
    This method implements an early versio of Cache using SingletonMap
    """

    _keeptime = TANGO_KEEPTIME

    def __init__(self, exported=False, keeptime=None, host="", mask="*"):
        """
        mask will not be used at __init__ but in get_all_devs call
        """
        self._all_devs = []
        self._last_call = 0
        self._exported = exported
        self._host = host and get_tango_host(host)
        if keeptime:
            self.set_keeptime(keeptime)

    @classmethod
    def set_keeptime(klass, keeptime):
        klass._keeptime = max(keeptime, 60)  # Only 1 query/minute to DB allowed

    def get_all_devs(self, mask="*"):
        now = time.time()

        if (
            mask != "*"
            or not self._all_devs
            or now > (self._last_call + self._keeptime)
        ):

            db = get_database(self._host)
            r = sorted(
                map(
                    lowstr,
                    (
                        db.get_device_exported(mask)
                        if self._exported
                        else db.get_device_name(mask, mask)
                    ),
                )
            )
            if mask != "*":
                return r

            self._all_devs = r
            self._last_call = now

        return self._all_devs

    def __new__(cls, *p, **k):
        instance = objects.SingletonMap.__new__(cls, *p, **k)
        return instance.get_all_devs(mask=k.get("mask", "*"))


def get_class_devices(klass, db=None):
    """Returns all registered devices for a given class"""
    if not db:
        db = get_database()
    if isString(db):
        db = get_database(db)
    return sorted(str(d).lower() for d in db.get_device_name("*", klass))


@objects.Cached(depth=100, expire=60.0)
def get_matching_devices(
    patterns, limit=0, exported=False, fullname=False, trace=False,
    check_alias = False):
    """
    Searches for devices matching patterns, if exported is True only
    running devices are returned Tango host will be included in
    the matched name if fullname is True
    """
    defhost = get_tango_host()
    patterns = list(map(toRegexp, toList(patterns)))
    
    if ":" in str(patterns):
        # Multi-host search
        fullname = True
        hosts = list(set(
                (m and m.groups()[0])
                for m in (matchCl(rehost, e) for e in patterns)
            ))
    else:
        hosts = [defhost]

    # Dont count slashes, as regexps may be complex
    fullname = fullname or any(h not in (defhost, None) for h in hosts)

    all_devs = []
    if trace:
        print((hosts, fullname))

    condition = clsearch if any(isRegexp(e) for e in patterns) else None
        
    for host in hosts:
        if host in (None, defhost):
            odb = get_database()
            db_devs = get_all_devices(exported)
        else:
            # print('get_matching_devices(*%s)'%host)
            odb = get_database(host)
            db_devs = list(odb.get_device_exported("*") if exported
                else odb.get_device_name("*", "*")
                )
        
        if condition:
            db_devs = set(d for d in db_devs for e in patterns if condition(e,d))
        else:
            # Regular expression search is much slower than just this
            db_devs = [d for d in db_devs if any(p in d for p in patterns)]
        
        if check_alias:
            alias = odb.get_device_alias_list('*')
            [db_devs.add(odb.get_device_alias(k)) 
                for k in alias for e in patterns 
                if condition(e,k)]

        for d in db_devs:
            if fullname and ':' not in d:
                d = "%s/%s" % (host or defhost, d)
            all_devs.append(d)

    if not fullname:
        all_devs = ['/'.join(d.split('/')[-3:]) for d in all_devs]
    
    return sorted(all_devs[:limit] if limit else all_devs)


def get_matching_servers(patterns, tango_host="", exported=False):
    """
    Return all servers in the given tango tango_host matching
        the given patterns.

    :param exported: whether servers should be running or not
    """
    patterns = toSequence(patterns)
    servers = get_database(tango_host).get_server_list()
    servers = sorted(set(s for s in servers if matchAny(patterns, s)))
    if exported:
        exported = get_all_devices(exported=True, host=tango_host)
        servers = [s for s in servers if ("dserver/" + s).lower() in exported]
    return sorted(servers)


def find_devices(*args, **kwargs):
    # A get_matching_devices() helper, just for backwards compatibility
    return get_matching_devices(*args, **kwargs)


@objects.Cached(depth=100, expire=30.0)
def get_matching_attributes(patterns, limit=0, fullname=None, trace=False):
    """
    Returns all matching device/attribute pairs.
    regexp only allowed in attribute names
    :param patterns: a list of patterns like
        [domain_wild/family_wild/member_wild/attribute_regexp]
    """
    attrs = []
    def_host = get_tango_host()
    matches = []
    if not isSequence(patterns):
        patterns = [patterns]
    fullname = any(matchCl(rehost, e) for e in patterns)

    for e in patterns:
        match = matchCl(retango, e, terminate=True)
        if not match:
            if "/" not in e:
                host, dev, attr = def_host, e.rsplit("/", 1)[0], "state"
                # raise Exception('Expression must match domain/family/'
                #'member/attribute shape!: %s'%e)
            else:
                host, dev, attr = def_host, e.rsplit("/", 1)[0], e.rsplit("/", 1)[1]
        else:
            host, dev, attr = [
                d[k]
                for k in ("host", "device", "attribute")
                for d in (match.groupdict(),)
            ]
            host, attr = host or def_host, attr or "state"
            dev, attr = dev+'$', attr+'$'
        if trace:
            print(
                "get_matching_attributes(%s): match:%s,host:%s,"
                "dev:%s,attr:%s" % (e, bool(match), host, dev, attr)
            )

        matches.append((host, dev, attr))

    fullname = fullname or any(m[0] != def_host for m in matches)

    for host, dev, attr in matches:

        if fullname and host not in dev:
            dev = host + "/" + dev

        for d in get_matching_devices(dev, exported=True, fullname=fullname):
            if matchCl(attr, "state", terminate=True):
                attrs.append(d + "/state") #should be else, but not
            if attr.lower().strip() != "state":
                try:
                    ats = get_device_attributes(d, [attr])
                    ats = sorted(map(lowstr, ats))
                    attrs.extend([d + "/" + a for a in ats])
                    if limit and len(attrs) > limit:
                        break
                except:
                    # This method should be silent!!!
                    # print 'Unable to get attributes for %s'%d
                    # print traceback.format_exc()
                    pass

    result = sorted(map(lowstr, set(attrs)))
    return result[:limit] if limit else result


def find_attributes(*args, **kwargs):
    # A get_matching_attributes() helper, just for backwards compatibility
    return get_matching_attributes(*args, **kwargs)


def get_matching_device_attribute_labels(device, attribute):
    """
    To get all gauge port labels:
    get_matching_device_attribute_labels('*vgct*','p*')
    """
    print(device,attribute)
    devs = get_matching_devices(device, check_alias=True)
    devs = [d for d in devs if check_device(d)]
    print(devs,attribute)
    return dict(
        (t + "/" + a, l)
        for t in devs
        for a, l in get_device_labels(t, attribute,brief=False).items()
    )


def get_all_models(expressions, limit=1000):
    """
    Customization of get_matching_attributes to be usable in Taurus widgets.
    It returns all the available Tango attributes (exported!) matching any of a list of regular expressions.
    """
    if isinstance(expressions, str):  # evaluating expressions ....
        if any(re.match(s, expressions) for s in ("\{.*\}", "\(.*\)", "\[.*\]")):
            expressions = list(eval(expressions))
        else:
            expressions = expressions.split(",")
    else:
        types = [list, tuple, dict]
        try:
            from PyQt4 import Qt

            types.append(Qt.QStringList)
        except:
            pass
        if isinstance(expressions, types):
            expressions = list(str(e) for e in expressions)

    print('In get_all_models(%s:"%s") ...' % (type(expressions), expressions))
    db = get_database()
    if "SimulationDatabase" in str(
        type(db)
    ):  # used by TauWidgets displayable in QtDesigner
        return expressions
    return get_matching_attributes(expressions, limit)


def get_matching_device_properties(
    devs, props='*', hosts=[], exclude="*dserver*", port=10000, trace=False
):
    """
    get_matching_device_properties enhanced with multi-host support
    @props: regexp are enabled!
    get_devices_properties('*alarms*',props,hosts=[get_bl_host(i) for i in bls])
    @TODO: Compare performance of this method with get_devices_properties
    """
    db = get_database()
    result = {}
    if not isSequence(devs):
        devs = [devs]
    if not isSequence(props):
        props = [props]
    if hosts:
        hosts = [h if ":" in h else "%s:%s" % (h, port) for h in hosts]
    else:
        hosts = set(get_tango_host(d) for d in devs)

    result = {}
    for h in hosts:
        result[h] = {}
        set_tango_host(h)
        db = get_database(h)
        #exps = [h + "/" + e if ":" not in e else e for e in devs]
        #if trace:
            #print(exps)
        #hdevs = [
            #d.replace(h + "/", "") for d in get_matching_devices(exps, fullname=False)
        #]
        hdevs = get_matching_devices(devs,fullname=False)
        if trace:
            print("%s: %s vs %s" % (h, hdevs, props))

        for d in hdevs:
            if exclude and matchCl(exclude, d):
                continue
            dd = d.split('/',1)[-1]
            dprops = [
                p for p in db.get_device_property_list(d, "*") if matchAny(props, p)
            ]
            if not dprops:
                continue
            
            if trace:
                print((d, dprops))
                
            vals = db.get_device_property(d, dprops)
            vals = dict(
                (k, list(v) if isSequence(v) else v) for k, v in list(vals.items())
            )
            if len(hosts) == 1 and len(hdevs) == 1:
                return vals
            else:
                result[h][d] = vals
        if len(hosts) == 1:
            return result[h]
    return result


def find_properties(devs, props="*"):
    """helper for get_matching_device_properties"""
    return get_matching_device_properties(devs, props)


# @}

###############################################################################
@objects.Cached(depth=200, expire=60.0)
def finder(*args):
    """
    Universal fandango helper, it will return a matching Tango object
    depending on the arguments passed
    Objects are: database (), server (*/*), attribute ((:/)?*/*/*/*),device (*)
    """
    if not args:
        return get_database()
    arg0 = args[0]
    if arg0.count("/") == 1:
        return fandango.servers.ServersDict(arg0)
    if arg0.count("/") > (2 + (":" in arg0)):
        return (
            sorted(get_matching_attributes(*args))
            if isRegexp(arg0, WILDCARDS + " ")
            else check_attribute(arg0, brief=True)
        )
    else:
        return (
            sorted(get_matching_devices(*args))
            if isRegexp(arg0, WILDCARDS + " ")
            else get_device(arg0)
        )


__test__["fandango.tango.finder"] = ("sys/database/2", ["sys/database/2"], {})

# For backwards compatibility
TGet = finder

########################################################################################

########################################################################################
## Methods for managing device/attribute lists


def get_domain(model):
    if model.count("/") in (2, 3):
        return model.split["/"][0]
    else:
        return ""


def get_family(model):
    if model.count("/") in (2, 3):
        return model.split["/"][1]
    else:
        return ""


def get_member(model):
    if model.count("/") in (2, 3):
        return model.split["/"][2]
    else:
        return ""


def get_distinct_devices(attrs):
    """It returns a list with the distinct device names appearing in a list"""
    return sorted(list(set(a.rsplit("/", 1)[0] for a in attrs)))


def get_distinct_domains(attrs):
    """It returns a list with the distinc member names appearing in a list"""
    return sorted(list(set(a.split("/")[0].split("-")[0] for a in attrs)))


def get_distinct_families(attrs):
    """It returns a list with the distinc member names appearing in a list"""
    return sorted(list(set(a.split("/")[1].split("-")[0] for a in attrs)))


def get_distinct_members(attrs):
    """It returns a list with the distinc member names appearing in a list"""
    return sorted(list(set(a.split("/")[2].split("-")[0] for a in attrs)))


def get_distinct_attributes(attrs):
    """It returns a list with the distinc attribute names (excluding device) appearing in a list"""
    return sorted(list(set(a.rsplit("/", 1)[-1] for a in attrs)))


def reduce_distinct(group1, group2):
    """It returns a list of (device,domain,family,member,attribute) keys that appear in group1 and not in group2"""
    vals, rates = {}, {}
    try:
        target = "devices"
        k1, k2 = get_distinct_devices(group1), get_distinct_devices(group2)
        vals[target] = [k for k in k1 if k not in k2]
        rates[target] = float(len(vals[target])) / (len(k1))
    except:
        vals[target], rates[target] = [], 0
    try:
        target = "domains"
        k1, k2 = get_distinct_domains(group1), get_distinct_domains(group2)
        vals[target] = [k for k in k1 if k not in k2]
        rates[target] = float(len(vals[target])) / (len(k1))
    except:
        vals[target], rates[target] = [], 0
    try:
        target = "families"
        k1, k2 = get_distinct_families(group1), get_distinct_families(group2)
        vals[target] = [k for k in k1 if k not in k2]
        rates[target] = float(len(vals[target])) / (len(k1))
    except:
        vals[target], rates[target] = [], 0
    try:
        target = "members"
        k1, k2 = get_distinct_members(group1), get_distinct_members(group2)
        vals[target] = [k for k in k1 if k not in k2]
        rates[target] = float(len(vals[target])) / (len(k1))
    except:
        vals[target], rates[target] = [], 0
    try:
        target = "attributes"
        k1, k2 = get_distinct_attributes(group1), get_distinct_attributes(group2)
        vals[target] = [k for k in k1 if k not in k2]
        rates[target] = float(len(vals[target])) / (len(k1))
    except:
        vals[target], rates[target] = [], 0
    return first(
        (vals[k], rates[k]) for k, r in list(rates.items()) if r == max(rates.values())
    )
