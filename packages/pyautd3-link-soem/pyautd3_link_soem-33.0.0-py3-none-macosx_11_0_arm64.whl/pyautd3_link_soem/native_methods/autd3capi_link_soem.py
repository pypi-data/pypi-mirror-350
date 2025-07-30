import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3capi_driver import Duration, ResultLink, ResultStatus

from pyautd3_link_soem.native_methods.autd3_link_soem import Status


class EthernetAdaptersPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EthernetAdaptersPtr) and self._fields_ == other._fields_  # pragma: no cover


class ThreadPriorityPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ThreadPriorityPtr) and self._fields_ == other._fields_  # pragma: no cover


class SOEMOption(ctypes.Structure):
    _fields_ = [
        ("ifname", ctypes.c_char_p),
        ("buf_size", ctypes.c_uint32),
        ("send_cycle", Duration),
        ("sync0_cycle", Duration),
        ("sync_mode", ctypes.c_uint8),
        ("process_priority", ctypes.c_uint8),
        ("thread_priority", ThreadPriorityPtr),
        ("state_check_interval", Duration),
        ("timer_strategy", ctypes.c_uint8),
        ("sync_tolerance", Duration),
        ("sync_timeout", Duration),
    ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SOEMOption) and self._fields_ == other._fields_  # pragma: no cover


class Singleton(type):
    _instances = {}  # type: ignore[var-annotated]
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_link_soem{bin_ext}"))

        self.dll.AUTDAdapterPointer.argtypes = []
        self.dll.AUTDAdapterPointer.restype = EthernetAdaptersPtr

        self.dll.AUTDAdapterGetSize.argtypes = [EthernetAdaptersPtr]
        self.dll.AUTDAdapterGetSize.restype = ctypes.c_uint32

        self.dll.AUTDAdapterGetAdapter.argtypes = [EthernetAdaptersPtr, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.AUTDAdapterGetAdapter.restype = None

        self.dll.AUTDAdapterPointerDelete.argtypes = [EthernetAdaptersPtr]
        self.dll.AUTDAdapterPointerDelete.restype = None

        self.dll.AUTDLinkSOEMTracingInit.argtypes = []
        self.dll.AUTDLinkSOEMTracingInit.restype = None

        self.dll.AUTDLinkSOEMTracingInitWithFile.argtypes = [ctypes.c_char_p]
        self.dll.AUTDLinkSOEMTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDLinkSOEM.argtypes = [ctypes.c_void_p, ctypes.c_void_p, SOEMOption]
        self.dll.AUTDLinkSOEM.restype = ResultLink

        self.dll.AUTDLinkSOEMIsDefault.argtypes = [SOEMOption]
        self.dll.AUTDLinkSOEMIsDefault.restype = ctypes.c_bool

        self.dll.AUTDLinkSOEMStatusGetMsg.argtypes = [ctypes.c_uint8, ctypes.c_char_p]
        self.dll.AUTDLinkSOEMStatusGetMsg.restype = ctypes.c_uint32

        self.dll.AUTDLinkRemoteSOEM.argtypes = [ctypes.c_char_p]
        self.dll.AUTDLinkRemoteSOEM.restype = ResultLink

        self.dll.AUTDLinkSOEMThreadPriorityMin.argtypes = []
        self.dll.AUTDLinkSOEMThreadPriorityMin.restype = ThreadPriorityPtr

        self.dll.AUTDLinkSOEMThreadPriorityCrossplatform.argtypes = [ctypes.c_uint8]
        self.dll.AUTDLinkSOEMThreadPriorityCrossplatform.restype = ThreadPriorityPtr

        self.dll.AUTDLinkSOEMThreadPriorityMax.argtypes = []
        self.dll.AUTDLinkSOEMThreadPriorityMax.restype = ThreadPriorityPtr

    def adapter_pointer(self) -> EthernetAdaptersPtr:
        return self.dll.AUTDAdapterPointer()

    def adapter_get_size(self, adapters: EthernetAdaptersPtr) -> ctypes.c_uint32:
        return self.dll.AUTDAdapterGetSize(adapters)

    def adapter_get_adapter(self, adapters: EthernetAdaptersPtr, idx: int, desc: bytes, name: bytes) -> None:
        return self.dll.AUTDAdapterGetAdapter(adapters, idx, desc, name)

    def adapter_pointer_delete(self, adapters: EthernetAdaptersPtr) -> None:
        return self.dll.AUTDAdapterPointerDelete(adapters)

    def link_soem_tracing_init(self) -> None:
        return self.dll.AUTDLinkSOEMTracingInit()

    def link_soem_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDLinkSOEMTracingInitWithFile(path)

    def link_soem(self, err_handler: ctypes.c_void_p, err_context: ctypes.c_void_p, option: SOEMOption) -> ResultLink:
        return self.dll.AUTDLinkSOEM(err_handler, err_context, option)

    def link_soem_is_default(self, option: SOEMOption) -> ctypes.c_bool:
        return self.dll.AUTDLinkSOEMIsDefault(option)

    def link_soem_status_get_msg(self, src: Status, dst: bytes) -> ctypes.c_uint32:
        return self.dll.AUTDLinkSOEMStatusGetMsg(src, dst)

    def link_remote_soem(self, addr: bytes) -> ResultLink:
        return self.dll.AUTDLinkRemoteSOEM(addr)

    def link_soem_thread_priority_min(self) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkSOEMThreadPriorityMin()

    def link_soem_thread_priority_crossplatform(self, value: int) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkSOEMThreadPriorityCrossplatform(value)

    def link_soem_thread_priority_max(self) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkSOEMThreadPriorityMax()
