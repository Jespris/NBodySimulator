import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def one():
        return Vector2(1, 1)

    def magnitude(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def normalize(self):
        m = self.magnitude()
        if m > 0:
            # can't divide by zero
            return Vector2(self.x / m, self.y / m)
        return Vector2.zero()

    def tuple(self):
        return tuple((self.x, self.y))

    def angle(self):
        return math.atan2(self.y, self.x)

    # overriding the addition and multiplication definitions
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return None

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        return None

    def __mul__(self, other):
        if isinstance(other, Vector2):
            if self.x is None or self.y is None:
                return Vector2.zero()
            return Vector2(self.x * other.x, self.y * other.y)
        return Vector2(self.x * other, self.y * other)

    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        return Vector2(self.x // other, self.y // other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        return Vector2(self.x / other, self.y / other)

    def __str__(self):
        return str((self.x, self.y))
