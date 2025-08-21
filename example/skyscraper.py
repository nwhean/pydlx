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

def generate_valids(const_row: Constraint, const_col: Constraint):
    """Apply edge clue elimination and return valid number for each cell."""
    n = len(const_row)

    # fill all cells with all numbers
    s = set(_ for _ in range(1, n+1))
    retval = {}
    for i in range(n):
        for j in range(n):
            retval[(i, j)] = s.copy()

    for i, (l, r) in enumerate(const_row):
        for j in range(n):
            for k in range(n + 2 - l + j, n + 1):   # apply left clue
                retval[(i, j)].discard(k)
            for k in range(2*n + 1 - r - j, n + 1): # apply right clue
                retval[(i, j)].discard(k)
        if l == 2:
            retval[(i, 1)].discard(n - 1)
        if r == 2:
            retval[(i, n - 2)].discard(n - 1)

    for j, (t, b) in enumerate(const_col):
        for i in range(n):
            for k in range(n + 2 - t + i, n + 1):   # apply top clue
                retval[(i, j)].discard(k)
            for k in range(2*n + 1 - b - i, n + 1): # apply bottom clue
                retval[(i, j)].discard(k)
        if t == 2:
            retval[(1, j)].discard(n - 1)
        if b == 2:
            retval[(n - 2, j)].discard(n - 1)

    return retval

def is_valid_row(valids: dict[(int, int), set[int]], i: int,
                 candidate: list[int]) -> bool:
    """Return True if row candidate is valid, false otherwise."""
    for j, k in enumerate(candidate):
        if k not in valids[(i, j)]:
            return False
    return True

def is_valid_col(valids: dict[(int, int), set[int]], j: int,
                 candidate: list[int]) -> bool:
    """Return True if col candidate is valid, false otherwise."""
    for i, k in enumerate(candidate):
        if k not in valids[(i, j)]:
            return False
    return True

def skyscraper_matrix(valids: dict[(int, int), set[int]],
                      candidates: dict[tuple, tuple],
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
            # disregard invalid candidates
            if not is_valid_row(valids, i, candidate):
                continue

            temp = template.copy()
            for j, k in enumerate(candidate):
                temp[(2 + i)*n + j] = str(k)
            retval.append(temp)

    # handle the columns
    for j, const in enumerate(const_col):
        template = [0] * n * (2 + n)
        template[n + j] = 1
        for candidate in candidates[const]:
            # disregard invalid candidates
            if not is_valid_col(valids, j, candidate):
                continue

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
    valids = generate_valids(const_row, const_col)
    candidates = generate_candidates(len(const_row))
    matrix = skyscraper_matrix(valids, candidates, const_row, const_col)
    print(f"Exact cover matrix size: {len(matrix)}, {len(matrix[0])}")

    network = NetworkColour(matrix, primary=len(const_row)*2)
    print(f"Total number of nodes: {len(network.top)}")
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
