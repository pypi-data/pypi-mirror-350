import unittest
from src.algosinpy.algorithm.dynamic_programming.longest_common_subsequence import *


class LCSTest(unittest.TestCase):
    def test_iterative_lcs(self):
        self.assertEqual(iterative_lcs([1, 5, 2, 4], [3, 2, 4, 1, 2, 5, 2]), 3)

    def test_recursive_lcs(self):
        self.assertEqual(recursive_lcs([1, 5, 2, 4], [3, 2, 4, 1, 2, 5, 2], 4, 7), 3)


if __name__ == "__main__":
    unittest.main()
