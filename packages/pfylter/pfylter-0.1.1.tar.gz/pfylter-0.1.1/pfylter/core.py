from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar('T')

class AbstractFilter(ABC, Generic[T]):
    @abstractmethod
    def keep(self, instance: T) -> bool:
        pass


class AllFilters(AbstractFilter[T]):
    def __init__(self, filters: List[AbstractFilter[T]]) -> None:
        self.filters = filters

    def keep(self, instance: T) -> bool:
        return all(f.keep(instance) for f in self.filters)

    def apply(self, elements: List[T]) -> List[T]:
        return [e for e in elements if self.keep(e)]


class AnyFilter(AbstractFilter[T]):
    def __init__(self, filters: List[AbstractFilter[T]]) -> None:
        self.filters = filters

    def keep(self, instance: T) -> bool:
        return any(f.keep(instance) for f in self.filters)

    def apply(self, elements: List[T]) -> List[T]:
        return [e for e in elements if self.keep(e)]


if __name__ == '__main__':
    class LenFilter(AbstractFilter[str]):
        def __init__(self, length: int) -> None:
            self.length = length

        def keep(self, instance: str) -> bool:
            return len(instance) == self.length


    class StartsWithFilter(AbstractFilter[str]):
        def __init__(self, start: str) -> None:
            self.start = start

        def keep(self, instance: str) -> bool:
            return instance.startswith(self.start)

    example = ['A', 'ABCD', 'B', 'BCDE', 'C', 'AAAAAAA']
    print(AllFilters([LenFilter(4), StartsWithFilter('A')]).apply(example))
    print(AnyFilter([LenFilter(4), StartsWithFilter('A')]).apply(example))

    print(AnyFilter(
            [AllFilters([LenFilter(4), StartsWithFilter('A')]),
            AllFilters([LenFilter(1), StartsWithFilter('B')])]
        ).apply(example))

    print(
       AllFilters([StartsWithFilter("A"), AnyFilter([LenFilter(1), LenFilter(4)])]).apply(example)
    )
