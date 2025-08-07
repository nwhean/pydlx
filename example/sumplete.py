"""Solve Sumplete Puzzle using DLX."""
from dancing_link import ColumnColour, LinkColour, create_network, xcc


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
    size = len(puzzle[0])
    combo = 2**size
    retval = []

    # handle each row
    for i, row in enumerate(puzzle):
        template = [0] * size * (2 + size)
        template[i] = 1     # primary column for rows
        for k in range(combo):
            condition = format(k, f'0{size}b')      # convert 'k' to bin string
            if sumproduct_equal(row, condition, const_row[i]):
                temp = template.copy()
                for j, c in enumerate(condition):
                    temp[(2 + i)*size + j] = int(c) + 2
                    # matrix representation: 2 = off, 3 = on
                    # dancing link representation: 1 = off, 2 = on
                retval.append(temp)

    # handle each column
    for j in range(size):
        col = [sub[j] for sub in puzzle]
        template = [0] * size * (2 + size)
        template[size + j] = 1  # primary column for columns
        for k in range(combo):
            condition = format(k, f'0{size}b')
            if sumproduct_equal(col, condition, const_col[j]):
                temp = template.copy()
                for i, c in enumerate(condition):
                    temp[(2 + i)*size + j] = int(c) + 2
                retval.append(temp)

    return retval

def sumproduct_equal(nums: list[int], condition: str, val: int):
    """Return True if subset of `nums` given the `condition` sums to `val`."""
    return sum(i for i, j in zip(nums, condition) if j == '1') == val

def sumplete_solution(solution: list[LinkColour]) -> Matrix:
    """Convert a dlx solution into Sumplete solution."""
    size = len(solution) // 2
    retval = [([0] * size) for _ in range(size)]

    for sol in solution:
        if int(sol.column.id) > size:   # only consider row solutions
            continue
        node: LinkColour = sol + 1
        column: ColumnColour= node.column
        while column:
            k = int(column.id) - 2*size - 1
            i, j = divmod(k, size)
            retval[i][j] = int(column.colour - 1)
            node += 1
            column = node.column

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
    network = create_network(matrix, primary=len(const_row)*2)

    for sol in xcc(network):
        sol_matrix = sumplete_solution(sol)
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
