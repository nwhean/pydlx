"""Solve Skyscraper Puzzle using DLX."""
from collections import defaultdict
from itertools import accumulate, pairwise, permutations

from dancing_link import ColumnColour, LinkColour, create_network, xcc


class SolutionNotFound(Exception):
    """Raised when there is no solution to the problem."""


class SolutionError(Exception):
    """Raised when the solution is wrong."""


Constraint = list[tuple[int, int]]
Matrix = list[list[int]]

def read_puzzle(arg: str) -> tuple[Constraint, Constraint]:
    """Read a Skyscraper puzzle and return the constraints."""
    constraint = [int(i) for i in arg.strip().split(' ')]
    n = len(constraint) // 4

    const_col = []
    const_row = []
    for i in range(n):
        const_col.append((constraint[i], constraint[n + i]))
        const_row.append((constraint[2*n + i], constraint[3*n + i]))

    return const_row, const_col

def see(nums: list[int]) -> int:
    """Return the number of skyscraper seen in the list of numbers."""
    running_max = accumulate(nums, max)
    return sum(x < y for x, y in pairwise(running_max)) + 1

def generate_candidates(n: int) -> dict[tuple, tuple]:
    """Generate all the possible candidates and return as dictionary."""
    nums = list(range(1, n + 1))
    retval = defaultdict(list)
    for candidate in permutations(nums):
        const = (see(candidate), see(candidate[::-1]))
        retval[const].append(candidate)
    return retval

def skyscraper_matrix(candidates: dict[tuple, tuple],
                      const_row: Constraint, const_col: Constraint
                      ) -> Matrix:
    """Convert puzzle into an exact cover matrix."""
    retval = []
    n = len(const_row)

    # handle the rows
    for i, const in enumerate(const_row):
        template = [0] * n * (2 + n)
        template[i] = 1
        for candidate in candidates[const]:
            temp = template.copy()
            for j, k in enumerate(candidate):
                temp[(2 + i)*n + j] = k + 1     # colours start from 2
            retval.append(temp)

    # handle the columns
    for j, const in enumerate(const_col):
        template = [0] * n * (2 + n)
        template[n + j] = 1
        for candidate in candidates[const]:
            temp = template.copy()
            for i, k in enumerate(candidate):
                temp[(2 + i)*n + j] = k + 1     # colours start from 2
            retval.append(temp)

    return retval

def skyscraper_solution(solution: list[LinkColour]) -> Matrix:
    """Convert a dlx solution into Skyscraper solution."""
    n = len(solution) // 2
    retval = [([0] * n) for _ in range(n)]

    for sol in solution:
        if int(sol.column.id) < n:
            continue
        node: LinkColour = sol + 1
        column: ColumnColour= node.column
        while column:
            k = int(column.id) - 2*n - 1
            i, j = divmod(k, n)
            retval[i][j] = int(column.colour)
            node += 1
            column = node.column

    for i, row in enumerate(retval):
        for j, val in enumerate(row):
            if val == 0:
                raise SolutionError(f"Incorrect solution at ({i}, {j}).")

    return retval

def verify(solution: Matrix,
           const_row: Constraint, const_col: Constraint) -> None:
    """Verify that the solution given is correct."""

    # check each row
    for i, row in enumerate(solution):
        if (see(row), see(row[::-1])) != const_row[i]:
            raise SolutionError(f"Incorrect Solution at row {i}")

    # check each column
    for j, const in enumerate(const_col):
        col = [sub[j] for sub in solution]
        if (see(col), see(col[::-1])) != const:
            raise SolutionError(f"Incorrect Solution at column {j}")

def main(filename: str):
    """Return the solution of the Skyscrapper puzzle."""
    const_row, const_col = read_puzzle(filename)
    candidates = generate_candidates(len(const_row))
    matrix = skyscraper_matrix(candidates, const_row, const_col)
    print(f"Exact cover matrix size: {len(matrix)}, {len(matrix[0])}")

    network = create_network(matrix, primary=len(const_row)*2)
    for sol in xcc(network):
        sol_matrix = skyscraper_solution(sol)
        for i in sol_matrix:
            print(i)
        break
    else:
        raise SolutionNotFound("The puzzle has no solution.")

    # check that the solution is correct
    verify(sol_matrix, const_row, const_col)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
