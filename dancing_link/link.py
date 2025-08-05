"""Class definitions used in Dancing Link algorithm."""
from abc import ABC


class DancingLink(ABC):
    """Base class of Link and Column classes."""
    _instances: list["DancingLink"] = []

    def __init__(self):
        self.id: int = len(DancingLink._instances)   # auto record id
        self.up: DancingLink = self
        self.down: DancingLink = self
        DancingLink._instances.append(self)          # record the instance

    def delete(self):
        """Remove instance from memory."""
        if self.up == self.down == self:            # if root node
            for node in DancingLink._instances[1:]:
                node.delete()                       # delete other nodes
            DancingLink._instances.clear()          # clear the instances list

        self.up = None
        self.down = None

    def __add__(self, other: int):
        return DancingLink._instances[self.id + other]

    def __sub__(self, other: int):
        return DancingLink._instances[self.id - other]

    def _add_down(self, node: "DancingLink") -> None:
        """Add a node to the bottom."""
        node.up = self
        node.down = self.down
        self.down.up = node
        self.down = node


class Column(DancingLink):
    """Represents a header in a DLX Algorithm."""
    def __init__(self, name: str | None = None):
        super().__init__()
        if name:
            self.name: str = name   # symbolic identifier for printing answers
        else:
            self.name = str(self.id)    # auto-generate name
        self.size: int = 0      # number of 1s in the column
        self.left: Column = self
        self.right: Column = self

    def delete(self):
        """Delete the instance from memory."""
        self.left = None
        self.right = None
        super().delete()

    def add_bottom(self, node: "Link") -> None:
        """Add a node to the bottom of the column."""
        self.up._add_down(node)
        self.size += 1

    def add_right(self, node: "Column") -> None:
        """Add a node to the right."""
        node.left = self
        node.right = self.right
        self.right.left = node
        self.right = node

    def cover(self) -> None:
        """
        Removes self from the header list and removes all rows in self's
        own list from the other column lists they are in.
        """

        node: Link = self.down
        while node != self:
            node.hide()
            node = node.down

        # remove column from horizontal linked list
        left = self.left
        right = self.right
        left.right = right
        right.left = left

    def uncover(self) -> None:
        """Uncover a previously covered column."""
        # restore column to horizontal linked list
        left = self.left
        right = self.right
        left.right = self
        right.left = self

        node: Link = self.up
        while node != self:
            node.unhide()
            node = node.up


class ColumnColour(Column):
    """Represents a header in a XCC Algorithm."""
    def __init__(self, name: str | None = None):
        super().__init__(name)
        self.colour: int | None = None      # header colour defaults to None


class Link(DancingLink):
    """Represents a Node in a DLX Algorithm."""
    def __init__(self, column: Column | None = None):
        super().__init__()
        self.column: Column = column    # pointer to the Column header
        if column:                      # spacer nodes  not in a column
            column.add_bottom(self)

    def delete(self):
        """Delete the instance from memory."""
        self.column = None
        super().delete()

    def hide(self):
        """Hide a row of solution."""
        node: Link = self + 1
        while node != self:
            column = node.column
            up = node.up
            down = node.down
            if not column:      # node is spacer
                node = up       # loop back to the left most node
            else:
                up.down = down      # remove from column
                down.up = up
                column.size -= 1
                node += 1

    def unhide(self):
        """Unhide a row of solution."""
        node: Link = self - 1
        while node != self:
            column = node.column
            up = node.up
            down = node.down
            if not column:      # node is spacer
                node = down     # loop back to the right most node
            else:
                up.down = node      # restore to column
                down.up = node
                column.size += 1
                node -= 1


class LinkColour(Link):
    """Represents a Node in a XCC Algorithm."""
    def __init__(self, column: ColumnColour | None = None, colour: int = 0):
        super().__init__(column)
        self.colour = colour

    def hide(self):
        """Hide a row of solution."""
        node: LinkColour = self + 1
        while node != self:
            column = node.column
            up = node.up
            down = node.down
            if not column:      # node is spacer
                node = up       # loop back to the left most node
            else:
                if node.colour >= 0:    # ignore when colour < 0
                    up.down = down      # remove from column
                    down.up = up
                    column.size -= 1
                node += 1

    def unhide(self):
        """Unhide a row of solution."""
        node: LinkColour = self - 1
        while node != self:
            column = node.column
            up = node.up
            down = node.down
            if not column:      # node is spacer
                node = down     # loop back to the right most node
            else:
                if node.colour >= 0:    # ignore when colour < 0
                    up.down = node      # restore to column
                    down.up = node
                    column.size += 1
                node -= 1

    def commit(self):
        """Either cover a column, or purify the node."""
        if self.colour == 0:
            self.column.cover()
        elif self.colour > 0:
            self.purify()

    def uncommit(self):
        """Reverse the commit function."""
        if self.colour == 0:
            self.column.uncover()
        elif self.colour > 0:
            self.unpurify()

    def purify(self):
        """Either erase the colour, or hide the node."""
        colour = self.colour
        column: ColumnColour = self.column
        column.colour = colour

        node: LinkColour = column.down
        while node != column:
            if node.colour == colour:
                node.colour = -1
            else:
                node.hide()
            node = node.down

    def unpurify(self):
        """Reverse the purify function."""
        colour = self.colour
        column: ColumnColour = self.column

        node: LinkColour = column.up
        while node != column:
            if node.colour < 0:
                node.colour = colour
            else:
                node.unhide()
            node = node.up
