# LCS: Longest Common Subsequence
from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


def iterative_lcs(var1, var2):
    """
    :param var1: variable
    :param var2: 2nd variable to compare and finding common sequence
    :return: return length of longest common subsequence

    examples:
    >>> iterative_lcs("abcd", "abxbxbc")
    3
    >>> iterative_lcs([1, 2, 4, 3], [1, 2, 3, 4])
    3
    """
    length1 = len(var1)
    length2 = len(var2)
    dp = [[0] * (length2 + 1) for _ in range(length1 + 1)]

    for i in range(length1 + 1):
        for j in range(length2 + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif var1[i - 1] == var2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
    return dp[length1][length2]


def recursive_lcs(var1, var2, length1, length2):
    """
    :param var1: variable
    :param var2: 2nd variable to compare and finding longest common sub seqeuence
    :param length1: length of variable
    :param length2: length of 2nd variable
    :return: return length of longest common subsequence

    examples:
    >>> recursive_lcs("abcd", "abxbxbc", 4, 7)
    3
    >>> recursive_lcs([1, 2, 4, 3], [1, 2, 3, 4], 4, 4)
    3
    """
    if length1 == 0 or length2 == 0:
        return 0
    elif var1[length1 - 1] == var2[length2 - 1]:
        return 1 + recursive_lcs(var1, var2, length1 - 1, length2 - 1)
    else:
        return max(
            recursive_lcs(var1, var2, length1, length2 - 1),
            recursive_lcs(var1, var2, length1 - 1, length2),
        )


if __name__ == "__main__":
    import doctest
    import time

    doctest.testmod()
    start = time.process_time()
    logger.info(f" lcs length: {iterative_lcs([1, 3, 2, 5], [1, 4, 2, 3, 5])}")
    logger.info(f"Processed time: {time.process_time() - start} seconds")
    start = time.process_time()
    logger.info(f" lcs length: {recursive_lcs([1, 3, 2, 5], [1, 4, 2, 3, 5], 4, 5)}")
    logger.info(f"Processed time: {time.process_time() - start} seconds")
