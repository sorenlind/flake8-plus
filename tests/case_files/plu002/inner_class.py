class SomeClass:
    def some_func(self) -> type:
        class SomeInnerClass:
            pass

        return SomeInnerClass
