import unittest

from pydlx.link import BaseDLX, Column, Link
from pydlx.operations import create_network


class TestColumn(unittest.TestCase):
    def tearDown(self):
        BaseDLX.instances.clear()

    def test_add_bottom(self):
        a = Column()
        b = Link()
        c = Link()

        # a
        # |
        # b
        a.add_bottom(b)
        self.assertEqual(a.up, b)
        self.assertEqual(a.down, b)
        self.assertEqual(b.up, a)
        self.assertEqual(b.down, a)
        self.assertEqual(a.size, 1)

        # a
        # |
        # b
        # |
        # c
        a.add_bottom(c)
        self.assertEqual(a.up, c)
        self.assertEqual(a.down, b)
        self.assertEqual(b.up, a)
        self.assertEqual(b.down, c)
        self.assertEqual(c.up, b)
        self.assertEqual(c.down, a)
        self.assertEqual(a.size, 2)

    def test_add_right(self):
        a = Column()
        b = Column()
        c = Column()

        # a -- b
        a.add_right(b)
        self.assertEqual(a.right, b)
        self.assertEqual(a.left, b)
        self.assertEqual(b.left, a)
        self.assertEqual(b.right, a)

        # a -- c -- b
        a.add_right(c)
        self.assertEqual(a.right, c)
        self.assertEqual(a.left, b)
        self.assertEqual(c.left, a)
        self.assertEqual(c.right, b)
        self.assertEqual(b.left, c)
        self.assertEqual(b.right, a)

        del a
        del b
        del c

    def test_cover(self):
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

        b = root.right
        c = b.right
        e = c.right
        f = e.right

        # cover and check
        b.cover()
        self.assertEqual(root.right, c)
        self.assertEqual(b.size, 1)
        self.assertEqual(b.down.id, 10)

        self.assertEqual(c.size, 1)
        self.assertEqual(c.down.id, 6)
        self.assertEqual(c.down.down, c)

        self.assertEqual(e.size, 1)
        self.assertEqual(e.down.id, 7)
        self.assertEqual(e.down.down, e)

        self.assertEqual(f.size, 1)
        self.assertEqual(f.down.id, 8)
        self.assertEqual(f.down.down, f)

    def test_uncover(self):
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

        b = root.right
        c = b.right
        e = c.right
        f = e.right

        # cover, uncover and check
        b.cover()
        b.uncover()

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


class TestBaseDLX(unittest.TestCase):
    def test_add_down(self):
        a = Link()
        b = Link()
        c = Link()

        # a
        # |
        # b
        a._add_down(b)
        self.assertEqual(a.down, b)
        self.assertEqual(a.up, b)
        self.assertEqual(b.up, a)
        self.assertEqual(b.down, a)

        # a
        # |
        # c
        # |
        # b
        a._add_down(c)
        self.assertEqual(a.down, c)
        self.assertEqual(a.up, b)
        self.assertEqual(c.up, a)
        self.assertEqual(c.down, b)
        self.assertEqual(b.up, c)
        self.assertEqual(b.down, a)
