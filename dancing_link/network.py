"""Implementation of Dancing Link algoritms using stored lists."""
from itertools import zip_longest
from typing import Generator
import time

from .utility import mrv, progress


Matrix = list[list[int]]

class Network:
    """Represent a whole Dancing Link network."""
    def __init__(self,
                 matrix: Matrix,
                 names: list[str] | None = None,
                 primary: int | None = None):
        """Convert a matrix into a dancing link network.

        Parameters
        ----------
        matrix : list[list[int]]
                exact cover matrix
        names : lst[str], default = None
                names for the headers
        primary : int, default = None
                number of primary columns
        """
        self._spacer = 0    # keeping track of spacer_id

        width = len(matrix[0])

        # calculate the values of 'primary'
        if primary is None:
            primary = width
        elif not 0 < primary < width:
            raise ValueError(f"Require 0 < primary < {width}.")
        self.primary = primary

        # initialise empty lists
        self.name: list[str] = []
        self.left: list[int | None] = []
        self.right: list[int | None]  = []
        self.top: list[int]  = []
        self.up: list[int | None]  = []
        self.down: list[int | None]  = []

        # create the root header
        root = self.add_column(None)

        # create the header list
        left = root
        if names is None:
            names = []
        for index, (_, name) in enumerate(zip_longest(matrix[0], names,
                                                      fillvalue="")):
            header = self.add_column(name)
            if index < primary: # secondary items are not pointed to by primary
                self._add_right(left, header)

            left = header

        # create the nodes
        first = None
        link = None
        for row in matrix:
            # create the spacer node
            spacer = self.add_link(None)    # spacer doesn't belong to column
            self.up[spacer] = first

            first = None
            for index, val in enumerate(row, 1):
                if val:
                    link = self.add_link(index)
                    if not first:
                        first = link    # record first node in option before spacer

            self.down[spacer] = link    # record last node in option after spacer

        # create the last spacer
        spacer = self.add_link(None)

        self.up[spacer] = first
        self.down[spacer] = None

    @property
    def len(self):
        """Return the number of links under a column."""
        return self.top

    def add_column(self, name: str | None) -> int:
        """Add a column / item."""
        id: int = len(self.up)
        self.up.append(id)
        self.down.append(id)

        self.name.append(name if name else str(id))
        self.len.append(0)
        self.left.append(id)
        self.right.append(id)

        return id

    def add_link(self, top: int | None = None) -> int:
        """Add a link, under column `top`."""
        id: int = len(self.up)
        self.up.append(id)
        self.down.append(id)

        if top:
            self.top.append(top)
            self._add_bottom(top, id)
        else:
            self.top.append(self._spacer)
            self._spacer -= 1

        return id

    def _add_down(self, i: int, j: int) -> None:
        """Add node 'j' directly below node 'i'."""
        self.up[j] = i
        self.down[j] = self.down[i]
        self.up[self.down[i]] = j
        self.down[i] = j

    def _add_bottom(self, i: int, j: int) -> None:
        """Add a node 'j' below column node 'i'."""
        u = self.up[i]
        self._add_down(u, j)
        self.len[i] += 1

    def _add_right(self, i: int, j: int) -> None:
        """Add a column node 'j' to the right column node 'i'."""
        self.left[j] = i
        self.right[j] = self.right[i]
        self.left[self.right[i]] = j
        self.right[i] = j

    def cover(self, i: int):
        """Cover a given item represented as column `i`."""
        p = self.down[i]
        while p != i:
            self.hide(p)
            p = self.down[p]

        # remove column i from horizontal connection
        l = self.left[i]
        r = self.right[i]
        self.right[l] = r
        self.left[r] = l

    def uncover(self, i: int):
        """Uncover a given item represented as column `i`."""
        # restore column i to horizontal connections
        l = self.left[i]
        r = self.right[i]
        self.right[l] = i
        self.left[r] = i

        p = self.up[i]
        while p != i:
            self.unhide(p)
            p = self.up[p]

    def hide(self, p: int):
        """Hide other nodes from the option that contains node `p`."""
        q = p + 1
        while q != p:
            x = self.top[q]
            u = self.up[q]
            d = self.down[q]

            if x <= 0:  # q was a spacer
                q = u
            else:
                self.down[u]= d
                self.up[d] = u
                self.len[x] -= 1
                q += 1

    def unhide(self, p: int):
        """Unhide other nodes from the option that contains node `p`."""
        q = p - 1
        while q != p:
            x = self.top[q]
            u = self.up[q]
            d = self.down[q]
            if x <= 0:  # q was a spacer
                q = d
            else:
                self.down[u] = q
                self.up[d] = q
                self.len[x] += 1
                q -= 1

    def search(self: "Network",
               sol: list[int] | None = None,
               level: int = 0,
               choose=mrv,
               interval: int | None = None,
               **kwargs
               ) -> Generator[list[int], None, None]:
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
        start_time: float = kwargs.get('start_time')
        threshold: list[int] = kwargs.get('threshold')
        choices: list[int] = kwargs.get('choices')
        branches: list[int] = kwargs.get('branches')

        runtime = time.time() - start_time
        if threshold and runtime > threshold[-1]:
            threshold[-1] += interval
            print(f"{runtime:.3f}", end=" ")
            print(f"{progress(choices, branches):.5f}", end=" ")
            for c, l in zip(choices, branches):
                print(f"{c}/{l}", end=" ")
            print()

        if self.right[0] == 0:  # all items have been covered
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
        i: int = choose(self)

        # Step X4: Cover item `i`
        self.cover(i)
        branches.append(self.len[i])
        x: int = self.down[i]
        sol.append(x)
        choices.append(1)   # the first choice

        # Step X5: Try x_l
        while x != i:
            # This covers the items != i in the option that contains x_l.
            p = x + 1
            while p != x:
                j = self.top[p]
                if j <= 0:              # node is a spacer
                    p = self.up[p]
                else:
                    self.commit(p, j)
                    p += 1

            yield from self.search(sol, level+1, choose=choose,
                                   interval=interval, **kwargs)

            # Step X6: Try again
            # This uncovers the items != i in the option that contains x_l,
            # using the reverse of the order in X5.
            p = x - 1
            while p != x:
                j = self.top[p]
                if j <= 0:              # node is a spacer
                    p = self.down[p]
                else:
                    self.uncommit(p, j)
                    p -= 1

            x = self.down[x]
            sol[-1] = x
            choices[-1] += 1

        # tried all options for i
        # Step X7: Backtrack
        self.uncover(i)

        # Step X8: Leave level `level`
        del sol[-1]
        del choices[-1]
        del branches[-1]

    def commit(self, p: int, j: int):
        """Alias for cover item 'j'."""
        self.cover(j)

    def uncommit(self, p: int, j: int):
        """Alias for uncover item 'j'."""
        self.uncover(j)


