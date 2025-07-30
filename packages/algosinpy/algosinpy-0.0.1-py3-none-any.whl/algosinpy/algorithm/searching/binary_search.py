from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


def binary_search_index(list_of_numbers, target_value):
    """
    :param list_of_numbers: given current increasing subsequence numbers
    :param target_value: for which position to be fixed
    :return: right position of the given value on the list of numbers (from 0 to length - 1)

    examples:
    >>> binary_search_index([3, 4, 5, 9, 13, 21, 35, 144], 5)
    2
    """
    lower_index = 0  # set lower bound to 0 index
    higher_index = len(list_of_numbers) - 1  # set higher bound to list_length - 1

    while lower_index <= higher_index:
        mid_index = (lower_index + higher_index) // 2
        if (
            list_of_numbers[mid_index] >= target_value
        ):  # set > to avoid strictly increasing sub sequence
            higher_index = mid_index - 1
        else:
            lower_index = mid_index + 1

    return lower_index


if __name__ == "__main__":
    import time

    start = time.process_time()
    logger.info(f"Index for {5} in {[3, 4, 5]}: {binary_search_index([3, 4, 5], 5)}")
    logger.info(f"Process time: {time.process_time() - start} seconds")
