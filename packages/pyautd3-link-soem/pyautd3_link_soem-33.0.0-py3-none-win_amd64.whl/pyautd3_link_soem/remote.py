from typing import Self

from pyautd3.driver.link import Link
from pyautd3.native_methods.autd3capi_driver import LinkPtr
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr

from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM


class RemoteSOEM(Link):
    addr: str

    def __init__(self: Self, addr: str) -> None:
        super().__init__()
        self.addr = addr

    def _resolve(self: Self) -> LinkPtr:
        return _validate_ptr(LinkSOEM().link_remote_soem(_to_null_terminated_utf8(self.addr)))  # pragma: no cover
