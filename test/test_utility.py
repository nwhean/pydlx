import unittest

from dancing_link.utility import mrv, progress
from dancing_link.network import Network


class TestUtility(unittest.TestCase):
    def test_mrv(self):
        network = Network([[0, 1, 0],
                           [1, 1, 0],
                           [1, 0, 1]])
        self.assertEqual(mrv(network), 3)

    def test_progress(self):
        self.assertAlmostEqual(0.3125, progress([1,3], [2,4]))
