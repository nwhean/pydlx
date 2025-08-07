"""Solve Sudoku Puzzle using DLX."""
import string

from dancing_link import Link, create_network, xc


class SolutionNotFound(Exception):
    """Raised if no Sudoku Solution is Found."""


class SolutionError(Exception):
    """Raised when the solution is wrong."""


CHARS = string.digits + string.ascii_uppercase
INT2CHAR = {i: j for i, j in enumerate(CHARS)}
CHAR2INT = {j: i for i, j in enumerate(CHARS)}

Matrix = list[list[int]]

def read_puzzle(filename: str) -> list[str]:
    """Read a sudoku puzzle and return as a list of strings."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def sudoku_matrix(n: int, strs: list[str]) -> Matrix:
    """Convert puzzle into an exact cover matrix."""
    n2 = n**2
    nr = int(n**0.5)

    retval = []
    for i, row in enumerate(strs):
        if len(row) != n:
            raise ValueError("Unequal row and column size.")

        for j, c in enumerate(row):
            if c == '.':
                candidates = [i for i in range(n)]
            else:
                candidates = [CHAR2INT[c] - 1]
            for k in candidates:
                new_row = [0] * (n2 * 4)
                new_row[i*n + j] = 1            # each cell must be filled
                new_row[n2 + i*n + k] = 1       # unique value in each row, and
                new_row[n2*2 + j*n + k] = 1     # each col, and
                new_row[n2*3 + (i//nr * nr + j//nr)*n + k] = 1 # each block
                retval.append(new_row)
    return retval

def sudoku_solution(n:int, solution: list[Link]) -> Matrix:
    """Convert a dlx solution into Sudoku solution."""
    # initialise a n x n matrix
    mat = [[-1] * n for _ in range(n)]
    n2 = n**2

    for node in solution:
        while node.column:  # move until we reach the row end spacer
            node += 1
        node: Link = node.up      # move to the first node of the row

        # get puzzle index
        node += 1
        column = node.column
        index = int(column.id) - n2 - 1
        i, k = divmod(index, n)

        node = node + 1
        column = node.column
        index = int(column.id) - n2*2 - 1
        j = index // n

        mat[i][j] = INT2CHAR[k + 1]

    return mat

def verify(n:int, matrix: Matrix) -> None:
    """Verify that the solution given is correct."""
    nr = int(n**0.5)

    target = set(INT2CHAR[i] for i in range(1, n+1))

    # check each row
    for i, row in enumerate(matrix):
        vals = set(row)
        if vals != target:
            raise SolutionError(f"Incorrect Solution at row {i}")

    # check each column
    for j in range(len(matrix)):
        vals = set(row[j] for row in matrix)
        if vals != target:
            raise SolutionError(f"Incorrect Solution at col {j}")

    # check each group
    for i_o in range(0, n, nr):
        for j_o in range(0, n, nr):
            vals = set(matrix[i_o + i][j_o + j]
                       for i in range(nr)
                       for j in range(nr))
            if vals != target:
                raise SolutionError(f"Incorrect Solution at group {i_o}{j_o}")


def main(filename: str):
    """Return the solution of the Sudoku puzzle."""
    puzzle = read_puzzle(filename)
    n = len(puzzle)
    matrix = sudoku_matrix(n, puzzle)
    network = create_network(matrix)

    sol_mat = None
    for sol in xc(network):
        sol_mat = sudoku_solution(n, sol)
        verify(n, sol_mat)
        for row in sol_mat:
            print(", ".join(c for c in row))
        print()

    if not sol_mat:
        raise SolutionNotFound("Sudoku Puzzle has no solution.")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
