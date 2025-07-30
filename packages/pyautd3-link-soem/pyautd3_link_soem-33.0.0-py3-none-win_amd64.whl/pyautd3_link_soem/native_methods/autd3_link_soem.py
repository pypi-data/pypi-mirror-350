import enum


class Status(enum.IntEnum):
    Error = 0
    Lost = 1
    StateChanged = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class ProcessPriority(enum.IntEnum):
    Idle = 0
    BelowNormal = 1
    Normal = 2
    AboveNormal = 3
    High = 4
    Realtime = 5

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class SyncMode(enum.IntEnum):
    DC = 0
    FreeRun = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class TimerStrategy(enum.IntEnum):
    SpinSleep = 0
    StdSleep = 1
    SpinWait = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover
