from algorithms_files.bubble import bubble_sort

def test_bubble_sort_ascending():
    assert bubble_sort([5, 2, 9, 1]) == [1, 2, 5, 9]
    assert bubble_sort([]) == []
    assert bubble_sort([3]) == [3]
    assert bubble_sort([2, 2, 1]) == [1, 2, 2]

def test_bubble_sort_descending():
    assert bubble_sort([5, 2, 9, 1], descending=True) == [9, 5, 2, 1]

