import pytest
from pfylter.core import AllFilters, AnyFilter, AbstractFilter

class DummyFilter(AbstractFilter[int]):
    def keep(self, instance: int) -> bool:
        return instance > 5

class EvenFilter(AbstractFilter[int]):
    def keep(self, instance: int) -> bool:
        return instance % 2 == 0

@pytest.fixture
def values():
    return [1, 2, 3, 6, 7, 8]

def test_all_filters(values):
    all_filters = AllFilters([DummyFilter(), EvenFilter()])
    assert all_filters.apply(values) == [6, 8]

def test_any_filter(values):
    any_filter = AnyFilter([DummyFilter(), EvenFilter()])
    assert any_filter.apply(values) == [2, 6, 7, 8]
