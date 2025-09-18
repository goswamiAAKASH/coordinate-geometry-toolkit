# line class

import math
from coordinate_geometry_toolkit.point import Point
from coordinate_geometry_toolkit.base import Shape  # Added import for Shape class
  # make sure your Point class is in same package point.py(means Go to the file point.py in the same folder/package as this file, and import the Point class from it.)

class Line(Shape):  

    # We define the coordinates (x, y) in the Point class constructor, and then pass two Point objects to the Line class constructor.

    def __init__(self, point_1, point_2):
        self._p1 = point_1                       # Changed to protected attribute
        self._p2 = point_2                       # Changed to protected attribute

# dx and dy represent the differences in x and y coordinates between the two points
        self._dx = self._p1.x - self._p2.x       # Changed to protected attribute (error show ho raha tha kyuki private var access kar karhe jabki humne to getter use karna hai)
        self._dy = self._p1.y - self._p2.y       # Changed to protected attribute
# HERE NOTE CONSTRUCTOR does not return any value

        if self._dx == 0:
            # return None
            self._m = None    # Changed to protected attributeOR  slope is infinite
            self._is_vertical_line = True     # Changed to protected attribute& then line is verticle
        else:
            self._m = self._dy / self._dx     # Changed to protected attribute, m is slope value
            self._is_vertical_line = False    # Changed to protected attribute
            
    # Getters and setters for encapsulation
    @property
    def p1(self):
        return self._p1
        
    @p1.setter
    def p1(self, value):
        self._p1 = value
        self._update_properties()
        
    @property
    def p2(self):
        return self._p2
        
    @p2.setter
    def p2(self, value):
        self._p2 = value
        self._update_properties()
        
    @property
    def dx(self):
        return self._dx
        
    @property
    def dy(self):
        return self._dy
        
    @property
    def m(self):
        return self._m
        
    @property
    def is_vertical_line(self):
        return self._is_vertical_line
        
    def _update_properties(self):
        self._dx = self._p1.x - self._p2.x
        self._dy = self._p1.y - self._p2.y
        if self._dx == 0:
            self._m = None
            self._is_vertical_line = True
        else:
            self._m = self._dy / self._dx
            self._is_vertical_line = False
            
    # Implementing required abstract methods
    def area(self):
        # A line has zero area
        return 0
        
    def perimeter(self):
        # For a line, perimeter is the same as length
        return self.length()


    # how line object look
    def __str__(self):
        return f"Line from {self.p1} to {self.p2}"

    # Returns True if both lines have the same points
    def __eq__(self, other):
        if isinstance(other, Line):
            return (self.p1 == other.p1 and self.p2 == other.p2) or (self.p1 == other.p2 and self.p2 == other.p1)
        return False


    # Length of the Line Segment
    def length_of_the_line_segment(self):
        return self.p1.distance_between_points(self.p2)


    # slope of a line
    def slope(self):
        return self.m

    # Equation of the line in the form y =mx+c or x=constant
    def equation(self):
        if self.is_vertical_line  :  # both x coordinate is equal
            return "x={:.2f}".format(self.p1.x)  # changed _x to x

        c = self.p1.y - (self.m * self.p1.x)  # changed _x, _y to x, y
        return f"y={self.m:.2f}x {c:+.2f}"


    # Is the line horizontal?
    def is_horizontal(self):
        return self.dy == 0

    # Is the line vertical?
    def is_vertical(self):
        return self.dx == 0

    # midpoint of the line segment
    def midpoint_line_segment(self):
        x_cod = (self.p1.x + self.p2.x) / 2  # changed _x to x
        y_cod = (self.p1.y + self.p2.y) / 2  # changed _y to y
        return Point(x_cod, y_cod)  # changed to return Point object instead of tuple


    # Is line parallel to another line?
    def is_Parallel(self, other):
        if self.m is None and other.m is None:
            return True  # changed string to boolean
        elif self.m == other.m:
            return True  # changed string to boolean
        else:
            return False  # changed string to boolean

    # lines are perpendicular to each other
    def is_perpendicular(self, other):
        # Case 1: One vertical ho and another  one horizontal ho
        if (self.m is None and other.m == 0) or (self.m == 0 and other.m is None):
            return True

        # Case 2: Both are vertical or both are horizontal
        if self.m is None and other.m is None:
            return False
        if self.m == 0 and other.m == 0:
            return False

        # Case 3: General case we know
        if self.m is not None and other.m is not None:
            return math.isclose(self.m * other.m, -1.0)

        return False

    # line distance_from_point
    def distance_from_point(self, point):
        # Ax +By +c=0
        A = self.p1.y - self.p2.y  # changed _y to y
        B = self.p2.x - self.p1.x  # changed _x to x
        C = self.p1.x * self.p2.y - self.p2.x * self.p1.y  # changed _x, _y to x, y
        num = abs(A * point.x + B * point.y + C)  # changed _x, _y to x, y
        den = math.sqrt(A**2 + B**2)

        return round(num / den, 2)

    # Angle Between Two Lines
    def angle_bw_two_line(self, other):
        if self.m is None and other.m is None:
            return 0
        if self.m is None or other.m is None:
            return 90
        if math.isclose(self.m * other.m, -1.0, rel_tol=1e-9):
            return 90

        tan_theta = abs((self.m - other.m) / (1 + self.m * other.m))
        theta_rad = math.atan(tan_theta)
        theta_deg = math.degrees(theta_rad)

        return round(theta_deg, 2)
    
    # check if point lies on the line
    def is_point_on_line(self, point):
        if self.is_vertical_line:
            return math.isclose(point.x, self.p1.x, rel_tol=1e-9)   # rel_tol bcz minor diff ho sakta hai
        else:
            expected_y = self.m * (point.x - self.p1.x) + self.p1.y
            return math.isclose(point.y, expected_y, rel_tol=1e-9)
        
        # Intersection with another line
    def intersection_with_another_line(self, other):
        if self.is_parallel(other):
            return None
        if self.is_vertical_line:
            x = self.p1.x
            y = other.m * (x - other.p1.x) + other.p1.y
            return Point(x, y)
        if other.is_vertical_line:
            x = other.p1.x
            y = self.m * (x - self.p1.x) + self.p1.y
            return Point(x, y)
        x = (other.p1.y - self.p1.y + self.m * self.p1.x - other.m * other.p1.x) / (self.m - other.m)
        y = self.m * (x - self.p1.x) + self.p1.y
        return Point(x, y)
    
    # Angle between two lines
    def angle_between_two_lines(self, other):
        if self.is_vertical_line and other.is_vertical_line:
            return 0.0
        if self.is_vertical_line or other.is_vertical_line:
            return 90.0
        tan_theta = abs((self.m - other.m) / (1 + self.m * other.m))
        theta_rad = math.atan(tan_theta)
        theta_deg = math.degrees(theta_rad)
        return round(theta_deg, 2)
    