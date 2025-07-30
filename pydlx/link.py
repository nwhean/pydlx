"""Class definitions used in Dancing Link algorithm."""
from abc import ABC


class BaseDLX(ABC):
    """Base class of Link and Column classes."""
    instances = []

    def __init__(self):
        self.id: int = len(BaseDLX.instances)   # auto record id
        self.up: BaseDLX = self
        self.down: BaseDLX = self
        BaseDLX.instances.append(self)          # record the instance

    def __del__(self):
        """Remove instance from record."""
        if self in BaseDLX.instances:
            BaseDLX.instances.remove(self)

    def __add__(self, other: int):
        return BaseDLX.instances[self.id + other]

    def __sub__(self, other: int):
        return BaseDLX.instances[self.id - other]

    def _add_down(self, node: "BaseDLX") -> None:
        """Add a node to the bottom."""
        node.up = self
        node.down = self.down
        self.down.up = node
        self.down = node


class Column(BaseDLX):
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


class Link(BaseDLX):
    """Represents a Node in a DLX Algorithm."""
    def __init__(self, column: Column | None = None):
        super().__init__()
        self.column: Column = column    # pointer to the Column header
        if column:                      # spacer nodes  not in a column
            column.add_bottom(self)

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
