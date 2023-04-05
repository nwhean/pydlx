"""Contains the implementation of DLX algorithm."""

from typing import List

from .link import Link, Column

Row = List[int]


def create_network(matrix: List[Row], names=None) -> Column:
    """Convert a matrix into a dancing link network and return the root.
    >>> root = create_network([\
    [0, 1],\
    [1, 1]\
    ])
    >>> root.size == 2
    True
    >>> header = [root.right, root.right.right]
    >>> root.right == header[0]
    True
    >>> root.left == header[1]
    True
    >>> header[0].left == root
    True
    >>> header[0].right == header[1]
    True
    >>> header[1].left == header[0]
    True
    >>> header[1].right == root
    True
    >>> link01 = header[1].down
    >>> link01.left == link01
    True
    >>> link01.right == link01
    True
    >>> link01.up == header[1]
    True
    >>> link01.down == header[1].up
    True
    """
    # create the root header
    root = Column("")

    # create the column header
    header = []
    left = root
    for j, _ in enumerate(matrix[0]):
        if names:
            left = Column(names[j] if j < len(names) else None, left)
        else:
            left = Column(str(j), left)
        header.append(left)
        root.size += 1

    for row in matrix:
        left = None
        for val, col in zip(row, header):
            if val:
                left = Link(left)
                col.add_link(left)

    return root

def search(root: Column, solution=None, k=0) -> List[Link]:
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
    >>> next(solution)
    Traceback (most recent call last):
    ...
    StopIteration
    
    Check that there is a valid solution
    >>> root = create_network([\
    [0, 0, 1, 0, 1, 1, 0], \
    [1, 0, 0, 1, 0, 0, 1], \
    [0, 1, 1, 0, 0, 1, 0], \
    [1, 0, 0, 1, 0, 0, 0], \
    [0, 1, 0, 0, 0, 0, 1], \
    [0, 0, 0, 1, 1, 0, 1]\
    ])
    >>> solution = search(root)
    >>> for i in solution:\
        print_solution(i)
    0 3
    1 6
    2 4 5
    
    Check that names are used when given
    >>> root = create_network([\
    [0, 0, 1, 0, 1, 1, 0], \
    [1, 0, 0, 1, 0, 0, 1], \
    [0, 1, 1, 0, 0, 1, 0], \
    [1, 0, 0, 1, 0, 0, 0], \
    [0, 1, 0, 0, 0, 0, 1], \
    [0, 0, 0, 1, 1, 0, 1] \
    ], \
    names=["A", "B", "C", "D", "E", "F", "G"] \
    )
    >>> solution = search(root)
    >>> for i in solution:\
        print_solution(i)
    A D
    B G
    C E F
    
    Check that multiple solutions are printed
    >>> root = create_network([\
    [1, 0, 1], \
    [0, 1, 0], \
    [1, 1, 1] \
    ], \
    names=["A", "B", "C"] \
    )
    >>> solution = search(root)
    >>> for i in solution:\
        print_solution(i)
    A C
    B
    A B C
    """
    if solution is None:
        solution = [0] * root.size

    if root.right == root:
        yield solution

    col = choose(root)    # choose a column (deterministically)
    col.cover()    # cover column c

    row = col.down
    while row != col:
        solution[k] = row    # include r in the partial solution

        j = row.right
        while j != row:
            j.column.cover()
            j = j.right

        solution = search(root, solution, k+1)   # recurse on reduced matrix
        try:
            if next(solution):
                yield [i for i in solution if i]
        except StopIteration:
            pass
        finally:
            row = solution[k]
            solution[k] = 0    # remove the last row selected
            col = row.column

        j = row.left
        while j != row:
            j.column.uncover()
            j = j.left

        row = row.down  # try another row

    col.uncover()
    return

def print_solution(solution: List[Link]) -> None:
    """
    Successively print the rows containing O0, O1, ..., Ok-1
    where the row containing data object O is printed by printing
    N[C[O]], N[C[R[O]]], N[C[R[R[O]]]], etc.
    """
    for row in solution:
        output = []
        output.append(row.column.name)
        j = row.right
        while j != row:
            output.append(j.column.name)
            j = j.right
        print(' '.join(sorted(output)))

def choose(root: Column) -> Column:
    """Choose a column such that the branching factor is minimised."""
    size = float("inf")
    j = root.right
    while j != root:
        if j.size < size:
            col = j
            size = j.size
        j = j.right
    return col


if __name__ == "__main__":
    import doctest
    doctest.testmod()
