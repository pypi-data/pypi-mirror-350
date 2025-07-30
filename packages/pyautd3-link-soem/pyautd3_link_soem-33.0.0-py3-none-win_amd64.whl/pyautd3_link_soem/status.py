from typing import Self

from pyautd3.native_methods.utils import ConstantADT

from pyautd3_link_soem.native_methods.autd3capi_link_soem import Status as Status_


class Status(metaclass=ConstantADT):
    _inner: Status_
    _msg: str

    @classmethod
    def __private_new__(cls: type["Status"], inner: Status_, msg: str) -> "Status":
        ins = super().__new__(cls)
        ins._inner = inner
        ins._msg = msg
        return ins

    def __new__(cls: type["Status"]) -> "Status":
        raise NotImplementedError

    def __repr__(self: Self) -> str:
        return f"{self._msg}"

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, Status):
            return False
        return self._inner == other._inner

    @staticmethod
    def Lost() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.Lost, "")

    @staticmethod
    def StateChanged() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.StateChanged, "")

    @staticmethod
    def Error() -> "Status":  # noqa: N802
        return Status.__private_new__(Status_.Error, "")
