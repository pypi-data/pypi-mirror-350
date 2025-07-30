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


class LambdaFilter(AbstractFilter[T]):
    def __init__(self, func) -> None:
        self.func = func

    def keep(self, instance: T) -> bool:
        return self.func(instance)

if __name__ == '__main__':
    example = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print('Numbers greater than 5:')
    print(LambdaFilter(lambda x: x > 5).apply(example))

    print('Numbers equal or lower than 5:')
    print(NotFilter(LambdaFilter(lambda x: x > 5)).apply(example))
    
    print('Numbers greater than 5 and divisible by two:')
    print(AllFilters([LambdaFilter(lambda x: x > 5), LambdaFilter(lambda x: x % 2 == 0)]).apply(example))
    
    print('Numbers greater than 5 and divisible by three:')
    print(AllFilters([LambdaFilter(lambda x: x > 5), LambdaFilter(lambda x: x % 3 == 0)]).apply(example))
    
    print('Numbers greater than 5 or divisible by two:')
    print(AnyFilter([LambdaFilter(lambda x: x > 5), LambdaFilter(lambda x: x % 2 == 0)]).apply(example))
    
