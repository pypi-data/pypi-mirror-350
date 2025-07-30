import abc

from pysnmp.hlapi.v1arch.asyncio import UdpTransportTarget as _BaseUdpTransportTarget
from pysnmp_sync_adapter import (
    get_cmd_sync, set_cmd_sync, next_cmd_sync,
    bulk_cmd_sync, walk_cmd_sync, bulk_walk_cmd_sync,
    create_transport
)
from pysnmp.proto.errind import RequestTimedOut


class UdpTransportTarget(_BaseUdpTransportTarget):
    """
    Wrapper for the legacy UdpTransportTarget class, supporting both:
    - UdpTransportTarget(("host", port, [timeout, [retries]]))
    - UdpTransportTarget(("host", port), timeout, retries)
    """
    def __init__(self, *args, **kwargs):
        opts = {}

        if len(args) == 1 and isinstance(args[0], tuple):
            # ("host", port, timeout, retries)
            host_tuple = args[0]
            host = host_tuple[0]
            port = host_tuple[1]
            if len(host_tuple) > 2 and host_tuple[2] is not None:
                opts['timeout'] = host_tuple[2]
            if len(host_tuple) > 3 and host_tuple[3] is not None:
                opts['retries'] = host_tuple[3]
        elif len(args) >= 2:
            # Possibly ("host", port), timeout, retries
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
    """
    HLAPI-compatible iterator wrapper around get_cmd_sync.
    """
    yield from _wrap_sync_result(get_cmd_sync, *snmp_args, **snmp_kwargs)


def setCmd(*snmp_args, **snmp_kwargs):
    """
    HLAPI-compatible iterator wrapper around set_cmd_sync.
    """
    yield from _wrap_sync_result(set_cmd_sync, *snmp_args, **snmp_kwargs)


def nextCmd(*snmp_args, **snmp_kwargs):
    """
    HLAPI-compatible iterator wrapper around next_cmd_sync.
    """
    yield from _wrap_sync_result(next_cmd_sync, *snmp_args, **snmp_kwargs)


def bulkCmd(*snmp_args, **snmp_kwargs):
    """
    HLAPI-compatible iterator wrapper around bulk_cmd_sync.
    """
    yield from _wrap_sync_result(bulk_cmd_sync, *snmp_args, **snmp_kwargs)


def walkCmd(*snmp_args, **snmp_kwargs):
    """
    HLAPI-compatible iterator wrapper around walk_cmd_sync.
    """
    yield from _wrap_sync_result(walk_cmd_sync, *snmp_args, **snmp_kwargs)


def bulkWalkCmd(*snmp_args, **snmp_kwargs):
    """
    HLAPI-compatible iterator wrapper around bulk_walk_cmd_sync.
    """
    yield from _wrap_sync_result(bulk_walk_cmd_sync, *snmp_args, **snmp_kwargs)
