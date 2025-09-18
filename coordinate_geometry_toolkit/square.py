import math
from coordinate_geometry_toolkit.point import Point  # Importing Point class for Point objects
from coordinate_geometry_toolkit.rectangle import Rectangle  # Importing Rectangle class

class Square(Rectangle):  
    def __init__(self, p1: Point, p2: Point):
        # rectangle is a square by making width and height equal
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        
        # Calculate side length
        side_length = max(abs(x2 - x1), abs(y2 - y1))
        
        # Create a square by adjusting p2 coordinates
        new_p2 = Point(x1 + side_length, y1 + side_length)
        
        # Call the parent Rectangle constructor
        super().__init__(p1, new_p2)
        
        # Store side length for square-specific calculations
        self._side_length = side_length
        
    @property
    def side_length(self):
        return self._side_length
    
    # we Override setters to maintain square properties (from the Rectangle class)
    @Rectangle.p1.setter
    def p1(self, value):
        super(Square, type(self)).p1.fset(self, value)
        self._update_side_length()
        
    @Rectangle.p2.setter
    def p2(self, value):
        super(Square, type(self)).p2.fset(self, value)
        self._update_side_length()
    
    def _update_side_length(self):
        self._side_length = self._width  # Width and height are equal in a square
        
    def __str__(self):
        """String representation of the square"""
        return f"Square with corners at {self._p1} and {self._p2}"

    # Override area and perimeter for clarity, though they would work from Rectangle too
    def area(self):
        return round(self._side_length ** 2, 2)

    def perimeter(self):
        return round(4 * self._side_length, 2)

    def diagonal_length(self):
        return round(math.sqrt(2) * self._side_length, 2)
    
    # is_point_inside and is_point_on_boundary are inherited from Rectangle
    # It will work correctly because we are using the polygon implementation