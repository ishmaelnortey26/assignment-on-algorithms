def factorial(n):
    """
    Computes the factorial of a non-negative integer using recursion.

    """
    if n < 0:
        raise ValueError("number must be positive")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)