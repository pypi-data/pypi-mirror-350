import pytest
from pfylter.core import AllFilters, AnyFilter, AbstractFilter
from pfylter.strings import LenFilter, StartsWithFilter, ContainsFilter, NotFilter

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

@pytest.fixture
def string_values():
    return ['A', 'ABCD', 'B', 'BCDE', 'C', 'AAAAAAA']

def test_contains_filter(string_values):
    f = ContainsFilter('BC')
    assert f.apply(string_values) == ['ABCD', 'BCDE']

def test_len_filter(string_values):
    f = LenFilter(1)
    assert f.apply(string_values) == ['A', 'B', 'C']

def test_not_len_filter(string_values):
    f = NotFilter(LenFilter(1))
    assert f.apply(string_values) == ['ABCD', 'BCDE', 'AAAAAAA']

def test_all_filters_string(string_values):
    f = AllFilters([LenFilter(4), StartsWithFilter('A')])
    assert f.apply(string_values) == ['ABCD']

def test_any_filters_string(string_values):
    f = AnyFilter([LenFilter(4), StartsWithFilter('A')])
    assert f.apply(string_values) == ['A', 'ABCD', 'BCDE', 'AAAAAAA']

def test_complex_any_all_filters_string(string_values):
    f = AnyFilter([
        AllFilters([LenFilter(4), StartsWithFilter('A')]),
        AllFilters([LenFilter(1), StartsWithFilter('B')])
    ])
    assert f.apply(string_values) == ['ABCD', 'B']

def test_all_filters_with_any(string_values):
    f = AllFilters([
        StartsWithFilter('A'),
        AnyFilter([LenFilter(1), LenFilter(4)])
    ])
    assert f.apply(string_values) == ['A', 'ABCD']

def test_exclude_bc_or_len1_allfilters(string_values):
    f = AllFilters([NotFilter(LenFilter(1)), NotFilter(ContainsFilter('BC'))])
    assert f.apply(string_values) == ['AAAAAAA']

def test_exclude_bc_or_len1_anyfilter(string_values):
    f = NotFilter(AnyFilter([ContainsFilter('BC'), LenFilter(1)]))
    assert f.apply(string_values) == ['AAAAAAA']
