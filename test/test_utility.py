from io import StringIO
import sys
import unittest

from dancing_link.algorithm import xc
from dancing_link.link import DancingLink, ColumnColour, LinkColour
from dancing_link.utility import create_network, mrv, print_solution, progress


class TestCreateNetwork(unittest.TestCase):
    def tearDown(self):
        DancingLink._instances.clear()

    def test_no_colour(self):
        # matrix:
        #       B   C   E   F
        #       0   1   1   1
        #       1   1   0   1

        # nodes:
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
        spacer_5 = root._instances[5]
        spacer_9 = root._instances[9]
        spacer_13 = root._instances[13]

        self.assertEqual(spacer_5.id, 5)
        self.assertIsNone(spacer_5.up)
        self.assertEqual(spacer_5.down.id, 8)

        self.assertEqual(spacer_9.id, 9)
        self.assertEqual(spacer_9.up.id, 6)
        self.assertEqual(spacer_9.down.id, 12)

        self.assertEqual(spacer_13.id, 13)
        self.assertEqual(spacer_13.up.id, 10)
        self.assertIsNone(spacer_13.down)

    def test_with_colour(self):
        # matrix:
        #       p   q   r   x   y
        #       1   1       1   2
        #       1       1   2   1
        #       1           3
        #           1       2
        #               1       3

        # nodes:
        #   0   1   2   3   4   5
        #   6   7   8       9   10
        #   11  12      13  14  15
        #   16  17          18
        #   19      20      21
        #   22          23      24
        #   25

        matrix = [[1, 1, 0, 1, 2],
                  [1, 0, 1, 2, 1],
                  [1, 0, 0, 3, 0],
                  [0, 1, 0, 2, 0],
                  [0, 0, 1, 0, 3]]

        create_network(matrix, names=["p", "q", "r", "x", "y"], primary=3)

        # ensure there are only 26 nodes
        self.assertEqual(len(DancingLink._instances), 26)

        # check node 0
        node: ColumnColour = DancingLink._instances[0]
        self.assertEqual(node.name, "0")    # defaults to node number
        self.assertEqual(node.left.id, 3)
        self.assertEqual(node.right.id, 1)
        self.assertEqual(node.size, 0)
        self.assertEqual(node.up.id, 0)
        self.assertEqual(node.down.id, 0)
        self.assertIsNone(node.colour)

        # check node 1
        node:ColumnColour = DancingLink._instances[1]
        self.assertEqual(node.name, "p")    # defaults to node number
        self.assertEqual(node.left.id, 0)
        self.assertEqual(node.right.id, 2)
        self.assertEqual(node.size, 3)
        self.assertEqual(node.up.id, 17)
        self.assertEqual(node.down.id, 7)
        self.assertIsNone(node.colour)

        # check node 2
        node:ColumnColour = DancingLink._instances[2]
        self.assertEqual(node.name, "q")
        self.assertEqual(node.left.id, 1)
        self.assertEqual(node.right.id, 3)
        self.assertEqual(node.size, 2)
        self.assertEqual(node.up.id, 20)
        self.assertEqual(node.down.id, 8)
        self.assertIsNone(node.colour)

        # check node 3
        node:ColumnColour = DancingLink._instances[3]
        self.assertEqual(node.name, "r")
        self.assertEqual(node.left.id, 2)
        self.assertEqual(node.right.id, 0)
        self.assertEqual(node.size, 2)
        self.assertEqual(node.up.id, 23)
        self.assertEqual(node.down.id, 13)
        self.assertIsNone(node.colour)

        # check node 4
        node:ColumnColour = DancingLink._instances[4]
        self.assertEqual(node.name, "x")
        self.assertEqual(node.left.id, 4)       # different from example
        self.assertEqual(node.right.id, 4)      # different from example
        self.assertEqual(node.size, 4)
        self.assertEqual(node.up.id, 21)
        self.assertEqual(node.down.id, 9)
        self.assertIsNone(node.colour)

        # check node 5
        node:ColumnColour = DancingLink._instances[5]
        self.assertEqual(node.name, "y")
        self.assertEqual(node.left.id, 5)       # different from example
        self.assertEqual(node.right.id, 5)      # different from example
        self.assertEqual(node.size, 3)
        self.assertEqual(node.up.id, 24)
        self.assertEqual(node.down.id, 10)
        self.assertIsNone(node.colour)

        # check node 6
        node:LinkColour = DancingLink._instances[6]
        self.assertIsNone(node.column)
        self.assertIsNone(node.up)
        self.assertEqual(node.down.id, 10)
        self.assertEqual(node.colour, 0)

        # check node 7
        node:LinkColour = DancingLink._instances[7]
        self.assertEqual(node.column.id, 1)
        self.assertEqual(node.up.id, 1)
        self.assertEqual(node.down.id, 12)
        self.assertEqual(node.colour, 0)

        # check node 8
        node:LinkColour = DancingLink._instances[8]
        self.assertEqual(node.column.id, 2)
        self.assertEqual(node.up.id, 2)
        self.assertEqual(node.down.id, 20)
        self.assertEqual(node.colour, 0)

        # check node 9
        node:LinkColour = DancingLink._instances[9]
        self.assertEqual(node.column.id, 4)
        self.assertEqual(node.up.id, 4)
        self.assertEqual(node.down.id, 14)
        self.assertEqual(node.colour, 0)

        # check node 10
        node:LinkColour = DancingLink._instances[10]
        self.assertEqual(node.column.id, 5)
        self.assertEqual(node.up.id, 5)
        self.assertEqual(node.down.id, 15)
        self.assertEqual(node.colour, 1)    # 1 = A in example

        # check node 11
        node:LinkColour = DancingLink._instances[11]
        self.assertIsNone(node.column)
        self.assertEqual(node.up.id, 7)
        self.assertEqual(node.down.id, 15)
        self.assertEqual(node.colour, 0)

        # check node 12
        node:LinkColour = DancingLink._instances[12]
        self.assertEqual(node.column.id, 1)
        self.assertEqual(node.up.id, 7)
        self.assertEqual(node.down.id, 17)
        self.assertEqual(node.colour, 0)

        # check node 13
        node:LinkColour = DancingLink._instances[13]
        self.assertEqual(node.column.id, 3)
        self.assertEqual(node.up.id, 3)
        self.assertEqual(node.down.id, 23)
        self.assertEqual(node.colour, 0)

        # check node 14
        node:LinkColour = DancingLink._instances[14]
        self.assertEqual(node.column.id, 4)
        self.assertEqual(node.up.id, 9)
        self.assertEqual(node.down.id, 18)
        self.assertEqual(node.colour, 1)        # 1 = A in example

        # check node 15
        node:LinkColour = DancingLink._instances[15]
        self.assertEqual(node.column.id, 5)
        self.assertEqual(node.up.id, 10)
        self.assertEqual(node.down.id, 24)
        self.assertEqual(node.colour, 0)

        # check node 16
        node:LinkColour = DancingLink._instances[16]
        self.assertIsNone(node.column)
        self.assertEqual(node.up.id, 12)
        self.assertEqual(node.down.id, 18)
        self.assertEqual(node.colour, 0)

        # check node 17
        node:LinkColour = DancingLink._instances[17]
        self.assertEqual(node.column.id, 1)
        self.assertEqual(node.up.id, 12)
        self.assertEqual(node.down.id, 1)
        self.assertEqual(node.colour, 0)

        # check node 18
        node:LinkColour = DancingLink._instances[18]
        self.assertEqual(node.column.id, 4)
        self.assertEqual(node.up.id, 14)
        self.assertEqual(node.down.id, 21)
        self.assertEqual(node.colour, 2)        # 2 = B in example

        # check node 19
        node:LinkColour = DancingLink._instances[19]
        self.assertIsNone(node.column)
        self.assertEqual(node.up.id, 17)
        self.assertEqual(node.down.id, 21)
        self.assertEqual(node.colour, 0)

        # check node 20
        node:LinkColour = DancingLink._instances[20]
        self.assertEqual(node.column.id, 2)
        self.assertEqual(node.up.id, 8)
        self.assertEqual(node.down.id, 2)
        self.assertEqual(node.colour, 0)

        # check node 21
        node:LinkColour = DancingLink._instances[21]
        self.assertEqual(node.column.id, 4)
        self.assertEqual(node.up.id, 18)
        self.assertEqual(node.down.id, 4)
        self.assertEqual(node.colour, 1)

        # check node 22
        node:LinkColour = DancingLink._instances[22]
        self.assertIsNone(node.column)
        self.assertEqual(node.up.id, 20)
        self.assertEqual(node.down.id, 24)
        self.assertEqual(node.colour, 0)

        # check node 23
        node:LinkColour = DancingLink._instances[23]
        self.assertEqual(node.column.id, 3)
        self.assertEqual(node.up.id, 13)
        self.assertEqual(node.down.id, 3)
        self.assertEqual(node.colour, 0)

        # check node 24
        node:LinkColour = DancingLink._instances[24]
        self.assertEqual(node.column.id, 5)
        self.assertEqual(node.up.id, 15)
        self.assertEqual(node.down.id, 5)
        self.assertEqual(node.colour, 2)

        # check node 25
        node:LinkColour = DancingLink._instances[25]
        self.assertIsNone(node.column)
        self.assertEqual(node.up.id, 23)
        self.assertIsNone(node.down)
        self.assertEqual(node.colour, 0)


class TestUtility(unittest.TestCase):
    def tearDown(self):
        DancingLink._instances.clear()

    def test_mrv(self):
        root = create_network([[0, 1, 0],
                               [1, 1, 0],
                               [1, 0, 1]])
        self.assertEqual(mrv(root).id, 3)

    def test_print_solution(self):
        root = create_network([[1, 0, 0, 1, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 1],
                               [0, 0, 1, 0, 1, 1, 0]],
                               ["A", "B", "C", "D", "E", "F", "G"])

        #   0   1   2   3   4   5   6   7
        #   8   9           10
        #   11      12                  13
        #   14          15      16  17
        #   18

        output = StringIO()         # Make StringIO.
        sys.stdout = output

        for solution in xc(root):
            print_solution(solution)
            break

        self.assertEqual(output.getvalue(),
                        "A D \n"
                        "B G \n"
                        "C E F \n")
        sys.stdout = sys.__stdout__                  # Reset redirect.

    def test_progress(self):
        self.assertAlmostEqual(0.3125, progress([1,3], [2,4]))
