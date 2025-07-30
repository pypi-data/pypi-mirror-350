import contextlib
from collections import OrderedDict
from typing import Any

from sag_py_cache_decorator.cache.key import KEY


class LRU(OrderedDict):  # type: ignore
    """A Least recently used cache.
    The longest unused cached parameter result is deleted after the max size is reached.
    """

    def __init__(self, maxsize: int | None, *args: Any, **kwargs: Any) -> None:
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def remove_by_key(self, key: KEY) -> None:
        with contextlib.suppress(KeyError):
            del self[key]

    def __getitem__(self, key: KEY) -> Any:
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key: KEY, value: Any) -> None:
        super().__setitem__(key, value)
        self._remove_oldest_if_max_reached()

    def _remove_oldest_if_max_reached(self) -> None:
        if self.maxsize and len(self) > self.maxsize:
            oldest = next(iter(self))
            self.remove_by_key(oldest)
