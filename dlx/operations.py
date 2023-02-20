from link import Link, Column

def search(root: Column, O=[]) -> None:
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
    """
    if root.right == root:
        print_solution(O)
        return
    
    c = choose(root)    # choose a column (deterministically)
    cover(c)    # cover column c
    
    r = c.down
    while r != c:
        O.append(r)    # include r in the partial solution
        
        j = r.right
        while j != r:
            cover(j)
            j = j.right
        
        search(root, O)   # repeat recursively on reduced matrix
        r = O.pop()     # remove r from the partion solution
        c = r.column
        
        j = r.left
        while j != r:
            uncover(j)
            j = j.left
        
        r = r.down  # try another row
    
    uncover(c)
    return


def print_solution(O: list) -> None:
    """
    Successively print the rows containing O0, O1, ..., Ok-1
    where the row containing data object O is printed by printing
    N[C[O]], N[C[R[O]]], N[C[R[R[O]]]], etc.
    """
    for r in O:
        print(r.column.name)
        j = r.right
        while (j != r):
            print(j.column.name)
            j = j.right


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


def cover(c: Column) -> None:
    """
    Removes c from the header list and removes all rows in c's own list
    from the other column lists they are in.
    """
    # remove c from the header list
    c.right.left = c.left
    c.left.right = c.right
    
    i = c.down  # i is link at the next row
    while i != c:
        # remove rows from c's own list
        j = i.right     # j is the link at the next column from i
        while j != i:
            # remove j from other column list
            j.down.up = j.up
            j.up.down = j.down
            j.column.size -= 1
            j = j.right
        i = i.down


def uncover(c: Column) -> None:
    """Uncover a previously covered column."""
    i = c.up
    while i != c:
        j = i.left
        while j != i:
            # unremove j from other column list
            j.column.size += 1
            j.down.up = j
            j.up.down = j
            j = j.left
        i = i.up
    
    # unremove c from the header list
    c.right.left = c
    c.left.right = c
