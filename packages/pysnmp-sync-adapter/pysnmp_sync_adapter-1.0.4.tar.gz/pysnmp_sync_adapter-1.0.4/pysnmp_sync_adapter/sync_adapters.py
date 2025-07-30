import os
import sys
import asyncio
import functools
import importlib

# Determine desired architecture:
# - honor PYSNMP_ARCH if set to 'v1arch' or 'v3arch',
# - otherwise auto-detect v3arch if its module is already loaded,
# - fallback to v1arch.
_env_arch = os.getenv("PYSNMP_ARCH", "").lower()
if _env_arch in ("v1arch", "v3arch"):
    arch = _env_arch
elif "pysnmp.hlapi.v3arch.asyncio" in sys.modules:
    arch = "v3arch"
else:
    arch = "v1arch"

# Import the selected asyncio HLAPI submodule
_mod = importlib.import_module("pysnmp.hlapi." + arch + ".asyncio")

# Bind symbols
UdpTransportTarget = _mod.UdpTransportTarget
Udp6TransportTarget = _mod.Udp6TransportTarget
get_cmd = _mod.get_cmd
next_cmd = _mod.next_cmd
set_cmd = _mod.set_cmd
bulk_cmd = _mod.bulk_cmd
walk_cmd = _mod.walk_cmd
bulk_walk_cmd = _mod.bulk_walk_cmd


# Event loop & transport helpers
def ensure_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def create_transport(transport_cls, *args, **kwargs):
    """
    Synchronously await the async factory on the given transport class.

    Example for IPv4:
    create_transport(UdpTransportTarget, ("demo.pysnmp.com", 161), timeout=2)

    Example for IPv6:
    create_transport(Udp6TransportTarget, ("2001:db8::1", 161), timeout=2)
    """
    loop = ensure_loop()
    # transport_cls.create is an async factory
    coro = transport_cls.create(*args, **kwargs)
    return loop.run_until_complete(coro)


# Sync runners
def _sync_coro(coro, timeout=None):
    """
    Run the given coroutine to completion on the shared loop,
    scheduling if needed. Supports timeout in seconds.
    """
    loop = ensure_loop()
    wrapped = asyncio.wait_for(coro, timeout=timeout)
    if loop.is_running():
        task = asyncio.ensure_future(wrapped)
        return loop.run_until_complete(task)
    return loop.run_until_complete(wrapped)


def _sync_agen(agen, timeout=None):
    """ Consume an async-generator into a list synchronously. """
    async def _collect():
        out = []
        async for item in agen:
            out.append(item)
        return out
    return _sync_coro(_collect(), timeout=timeout)


def make_sync(fn):
    """ Turn any pysnmp async‐HLAPI fn into a sync wrapper. """
    @functools.wraps(fn)
    def wrapper(*args, timeout=None, **kwargs):
        return _sync_coro(fn(*args, **kwargs), timeout=timeout)
    return wrapper


# Exposed sync API
get_cmd_sync = make_sync(get_cmd)
next_cmd_sync = make_sync(next_cmd)
set_cmd_sync = make_sync(set_cmd)
bulk_cmd_sync = make_sync(bulk_cmd)


def walk_cmd_sync(*args, timeout=None, **kwargs):
    """ Sync wrapper for walk_cmd (async generator). """
    return _sync_agen(walk_cmd(*args, **kwargs), timeout=timeout)


def bulk_walk_cmd_sync(*args, timeout=None, **kwargs):
    """ Sync wrapper for bulk_walk_cmd (async generator). """
    return _sync_agen(bulk_walk_cmd(*args, **kwargs), timeout=timeout)
