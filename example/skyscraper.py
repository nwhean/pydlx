"""Solve Skyscraper Puzzle using DLX."""
from collections import defaultdict
from itertools import accumulate, pairwise, permutations

from dancing_link import NetworkColour


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
                temp[(2 + i)*n + j] = str(k)
            retval.append(temp)

    # handle the columns
    for j, const in enumerate(const_col):
        template = [0] * n * (2 + n)
        template[n + j] = 1
        for candidate in candidates[const]:
            temp = template.copy()
            for i, k in enumerate(candidate):
                temp[(2 + i)*n + j] = str(k)
            retval.append(temp)

    return retval

def skyscraper_solution(network: NetworkColour, solution: list[int]) -> Matrix:
    """Convert a dlx solution into Skyscraper solution."""
    n = len(solution) // 2
    retval = [([0] * n) for _ in range(n)]

    for node in solution:
        if int(network.top[node]) > n:  # only consider row solutions
            continue

        node += 1
        column = network.top[node]
        while column > 0:
            k = int(column) - 2*n - 1
            i, j = divmod(k, n)
            c = network.colour[column]
            retval[i][j] = int(network.colour_map_inv[c])
            node += 1
            column = network.top[node]

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

    network = NetworkColour(matrix, primary=len(const_row)*2)
    for sol in network.search():
        sol_matrix = skyscraper_solution(network, sol)
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
