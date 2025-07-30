import pyautd3

from pyautd3_link_soem.native_methods.autd3_link_soem import ProcessPriority, SyncMode, TimerStrategy
from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as Soem

from .adapter import EtherCATAdapter
from .local import SOEM, SOEMOption
from .remote import RemoteSOEM
from .status import Status
from .thread_priority import ThreadPriority

pyautd3._ext_tracing_init.append(lambda: Soem().link_soem_tracing_init())


__all__ = [
    "SOEM",
    "EtherCATAdapter",
    "ProcessPriority",
    "RemoteSOEM",
    "SOEMOption",
    "Status",
    "SyncMode",
    "ThreadPriority",
    "TimerStrategy",
]


__version__ = "33.0.0"
