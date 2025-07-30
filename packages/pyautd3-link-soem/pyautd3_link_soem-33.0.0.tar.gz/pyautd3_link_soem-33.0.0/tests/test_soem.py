import pytest
from pyautd3 import tracing_init

from pyautd3_link_soem import SOEM, RemoteSOEM, Status, ThreadPriority
from pyautd3_link_soem.local import SOEMOption
from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as NativeSOEM
from pyautd3_link_soem.native_methods.autd3capi_link_soem import Status as Status_


def test_tracing_init():
    tracing_init()


def test_soem_adapers():
    adapters = SOEM.enumerate_adapters()
    for adapter in adapters:
        print(adapter)


def test_soem_thread_priority():
    _ = ThreadPriority.Max
    _ = ThreadPriority.Min
    _ = ThreadPriority.Crossplatform(0)
    _ = ThreadPriority.Crossplatform(99)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(-1)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = ThreadPriority.Crossplatform(100)


def test_status():
    lost = Status.Lost()
    state_change = Status.StateChanged()
    err = Status.Error()

    assert lost == Status.Lost()
    assert state_change == Status.StateChanged()
    assert err == Status.Error()
    assert lost != state_change
    assert lost != err
    assert lost != Status_.Lost
    assert state_change != err
    assert state_change != lost
    assert state_change != Status_.StateChanged
    assert err != lost
    assert err != state_change
    assert err != Status_.Error

    status = Status.__private_new__(Status_.Lost, "lost")
    assert status == Status.Lost()
    assert str(status) == "lost"

    with pytest.raises(NotImplementedError):
        _ = Status()


def test_soem_is_default():
    assert NativeSOEM().link_soem_is_default(SOEMOption()._inner())


def test_soem():
    def err_handler(slave: int, status: Status) -> None:
        print(f"slave: {slave}, status: {status}")

    _ = SOEM(err_handler, SOEMOption())


def test_remote_soem():
    _ = RemoteSOEM("127.0.0.1:8080")
