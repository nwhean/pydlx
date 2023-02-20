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
    c.cover()    # cover column c
    
    r = c.down
    while r != c:
        O.append(r)    # include r in the partial solution
        
        j = r.right
        while j != r:
            j.cover()
            j = j.right
        
        search(root, O)   # repeat recursively on reduced matrix
        r = O.pop()     # remove r from the partion solution
        c = r.column
        
        j = r.left
        while j != r:
            j.uncover()
            j = j.left
        
        r = r.down  # try another row
    
    c.uncover()
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
