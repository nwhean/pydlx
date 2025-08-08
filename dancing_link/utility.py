"""Contains the implementation of DLX algorithm."""


def mrv(network) -> int:
    """Return the column with the minimum remaining values."""
    retval = 0
    j = network.right[0]
    l = network.len[j] + 1

    while j != 0:
        if network.len[j] < l:
            retval = j
            l = network.len[j]
        j = network.right[j]

    return retval

def progress(choices: list[int], branches: list[int]) -> float:
    """Calculate the progress of the algorithm.

    Parameters
    ----------
    choices : list[int]
              list containing the index of the choices chosen at each level
    branches : list[int]
               list containing the total number of choices at each level
    """
    retval = 0.5
    for c, l in zip(choices[::-1], branches[::-1]):
        retval += c - 1
        retval /= l
    return retval
