# LIS: Longest Increasing Subsequence

import math
from src.algosinpy.logger.py_logger import PyLogger
from src.algosinpy.algorithm.searching.binary_search import binary_search_index

logger = PyLogger.get_configured_logger()


def lis(list_of_number):
    """
    :param list_of_number: list of integer
    :return: return a longest strictly increasing subsequence with smallest value among all possible sequences

    examples:
    >>> lis([3, -2, 3, 1, 2, 5, 2, 4])
    [-2, 1, 2, 4]
    """

    index = []  # store the position of numbers in increasing sequence
    increasing_order = [math.inf for _ in list_of_number]
    lis_length = 0

    for i in range(len(list_of_number)):
        idx = binary_search_index(increasing_order, list_of_number[i])
        increasing_order[idx] = list_of_number[i]
        lis_length = max(lis_length, idx + 1)
        index.append(idx + 1)

    increasing_subsequence = [
        None for _ in range(lis_length)
    ]  # longest increasing subsequence

    for i in range(len(list_of_number) - 1, -1, -1):
        if index[i] == lis_length:
            lis_length -= 1
            increasing_subsequence[lis_length] = list_of_number[i]

    return increasing_subsequence


if __name__ == "__main__":
    import time
    import doctest

    doctest.testmod()

    start = time.process_time()
    logger.info(f"longest increasing subsequence: {lis([3, -2, 3, 1, 2, 5, 2, 4])}")
    logger.info("Process time: {} seconds".format(time.process_time() - start))
