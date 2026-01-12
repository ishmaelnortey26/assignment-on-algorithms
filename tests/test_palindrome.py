import pytest
from algorithms_files.palindrome import count_palindromic_substrings

def test_empty():
    assert count_palindromic_substrings("") == 0

def test_single_char():
    assert count_palindromic_substrings("a") == 1

def test_aaa():
    # "a","a","a","aa","aa","aaa" = 6
    assert count_palindromic_substrings("aaa") == 6

def test_abc():
    # only "a","b","c"
    assert count_palindromic_substrings("abc") == 3

def test_abba():
    # "a","b","b","a","bb","abba" = 6
    assert count_palindromic_substrings("abba") == 6

def test_none():
    with pytest.raises(ValueError):
        count_palindromic_substrings(None)
