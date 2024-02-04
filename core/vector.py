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

    # returns the product of a vector and a scalar
    def __rmul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # returns the division of a vector and a scalar 
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    
    # returns the negation of a vector
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    # returns the magnitude of a vector
    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    # compares two vectors
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # returns the opposite of a vector
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # returns less than comparison of two vectors
    def __lt__(self, other):
        return abs(self) < abs(other)
    
    # returns less than or equal to comparison of two vectors
    def __le__(self, other):
        return abs(self) <= abs(other)
    
    # returns greater than comparison of two vectors
    def __gt__(self, other):
        return abs(self) > abs(other)
    
    # returns greater than or equal to comparison of two vectors
    def __ge__(self, other):
        return abs(self) >= abs(other)
    
    # returns the string representation of a vector
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def returnMagnitude(self):
        return abs(self)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def normalize(self):
        if abs(self) == 0:
            return Vector(0, 0)  # Avoid division by zero
        return self / abs(self)
    
    def angle_with(self, other):
        dot_product = self.dot(other)
        mag_self = abs(self)
        mag_other = abs(other)
        if mag_self == 0 or mag_other == 0:
            return 0  # Avoid division by zero
        return math.acos(dot_product / (mag_self * mag_other))
    
    def projection_onto(self, other):
        unit_other = other.normalize()
        projection_magnitude = self.dot(unit_other)
        return unit_other * projection_magnitude
    
    def parallel_component(self, other):
        unit_other = other.normalize()
        return unit_other * self.dot(unit_other)

    def perpendicular_component(self, other):
        return self - self.parallel_component(other)
    
    def rotate(self, angle):
        cos_theta, sin_theta = math.cos(angle), math.sin(angle)
        return Vector(self.x * cos_theta - self.y * sin_theta,
                    self.x * sin_theta + self.y * cos_theta)

    def reflect(self, normal):
        n = normal.normalize()
        return self - 2 * self.dot(n) * n

    def distance_to(self, other):
        return abs(self - other)






    

    