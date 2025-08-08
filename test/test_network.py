import unittest

from dancing_link.network import Network


class TestNetwork(unittest.TestCase):
    def test_init(self):
        # matrix:
        #       a   b   c   d   e   f   g
        #       0   0   1   0   1   0   0
        #       1   0   0   1   0   0   1
        #       0   1   1   0   0   1   0
        #       1   0   0   1   0   1   0
        #       0   1   0   0   0   0   1
        #       0   0   0   1   1   0   1

        # nodes:
        #   0   1   2   3   4   5   6   7
        #   8           9       10
        #   11  12          13          14
        #   15      16  17          18
        #   19  20          21      22
        #   23      24                  25
        #   26              27  28      29
        #   30

        # create the headers
        matrix = [[0, 0, 1, 0, 1, 0, 0],
                  [1, 0, 0, 1, 0, 0, 1],
                  [0, 1, 1, 0, 0, 1, 0],
                  [1, 0, 0, 1, 0, 1, 0],
                  [0, 1, 0, 0, 0, 0, 1],
                  [0, 0, 0, 1, 1, 0, 1]]
        names = ["a", "b", "c", "d", "e", "f", "g"]
        network = Network(matrix, names)

        self.assertListEqual(network.name,
                             ["0", "a", "b", "c", "d", "e", "f", "g"])
        self.assertListEqual(network.left,
                             [7, 0, 1, 2, 3, 4, 5, 6])
        self.assertListEqual(network.right,
                             [1, 2, 3, 4, 5, 6, 7, 0])
        self.assertListEqual(network.len,
                             [0, 2, 2, 2, 3, 2, 2, 3,
                              0, 3, 5, -1, 1, 4, 7, -2,
                              2, 3, 6, -3, 1, 4, 6, -4,
                              2, 7, -5, 4, 5, 7, -6])
        self.assertListEqual(network.up,
                             [0, 20, 24, 17, 27, 28, 22, 29,
                              None, 3, 5, 9, 1, 4, 7, 12,
                              2, 9, 6, 16, 12, 13, 18, 20,
                              16, 14, 24, 21, 10, 25, 27])
        self.assertListEqual(network.down,
                             [0, 12, 16, 9, 13, 10, 18, 14,
                              10, 17, 28, 14, 20, 21, 25, 18,
                              24, 3, 22, 22, 1, 27, 6, 25,
                              2, 29, 29, 4, 5, 7, None])

    def test_hide_unhide(self):
        #       B   C   E   F
        #       0   1   1   1
        #       1   1   0   1

        # nodes
        #   0   1   2   3   4
        #   5       6   7   8
        #   9   10  11      12
        #   13

        # create the headers
        matrix = [[0, 1, 1, 1],
                  [1, 1, 0, 1]]
        names = ["B", "C", "E", "F"]
        network = Network(matrix, names)

        self.assertListEqual(network.name, ["0", "B", "C", "E", "F"])
        self.assertListEqual(network.left, [4, 0, 1, 2, 3])
        self.assertListEqual(network.right, [1, 2, 3, 4, 0])
        self.assertListEqual(network.len, [0, 1, 2, 1, 2,
                                           0, 2, 3, 4,
                                           -1, 1, 2, 4,
                                           -2])
        self.assertListEqual(network.up, [0, 10, 11, 7, 12,
                                          None, 2, 3, 4,
                                          6, 1, 6, 8,
                                          10])
        self.assertListEqual(network.down, [0, 10, 6, 7, 8,
                                            8, 11, 3, 12,
                                            12, 1, 2, 4,
                                            None])

        # cover and check
        network.hide(10)

        self.assertListEqual(network.name, ["0", "B", "C", "E", "F"])
        self.assertListEqual(network.left, [4, 0, 1, 2, 3])     # no change
        self.assertListEqual(network.right, [1, 2, 3, 4, 0])    # no change
        self.assertListEqual(network.len, [0, 1, 1, 1, 1,
                                           0, 2, 3, 4,
                                           -1, 1, 2, 4,
                                           -2])
        self.assertListEqual(network.up, [0, 10, 6, 7, 8,
                                          None, 2, 3, 4,
                                          6, 1, 6, 8,
                                          10])
        self.assertListEqual(network.down, [0, 10, 6, 7, 8,
                                            8, 2, 3, 4,
                                            12, 1, 2, 4,
                                            None])

        network.unhide(10)
        self.assertListEqual(network.name, ["0", "B", "C", "E", "F"])
        self.assertListEqual(network.left, [4, 0, 1, 2, 3])
        self.assertListEqual(network.right, [1, 2, 3, 4, 0])
        self.assertListEqual(network.len, [0, 1, 2, 1, 2,
                                           0, 2, 3, 4,
                                           -1, 1, 2, 4,
                                           -2])
        self.assertListEqual(network.up, [0, 10, 11, 7, 12,
                                          None, 2, 3, 4,
                                          6, 1, 6, 8,
                                          10])
        self.assertListEqual(network.down, [0, 10, 6, 7, 8,
                                            8, 11, 3, 12,
                                            12, 1, 2, 4,
                                            None])

    def test_cover_uncover(self):
        #       B   C   E   F
        #       0   1   1   1
        #       1   1   0   1

        # nodes
        #   0   1   2   3   4
        #   5       6   7   8
        #   9   10  11      12
        #   13

        # create the headers
        matrix = [[0, 1, 1, 1],
                  [1, 1, 0, 1]]
        names = ["B", "C", "E", "F"]
        network = Network(matrix, names)

        self.assertListEqual(network.name, ["0", "B", "C", "E", "F"])
        self.assertListEqual(network.left, [4, 0, 1, 2, 3])
        self.assertListEqual(network.right, [1, 2, 3, 4, 0])
        self.assertListEqual(network.len, [0, 1, 2, 1, 2,
                                           0, 2, 3, 4,
                                           -1, 1, 2, 4,
                                           -2])
        self.assertListEqual(network.up, [0, 10, 11, 7, 12,
                                          None, 2, 3, 4,
                                          6, 1, 6, 8,
                                          10])
        self.assertListEqual(network.down, [0, 10, 6, 7, 8,
                                            8, 11, 3, 12,
                                            12, 1, 2, 4,
                                            None])

        # cover and check
        network.cover(1)

        self.assertListEqual(network.name, ["0", "B", "C", "E", "F"])
        self.assertListEqual(network.left, [4, 0, 0, 2, 3])
        self.assertListEqual(network.right, [2, 2, 3, 4, 0])
        self.assertListEqual(network.len, [0, 1, 1, 1, 1,
                                           0, 2, 3, 4,
                                           -1, 1, 2, 4,
                                           -2])
        self.assertListEqual(network.up, [0, 10, 6, 7, 8,
                                          None, 2, 3, 4,
                                          6, 1, 6, 8,
                                          10])
        self.assertListEqual(network.down, [0, 10, 6, 7, 8,
                                            8, 2, 3, 4,
                                            12, 1, 2, 4,
                                            None])

        network.uncover(1)
        self.assertListEqual(network.name, ["0", "B", "C", "E", "F"])
        self.assertListEqual(network.left, [4, 0, 1, 2, 3])
        self.assertListEqual(network.right, [1, 2, 3, 4, 0])
        self.assertListEqual(network.len, [0, 1, 2, 1, 2,
                                           0, 2, 3, 4,
                                           -1, 1, 2, 4,
                                           -2])
        self.assertListEqual(network.up, [0, 10, 11, 7, 12,
                                          None, 2, 3, 4,
                                          6, 1, 6, 8,
                                          10])
        self.assertListEqual(network.down, [0, 10, 6, 7, 8,
                                            8, 11, 3, 12,
                                            12, 1, 2, 4,
                                            None])
