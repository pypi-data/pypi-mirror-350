import threading
from collections import defaultdict
from threading import local as TLocal


class GLocal:
    __slots__ = ("__storage__", "__ident_func__")

    def __init__(self):
        try:
            from greenlet import getcurrent as get_ident  # type: ignore
        except ImportError:
            from threading import get_ident as get_ident
        object.__setattr__(self, "__storage__", defaultdict(lambda: {}))
        object.__setattr__(self, "__ident_func__", get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    @property
    def ident(self):
        return self.__ident_func__()

    @property
    def storage(self) -> dict:
        return self.__storage__[self.ident]

    def release(self):
        self.__release_local__()


class Local(TLocal):
    def __init__(self):
        super(__class__, self).__init__()
        super(__class__, self).__setattr__("_local", GLocal())

    def __getattr__(self, name):
        return getattr(self._local, name)

    def __setattr__(self, name, value):
        if isinstance(getattr(__class__, name, None), property):
            raise AttributeError("can't set attribute")
        return setattr(self._local, name, value)

    def __delattr__(self, name):
        return delattr(self._local, name)


local = Local()
request = Local()

__execution_lock = threading.Lock()


def require_execution_lock():
    __execution_lock.acquire()


def release_execution_lock():
    __execution_lock.release()
