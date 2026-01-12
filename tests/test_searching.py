import pytest
from algorithms_files.searching import compute_statistics


def test_basic_odd_with_mode():
    # sorted: [1,2,2,5,9]
    stats = compute_statistics([5, 2, 2, 9, 1])
    assert stats["smallest"] == 1
    assert stats["largest"] == 9
    assert stats["median"] == 2
    assert stats["q1"] == 1.5
    assert stats["q3"] == 7.0
    assert stats["mode"] == [2]


def test_even_no_mode():
    # sorted: [1,2,3,4]
    stats = compute_statistics([1, 2, 3, 4])
    assert stats["smallest"] == 1
    assert stats["largest"] == 4
    assert stats["median"] == 2.5
    assert stats["q1"] == 1.5
    assert stats["q3"] == 3.5
    assert stats["mode"] is None


def test_multiple_modes():
    # 1 and 2 appear twice
    stats = compute_statistics([1, 1, 2, 2, 3])
    assert stats["mode"] == [1, 2]


def test_all_same():
    stats = compute_statistics([7, 7, 7, 7])
    assert stats["smallest"] == 7
    assert stats["largest"] == 7
    assert stats["median"] == 7
    assert stats["q1"] == 7
    assert stats["q3"] == 7
    assert stats["mode"] == [7]


def test_two_values():
    # sorted [10, 20]
    stats = compute_statistics([20, 10])
    assert stats["smallest"] == 10
    assert stats["largest"] == 20
    assert stats["median"] == 15
    assert stats["q1"] == 10
    assert stats["q3"] == 20
    assert stats["mode"] is None


def test_negative_numbers():
    stats = compute_statistics([-5, -1, -3, -3, -2])
    assert stats["smallest"] == -5
    assert stats["largest"] == -1
    assert stats["median"] == -3
    assert stats["mode"] == [-3]


def test_empty_raises():
    with pytest.raises(ValueError):
        compute_statistics([])


def test_none_raises():
    with pytest.raises(ValueError):
        compute_statistics(None)
