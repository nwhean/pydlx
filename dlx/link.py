"""Class definitions used in Dancing Link algorithm."""

class Link:
    """Data object as described in Dancing Link by Donald Knuth."""
    def __init__(self, column: "Column"):
        """
        >>> a = Link(None)
        >>> a.up == a
        True
        >>> a.down == a
        True
        >>> a.left == a
        True
        >>> a.right == a
        True
        """
        # pylint: disable=invalid-name
        self.column = column    # pointer to the Column header
        self.up = self          # pointer to the Link above
        self.down = self        # pointer to the Link below
        self.left = self        # pointer to the Link to the left
        self.right = self       # pointer to the Link to the right
        # pylint: enable=invalid-name

    def add_right(self, link: "Link") -> None:
        """Add a link to the right.
        >>> a = Link(None)
        >>> b = Link(None)
        >>> c = Link(None)

        a -- b
        >>> a.add_right(b)
        >>> a.right == b
        True
        >>> a.left == b
        True
        >>> b.left == a
        True
        >>> b.right == a
        True

        a -- c -- b
        >>> a.add_right(c)
        >>> a.right == c
        True
        >>> a.left == b
        True
        >>> c.left == a
        True
        >>> c.right == b
        True
        >>> b.left == c
        True
        >>> b.right == a
        True
        """
        link.left = self
        link.right = self.right
        self.right.left = link
        self.right = link

    def add_down(self, link: "Link") -> None:
        """Add a link to the bottom.
        >>> a = Link(None)
        >>> b = Link(None)
        >>> c = Link(None)

        a
        |
        b
        >>> a.add_down(b)
        >>> a.down == b
        True
        >>> a.up == b
        True
        >>> b.up == a
        True
        >>> b.down == a
        True

        a
        |
        c
        |
        b
        >>> a.add_down(c)
        >>> a.down == c
        True
        >>> a.up == b
        True
        >>> c.up == a
        True
        >>> c.down == b
        True
        >>> b.up == c
        True
        >>> b.down == a
        True
        """
        link.up = self
        link.down = self.down
        self.down.up = link
        self.down = link

    def remove_row(self) -> None:
        """Remove the row of which self is a member of from linked list.
        >>> a = Link(None)
        >>> b = Link(None)
        >>> c = Link(None)
        >>> a.add_down(b)
        >>> b.add_down(c)

        a
        |
        b
        |
        c

        >>> a.remove_row()
        >>> a.up == c
        True
        >>> a.down == b
        True
        >>> b.up == c
        True
        >>> b.down == c
        True
        >>> c.up == b
        True
        >>> c.down == b
        True
        """
        self.down.up = self.up
        self.up.down = self.down

    def remove_column(self) -> None:
        """Remove the col of which self is a member of from linked list.
        >>> a = Link(None)
        >>> b = Link(None)
        >>> c = Link(None)
        >>> a.add_right(b)
        >>> b.add_right(c)

        a -- b -- c

        >>> a.remove_column()
        >>> a.left == c
        True
        >>> a.right == b
        True
        >>> b.left == c
        True
        >>> b.right == c
        True
        >>> c.left == b
        True
        >>> c.right == b
        True
        """
        self.right.left = self.left
        self.left.right = self.right

    def restore_row(self) -> None:
        """Restore the row of which self is a member of into linked list.
        >>> a = Link(None)
        >>> b = Link(None)
        >>> c = Link(None)
        >>> a.add_down(b)
        >>> b.add_down(c)
        >>> a.remove_row()
        >>> a.restore_row()
        >>> b.up == a
        True
        >>> b.down == c
        True
        >>> c.up == b
        True
        >>> c.down == a
        True
        """
        self.down.up = self
        self.up.down = self

    def restore_column(self) -> None:
        """Restore the col of which self is a member of into linked list.
        >>> a = Link(None)
        >>> b = Link(None)
        >>> c = Link(None)
        >>> a.add_right(b)
        >>> b.add_right(c)
        >>> a.remove_column()
        >>> a.restore_column()
        >>> b.left == a
        True
        >>> b.right == c
        True
        >>> c.left == b
        True
        >>> c.right == a
        True
        """
        self.right.left = self
        self.left.right = self


class Column(Link):
    """Column object as described in Dancing Link by Donald Knuth."""
    def __init__(self, name: str = ""):
        super().__init__(self)
        self.name: str = name   # symbolic identifier for printing answers
        self.size: int = 0      # number of 1s in the column

    def add_link(self, link: Link):
        """Add a link to a column"""
        link.up = self.up
        link.down = self
        link.column = self
        self.up.down = link
        self.up = link

    def cover(self) -> None:
        """
        Removes c from the header list and removes all rows in c's own list
        from the other column lists they are in.
        """
        # remove c from the header list
        self.remove_column()

        i = self.down  # i is link at the next row
        while i != self:
            # remove rows from c's own list
            j = i.right     # j is the link at the next column from i
            while j != i:
                # remove j from other column list
                j.remove_row()
                j.column.size -= 1
                j = j.right
            i = i.down

    def uncover(self) -> None:
        """Uncover a previously covered column."""
        i = self.up
        while i != self:
            j = i.left
            while j != i:
                # unremove j from other column list
                j.column.size += 1
                j.restore_row()
                j = j.left
            i = i.up

        # unremove c from the header list
        self.restore_column()
