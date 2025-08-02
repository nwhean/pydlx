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
    for (r, c, u, d) in cand:
        row: list[int] = [0] * width
        row[r] = 1              # row
        row[n + c] = 1          # column
        row[2*n + u] = 1        # up-diagonal
        row[4*n - 1 + d] = 1    # down-diagonal
        retval.append(row)
    return retval

def queens_names(n):
    """Return the names for the exact cover matrix columns."""
    return [f"R{i}" for i in range(n)] + [f"C{i}" for i in range(n)]

def queens_solution(sol: list[Link]) -> Matrix:
    """Convert exact cover solution to n-queens problem solution."""
    n: int = len(sol)
    retval = [[0] * n for _ in range(n)]
    for node in sol:
        while node.column:  # move until we reach the row end spacer
            node += 1
        node: Link = node.up      # move to the first node of the row

        r = int(node.column.name[1:])
        node += 1
        c = int(node.column.name[1:])

        retval[r][c] = 1

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
