from io import StringIO
import sys
import unittest

from pydlx.link import BaseDLX
from pydlx.operations import create_network, ecx, mrv, print_solution, progress


class TestOperations(unittest.TestCase):
    def tearDown(self):
        BaseDLX._instances.clear()

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

    def test_ecx_no_solution(self):
        """Test that there is no solution."""
        root = create_network([[0, 1],
                               [0, 0]])

        solutions = [i for i in ecx(root)]
        self.assertFalse(solutions)

    def test_ecx_with_solution(self):
        """Test that there is a valid solution."""

        root = create_network([
                [0, 0, 1, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 0, 1],
                [0, 1, 1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 1, 0, 1]])

        #   0   1   2   3   4   5   6   7
        #   8           9       10  11
        #   12  13          14          15
        #   16      17  18          19
        #   20  21          22
        #   23      24                  25
        #   26              27  28      29
        #   30

        for solution in ecx(root):
            self.assertEqual(solution[0].id, 21)
            self.assertEqual(solution[0].column.name, "1")
            self.assertEqual(solution[1].id, 10)
            self.assertEqual(solution[1].column.name, "5")
            self.assertEqual(solution[2].id, 24)
            self.assertEqual(solution[2].column.name, "2")
            break

    def test_ecx_with_solution_name(self):
        """Test that there is a valid solution, with given name."""

        root = create_network([
                [0, 0, 1, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 0, 1],
                [0, 1, 1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 1, 0, 1]],
                ["A", "B", "C", "D", "E", "F", "G"])

        #   0   1   2   3   4   5   6   7
        #   8           9       10  11
        #   12  13          14          15
        #   16      17  18          19
        #   20  21          22
        #   23      24                  25
        #   26              27  28      29
        #   30

        for solution in ecx(root):
            self.assertEqual(solution[0].id, 21)
            self.assertEqual(solution[0].column.name, "A")
            self.assertEqual(solution[1].id, 10)
            self.assertEqual(solution[1].column.name, "E")
            self.assertEqual(solution[2].id, 24)
            self.assertEqual(solution[2].column.name, "B")
            break

    def test_ecx_with_solution_many(self):
        """Check that multiple solutions are returned."""
        root = create_network([
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 1]],
            names=["A", "B", "C"])
        solutions = [_ for _ in ecx(root)]
        self.assertEqual(len(solutions), 2)

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

        for solution in ecx(root):
            print_solution(solution)
            break

        self.assertEqual(output.getvalue(),
                        "A D \n"
                        "B G \n"
                        "C E F \n")
        sys.stdout = sys.__stdout__                  # Reset redirect.

    def test_progress(self):
        self.assertAlmostEqual(0.3125, progress([1,3], [2,4]))
