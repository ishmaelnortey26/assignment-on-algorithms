import pytest
from algorithms_files.merge_sorting import merge_sort

def test_merge_sort_ascending():
    assert merge_sort([5, 2, 9, 1]) == [1, 2, 5, 9]
    assert merge_sort([]) == []
    assert merge_sort([3]) == [3]
    assert merge_sort([2, 2, 1]) == [1, 2, 2]

def test_merge_sort_descending():
    assert merge_sort([5, 2, 9, 1], descending=True) == [9, 5, 2, 1]
    assert merge_sort([2, 2, 1], descending=True) == [2, 2, 1]

def test_merge_sort_none():
    with pytest.raises(ValueError):
        merge_sort(None)
