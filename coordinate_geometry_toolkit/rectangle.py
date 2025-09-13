import math
from coordinate_geometry_toolkit.point import Point  # Importing Point class for Point objects

class Rectangle:
    
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        self.width = abs(p2.x - p1.x)
        self.height = abs(p2.y - p1.y)

    def __str__(self):
        """String representation of the rectangle
        """
        return f"Rectangle with corners at {self.p1} and {self.p2}"

    def __repr__(self):
        return self.__str__()

    # Area and Perimeter calculations
    def area(self):
        return round(self.width * self.height, 2)

    def perimeter(self):
        return round(2 * (self.width + self.height), 2)

    def diagonal_length(self):
        return round(math.sqrt(self.width**2 + self.height**2), 2)

    def is_point_inside(self, point: Point):
        """Check if a point is inside the rectangle
        """
        return (self.p1.x <= point.x <= self.p2.x) and (self.p1.y <= point.y <= self.p2.y)  

    def is_point_on_boundary(self, point: Point):
        """Check if a point is on the boundary of the rectangle
        """
        return ((self.p1.x <= point.x <= self.p2.x and (point.y == self.p1.y or point.y == self.p2.y)) or
                (self.p1.y <= point.y <= self.p2.y and (point.x == self.p1.x or point.x == self.p2.x)))
    