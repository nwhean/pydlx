"""Contains the implementation of DLX algorithm."""
from .link import Link, Column


class SolutionNotFound(Exception):
    """Raised when there is no solution to the problem."""


def create_network(matrix: list[list[int]], names=None) -> Column:
    """Convert a matrix into a dancing link network and return the root.
    >>> root = create_network([
    ...         [0, 1],
    ...         [1, 1]])
    >>> root.size == 2
    True

    # put all headers in a list
    >>> header0 = root.right
    >>> header1 = root.right.right
    >>> header0.left == root
    True
    >>> header0.right == header1
    True
    >>> header1.left == header0
    True
    >>> header1.right == root
    True

    # check that the links are correctly placed
    >>> link01 = header1.down
    >>> link10 = header0.down
    >>> link11 = header1.down.down
    >>> link01.left == link01
    True
    >>> link01.right == link01
    True
    >>> link01.up == header1
    True
    >>> link01.down == link11
    True
    >>> link10.left == link11
    True
    >>> link10.right == link11
    True
    >>> link10.up == header0
    True
    >>> link10.down == header0
    True
    >>> link11.left == link10
    True
    >>> link11.right == link10
    True
    >>> link11.up == link01
    True
    >>> link11.down == header1
    True
    """
    # automatically generate names if not given
    if names is None:
        names = [str(i) for i in range(len(matrix[0]))]

    # create the root header
    root = Column("")
    root.size = len(matrix[0])

    # create the header list
    left = root
    headers = []
    for name in names:
        header = Column(name)
        left.add_right(header)
        left = header
        headers.append(header)

    for row in matrix:
        left = None
        for val, header in zip(row, headers):
            if val:
                link = Link(header)
                if left is not None:
                    left.add_right(link)
                left = link

    return root

def search(root: Column, solution: list[Link] = None, k: int = 0
           ) -> list[Link]:
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
    >>> root = create_network([[0, 1], [0, 0]])
    >>> solution = search(root)
    >>> not solution
    True

    Check that there is a valid solution
    >>> root = create_network([
    ...         [0, 0, 1, 0, 1, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 1],
    ...         [0, 1, 1, 0, 0, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 0],
    ...         [0, 1, 0, 0, 0, 0, 1],
    ...         [0, 0, 0, 1, 1, 0, 1]])
    >>> solution = search(root)
    >>> print_solution(solution)
    0 3
    4 5 2
    1 6

    Check that names are used when given
    >>> root = create_network([
    ...         [0, 0, 1, 0, 1, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 1],
    ...         [0, 1, 1, 0, 0, 1, 0],
    ...         [1, 0, 0, 1, 0, 0, 0],
    ...         [0, 1, 0, 0, 0, 0, 1],
    ...         [0, 0, 0, 1, 1, 0, 1]],
    ...         names=["A", "B", "C", "D", "E", "F", "G"])
    >>> solution = search(root)
    >>> print_solution(solution)
    A D
    E F C
    B G
    """
    if solution is None:
        solution = []   # initialise an empty list

    if root.right == root:  # the "matrix" is empty
        return solution

    col = choose(root)    # choose a column (deterministically)
    col.cover()    # cover column col

    row = col.down
    while row != col:
        solution.append(row)    # include r in the partial solution

        j = row.right
        while j != row:
            j.column.cover()
            j = j.right

        temp = search(root, solution, k+1)   # recurse on reduced matrix
        if temp:
            return solution     # return if a solution is found
        row = solution.pop()
        col = row.column

        j = row.left
        while j != row:
            j.column.uncover()
            j = j.left

        row = row.down  # try another row

    col.uncover()
    return None

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
