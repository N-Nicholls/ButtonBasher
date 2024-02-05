import math

class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    # returns two product of two vectors
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # returns the difference of two vectors
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)   

    # returns the dot product of two vectors
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
 
    # returns the negation of a vector
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    # returns the magnitude of a vector
    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    # comparison operators
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not self.__eq__(other)
    def __lt__(self, other):
        return abs(self) < abs(other)
    def __le__(self, other):
        return abs(self) <= abs(other)
    def __gt__(self, other):
        return abs(self) > abs(other)
    def __ge__(self, other):
        return abs(self) >= abs(other)
    
    # returns the string representation of a vector
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    def distance_to(self, other):
        return abs(self - other)
    def normalize(self):
        if abs(self) == 0:
            return Vector(0, 0)
        return self * (1 / abs(self))





    

    