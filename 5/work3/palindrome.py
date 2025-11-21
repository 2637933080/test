def is_palindrome(s):
    """
    判断字符串是否为回文
    
    Args:
        s (str): 待检测的字符串
    
    Returns:
        bool: 如果是回文返回True，否则返回False
    """
    # 移除空格并转换为小写
    cleaned = ''.join(s.split()).lower()
    # 比较字符串与其反转
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    # 示例用法
    test_strings = ["level", "hello", "A man a plan a canal Panama", "race a car"]
    for string in test_strings:
        result = is_palindrome(string)
        print(f"'{string}' is {'a palindrome' if result else 'not a palindrome'}")