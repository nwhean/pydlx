"""Contains the algorithms associated with Dancing Link."""
from typing import Generator
import time

from .link import Column, ColumnColour, Link, Link, LinkColour
from .utility import mrv, progress


def xc(root: Column,
        sol: list[Link] | None = None,
        level: int = 0,
        choose=mrv,
        interval: int | None = None,
        **kwargs
        ) -> Generator[list[Link], None, None]:
    """Exact Cover via Dancing Link using Algorithm X.

    Parameters
    ----------
    root : Column
           the root node of the exact cover network
    sol : list[Link] | None
          a list containing the partial solution to the exact cover problem
    level : int
            the current level of search tree
    choose : Callable[Column, Column]
             heuristics function that returns the next column to be chosen
    interval : int | None, default = None
               the time interval between printing progess status.
               None: no progress status printed
               0: progress status is printed at every node
    """
    if sol is None:
        sol = []

    # handle keyword arguments
    if 'choices' not in kwargs:     # index of the choice chosen at a level
        kwargs['choices'] = []
    if 'branches' not in kwargs:    # total number of choices at a level
        kwargs['branches'] = []
    if 'start_time' not in kwargs:  # time when algorithm started
        kwargs['start_time'] = time.time()
    if 'threshold' not in kwargs and interval is not None:
        kwargs['threshold'] = [interval]    # value above which status printed

    # Step X2: Enter Level `level`
    # handle the progress report printing
    start_time = kwargs.get('start_time')
    threshold = kwargs.get('threshold')
    choices = kwargs.get('choices')
    branches = kwargs.get('branches')

    runtime = time.time() - start_time
    if threshold and runtime > threshold[-1]:
        threshold[-1] += interval
        print(f"{runtime:.3f}", end=" ")
        print(f"{progress(choices, branches):.5f}", end=" ")
        for c, l in zip(choices, branches):
            print(f"{c}/{l}", end=" ")
        print()

    if root.right == root:  # all items have been covered
        # visit the solution specified by x_0 x_1 x_2 ... x_level-1
        yield sol

        # Step X8: Leave Level `level`
        # if level == 0:  # terminate if level == 0
        #     return
        # else:
        #     level -= 1
        #     return      # go to X6
        return

    # Step X3: Choose item `i`
    i: Column = choose(root)

    # Step X4: Cover item `i`
    i.cover()
    branches.append(i.size)
    x: Link = i.down
    sol.append(x)
    choices.append(1)   # the first choice

    # Step X5: Try x_l
    while x != i:
        # This covers the items != i in the option that contains x_l.
        node: Link = x + 1
        while node != x:
            column: Column = node.column
            if not column:  # node is a spacer
                node = node.up
            else:
                column.cover()
                node += 1

        yield from xc(root, sol, level+1, choose=choose, interval=interval,
                       **kwargs)

        # Step X6: Try again
        # This uncovers the items != i in the option that contains x_l,
        # using the reverse of the order in X5.
        node: Link = x - 1
        while node != x:
            column: Column = node.column
            if not column:  # node is a spacer
                node = node.down
            else:
                column.uncover()
                node -= 1

        x = x.down
        sol[-1] = x
        choices[-1] += 1

    # tried all options for i
    # Step X7: Backtrack
    i.uncover()
    del sol[-1]
    del choices[-1]
    del branches[-1]

def xcc(root: ColumnColour,
        sol: list[LinkColour] | None = None,
        level: int = 0,
        choose=mrv,
        interval: int | None = None,
        **kwargs
        ) -> Generator[list[LinkColour], None, None]:
    """Exact Cover with Colour via Dancing Link using Algorithm C.

    Parameters
    ----------
    root : ColumnColour
           the root node of the exact cover network
    sol : list[Link] | None
          a list containing the partial solution to the exact cover problem
    level : int
            the current level of search tree
    choose : Callable[ColumnColour, ColumnColour]
             heuristics function that returns the next column to be chosen
    interval : int | None, default = None
               the time interval between printing progess status.
               None: no progress status printed
               0: progress status is printed at every node
    """
    if sol is None:
        sol = []

    # handle keyword arguments
    if 'choices' not in kwargs:     # index of the choice chosen at a level
        kwargs['choices'] = []
    if 'branches' not in kwargs:    # total number of choices at a level
        kwargs['branches'] = []
    if 'start_time' not in kwargs:  # time when algorithm started
        kwargs['start_time'] = time.time()
    if 'threshold' not in kwargs and interval is not None:
        kwargs['threshold'] = [interval]    # value above which status printed

    # Step C2: Enter Level `level`
    # handle the progress report printing
    start_time = kwargs.get('start_time')
    threshold = kwargs.get('threshold')
    choices = kwargs.get('choices')
    branches = kwargs.get('branches')

    runtime = time.time() - start_time
    if threshold and runtime > threshold[-1]:
        threshold[-1] += interval
        print(f"{runtime:.3f}", end=" ")
        print(f"{progress(choices, branches):.5f}", end=" ")
        for c, l in zip(choices, branches):
            print(f"{c}/{l}", end=" ")
        print()

    if root.right == root:  # all items have been covered
        # visit the solution specified by x_0 x_1 x_2 ... x_level-1
        yield sol

        # Step X8: Leave Level `level`
        # if level == 0:  # terminate if level == 0
        #     return
        # else:
        #     level -= 1
        #     return      # go to X6
        return

    # Step C3: Choose item `i`
    i: ColumnColour = choose(root)

    # Step C4: Cover item `i`
    i.cover()
    branches.append(i.size)
    x: LinkColour = i.down
    sol.append(x)
    choices.append(1)   # the first choice

    # Step C5: Try x_l
    while x != i:
        # This covers the items != i in the option that contains x_l.
        node: LinkColour = x + 1
        while node != x:
            column: ColumnColour = node.column
            if not column:  # node is a spacer
                node = node.up
            else:
                node.commit()
                node += 1

        yield from xcc(root, sol, level+1, choose=choose, interval=interval,
                       **kwargs)

        # Step C6: Try again
        # This uncovers the items != i in the option that contains x_l,
        # using the reverse of the order in X5.
        node: LinkColour = x - 1
        while node != x:
            column: ColumnColour = node.column
            if not column:  # node is a spacer
                node = node.down
            else:
                node.uncommit()
                node -= 1

        x = x.down
        sol[-1] = x
        choices[-1] += 1

    # tried all options for i
    # Step C7: Backtrack
    i.uncover()
    del sol[-1]
    del choices[-1]
    del branches[-1]
