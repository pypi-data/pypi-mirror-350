import abc
import json
import os
import typing
from datetime import timedelta, datetime
from threading import Lock

from .utils import FrozenModel


class ICache(abc.ABC):
    @abc.abstractmethod
    def store(self, *, key: str, value: typing.Any, ttl: timedelta) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch(self, *, key: str) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_segment(self, *, segment: str) -> typing.Self:
        raise NotImplementedError


class JSONCache(ICache):
    class _CacheValue(FrozenModel):
        value: typing.Any
        expiration: datetime

    def __init__(self, *, dir_path: str):
        self._dir_path = dir_path
        self._lock = Lock()
        self._cache: typing.Dict[str, JSONCache._CacheValue] = {}

        try:
            with open(os.path.join(self._dir_path, "cache.json"), "r") as f:
                self._cache.update({key: JSONCache._CacheValue(**val) for key, val in json.load(f).items()})
        except FileNotFoundError:
            pass

    def store(self, *, key: str, value: typing.Any, ttl: timedelta) -> None:
        with self._lock:
            self._cache[key] = JSONCache._CacheValue(value=value, expiration=datetime.now() + ttl)

            os.makedirs(self._dir_path, exist_ok=True)

            with open(os.path.join(self._dir_path, "cache.json"), "w") as f:
                json.dump({key: value.model_dump(mode="json") for key, value in self._cache.items()}, f)

    def fetch(self, *, key: str) -> typing.Any:
        if value := self._cache.get(key):
            if datetime.now() < value.expiration:
                return value.value

        raise LookupError

    def get_segment(self, *, segment: str) -> typing.Self:
        return JSONCache(dir_path=os.path.join(self._dir_path, segment))
