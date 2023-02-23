class Link:
    def __init__(self, left: "Link" = None):
        self.column = None
        self.up = self
        self.down = self
        
        if left:
            self.left = left
            self.right = left.right
            left.right.left = self
            left.right = self
        else:
            self.left = self
            self.right = self
    
    def remove_row(self) -> None:
        self.down.up = self.up
        self.up.down = self.down
    
    def remove_column(self) -> None:
        self.right.left = self.left
        self.left.right = self.right
    
    def restore_row(self) -> None:
        self.down.up = self
        self.up.down = self
        
    def restore_column(self) -> None:
        self.right.left = self
        self.left.right = self


class Column(Link):
    def __init__(self, name: str, left: "Column" = None) -> None:
        super().__init__(left=left)
        self.size = 0
        self.name = name
        self.column = self
    
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
