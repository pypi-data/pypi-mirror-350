import unittest
from src.algosinpy.algorithm.tree.binary_indexed_tree import *


class BinaryIndexedTreeTestCase(unittest.TestCase):
    def test_binary_indexed_tree(self):
        bit = BinaryIndexedTree([1, 2, 3, 5, 6])
        bit.build()
        self.assertEqual(bit.query(3), 6)
        self.assertEqual(bit.query(4), 11)
        bit.update(2, 4)
        self.assertEqual(bit.query(3), 10)


if __name__ == "__main__":
    unittest.main()
