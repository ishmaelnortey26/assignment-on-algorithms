from algorithms_files.selection import selection_sort


def test_selection_sort_ascending():
    assert selection_sort([5, 2, 9, 1]) == [1, 2, 5, 9]
    assert selection_sort([9, 9, 1]) == [1, 9, 9]
    assert selection_sort([]) == []

def test_selection_sort_descending():
    assert selection_sort([5, 2, 9, 1], descending=True) == [9, 5, 2, 1]
    assert selection_sort([10, 5, 2], descending=True) == [10, 5, 2]