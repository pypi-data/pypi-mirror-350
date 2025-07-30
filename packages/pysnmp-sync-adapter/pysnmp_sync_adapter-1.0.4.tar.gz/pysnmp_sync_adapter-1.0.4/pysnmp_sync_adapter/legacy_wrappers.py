import os
import sys
import abc

# Architecture selection logic
_env_arch = os.getenv("PYSNMP_ARCH", "").lower()
if _env_arch in ("v1arch", "v3arch"):
    arch = _env_arch
elif "pysnmp.hlapi.v3arch.asyncio" in sys.modules:
    arch = "v3arch"
else:
    arch = "v1arch"

# Dynamic import of base UdpTransportTarget classes
if arch == "v1arch":
    from pysnmp.hlapi.v1arch.asyncio import (
        UdpTransportTarget as _BaseUdpTransportTarget,
        Udp6TransportTarget as _BaseUdp6TransportTarget,
    )
elif arch == "v3arch":
    from pysnmp.hlapi.v3arch.asyncio import (
        UdpTransportTarget as _BaseUdpTransportTarget,
        Udp6TransportTarget as _BaseUdp6TransportTarget,
    )
else:
    raise ImportError(f"Unknown SNMP architecture: {arch}")

from pysnmp_sync_adapter import (
    get_cmd_sync, set_cmd_sync, next_cmd_sync,
    bulk_cmd_sync, walk_cmd_sync, bulk_walk_cmd_sync,
    create_transport
)
from pysnmp.proto.errind import RequestTimedOut


class UdpTransportTarget(_BaseUdpTransportTarget):
    """
    Wrapper for the legacy UdpTransportTarget class.
    """
    def __init__(self, *args, **kwargs):
        opts = {}

        if len(args) == 1 and isinstance(args[0], tuple):
            host_tuple = args[0]
            host = host_tuple[0]
            port = host_tuple[1]
            if len(host_tuple) > 2 and host_tuple[2] is not None:
                opts['timeout'] = host_tuple[2]
            if len(host_tuple) > 3 and host_tuple[3] is not None:
                opts['retries'] = host_tuple[3]
        elif len(args) >= 2:
            host_tuple = args[0]
            host, port = host_tuple
            if len(args) > 1 and args[1] is not None:
                opts['timeout'] = args[1]
            if len(args) > 2 and args[2] is not None:
                opts['retries'] = args[2]
        else:
            raise ValueError("Unsupported arguments for UdpTransportTarget")

        transport = create_transport(_BaseUdpTransportTarget, (host, port), **opts)
        self.__dict__ = transport.__dict__


class Udp6TransportTarget(_BaseUdp6TransportTarget):
    """
    Wrapper for the legacy Udp6TransportTarget class.
    """
    def __init__(self, *args, **kwargs):
        opts = {}

        if len(args) == 1 and isinstance(args[0], tuple):
            host_tuple = args[0]
            host = host_tuple[0]
            port = host_tuple[1]
            if len(host_tuple) > 2 and host_tuple[2] is not None:
                opts['timeout'] = host_tuple[2]
            if len(host_tuple) > 3 and host_tuple[3] is not None:
                opts['retries'] = host_tuple[3]
        elif len(args) >= 2:
            host_tuple = args[0]
            host, port = host_tuple
            if len(args) > 1 and args[1] is not None:
                opts['timeout'] = args[1]
            if len(args) > 2 and args[2] is not None:
                opts['retries'] = args[2]
        else:
            raise ValueError("Unsupported arguments for Udp6TransportTarget")

        transport = create_transport(_BaseUdp6TransportTarget, (host, port), **opts)
        self.__dict__ = transport.__dict__


def _wrap_sync_result(sync_func, *snmp_args, **snmp_kwargs):
    result = sync_func(*snmp_args, **snmp_kwargs)
    if result is None:
        return
    errInd, errStat, errIdx, varBinds = result
    if errInd:
        text = str(errInd)
        if isinstance(errInd, RequestTimedOut) and 'before timeout' in text:
            text += " - timed out"
        result = text, errStat, errIdx, varBinds
    yield result


def getCmd(*snmp_args, **snmp_kwargs):
    yield from _wrap_sync_result(get_cmd_sync, *snmp_args, **snmp_kwargs)


def setCmd(*snmp_args, **snmp_kwargs):
    yield from _wrap_sync_result(set_cmd_sync, *snmp_args, **snmp_kwargs)


def nextCmd(*snmp_args, **snmp_kwargs):
    yield from _wrap_sync_result(next_cmd_sync, *snmp_args, **snmp_kwargs)


def bulkCmd(*snmp_args, **snmp_kwargs):
    yield from _wrap_sync_result(bulk_cmd_sync, *snmp_args, **snmp_kwargs)


def walkCmd(*snmp_args, **snmp_kwargs):
    yield from _wrap_sync_result(walk_cmd_sync, *snmp_args, **snmp_kwargs)


def bulkWalkCmd(*snmp_args, **snmp_kwargs):
    yield from _wrap_sync_result(bulk_walk_cmd_sync, *snmp_args, **snmp_kwargs)
