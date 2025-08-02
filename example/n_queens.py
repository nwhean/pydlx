"""n queens problem: placing n non-attacking queens on an n×n chessboard."""
from pydlx import Link, create_network, ecx


Matrix = list[list[int]]


def queens_candidates(n: int) -> list[tuple[int]]:
    """Return a list containing the position a candidate and its location:
    where each entry contains:
    R: row
    C: column
    U: up-right diagonal
    D: down-right diagonal
    """
    retval: list[tuple[int]] = []
    for i in range(n):
        for j in range(n):
            retval.append((i, j, i+j, n-1-i+j))
    return retval

def queens_matrix(n: int, cand: list[tuple[int]]) -> Matrix:
    """Return the exact cover matrix for size 'n' n-queens problem."""
    width = 2 * n + 2 * (2*n - 1)
    retval = []
    # example of n = 8
    # instead of R0 R1 . . . R7 F0 F1 . . . F7
    # we order by R4 F4 R3 F3 R5 F5 R2 F2 R6 F6 R1 F1 R7 F7 R0 F0
    # to make the column that is most constraining chosen
    order = organ_pipe_ordering(n)
    for (r, c, u, d) in cand:
        row: list[int] = [0] * width
        r_index = order.index(r)
        c_index = order.index(c)
        row[r_index * 2] = 1        # row
        row[c_index * 2 + 1] = 1    # column
        row[2*n + u] = 1            # up-diagonal
        row[4*n - 1 + d] = 1        # down-diagonal
        retval.append(row)
    return retval

def queens_names(n):
    """Return the names for the exact cover matrix columns."""
    order = organ_pipe_ordering(n)
    retval = []
    for i in order:
        retval.append(f"R{i}")
        retval.append(f"C{i}")
    return retval

def queens_solution(sol: list[Link]) -> Matrix:
    """Convert exact cover solution to n-queens problem solution."""
    n: int = len(sol)
    matrix = [[0] * n for _ in range(n)]
    for node in sol:
        while node.column:  # move until we reach the row end spacer
            node += 1
        node: Link = node.up      # move to the first node of the row

        count = 0
        while count < 2:
            if node.column.name[0] == "R":
                r = int(node.column.name[1:])
            else:
                c = int(node.column.name[1:])
            node += 1
            count += 1

        matrix[r][c] = 1

    character = {0: '.', 1: 'Q'}
    retval = '\n'.join(' '.join(character[j] for j in i) for i in matrix) + '\n'
    return retval

def organ_pipe_ordering(n: int) -> list[int]:
    """Return the organ pipe ordering of a list of number from 0 to n - 1."""
    mid = n//2
    retval = [mid]
    for i in range(1, mid + 1):
        val = mid - i
        if val >= 0:
            retval.append(val)
        val = mid + i
        if val < n:
            retval.append(val)
    return retval


def main():
    """Calculate the number of solutions to n-Queens Problem."""
    for n in range(1, 10):
        candidates = queens_candidates(n)
        matrix = queens_matrix(n, candidates)
        names = queens_names(n)
        network = create_network(matrix, names, primary=2*n)
        solutions = [_ for _ in ecx(network)]

        print(f"n = {n:,}, solutions = {len(solutions):,}")
        network.delete()


if __name__ ==  "__main__":
    main()
