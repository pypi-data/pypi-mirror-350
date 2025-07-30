import unittest
from src.algosinpy.algorithm.sorting.sorting import *


class SortingTest(unittest.TestCase):
    def test_bubble_sort(self):
        self.assertEqual(
            bubble_sort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90]
        )

    def test_selection_sort(self):
        self.assertEqual(
            selection_sort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90]
        )

    def test_insertion_sort(self):
        self.assertEqual(
            insertion_sort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90]
        )

    def test_quick_sort(self):
        array = [64, 34, 25, 12, 22, 11, 90]
        self.assertEqual(
            quick_sort(array, 0, (len(array) - 1)), [11, 12, 22, 25, 34, 64, 90]
        )

    def test_merge_sort(self):
        array = [64, 34, 25, 12, 22, 11, 90]
        self.assertEqual(
            merge_sort(array, 0, len(array) - 1), [11, 12, 22, 25, 34, 64, 90]
        )

        array = [12, 11, 13, 5, 6, 7]
        self.assertEqual(merge_sort(array, 0, len(array) - 1), [5, 6, 7, 11, 12, 13])

    def test_countSort(self):
        self.assertEqual(
            countSort("geeksforgeeks"),
            ["e", "e", "e", "e", "f", "g", "g", "k", "k", "o", "r", "s", "s"],
        )

    def test_radixSort(self):
        self.assertEqual(
            radixSort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90]
        )

    def test_bucketSort(self):
        self.assertEqual(
            bucketSort([0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]),
            [0.1234, 0.3434, 0.565, 0.656, 0.665, 0.897],
        )


if __name__ == "__main__":
    unittest.main()
