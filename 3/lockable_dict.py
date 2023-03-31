from __future__ import annotations


class LockedError(Exception):
    ...


class LockableDict(dict[str, str | int]):
    locked: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locked = False

    def check_lock(self):
        if self.locked:
            raise LockedError()

    def __setitem__(self, key: str, value: str | int) -> None:
        self.check_lock()
        super().__setitem__(key, value)

    def lock(self) -> LockableDict:
        self.check_lock()
        self.locked = True
        return self

    def unlock(self) -> LockableDict:
        self.locked = False
        return self

lockable_dict = LockableDict()