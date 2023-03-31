from collections.abc import Generator
from contextlib import AbstractContextManager
from functools import wraps
from types import TracebackType
from typing import Any, Callable, ParamSpec, TypeVar, Generic

P = ParamSpec('P')
T = TypeVar('T')

class MyContextManager(AbstractContextManager, Generic[T, P]):
    f: Callable[P, Generator[T, None, None]]
    g: Generator[T, None, None] | None = None

    def __init__(self, f: Callable[P, Generator[T, None, None]]) -> None:
        self.f = f
    
    def _start(self, *args: P.args, **kwargs: P.kwargs) -> None:
        self.g = self.f(*args, **kwargs)
        self.t = next(self.g)
    
    def __enter__(self) -> T:
        return self.t

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> bool | None:
        if self.g and exc_type is not None:
            self.g.throw(exc_type, exc_value, traceback)
        return True
        
def mycontextmanager(f: Callable[P, Generator[T, None, None]]) -> Callable[P, MyContextManager[T,P]]:
    manager = MyContextManager(f)
    @wraps(f)
    def _create(*args: P.args, **kwargs: P.kwargs) -> MyContextManager[T,P]:
        manager._start(*args, **kwargs)
        return manager
    
    return _create
