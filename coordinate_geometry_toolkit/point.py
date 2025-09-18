import math

class Point:
    def __init__(self, x, y):
        self._x = x           # x is an attribute
        self._y = y           # y is an attribute

    # use get and set method to access the value of x and y coordinates

    # Getter and Setter for x
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    # Getter and Setter for y
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    # str magic method
    # it show that how my point object look
    def __str__(self):
        return f"({self._x}, {self._y})"

    # Distance from origin
    def distance_from_origin(self):
        return math.sqrt(self._x**2 + self._y**2)

    # Distance between two points
    def distance_between_points(self, other):
        return math.sqrt((self._x - other._x)**2 + (self._y - other._y)**2)

    # returns True if  both points have the same coordinates
    def __eq__(self, other):
        return isinstance(other, Point) and self._x == other._x and self._y == other._y

    # midpoint
    # it return the tuple so further we can not use the point class mehods again it will give an error of tuple has no attribute like.
    # return ((self._x+other._x)/2,(self._y+other._y)/2)
    # above (therefore we return the coordinates inside the class" Point()" again so )
    # 1.we're calling the constructor (__init__) of the Point class again.
    # 2. It creates a new Point object using the midpoint coordinates.
    def midpoint(self, other):
        mid_x = (self._x + other._x) / 2
        mid_y = (self._y + other._y) / 2
        return Point(mid_x, mid_y)

    # Reflection about x-axis
    def reflect_about_x_axis(self):
        return Point(self._x, -self._y)

    # Reflection about y-axis
    def reflect_about_y_axis(self):
        return Point(-self._x, self._y)

    # Reflection about origin
    def reflect_about_origin(self):
        return Point(-self._x, -self._y)

    # translate a point
    def translate_point(self, m, n):          # m,n ---> translate points
        return Point(self._x + m, self._y + n)

    # Get quadrant of a point
    def get_quadrant(self):
        if self._x > 0 and self._y > 0:
            return "I Quadrant"
        elif self._x < 0 and self._y > 0:
            return "II Quadrant"
        elif self._x < 0 and self._y < 0:
            return "III Quadrant"
        elif self._x > 0 and self._y < 0:
            return "IV Quadrant"
        elif self._x == 0 and self._y == 0:
            return "Point on Origin"
        elif self._x == 0:
            return "Point on Y Axis"
        elif self._y == 0:
            return "Point on X Axis"
    
    # midpoint with origin
    def midpoint_with_origin(self):
        return Point(self._x / 2, self._y / 2)
    
    # slope between two points
    def slope_between_two_points(self, other):
        if self._x == other._x:
            raise ValueError("Slope is undefined for vertical line segments.")
        return (other._y - self._y) / (other._x - self._x)
    
    #vector conversion
    def to_vector(self):
        # Import inside method to avoid circular import
        from coordinate_geometry_toolkit.vector import Vector
        return Vector(self._x, self._y)
    
    
