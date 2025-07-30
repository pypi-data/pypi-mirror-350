import inspect
import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from sag_py_cache_decorator.cache.key import KEY
from sag_py_cache_decorator.cache.lru import LRU

logger = logging.getLogger(__name__)

# With python 3.10 param spec can be used instead - as described here:
# https://stackoverflow.com/questions/66408662/type-annotations-for-decorators
F = TypeVar("F", bound=Callable[..., Any])


def lru_cache(maxsize: int | None = 128) -> Callable[[F], F]:
    cache = LRU(maxsize=maxsize)

    def decorator(func: F) -> F:
        setattr(func, "cache", cache)

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper_async(
                *args: Any,
                lru_use_cache: bool = True,
                lru_clear_cache: bool = False,
                lru_clear_arg_cache: bool = False,
                **kw: Any
            ) -> Any:
                key = KEY(args, kw)

                _clear_requested_cache_items(cache, lru_clear_cache, lru_clear_arg_cache, func, key)

                if not lru_use_cache:
                    logger.debug(
                        "Skipping cache for function %s with argument hash %s", func.__qualname__, key.__hash__
                    )
                    return await func(*args, **kw)

                if key in cache:
                    logger.debug(
                        "Using cached result for function %s with argument hash %s", func.__qualname__, key.__hash__
                    )
                    return cache[key]

                logger.debug(
                    "Executing function %s with argument hash %s and caching result", func.__qualname__, key.__hash__
                )
                cache[key] = await func(*args, **kw)
                return cache[key]

            return cast(F, wrapper_async)

        else:

            @wraps(func)
            def wrapper_sync(
                *args: Any,
                lru_use_cache: bool = True,
                lru_clear_cache: bool = False,
                lru_clear_arg_cache: bool = False,
                **kw: Any
            ) -> Any:
                key = KEY(args, kw)

                _clear_requested_cache_items(cache, lru_clear_cache, lru_clear_arg_cache, func, key)

                if not lru_use_cache:
                    logger.debug(
                        "Skipping cache for function %s with argument hash %s", func.__qualname__, key.__hash__
                    )
                    return func(*args, **kw)

                if key in cache:
                    logger.debug(
                        "Using cached result for function %s with argument hash %s", func.__qualname__, key.__hash__
                    )
                    return cache[key]

                logger.debug(
                    "Executing function %s with argument hash %s and caching result", func.__qualname__, key.__hash__
                )
                cache[key] = func(*args, **kw)
                return cache[key]

            return cast(F, wrapper_sync)

    return decorator


def _clear_requested_cache_items(
    cache: LRU, lru_clear_cache: bool, lru_clear_arg_cache: bool, func: F, key: KEY
) -> None:
    if lru_clear_cache:
        cache.clear()
        logger.debug("Cleared cache for function %s", func.__qualname__)

    if lru_clear_arg_cache:
        cache.remove_by_key(key)
        logger.debug("Cleared argument cache for function %s with argument hash %s", func.__qualname__, key.__hash__)
