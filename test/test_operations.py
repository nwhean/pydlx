import unittest

from pydlx.operations import create_network


class TestOperations(unittest.TestCase):
    def test_create_network(self):
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
        root = create_network(matrix, names)

        # recognise the headers
        b = root.right
        c = b.right
        e = c.right
        f = e.right

        # check header id
        self.assertEqual(b.id, 1)
        self.assertEqual(c.id, 2)
        self.assertEqual(e.id, 3)
        self.assertEqual(f.id, 4)

        # check header sizes
        self.assertEqual(b.size, 1)
        self.assertEqual(c.size, 2)
        self.assertEqual(e.size, 1)
        self.assertEqual(f.size, 2)

        # check column members
        self.assertEqual(c.down.id, 6)
        self.assertEqual(e.down.id, 7)
        self.assertEqual(f.down.id, 8)
        self.assertEqual(b.down.id, 10)
        self.assertEqual(c.down.down.id, 11)
        self.assertEqual(f.down.down.id, 12)

        # check spacers info
        spacer_5 = root.instances[5]
        spacer_9 = root.instances[9]
        spacer_13 = root.instances[13]

        self.assertEqual(spacer_5.id, 5)
        self.assertIsNone(spacer_5.up)
        self.assertEqual(spacer_5.down.id, 8)

        self.assertEqual(spacer_9.id, 9)
        self.assertEqual(spacer_9.up.id, 6)
        self.assertEqual(spacer_9.down.id, 12)

        self.assertEqual(spacer_13.id, 13)
        self.assertEqual(spacer_13.up.id, 10)
        self.assertIsNone(spacer_13.down)
