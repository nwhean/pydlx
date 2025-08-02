"""Contains the implementation of DLX algorithm."""
from typing import Generator
from itertools import zip_longest
import time

from .link import Link, Column


class SolutionNotFound(Exception):
    """Raised when there is no solution to the problem."""


Matrix = list[list[int]]
def create_network(matrix: Matrix,
                   names: list[str] | None = None,
                   primary: int | None = None,
                   secondary: int | None = None) -> Column:
    """Convert a matrix into a dancing link network and return the root.

    Parameters
    ----------
    matrix : list[list[int]]
             exact cover matrix
    names : lst[str], default = None
            names for the headers
    primary : int, default = None
              number of primary columns
    secondary : int, default = None
                number of secondary columns
    """
    width = len(matrix[0])

    if primary is None and secondary is None:
        primary = width
        secondary = 0
    elif primary is None:       # secondary is given
        if secondary < 0:
            raise ValueError("'secondary' must be non-negative.")
        primary = width - secondary     # calculate primary automatically
    elif secondary is None:     # primary is given
        if primary < 0:
            raise ValueError("'primary' must be non-negative.")
        secondary = width - primary     # calculate secondary automatically
    else:
        if primary != width - secondary:
            raise ValueError(
                "'primary' and 'secondary' must sum to matrix width.")

    # create the root header
    root = Column()

    # create the header list
    left = root
    headers: list[Column] = []
    if names is None:
        names = []
    for index, (_, name) in enumerate(zip_longest(matrix[0], names,
                                                  fillvalue="")):
        header = Column(name)
        if index < primary:     # secondary items are not pointed to by primary
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

def ecx(root: Column,
        sol: list[Link] | None = None,
        level: int = 0,
        choose=mrv,
        interval: int | None = None,
        **kwargs
        ) -> Generator[list[Link], None, None]:
    """Exact Cover via Dancing Link using Algorithm X.

    Parameters
    ----------
    root : Column
           the root node of the exact cover network
    sol : list[Link] | None
          a list containing the partial solution to the exact cover problem
    level : int
            the current level of search tree
    choose : Callable[Column, Column]
             heuristics function that returns the next column to be chosen
    interval : int | None, default = None
               the time interval between printing progess status.
               None: no progress status printed
               0: progress status is printed at every node
    """
    if sol is None:
        sol = []

    # handle keyword arguments
    if 'choices' not in kwargs:     # index of the choice chosen at a level
        kwargs['choices'] = []
    if 'branches' not in kwargs:    # total number of choices at a level
        kwargs['branches'] = []
    if 'start_time' not in kwargs:  # time when algorithm started
        kwargs['start_time'] = time.time()
    if 'threshold' not in kwargs and interval is not None:
        kwargs['threshold'] = [interval]    # value above which status printed

    # Step X2: Enter Level `level`
    # handle the progress report printing
    start_time = kwargs.get('start_time')
    threshold = kwargs.get('threshold')
    choices = kwargs.get('choices')
    branches = kwargs.get('branches')

    runtime = time.time() - start_time
    if threshold and runtime > threshold[-1]:
        threshold[-1] += interval
        print(f"{runtime:.3f}", end=" ")
        print(f"{progress(choices, branches):.5f}", end=" ")
        for c, l in zip(choices, branches):
            print(f"{c}/{l}", end=" ")
        print()

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
    branches.append(i.size)
    x: Link = i.down
    sol.append(x)
    choices.append(1)

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

        yield from ecx(root, sol, level+1, choose=choose, interval=interval,
                       **kwargs)

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
        choices[-1] += 1

    # tried all options for i
    # Step X7: Backtrack
    i.uncover()
    del sol[-1]
    del choices[-1]
    del branches[-1]

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

def progress(choices: list[int], branches: list[int]) -> float:
    """Calculate the progress of the algorithm.

    Parameters
    ----------
    choices : list[int]
              list containing the index of the choices chosen at each level
    branches : list[int]
               list containing the total number of choices at each level
    """
    retval = 0.5
    for c, l in zip(choices[::-1], branches[::-1]):
        retval += c - 1
        retval /= l
    return retval