class NetworkColour(Network):
    """Represent a whole Dancing Link network, with colour."""
    def __init__(self,
                 matrix: Matrix,
                 names: list[str] | None = None,
                 primary: int | None = None):
        super().__init__(matrix, names, primary)

        # update left
        spacer = len(matrix[0]) + 1
        self.left.insert(primary + 1, spacer)

        # update right
        for index in range(primary + 1, spacer):
            self.right[index] += 1
        self.right.append(primary + 1)

        # create colour map
        colours = {val for row in matrix for val in row[primary:]}
        colours.discard(0)
        colours.discard(1)
        self.colour_map = {}
        for index, colour in enumerate(colours, 1):
            self.colour_map[colour] = index
        self.colour_map_inv = {value: key
                               for key, value in self.colour_map.items()}

        self.colour: list[int | None] = [None] * len(self.name) # headers
        self.colour.append(0)   # for spacer
        for row in matrix:
            for index, val in enumerate(row, 0):
                if not val:
                    continue

                if index < primary:
                    self.colour.append(0)
                else:
                    self.colour.append(self.colour_map.get(val, 0))

            self.colour.append(0)   # for spacer

    def hide(self, p: int):
        """Hide other nodes from the option that contains node `p`."""
        q = p + 1
        while q != p:
            x = self.top[q]
            u = self.up[q]
            d = self.down[q]

            if x <= 0:  # q was a spacer
                q = u
            else:
                if self.colour[q] >= 0: # ignores node q when colour < 0
                    self.down[u]= d
                    self.up[d] = u
                    self.len[x] -= 1
                q += 1

    def unhide(self, p: int):
        """Unhide other nodes from the option that contains node `p`."""
        q = p - 1
        while q != p:
            x = self.top[q]
            u = self.up[q]
            d = self.down[q]
            if x <= 0:  # q was a spacer
                q = d
            else:
                if self.colour[q] >= 0: # ignores node q when colour < 0
                    self.down[u] = q
                    self.up[d] = q
                    self.len[x] += 1
                q -= 1

    def commit(self, p: int, j: int):
        """Either cover or purify a column."""
        c = self.colour[p]
        if c == 0:
            self.cover(j)
        elif c > 0:
            self.purify(p)

    def uncommit(self, p: int, j: int):
        """Either uncover or unpurify a column."""
        c = self.colour[p]
        if c == 0:
            self.uncover(j)
        elif c > 0:
            self.unpurify(p)

    def purify(self, p: int):
        """Hide node of different colour, or set same colour to -1."""
        c = self.colour[p]
        i = self.top[p]
        self.colour[i] = c
        q = self.down[i]

        while q != i:
            if self.colour[q] == c:
                self.colour[q] = -1
            else:
                self.hide(q)
            q = self.down[q]

    def unpurify(self, p: int):
        """Unhide node of different colour, or restore colour from -1."""
        c = self.colour[p]
        i = self.top[p]
        q = self.up[i]

        while q != i:
            if self.colour[q] < 0:
                self.colour[q] = c
            else:
                self.unhide(q)
            q = self.up[q]
