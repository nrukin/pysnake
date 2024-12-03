class vector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_zero(self):
        return self.x == 0 and self.y == 0

    def copy(self):
        return vector(self.x, self.y)

    def add(self, other):
        self.x += other.x
        self.y += other.y
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)

    @classmethod
    def up(cls):
        return cls(0, -1)

    @classmethod
    def down(cls):
        return cls(0, 1)

    @classmethod
    def left(cls):
        return cls(-1, 0)

    @classmethod
    def right(cls):
        return cls(1, 0)

    @classmethod
    def zero(cls):
        return cls(0, 0)
