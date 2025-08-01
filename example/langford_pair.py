"""
Langford sequence, is a permutation of the sequence of 2n numbers
1, 1, 2, 2, ..., n, n in which the two 1s are one unit apart, the two 2s
are two units apart, and more generally the two copies of each number k
are k units apart.
"""
from pydlx import Link, create_network, ecx


Matrix = list[list[int]]

def langford_candidates(n: int) -> list[tuple[int]]:
    """Return all the valid candidates for a langford pair of size n."""
    retval: list[tuple[int]] = []
    for i in range(1, n + 1):
        j = 0
        k = i + j + 1
        while k < 2 * n:
            retval.append((i, j, k))
            j += 1
            k += 1
    return retval

def langford_matrix(n: int, cand: list[tuple[int]]) -> Matrix:
    """Return the exact cover matrix for size 'n' langford pair."""
    retval = []
    for (i, j, k) in cand:
        row: list[int] = [0] * 3 * n
        row[i - 1] = 1      # i
        row[n + j] = 1      # j
        row[n + k] = 1      # k
        retval.append(row)
    return retval

def langford_names(n: int) -> list[str]:
    """Return the names for the exact cover matrix columns."""
    return [str(i) for i in range(1, n+1)] + [str(i) for i in range(0, 2*n)]

def langford_solution(sol: list[Link]) -> str:
    """Convert exact cover solution to Langford pair string."""
    retval = [0] * len(sol) * 2
    for node in sol:
        while node.column:  # move until we reach the row end spacer
            node += 1
        node: Link = node.up      # move to the first node of the row

        i = node.column.name
        node += 1
        j = int(node.column.name)
        node += 1
        k = int(node.column.name)

        retval[j] = i
        retval[k] = i

    return ''.join(retval)

def main():
    """Calculate the number of solutions to Langford Pairs."""
    for n in range(1, 10):
        candidates = langford_candidates(n)
        if not candidates:
            print(f"n = {n}, solutions = 0")
            continue

        matrix = langford_matrix(n, candidates)
        names = langford_names(n)
        network = create_network(matrix, names)
        solutions = [_ for _ in ecx(network)]

        print(f"n = {n:,}, solutions = {len(solutions) // 2:,}")
        network.delete()


if __name__ == '__main__':
    main()
