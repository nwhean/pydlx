from typing import List
Row = List[int]

from .link import Link, Column


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
    for j, v in enumerate(matrix[0]):
        if names:
            left = Column(names[j] if j < len(names) else None, left)
        else:
            left = Column(str(j), left)
        header.append(left)
        root.size += 1
    
    for row in matrix:
        left = None
        for v, col in zip(row, header):
            if v:
                left = Link(left)
                col.add_link(left)
    
    return root

def search(root: Column, O=None) -> List[Link]:
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
    
    Check solution is empty if there is none
    >>> root = create_network([[0, 1], [0, 0]])
    >>> solution = search(root)
    >>> not solution
    True
    
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
    >>> print_solution(solution)
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
    >>> print_solution(solution)
    A D
    B G
    C E F
    """
    if O is None:
        O = []
    
    if root.right == root:
        return O
    
    c = choose(root)    # choose a column (deterministically)
    c.cover()    # cover column c
    
    r = c.down
    while r != c:
        O.append(r)    # include r in the partial solution
        
        j = r.right
        while j != r:
            j.column.cover()
            j = j.right
        
        if search(root, O):   # repeat recursively on reduced matrix
            return O
        
        O.pop()     # remove the last row selected
        
        j = r.left
        while j != r:
            j.column.uncover()
            j = j.left
        
        r = r.down  # try another row
    
    c.uncover()
    return

def print_solution(O: List[Link]) -> None:
    """
    Successively print the rows containing O0, O1, ..., Ok-1
    where the row containing data object O is printed by printing
    N[C[O]], N[C[R[O]]], N[C[R[R[O]]]], etc.
    """
    for r in O:
        output = []
        output.append(r.column.name)
        j = r.right
        while (j != r):
            output.append(j.column.name)
            j = j.right
        print(' '.join(sorted(output)))

def choose(root: Column) -> Column:
    """Choose a column such that the branching factor is minimised."""
    s = float("inf")
    j = root.right
    while j != root:
        if j.size < s:
            c = j
            s = j.size
        j = j.right
    return c


if __name__ == "__main__":
    import doctest
    doctest.testmod()
