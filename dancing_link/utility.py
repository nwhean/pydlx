"""Contains the implementation of DLX algorithm."""
from itertools import zip_longest

from .link import Column, ColumnColour, Link, LinkColour


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
    # test whether colour is required
    maxval = max(max(_) for _ in matrix)
    if maxval == 1:
        ColumnCls = Column
        LinkCls = Link
    else:
        ColumnCls = ColumnColour
        LinkCls = LinkColour

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
    root = ColumnCls()

    # create the header list
    left = root
    headers: list[Column | ColumnColour] = []
    if names is None:
        names = []
    for index, (_, name) in enumerate(zip_longest(matrix[0], names,
                                                  fillvalue="")):
        header = ColumnCls(name)
        if index < primary:     # secondary items are not pointed to by primary
            left.add_right(header)
        left = header
        headers.append(header)

    # create the nodes
    first = None
    link = None
    for row in matrix:
        # create the spacer node
        spacer = LinkCls(None)     # spacer node doesn't belong to column
        spacer.up = first

        first = None
        for index, (val, header) in enumerate(zip(row, headers)):
            if val:
                kwargs = {'column': header}
                if maxval != 1 and index >= primary:     # colour is required
                    kwargs['colour'] = val - 1      # no colour = 0
                link = LinkCls(**kwargs)
                if not first:
                    first = link    # record first node in option before spacer

        spacer.down = link          # record last node in option after spacer

    # create the last spacer
    spacer = LinkCls(None)
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
