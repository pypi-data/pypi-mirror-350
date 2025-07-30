from typing import Any, Union


class KEY:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

        # Remove/ignore the decorator args
        kwargs.pop("use_cache", None)
        kwargs.pop("clear_cache", None)
        kwargs.pop("clear_arg_cache", None)

    def __eq__(self, obj: Any) -> bool:
        return hash(self) == hash(obj)

    def __hash__(self) -> int:
        def _hash(param: Any) -> Union[str, Any]:
            if isinstance(param, tuple):
                return tuple(map(_hash, param))
            if isinstance(param, dict):
                return tuple(map(_hash, param.items()))
            elif hasattr(param, "__dict__"):
                return str(vars(param))
            else:
                return str(param)

        return hash(_hash(self.args) + _hash(self.kwargs))
