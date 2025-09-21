import math
from coordinate_geometry_toolkit.point import Point   # added import for Point class
from coordinate_geometry_toolkit.base import Shape    # added import for Shape class

class Ellipse(Shape):
    
    def __init__(self, center: Point, a: float, b: float, orientation: str = "horizontal"):
        """
        Ellipse definition
        center       : Point object (h, k)
        a : Semi-major axis length (> b)
        b : Semi-minor axis length
        orientation: 'horizontal' or 'vertical'
        """
        self.center = center
        
        # Ensure positive values with minimum threshold
        self.a = max(abs(a), 0.1) if a != 0 else 1.0
        self.b = max(abs(b), 0.1) if b != 0 else 1.0

        # Axis length checks - now guaranteed to be positive
        if self.a < self.b:
            raise ValueError("a (semi-major) must be >= b (semi-minor)")

        # Orientation validation
        if orientation not in ("horizontal", "vertical"):
            raise ValueError("Orientation must be 'horizontal' or 'vertical'")
        self.orientation = orientation

        # Eccentricity
        self.e = math.sqrt(1 - (self.b**2) / (self.a**2))

    def __str__(self):
            return f"Ellipse with center at {self.center}, semi-major axis {self.a}, semi-minor axis {self.b}, orientation {self.orientation}"


    def eccentricity(self):
        return self.e

    def equation(self):
        """
        Standard equation of the ellipse
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            return f"((x - {h})^2)/({self.a}^2) + ((y - {k})^2)/({self.b}^2) = 1"
        else:
            return f"((x - {h})^2)/({self.b}^2) + ((y - {k})^2)/({self.a}^2) = 1"

    def foci(self):
        """
        Focal points of the ellipse
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        c = self.a * self.e  # focal distance from center

        if self.orientation == "horizontal":
            return Point(h + c, k), Point(h - c, k)
        else:
            return Point(h, k + c), Point(h, k - c)

    def vertices(self):
        """
        Endpoints of the major axis
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            return Point(h + self.a, k), Point(h - self.a, k)
        else:
            return Point(h, k + self.a), Point(h, k - self.a)

    def co_vertices(self):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        if self.orientation == "horizontal":
            return Point(h, k + self.b), Point(h, k - self.b)
        else:
            return Point(h + self.b, k), Point(h - self.b, k)

    def major_axis_length(self):
        return 2 * self.a

    def minor_axis_length(self):
        return 2 * self.b

    def area(self):
        return math.pi * self.a * self.b

    def perimeter(self):
        """
        Perimeter approximation using Ramanujan’s formula
        π [ 3(a+b) - sqrt((3a+b)(a+3b)) ]
        """
        return math.pi * (3 * (self.a + self.b) -
                          math.sqrt((3 * self.a + self.b) * (self.a + 3 * self.b)))

    def point_on_ellipse(self, point: Point, tol=1e-6):
        """
        Check if a point lies on the ellipse
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            lhs = ((x - h)**2) / (self.a**2) + ((y - k)**2) / (self.b**2)
        else:
            lhs = ((x - h)**2) / (self.b**2) + ((y - k)**2) / (self.a**2)

        return math.isclose(lhs, 1.0, abs_tol=tol)

    def is_point_inside(self, point: Point):
        """
        Check if a point lies inside the ellipse
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            lhs = ((x - h)**2) / (self.a**2) + ((y - k)**2) / (self.b**2)
        else:
            lhs = ((x - h)**2) / (self.b**2) + ((y - k)**2) / (self.a**2)

        return lhs < 1.0

    def distance_to_focus(self, point: Point):
        """
        Minimum distance from a point to either focus
        """
        f1, f2 = self.foci()
        d1 = math.dist((point.x, point.y), (f1.x, f1.y))  # changed get_x()/get_y() to x/y
        d2 = math.dist((point.x, point.y), (f2.x, f2.y))  # changed get_x()/get_y() to x/y
        return min(d1, d2)

    def generate_points(self, n=200):
        """
        Generate n points along the ellipse using parametric equations
        Horizontal: x = h + a*cos(t), y = k + b*sin(t)
        Vertical  : x = h + b*cos(t), y = k + a*sin(t)
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        points = []
        for i in range(n):
            t = 2 * math.pi * i / (n - 1)
            if self.orientation == "horizontal":
                x = h + self.a *math.cos(t)
                y = k + self.b * math.sin(t)
            else:
                x = h + self.b * math.cos(t)
                y = k + self.a*math.sin(t)
            points.append(Point(x, y))
        return points  # fixed from 'return point' to 'return points'  # changed

    def axis_of_symmetry(self):
        """
        Axis of symmetry
        Horizontal: y = k
        Vertical  : x = h
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        if self.orientation == "horizontal":
            return f"Symmetry about the horizontal axis: y = {k}"
        else:
            return f"Symmetry about the vertical axis: x = {h}"
        
    def latus_rectum_length(self):
        """
        Length of the latus rectum
        Horizontal: 2b^2/a
        Vertical  : 2a^2/b
        """
        if self.orientation == "horizontal":
            return 2 * (self.b**2) / self.a
        else:
            return 2 * (self.a**2) / self.b
        
    def directrix(self):
        """
        Directrix of the ellipse
        Horizontal: x = h - (a/e)
        Vertical  : y = k - (b/e)
        """
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        if self.orientation == "horizontal":
            return f"x = {h - (self.a / self.e)}"
        else:
            return f"y = {k - (self.b / self.e)}"
    
    def focus_point(self):
        """
        Focus point of the ellipse
        """
        f1, _ = self.foci()
        return f1
        # return f"Focus point at {f1}"  # changed to return Point object instead of string

    def co_focus_point(self):
        """
        Co-focus point of the ellipse
        """
        _, f2 = self.foci()
        # return f"Co-focus point at {f2}""
        return f2
        
    # reflection of ellipse about X-axis
    def reflection_of_ellipse_about_X_axis(self):
        """
        Reflect the ellipse about the X-axis
        """
        new_center = Point(self.center.x, -self.center.y)   # changed get_x()/get_y() to x/y
        return Ellipse(new_center, self.a, self.b, self.orientation)
    
    # reflection of ellipse about Y-axis
    def reflection_of_ellipse_about_Y_axis(self):
        """
        Reflect the ellipse about the Y-axis
        """
        new_center = Point(-self.center.x, self.center.y)  # changed get_x()/get_y() to x/y
        return Ellipse(new_center, self.a, self.b, self.orientation)