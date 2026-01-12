def count_palindromic_substrings(s):
    """
    Counts how many substrings of s are palindromes.
    Uses dynamic programming (DP).

    Example:
    s = "aaa"
    palindromic substrings are: "a","a","a","aa","aa","aaa" -> 6
    """
    if s is None:
        raise ValueError("Input text cannot be None")

    s = str(s)
    n = len(s)
    if n == 0:
        return 0

    # dp[i][j] = True if s[i:j+1] is palindrome
    dp = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(False)
        dp.append(row)

    count = 0

    # length 1
    for i in range(n):
        dp[i][i] = True
        count += 1

    # length 2..n
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                if length == 2:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i + 1][j - 1]

            if dp[i][j]:
                count += 1

    return count

def palindromic_substrings(s):
    if s is None:
        raise ValueError("Input cannot be None")

    s = str(s)
    n = len(s)
    if n == 0:
        return [], 0

    dp = [[False] * n for _ in range(n)]
    found = []

    # length 1
    for i in range(n):
        dp[i][i] = True
        found.append(s[i])

    # length 2..n
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    found.append(s[i:j+1])

    return found, len(found)