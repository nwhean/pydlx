class Link:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = self

class Column(Link):
    def __init__(self, name: str):
        super().__init__()
        self.size = 0
        self.name = name
