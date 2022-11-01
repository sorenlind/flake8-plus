from typing import Callable


class SomeClass:
    def some_func(self) -> Callable[..., int]:
        def inner_func() -> int:
            return 27

        return inner_func
