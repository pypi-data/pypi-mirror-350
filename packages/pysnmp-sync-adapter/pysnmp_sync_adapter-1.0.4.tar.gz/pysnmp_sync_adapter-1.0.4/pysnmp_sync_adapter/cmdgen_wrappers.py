"""
cmdgen_wrappers.py: compatibility layer mapping HLAPI-style cmdgen v3 usage
onto pysnmp_sync_adapter sync functions and asyncio transports.
Also monkey-patches pysnmp.hlapi.v3arch.asyncio.cmdgen module for seamless HLAPI import.
"""
from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    UdpTransportTarget as _BaseUdpTransportTarget,
    Udp6TransportTarget as _BaseUdp6TransportTarget,
    CommunityData, UsmUserData,
    ContextData,
    ObjectType, ObjectIdentity
)
from pysnmp_sync_adapter import (
    get_cmd_sync, set_cmd_sync, next_cmd_sync,
    bulk_cmd_sync, walk_cmd_sync, bulk_walk_cmd_sync,
    create_transport
)
from pysnmp.proto.errind import RequestTimedOut
import pysnmp.hlapi.v3arch.asyncio.cmdgen as _hlapi_cmdgen


class UdpTransportTarget(_BaseUdpTransportTarget):
    """
    Legacy-compatible UdpTransportTarget wrapper supporting:
    - UdpTransportTarget((host, port, [timeout, [retries]]))
    - UdpTransportTarget((host, port), timeout, retries)
    """
    def __init__(self, *args, **kwargs):
        opts = {}
        if len(args) == 1 and isinstance(args[0], tuple):
            host, port = args[0][:2]
            if len(args[0]) > 2 and args[0][2] is not None:
                opts['timeout'] = args[0][2]
            if len(args[0]) > 3 and args[0][3] is not None:
                opts['retries'] = args[0][3]
        elif len(args) >= 2 and isinstance(args[0], tuple):
            host, port = args[0]
            if args[1] is not None:
                opts['timeout'] = args[1]
            if len(args) > 2 and args[2] is not None:
                opts['retries'] = args[2]
        else:
            raise ValueError(f"Unsupported args for UdpTransportTarget: {args!r}")
        transport = create_transport(_BaseUdpTransportTarget, (host, port), **opts)
        self.__dict__ = transport.__dict__


class Udp6TransportTarget(_BaseUdp6TransportTarget):
    """
    Legacy-compatible Udp6TransportTarget wrapper.
    """
    def __init__(self, *args, **kwargs):
        opts = {}
        if len(args) == 1 and isinstance(args[0], tuple):
            host, port = args[0][:2]
            if len(args[0]) > 2 and args[0][2] is not None:
                opts['timeout'] = args[0][2]
            if len(args[0]) > 3 and args[0][3] is not None:
                opts['retries'] = args[0][3]
        elif len(args) >= 2 and isinstance(args[0], tuple):
            host, port = args[0]
            if args[1] is not None:
                opts['timeout'] = args[1]
            if len(args) > 2 and args[2] is not None:
                opts['retries'] = args[2]
        else:
            raise ValueError(f"Unsupported args for Udp6TransportTarget: {args!r}")
        transport = create_transport(_BaseUdp6TransportTarget, (host, port), **opts)
        self.__dict__ = transport.__dict__


def _prepare_args(snmp_args):
    """
    Wrap raw OID tuples into ObjectType(ObjectIdentity).
    """
    new_args = []
    for arg in snmp_args:
        if isinstance(arg, tuple) and all(isinstance(x, int) for x in arg):
            new_args.append(ObjectType(ObjectIdentity(arg)))
        else:
            new_args.append(arg)
    return new_args


def _wrap_sync_result(sync_func, *snmp_args, **snmp_kwargs):
    # ensure engine and credentials
    args = list(snmp_args)
    # first: CommunityData or UsmUserData -> need SnmpEngine
    if args and isinstance(args[0], (CommunityData, UsmUserData)):
        args.insert(0, SnmpEngine())
    # next: transport -> need ContextData
    # find first transport instance
    for idx, a in enumerate(args):
        if isinstance(a, (_BaseUdpTransportTarget, _BaseUdp6TransportTarget)):
            args.insert(idx+1, ContextData())
            break
    # prepare OID args
    args = _prepare_args(args)
    result = sync_func(*args, **snmp_kwargs)
    if result is None:
        return None
    errInd, errStat, errIdx, varBinds = result
    if errInd:
        text = str(errInd)
        if isinstance(errInd, RequestTimedOut) and 'before timeout' in text:
            text += ' - timed out'
        return text, errStat, errIdx, varBinds
    return errInd, errStat, errIdx, varBinds


class CommandGenerator:
    """
    HLAPI-compatible CommandGenerator mapping to sync adapter.
    Methods return (errInd, errStat, errIdx, varBinds).
    """
    def getCmd(self, *args, **kwargs):
        return _wrap_sync_result(get_cmd_sync, *args, **kwargs)

    def setCmd(self, *args, **kwargs):
        return _wrap_sync_result(set_cmd_sync, *args, **kwargs)

    def nextCmd(self, *args, **kwargs):
        return _wrap_sync_result(next_cmd_sync, *args, **kwargs)

    def bulkCmd(self, *args, **kwargs):
        return _wrap_sync_result(bulk_cmd_sync, *args, **kwargs)

    def walkCmd(self, *args, **kwargs):
        return _wrap_sync_result(walk_cmd_sync, *args, **kwargs)

    def bulkWalkCmd(self, *args, **kwargs):
        return _wrap_sync_result(bulk_walk_cmd_sync, *args, **kwargs)


# Monkey-patch HLAPI cmdgen module
_hlapi_cmdgen.CommandGenerator = CommandGenerator
_hlapi_cmdgen.UdpTransportTarget = UdpTransportTarget
_hlapi_cmdgen.Udp6TransportTarget = Udp6TransportTarget
_hlapi_cmdgen.getCmd = lambda *a, **k: CommandGenerator().getCmd(*a, **k)
_hlapi_cmdgen.setCmd = lambda *a, **k: CommandGenerator().setCmd(*a, **k)
_hlapi_cmdgen.nextCmd = lambda *a, **k: CommandGenerator().nextCmd(*a, **k)
_hlapi_cmdgen.bulkCmd = lambda *a, **k: CommandGenerator().bulkCmd(*a, **k)
_hlapi_cmdgen.walkCmd = lambda *a, **k: CommandGenerator().walkCmd(*a, **k)
_hlapi_cmdgen.bulkWalkCmd = lambda *a, **k: CommandGenerator().bulkWalkCmd(*a, **k)
