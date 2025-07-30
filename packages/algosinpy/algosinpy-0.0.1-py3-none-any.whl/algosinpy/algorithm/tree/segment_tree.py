# Segment Tree: is a range queries algorithm.
# we can find maximum/minimum sum/value in a given range

import math
from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


class SegmentTree:
    tree = []
    size = int(0)
    array = []

    def __init__(self, array=None):
        self.array = array
        self.size = len(self.array)
        self.tree = [-math.inf] * (self.size * 3 + 1)  # need 3x space of array size

    def query(self, lower_index, higher_index, start, end, segment):
        if start <= lower_index and end >= higher_index:
            return self.tree[segment]
        elif start > higher_index or end < lower_index:
            return -math.inf
        else:
            mid = (lower_index + higher_index) // 2
            return max(
                self.query(lower_index, mid, start, end, segment * 2),
                self.query(mid + 1, higher_index, start, end, segment * 2 + 1),
            )

    def build(self, lower_index, higher_index, segment):
        if lower_index == higher_index:
            self.tree[segment] = self.array[lower_index]
            return self.tree[segment]
        mid = (lower_index + higher_index) // 2
        self.tree[segment] = max(
            self.build(lower_index, mid, segment * 2),
            self.build(mid + 1, higher_index, segment * 2 + 1),
        )  # max operation to update maximum value for every range;
        return self.tree[segment]


if __name__ == "__main__":
    import time

    started = time.process_time()
    obj = SegmentTree([1, -2, 4, -1, 6, 2])
    obj.build(0, obj.size - 1, 1)
    logger.info(f"Maximum in range {[4, 5]}: {obj.query(0, obj.size - 1, 4, 5, 1)}")
    logger.info(f"Segment Tree: {obj.tree}")
    logger.info(f"Process time: {time.process_time() - started} seconds")
