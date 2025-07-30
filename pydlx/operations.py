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

def search(root: Column, solution: list[Link] = None, k: int = 0
           ) -> Generator[list[Link], None, None]:
    """
    If R[h] = h, print the current solution and return.
    Otherwise choose a column object c.
    Cover column c.
    For each r ← D[c], D[D[c]], ..., while r != c,
        set O_k ← r;
        for each j ← R[r], R[R[r]], ..., while j != r,
            cover column j;
        search(k + 1);
        set r ← O_k and c ← C[r];
        for each j ← L[r], L[L[r]], ..., while j != r,
            uncover column j.
    Uncover column c and return.

    Check that there is no solution
    >>> root = create_network([[0, 1],
    ...                        [0, 0]])
    >>> for solution in search(root):
    ...     print_solution(solution)

    Check that there is a valid solution
    >>> root = create_network([
    ...         [0, 0, 1, 0, 1, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 1],
    ...         [0, 1, 1, 0, 0, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 0],
    ...         [0, 1, 0, 0, 0, 0, 1],
    ...         [0, 0, 0, 1, 1, 0, 1]])
    >>> for solution in search(root):
    ...     print_solution(solution)
    0 3
    4 5 2
    1 6
    <BLANKLINE>

    Check that names are used when given
    >>> root = create_network([
    ...         [0, 0, 1, 0, 1, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 1],
    ...         [0, 1, 1, 0, 0, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 0],
    ...         [0, 1, 0, 0, 0, 0, 1],
    ...         [0, 0, 0, 1, 1, 0, 1]],
    ...         names=["A", "B", "C", "D", "E", "F", "G"])
    >>> for solution in search(root):
    ...     print_solution(solution)
    A D
    E F C
    B G
    <BLANKLINE>

    Check that multiple solutions are printed
    >>> root = create_network([
    ...     [1, 0, 1],
    ...     [0, 1, 0],
    ...     [1, 1, 1]],
    ...     names=["A", "B", "C"])
    >>> for solution in search(root):
    ...     print_solution(solution)
    A C
    B
    <BLANKLINE>
    A B C
    <BLANKLINE>
    """
    if solution is None:
        solution = []   # initialise an empty list

    if root.right == root:  # the "matrix" is empty
        yield solution
        return

    col = choose(root)    # choose a column (deterministically)
    col.cover()    # cover column col

    row = col.down
    while row != col:
        solution.append(row)    # include r in the partial solution

        j = row.right
        while j != row:
            j.column.cover()
            j = j.right

        yield from search(root, solution, k+1)   # recurse on reduced matrix
        row = solution.pop()
        col = row.column

        j = row.left
        while j != row:
            j.column.uncover()
            j = j.left

        row = row.down  # try another row

    col.uncover()
    return

def print_solution(solution: list[Link]) -> None:
    """
    Successively print the rows in 'solution'.
    For each row, print N[C[O]], N[C[R[O]]], N[C[R[R[O]]]], etc.
        where O is a link

    >>> root = create_network(
    ...         [[1, 0, 0, 1, 0, 0, 0],
    ...          [0, 1, 0, 0, 0, 0, 1],
    ...          [0, 0, 1, 0, 1, 1, 0]],
    ...         ["A", "B", "C", "D", "E", "F", "G"])
    >>> solution = [root.right.up,
    ...             root.right.right.up,
    ...             root.right.right.right.up]
    >>> print_solution(solution)
    A D
    B G
    C E F
    <BLANKLINE>
    """
    if not solution:
        raise SolutionNotFound

    for link in solution:
        root = link
        print(link.column.name, end="")
        link = link.right
        while link != root:
            print("", link.column.name, end="")
            link = link.right
        print()
    print()

def choose(root: Column) -> Column:
    """Choose a column such that the branching factor is minimised.
    >>> root = create_network([
    ...         [0, 1, 0],
    ...         [1, 1, 0],
    ...         [1, 0, 1]])
    >>> choose(root).name == "2"
    True
    """
    size = float("inf")
    j = root.right
    while j != root:
        if j.size < size:
            col = j
            size = j.size
        j = j.right
    return col
