"""Skyscraper Puzzle Generator."""
from itertools import accumulate, pairwise
import random

def rm_unavailable(tbl, avail_num, i, j, size):
    """Remove unavailable candidate from avai_num list."""
    # remove existing candidate from same column
    for tmp in range(0, size):
        try:
            avail_num.remove(tbl[i][tmp])
        except ValueError:
            pass

    # remove existing candidate from same row
    for tmp in range(0, size):
        try:
            avail_num.remove(tbl[tmp][j])
        except ValueError:
            pass
    return avail_num

def see(nums: list[int]) -> int:
    """Return the number of skyscraper seen in the list of numbers."""
    running_max = accumulate(nums, max)
    return sum(x < y for x, y in pairwise(running_max)) + 1

def print_views(tbl, size):
    """Print the top, bot, left and right constraints of the puzzle."""
    top = []
    bot = []
    left = []
    right = []
    for j in range(0, size):
        nums = [tbl[i][j] for i in range(size)]
        top.append(see(nums))
        bot.append(see(nums[::-1]))

    for i in range(0, size):
        left.append(see(tbl[i]))
        right.append(see(tbl[i][::-1]))

    print(" ".join(str(i) for i in sum([top, bot, left, right], [])))

def print_table(tbl, size):
    """Print the generated Skyscraper Puzzle."""
    # calculate the width of the numbers
    width = 0
    n = size
    while n:
        width += 1
        n //= 10
    str_format = "{:>" + str(width) + "}"

    print()
    for i in range(0, size):
        for j in range(0, size):
            print (str_format.format(tbl[i][j]), end=" ")
        print()

def generate_table(size):
    """Return a Skyscraper Puzzle if valid, or None otherwise. """
    tbl = [[0 for x in range(size)] for y in range(size)]
    for i in range(0, size):
        for j in range(0, size):
            avail_num = list(range(1, size + 1))
            avail_num = rm_unavailable(tbl, avail_num, i, j, size)
            if not avail_num:
                return None
            tbl[i][j] = random.choice(avail_num)

    return tbl


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print ("Usage: ./generator <size>")
        sys.exit(0)
    size = int(sys.argv[1])
    tbl = None
    while tbl is None:
        tbl = generate_table(size)
    print_views(tbl, size)
    print_table(tbl, size)
