import pytest
from palindrome import is_palindrome


def test_simple_palindrome():
    """测试简单回文"""
    assert is_palindrome("level") == True


def test_non_palindrome():
    """测试非回文"""
    assert is_palindrome("hello") == False


def test_palindrome_with_spaces():
    """测试带空格的回文"""
    assert is_palindrome("A man a plan a canal Panama") == True


def test_palindrome_mixed_case():
    """测试大小写混合的回文"""
    assert is_palindrome("RaceCar") == True


def test_empty_string():
    """测试空字符串"""
    assert is_palindrome("") == True


def test_single_character():
    """测试单个字符"""
    assert is_palindrome("a") == True


def test_palindrome_with_punctuation():
    """测试带标点符号的回文"""
    assert is_palindrome("A man, a plan, a canal: Panama!") == True


if __name__ == "__main__":
    pytest.main([__file__])