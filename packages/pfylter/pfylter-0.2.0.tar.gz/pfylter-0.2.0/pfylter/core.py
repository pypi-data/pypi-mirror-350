from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar('T')

class AbstractFilter(ABC, Generic[T]):
    def apply(self, elements: List[T]) -> List[T]:
        return [e for e in elements if self.keep(e)]

    @abstractmethod
    def keep(self, instance: T) -> bool:
        pass


class AllFilters(AbstractFilter[T]):
    def __init__(self, filters: List[AbstractFilter[T]]) -> None:
        self.filters = filters

    def keep(self, instance: T) -> bool:
        return all(f.keep(instance) for f in self.filters)


class AnyFilter(AbstractFilter[T]):
    def __init__(self, filters: List[AbstractFilter[T]]) -> None:
        self.filters = filters

    def keep(self, instance: T) -> bool:
        return any(f.keep(instance) for f in self.filters)


class NotFilter(AbstractFilter[T]):
    def __init__(self, base_filter: AbstractFilter[T]) -> None:
        self.base_filter = base_filter

    def keep(self, instance: T) -> bool:
        return not self.base_filter.keep(instance)

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

    class ExcludeFilter(AbstractFilter[str]):
        def __init__(self, substring: str) -> None:
            self.substring = substring

        def keep(self, instance: str) -> bool:
            return self.substring in instance

    print(AllFilters([ExcludeFilter('BC')]).apply(example))

    class ExcludeLengthFilter(AbstractFilter[str]):
        def __init__(self, length: int) -> None:
            self.length = length

        def keep(self, instance: str) -> bool:
            return len(instance) == self.length

    print(AllFilters([ExcludeLengthFilter(1)]).apply(example))

    # Two alternatives to exclude any string that includes 'BC' or has length 1:
    # 1. Using AllFilters with NotFilter(filter)
    print('Exclude any string that includes BC or has length 1')
    print(AllFilters([NotFilter(LenFilter(1)), NotFilter(ExcludeFilter('BC'))]).apply(example))
    # 2. Using NotFilter with AnyFilter
    print(NotFilter(AnyFilter([ExcludeFilter('BC'), ExcludeLengthFilter(1)])).apply(example))
