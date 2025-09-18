# circle class
# from .filename import class
import math
from coordinate_geometry_toolkit.point import Point  # added import for Point class
from coordinate_geometry_toolkit.base import Shape    # added import for Shape class

class Circle(Shape):

    def __init__(self, center: Point, radius: float):
        self._radius = radius
        self._center = center

    # Getter and Setter for radius
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value
    
    # Getter and Setter for center
    @property
    def center(self):
        return self._center
    
    @center.setter
    def center(self, value):
        self._center = value

    def __str__(self):
        return f" Circle with center at {self._center} and radius {self._radius}"

# area of circle
    def area(self):
        return round(math.pi * self.radius**2, 2)

# perimeter of circle
    def perimeter(self):
        return round(2 * math.pi * self.radius, 2)

# diameter of circle
    def diameter(self):
        return round(2 * self.radius, 2)

#  check the point lie where (on ,inside or outside)
# (x−h)^2 +(y-k)^2=r^2 ----->> sqrt(distance) = r
    def is_point_on_circle(self, point: Point):
        distance = self.center.distance_bw_two_points(point)  # changed _x/_y to use Point class getters inside distance_bw_two_points
        if math.isclose(distance, self.radius, rel_tol=1e-9):             # best for comparing the floats
            return "on the circle"
        elif (distance < self.radius):
            return "inside the circle"
        else:
            return "outside the circle"

# creating a Circle using two points that form the diameter
# it is a part of a class

    @classmethod
    def cir_from_diameter(cls, p1: Point, p2: Point):
    # Center = midpoint, Radius = half the distance
    # we are inside the a @classmethod that creates the instance — so self doesn't exist here
        center_x = (p1.x + p2.x)/2  # changed _x to x
        center_y = (p1.y + p2.y)/2  # changed _y to y

        center = Point(center_x, center_y)
        half_radius = p1.distance_bw_two_points(p2)/2  # changed _x/_y to use Point class getters inside distance_bw_two_points

        return cls(center, half_radius)

# generate points on circle
    def generate_points(self, n=100):
        points = []
        for i in range(n):
            angle = 2 * math.pi * i / n
            x = self.center.x + self.radius * math.cos(angle)  # changed get_x()/get_y() to x/y
            y = self.center.y + self.radius * math.sin(angle)  # changed get_x()/get_y() to x/y
            points.append(Point(x, y))  # changed 'point' to 'points' for clarity
        return points

    # Equation of chord (with midpoint)
    def equation_of_chord(self, point1: Point, point2: Point):
        mid_x = (point1.x + point2.x) / 2  # changed _x to x
        mid_y = (point1.y + point2.y) / 2  # changed _y to y
        mid_point = Point(mid_x, mid_y)

        A = point1.y - point2.y  # changed _y to y
        B = point2.x - point1.x  # changed _x to x
        C = point1.x * point2.y - point2.x * point1.y  # changed _x/_y to x/y

        D = -(A * mid_point.x + B * mid_point.y)  # changed _x/_y to x/y

        return (A, B, D)  # Ax +By +D =0