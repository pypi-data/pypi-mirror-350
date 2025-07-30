import unittest
from src.algosinpy.algorithm.tree.segment_tree import *


class SegmentTreeTestCase(unittest.TestCase):
    def test_segment_tree(self):
        segment_tree = SegmentTree([1, -2, 4, -1, 6, 2])
        segment_tree.build(lower_index=0, higher_index=segment_tree.size - 1, segment=1)
        self.assertEqual(
            segment_tree.query(
                lower_index=0,
                higher_index=segment_tree.size - 1,
                start=3,
                end=5,
                segment=1,
            ),
            6,
        )
        self.assertEqual(
            segment_tree.query(
                lower_index=0,
                higher_index=segment_tree.size - 1,
                start=1,
                end=3,
                segment=1,
            ),
            4,
        )


if __name__ == "__main__":
    unittest.main()
