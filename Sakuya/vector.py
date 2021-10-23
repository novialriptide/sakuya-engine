class vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def __and__(self, other):
        return self.x == other.x and self.y == other.y