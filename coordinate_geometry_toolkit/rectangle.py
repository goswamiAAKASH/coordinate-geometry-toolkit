import math
from coordinate_geometry_toolkit.point import Point  # Importing Point class for Point objects
from coordinate_geometry_toolkit.base import Shape  #  import for Shape class
from coordinate_geometry_toolkit.polygon import Polygon  #  import for Polygon class

class Rectangle(Shape):  
        
    def __init__(self, p1: Point, p2: Point):
        self._p1 = p1  # Changed to protected attribute
        self._p2 = p2  # Changed to protected attribute
        self._width = abs(p2.x - p1.x)  # Changed to protected attribute
        self._height = abs(p2.y - p1.y)  # Changed to protected attribute
        
        # Create four corners of the rectangle
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        
        # Create the polygon representation
        self._polygon = Polygon([
            Point(x1, y1),  # Bottom-left
            Point(x2, y1),  # Bottom-right
            Point(x2, y2),  # Top-right
            Point(x1, y2)   # Top-left
        ])
        
    # Getters and setters for encapsulation
    @property
    def p1(self):
        return self._p1
        
    @p1.setter
    def p1(self, value):
        self._p1 = value
        self._update_dimensions()
        
    @property
    def p2(self):
        return self._p2
        
    @p2.setter
    def p2(self, value):
        self._p2 = value
        self._update_dimensions()
        
    @property
    def width(self):
        return self._width
        
    @property
    def height(self):
        return self._height
        
    @property
    def polygon(self):
        return self._polygon
        
    def _update_dimensions(self):
        self._width = abs(self._p2.x - self._p1.x)
        self._height = abs(self._p2.y - self._p1.y)
        
        # Update the polygon vertices when dimensions change
        x1, y1 = self._p1.x, self._p1.y
        x2, y2 = self._p2.x, self._p2.y
        
        self._polygon = Polygon([
            Point(x1, y1),  # Bottom-left
            Point(x2, y1),  # Bottom-right
            Point(x2, y2),  # Top-right
            Point(x1, y2)   # Top-left
        ])

    def __str__(self):
        """String representation of the rectangle
        """
        return f"Rectangle with corners at {self._p1} and {self._p2}"

    def __repr__(self):
        return self.__str__()

    # Area and Perimeter calculations - now using Polygon implementation
    def area(self):
        return round(self._width * self._height, 2)  # Direct calculation is more efficient for rectangles

    def perimeter(self):
        return round(2 * (self._width + self._height), 2)  # Direct calculation is more efficient for rectangles

    def diagonal_length(self):
        return round(math.sqrt(self._width**2 + self._height**2), 2)

    def is_point_inside(self, point: Point):
        """Check if a point is inside the rectangle
        """
        return self._polygon.is_point_inside(point)

    def is_point_on_boundary(self, point: Point):
        """Check if a point is on the boundary of the rectangle
        """
        return ((self._p1.x <= point.x <= self._p2.x and (point.y == self._p1.y or point.y == self._p2.y)) or
                (self._p1.y <= point.y <= self._p2.y and (point.x == self._p1.x or point.x == self._p2.x)))
    