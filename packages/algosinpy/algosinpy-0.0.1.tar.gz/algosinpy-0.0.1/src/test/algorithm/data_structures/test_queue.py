import unittest
from src.algosinpy.algorithm.data_structures.queue import *


class TestQueue(unittest.TestCase):
    def test_front(self):
        q = Queue([1, 10, 2, 9])
        self.assertEqual(q.front(), 1)

    def test_pop(self):
        q = Queue([1, 10, 2, 9])
        q.pop()
        self.assertEqual(q.size(), 3)
        self.assertEqual(q.front(), 10)

    def test_push(self):
        q = Queue()  # initiated an empty queue
        #    q.pop()      # to check exception is working or not
        q.push(5)
        q.push(3)
        self.assertEqual(q.size(), 2)
        self.assertEqual(q.front(), 5)

    def test_size(self):
        q = Queue([1, 100, 2, 30, 5, 10, 9])
        self.assertEqual(q.size(), 7)

    def test_empty(self):
        q = Queue()
        self.assertEqual(q.empty(), True)
        q.push(5)
        self.assertEqual(q.empty(), False)

    def test_display(self):
        q = Queue([1, 7, 5, 3, 2, 6, 4])
        self.assertEqual(q.display(), [1, 7, 5, 3, 2, 6, 4])


if __name__ == "__main__":
    unittest.main()
