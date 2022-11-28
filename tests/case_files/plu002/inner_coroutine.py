from typing import Any, Callable, Coroutine


def some_func() -> Callable[..., Coroutine[Any, Any, int]]:
    async def inner_func() -> int:
        return 27

    return inner_func
