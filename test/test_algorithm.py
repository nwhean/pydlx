import unittest

from dancing_link.algorithm import ecx
from dancing_link.link import DancingLink
from dancing_link.utility import create_network


class TestECX(unittest.TestCase):
    def tearDown(self):
        DancingLink._instances.clear()

    def test_no_solution(self):
        """Test that there is no solution."""
        root = create_network([[0, 1],
                               [0, 0]])

        solutions = [i for i in ecx(root)]
        self.assertFalse(solutions)

    def test_with_solution(self):
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

    def test_with_solution_name(self):
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

    def test_with_solution_many(self):
        """Check that multiple solutions are returned."""
        root = create_network([
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 1]],
            names=["A", "B", "C"])
        solutions = [_ for _ in ecx(root)]
        self.assertEqual(len(solutions), 2)
