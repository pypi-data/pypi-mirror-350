# BIT: Binary Indexed Tree or Fenwick Tree
# A range queries algorithm
from src.algosinpy.logger.py_logger import PyLogger

logger = PyLogger.get_configured_logger()


class BinaryIndexedTree:
    tree = []
    size = 0
    array = []

    def __init__(self, array=None):
        self.array = array
        self.size = len(array)
        self.tree = [0] * (self.size + 1)

    def query(self, index):
        """
        :param index: index of tree
        :return: summation from 1 to given index
        """
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & -index
        return total

    def update(self, index, value):
        """
        :param index: which position to be update
        :param value: add value at the given index
        """
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def build(self):
        for idx in range(1, self.size + 1):
            self.update(idx, self.array[idx - 1])


if __name__ == "__main__":
    import time

    start = time.process_time()
    obj = BinaryIndexedTree([1, 2, 3, 5, 6])
    obj.build()
    logger.info(f"Summation in range {[1, 3]}: {obj.query(3)}")
    logger.info(f"Process time: {time.process_time() - start} seconds")
