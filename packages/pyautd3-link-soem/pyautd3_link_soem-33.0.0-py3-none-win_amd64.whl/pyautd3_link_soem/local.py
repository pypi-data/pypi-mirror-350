import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr
from pyautd3.utils import Duration

from pyautd3_link_soem.adapter import EtherCATAdapter
from pyautd3_link_soem.native_methods.autd3_link_soem import ProcessPriority, SyncMode, TimerStrategy
from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3_link_soem.native_methods.autd3capi_link_soem import SOEMOption as SOEMOption_
from pyautd3_link_soem.native_methods.autd3capi_link_soem import Status as Status_
from pyautd3_link_soem.native_methods.autd3capi_link_soem import ThreadPriorityPtr
from pyautd3_link_soem.status import Status
from pyautd3_link_soem.thread_priority import ThreadPriority

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[arg-type]


class SOEMOption:
    ifname: str
    buf_size: int
    send_cycle: Duration
    sync0_cycle: Duration
    timer_strategy: TimerStrategy
    sync_mode: SyncMode
    sync_tolerance: Duration
    sync_timeout: Duration
    state_check_interval: Duration
    process_priority: ProcessPriority
    thread_priority: ThreadPriorityPtr

    def __init__(
        self: Self,
        *,
        ifname: str = "",
        buf_size: int = 32,
        send_cycle: Duration | None = None,
        sync0_cycle: Duration | None = None,
        timer_strategy: TimerStrategy = TimerStrategy.SpinSleep,
        sync_mode: SyncMode = SyncMode.DC,
        sync_tolerance: Duration | None = None,
        sync_timeout: Duration | None = None,
        state_check_interval: Duration | None = None,
        process_priority: ProcessPriority = ProcessPriority.High,
        thread_priority: ThreadPriorityPtr | None = None,
    ) -> None:
        self.ifname = ifname
        self.buf_size = buf_size
        self.send_cycle = send_cycle or Duration.from_millis(1)
        self.sync0_cycle = sync0_cycle or Duration.from_millis(1)
        self.timer_strategy = timer_strategy
        self.sync_mode = sync_mode
        self.sync_tolerance = sync_tolerance or Duration.from_micros(1)
        self.sync_timeout = sync_timeout or Duration.from_secs(10)
        self.state_check_interval = state_check_interval or Duration.from_millis(100)
        self.process_priority = process_priority
        self.thread_priority = thread_priority or ThreadPriority.Max

    def _inner(self: Self) -> SOEMOption_:
        return SOEMOption_(
            _to_null_terminated_utf8(self.ifname),
            self.buf_size,
            self.send_cycle._inner,
            self.sync0_cycle._inner,
            self.sync_mode,
            self.process_priority,
            self.thread_priority,
            self.state_check_interval._inner,
            self.timer_strategy,
            self.sync_tolerance._inner,
            self.sync_timeout._inner,
        )


class SOEM(Link):
    _err_handler: Callable[[int, Status], None]
    _option: SOEMOption

    @staticmethod
    def enumerate_adapters() -> list[EtherCATAdapter]:
        handle = LinkSOEM().adapter_pointer()
        size = LinkSOEM().adapter_get_size(handle)

        def get_adapter(i: int) -> EtherCATAdapter:
            sb_desc = bytes(bytearray(128))
            sb_name = bytes(bytearray(128))
            LinkSOEM().adapter_get_adapter(handle, i, sb_desc, sb_name)
            return EtherCATAdapter(sb_name.decode("utf-8").rstrip(" \t\r\n\0"), sb_desc.decode("utf-8").rstrip(" \t\r\n\0"))

        res = list(map(get_adapter, range(int(size))))

        LinkSOEM().adapter_pointer_delete(handle)

        return res

    def __init__(self: Self, err_handler: Callable[[int, Status], None], option: SOEMOption) -> None:
        super().__init__()
        self._err_handler = err_handler
        self._option = option

    def _resolve(self: Self) -> LinkPtr:
        def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8) -> None:  # pragma: no cover
            err = bytes(bytearray(128))  # pragma: no cover
            status_ = Status_(int(status))  # pragma: no cover
            LinkSOEM().link_soem_status_get_msg(status_, err)  # pragma: no cover
            self._err_handler(int(slave), Status.__private_new__(status_, err.decode("utf-8").rstrip(" \t\r\n\0")))  # pragma: no cover

        self._err_handler_f = ErrHandlerFunc(callback_native)  # pragma: no cover

        return _validate_ptr(  # pragma: no cover
            LinkSOEM().link_soem(
                self._err_handler_f,  # type: ignore[arg-type]
                ctypes.c_void_p(0),
                self._option._inner(),
            ),
        )
