import pytest
from streak import longest_positive_streak

def test_empty_list():
    """Test with an empty list, expecting 0."""
    assert longest_positive_streak([]) == 0

def test_multiple_streaks_longest_in_middle():
    """Test with multiple streaks to ensure the longest one is chosen."""
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_all_positive_numbers():
    """Test with a list of all positive numbers."""
    assert longest_positive_streak([1, 2, 3, 4, 5]) == 5

def test_with_zeros():
    """Test with zeros breaking the streaks."""
    assert longest_positive_streak([1, 2, 0, 3, 4, 0, 1]) == 2

def test_with_negatives():
    """Test with negative numbers breaking the streaks."""
    assert longest_positive_streak([1, 2, -3, 4, 5, -6, 7]) == 2

def test_no_positive_numbers():
    """Test with a list containing no positive numbers."""
    assert longest_positive_streak([-1, -2, -3, 0]) == 0

def test_single_element_list_positive():
    """Test with a single positive number."""
    assert longest_positive_streak([5]) == 1

def test_single_element_list_non_positive():
    """Test with a single non-positive number."""
    assert longest_positive_streak([-5]) == 0

def test_streak_at_the_beginning():
    """Test with the longest streak at the beginning."""
    assert longest_positive_streak([1, 2, 3, 0, 1, -2, 1]) == 3

def test_streak_at_the_end():
    """Test with the longest streak at the end."""
    assert longest_positive_streak([1, -2, 1, 2, 0, 1, 2, 3, 4]) == 4
