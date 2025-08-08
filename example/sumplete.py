"""Solve Sumplete Puzzle using DLX."""
from dancing_link import NetworkColour


class SolutionNotFound(Exception):
    """Raised when there is no solution to the problem."""


class SolutionError(Exception):
    """Raised when the solution is wrong."""

Matrix = list[list[int]]
Constraint = list[int]

def read_puzzle(filename: str) -> tuple[Matrix, Constraint, Constraint]:
    """Read a Sumplete puzzle and return the matrix and constraint."""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
    puzzle = []
    const_row = []

    for l in lines[:-1]:
        temp = [int(c) for c in l.split()]
        puzzle.append(temp[:-1])
        const_row.append(temp[-1])
    const_col = [int(c) for c in lines[-1].split()]

    return puzzle, const_row, const_col

def sumplete_matrix(
        puzzle: Matrix, const_row: Constraint, const_col: Constraint) -> Matrix:
    """Convert puzzle into an exact cover matrix."""
    n = len(puzzle[0])
    combo = 2**n
    retval = []

    # handle each row
    for i, row in enumerate(puzzle):
        template = [0] * n * (2 + n)
        template[i] = 1     # primary column for rows
        for k in range(combo):
            condition = format(k, f'0{n}b')      # convert 'k' to bin string
            if sumproduct_equal(row, condition, const_row[i]):
                temp = template.copy()
                for j, c in enumerate(condition):
                    temp[(2 + i)*n + j] = str(c)
                retval.append(temp)

    # handle each column
    for j in range(n):
        col = [sub[j] for sub in puzzle]
        template = [0] * n * (2 + n)
        template[n + j] = 1  # primary column for columns
        for k in range(combo):
            condition = format(k, f'0{n}b')
            if sumproduct_equal(col, condition, const_col[j]):
                temp = template.copy()
                for i, c in enumerate(condition):
                    temp[(2 + i)*n + j] = str(c)
                retval.append(temp)

    return retval

def sumproduct_equal(nums: list[int], condition: str, val: int):
    """Return True if subset of `nums` given the `condition` sums to `val`."""
    return sum(i for i, j in zip(nums, condition) if j == '1') == val

def sumplete_solution(network: NetworkColour, solution: list[int]) -> Matrix:
    """Convert a dlx solution into Sumplete solution."""
    n = len(solution) // 2
    retval = [([0] * n) for _ in range(n)]

    for node in solution:
        column = network.top[node]
        if int(column) > n:   # only consider row solutions
            continue

        node = node + 1
        column = network.top[node]
        while column > 0:
            k = int(network.name[column]) - 2*n - 1
            i, j = divmod(k, n)
            c = network.colour[column]
            retval[i][j] = int(network.colour_map_inv[c])
            node += 1
            column = network.top[node]

    return retval

def verify(puzzle: Matrix, solution: Matrix,
           const_row: Constraint, const_col: Constraint) -> None:
    """Verify that the solution given is correct."""

    # check each row
    for i, (row, sol_row, val) in enumerate(zip(puzzle, solution, const_row)):
        if not sumproduct_equal(row, ''.join(str(i) for i in sol_row), val):
            raise SolutionError(f"Incorrect Solution at row {i}")

    # check each column
    for j, val in enumerate(const_col):
        col = [sub[j] for sub in puzzle]
        sol_col = [sub[j] for sub in solution]
        if not sumproduct_equal(col, ''.join(str(i) for i in sol_col), val):
            raise SolutionError(f"Incorrect Solution at column {j}.")

def main(filepath: str):
    """Calculate the solution to Sumplete puzzle."""
    puzzle, const_row, const_col = read_puzzle(filepath)
    matrix = sumplete_matrix(puzzle, const_row, const_col)
    network = NetworkColour(matrix, primary=len(const_row)*2)

    for sol in network.search():
        sol_matrix = sumplete_solution(network, sol)
        for i in sol_matrix:
            print(i)
        break   # only consider the first valid solution
    else:
        raise SolutionNotFound("The puzzle has no solution.")

    # check that the solution is correct
    verify(puzzle, sol_matrix, const_row, const_col)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
