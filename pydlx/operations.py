"""Contains the implementation of DLX algorithm."""
from typing import Generator
from itertools import zip_longest

from .link import Link, Column


class SolutionNotFound(Exception):
    """Raised when there is no solution to the problem."""


Matrix = list[list[int]]
def create_network(matrix: Matrix, names: list[str] | None = None) -> Column:
    """Convert a matrix into a dancing link network and return the root."""
    # create the root header
    root = Column()

    # create the header list
    left = root
    headers: list[Column] = []
    if names is None:
        names = []
    for _, name in zip_longest(matrix[0], names, fillvalue=""):
        header = Column(name)
        left.add_right(header)
        left = header
        headers.append(header)

    # create the nodes
    first = None
    for row in matrix:
        # create the spacer node
        spacer = Link(None)     # spacer node doesn't belong to column
        spacer.up = first

        first = None
        for val, header in zip(row, headers):
            if val:
                link = Link(header)
                if not first:
                    first = link    # record first node in option before spacer

        spacer.down = link          # record last node in option after spacer

    # create the last spacer
    spacer = Link(None)
    spacer.up = first
    spacer.down = None

    return root

def mrv(root: Column) -> Column:
    """Return the column with minimum remaining values."""
    retval = root
    j = root.right
    size = j.size + 1

    while j != root:
        if j.size < size:
            retval = j
            size = j.size
        j = j.right

    return retval

def ecx(root: Column, sol: list[Link] | None = None, level: int = 0,
        choose=mrv) -> Generator[list[Link], None, None]:
    """Exact Cover via Dancing Link using Algorithm X."""
    if sol is None:
        sol = []

    # Step X2: Enter Level `level`
    if root.right == root:  # all items have been covered
        # visit the solution specified by x_0 x_1 x_2 ... x_level-1
        yield sol

        # Step X8: Leave Level `level`
        # if level == 0:  # terminate if level == 0
        #     return
        # else:
        #     level -= 1
        #     return      # go to X6
        return

    # Step X3: Choose item `i`
    i: Column = choose(root)

    # Step X4: Cover item `i`
    i.cover()
    x: Link = i.down
    sol.append(x)

    # Step X5: Try x_l
    while x != i:
        # This covers the items != i in the option that contains x_l.
        node: Link = x + 1
        while node != x:
            column: Column = node.column
            if not column:  # node is a spacer
                node = node.up
            else:
                column.cover()
                node += 1

        yield from ecx(root, sol, level+1, choose=choose)

        # Step X6: Try again
        # This uncovers the items != i in the option that contains x_l,
        # using the reverse of the order in X5.
        node: Link = x - 1
        while node != x:
            column: Column = node.column
            if not column:  # node is a spacer
                node = node.down
            else:
                column.uncover()
                node -= 1

        x = x.down
        sol[-1] = x

    # tried all options for i
    # Step X7: Backtrack
    i.uncover()
    del sol[-1]

def print_solution(solution: list[Link]) -> None:
    """Successively print the rows in 'solution'."""
    if not solution:
        raise SolutionNotFound

    for node in solution:
        while node.column:  # move until we reach the row end spacer
            node += 1
        node: Link = node.up      # move to the first node of the row

        while node.column:
            print(node.column.name, end=" ")
            node += 1
        print()
