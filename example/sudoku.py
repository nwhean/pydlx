"""Solve Sudoku Puzzle using DLX."""
from dancing_link import Link, create_network, xc


class SolutionNotFound(Exception):
    """Raised if no Sudoku Solution is Found."""


class SolutionError(Exception):
    """Raised when the solution is wrong."""


Matrix = list[list[int]]

def read_puzzle(filename: str) -> list[str]:
    """Read a sudoku puzzle and return as a list of strings."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def puzzle_to_matrix(strs: list[str]) -> Matrix:
    """Convert puzzle into an exact cover matrix."""
    retval = []
    for i, row in enumerate(strs):
        for j, char in enumerate(row):
            if char.isdigit():
                candidates = [int(char) - 1]
            else:
                candidates = [i for i in range(9)]
            for k in candidates:
                new_row = [0] * (81 * 4)
                new_row[i*9 + j] = 1    # each cell must be filled
                new_row[81 + i*9 + k] = 1   # unique value in each row, and
                new_row[81*2 + j*9 + k] = 1   # each col, and
                new_row[81*3 + (i//3 * 3 + j//3)*9 + k] = 1     # each block
                retval.append(new_row)
    return retval

def solution_to_matrix(solution: list[Link]) -> Matrix:
    """Convert a dlx solution into Sudoku solution."""
    # initialise a 9 x 9 matrix
    mat = [[-1] * 9 for _ in range(9)]

    for node in solution:
        while node.column:  # move until we reach the row end spacer
            node += 1
        node: Link = node.up      # move to the first node of the row

        # get puzzle index
        node += 1
        column = node.column
        index = int(column.id) - 81 - 1
        i, k = divmod(index, 9)

        node = node + 1
        column = node.column
        index = int(column.id) - 81*2 - 1
        j = index // 9
        if j > 9:
            print(index)

        mat[i][j] = k + 1

    return mat

def verify(matrix: Matrix) -> None:
    """Verify that the solution given is correct."""

    target = set([i for i in range(1, 10)])

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
    for i_o in range(0, 9, 3):
        for j_o in range(0, 9, 3):
            vals = set(matrix[i_o + i][j_o + j]
                       for i in range(3)
                       for j in range(3))
            if vals != target:
                raise SolutionError(f"Incorrect Solution at group {i_o}{j_o}")


if __name__ == "__main__":
    import sys

    puzzle = read_puzzle(sys.argv[1])
    matrix = puzzle_to_matrix(puzzle)
    network = create_network(matrix)

    sol_mat = None
    for sol in xc(network):
        sol_mat = solution_to_matrix(sol)
        verify(sol_mat)
        for _ in sol_mat:
            print(_)
        print()

    if not sol_mat:
        raise SolutionNotFound("Sudoku Puzzle has no solution.")
