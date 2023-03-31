from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager, AbstractContextManager
from random import randint

from lockable_dict import lockable_dict, LockableDict, LockedError
from mycontextlib import mycontextmanager


# @contextmanager
@mycontextmanager
def lock(lockable_dict: LockableDict) -> Generator[LockableDict | None, None, None]:
    try:
        locked = lockable_dict.lock()
    except LockedError as e:
        print(f"locked! {e}")
        locked = None

    try:
        yield locked
    except LockedError as e:
        print(f"locked! {e}")

    if locked:
        locked.unlock()


def do_stuff(lockable_dict: LockableDict) -> None:
    rand_val = randint(0, 9)
    if rand_val % 2:
        lockable_dict["odd_val"] = rand_val
    else:
        print(f"do_stuff: {rand_val=}")


if __name__ == "__main__":
    from pprint import pprint

    lockable_dict.update(x=1, y=2)
    pprint(lockable_dict)
    breakpoint()
    for _ in range(10):
        with lock(lockable_dict) as locked:
            if locked:
                do_stuff(locked)
