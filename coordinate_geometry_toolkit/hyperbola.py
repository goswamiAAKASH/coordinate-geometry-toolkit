import math
from coordinate_geometry_toolkit.point import Point   # added import for Point class
from coordinate_geometry_toolkit.base import Shape    # added import for Shape class

class Hyperbola(Shape):
   
    def __init__(self, center: Point, a: float, b: float, orientation: str = "horizontal"):
        self.center = center
        self.a = abs(a)
        self.b = abs(b)

        if self.a <= 0 or self.b <= 0:
            raise ValueError("Semi-axis lengths must be positive.")

        if orientation not in ("horizontal", "vertical"):
            raise ValueError("Orientation must be 'horizontal' or 'vertical'.")
        self.orientation = orientation
        # Eccentricity
        self.e = math.sqrt(1 + (self.b**2) / (self.a**2))

# String representation of Hyperbola
    def __str__(self):
        return f"Hyperbola with center at {self.center}, semi-major axis {self.a}, semi-minor axis {self.b}, orientation {self.orientation}"
    
# equation of hyperbola
    def equation(self):
       h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y

       if self.orientation == "horizontal":
           return f"((x - {h})²)/{self.a**2} - ((y - {k})²)/{self.b**2} = 1"
       else:
           return f"((y - {k})²)/{self.a**2} - ((x - {h})²)/{self.b**2} = 1"

# foci of hyperbola
    def foci(self):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        c = math.sqrt(self.a**2 + self.b**2)

        if self.orientation == "horizontal":
            return Point(h + c, k), Point(h - c, k)
        else:
            return Point(h, k + c), Point(h, k - c)

# vertices of hyperbola
    def vertices(self):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            return Point(h + self.a, k), Point(h - self.a, k)
        else:
            return Point(h, k + self.a), Point(h, k - self.a)

# asymptotes of hyperbola
    def asymptotes(self):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            slope = self.b / self.a
        else:
            slope = self.a / self.b

        return [
            f"y - {k} = {slope}(x - {h})",
            f"y - {k} = {-slope}(x - {h})"
        ]

    # Eccentricity of hyperbola
    def eccentricity(self):
        return self.e

# transverse axis length
    def transverse_axis_length(self):
        return 2 * self.a

# conjugate axis length
    def conjugate_axis_length(self):
        return 2 * self.b

# generate points on hyperbola
    def point_on_hyperbola(self, point: Point, tol=1e-6):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            lhs = ((x - h)**2) / (self.a**2) - ((y - k)**2) / (self.b**2)
        else:
            lhs = ((y - k)**2) / (self.a**2) - ((x - h)**2) / (self.b**2)

        return math.isclose(lhs, 1.0, abs_tol=tol)

# check if point is between branches of hyperbola
    # for horizontal hyperbola: (x - h)²/a² - (y - k)²/b² < 1
    # for vertical hyperbola: (y - k)²/a² - (x - h)²/b² < 1
    def is_between_branches(self, point: Point):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y

        if self.orientation == "horizontal":
            lhs = ((x - h)**2) / (self.a**2) - ((y - k)**2) / (self.b**2)
        else:
           lhs = ((y - k)**2) / (self.a**2) - ((x - h)**2) / (self.b**2)

        return lhs < 1

# distance to foci
    # returns the distance to the nearest focus
    def distance_to_focus(self, point: Point):
        f1, f2 = self.foci()
        d1 = math.dist((point.x, point.y), (f1.x, f1.y))  # changed get_x()/get_y() to x/y
        d2 = math.dist((point.x, point.y), (f2.x, f2.y))  # changed get_x()/get_y() to x/y
        return min(d1, d2)

# generate points on hyperbola
    def generate_points(self, n=200, t_max=2.0):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        points = []

        t_min = -t_max
        step = (t_max - t_min) / (n - 1)

        for i in range(n):
            t = t_min + i * step
            if abs(math.cos(t)) < 1e-6:
                continue

            if self.orientation == "horizontal":
                x = h + self.a / math.cos(t)
                y = k + self.b * math.tan(t)
            else:
                x = h + self.b * math.tan(t)
                y = k + self.a / math.cos(t)

            points.append(Point(x, y))
        return points  # corrected 'point' → 'points'  # changed return variable

# check if point is on hyperbola
    def is_point_on_hyperbola(self, point: Point):
        h, k = self.center.x, self.center.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y
        if self.orientation == "horizontal":
            return abs((x - h)**2 / self.a**2 - (y - k)**2 / self.b**2 - 1) < 1e-9
        else:
            return abs((y - k)**2 / self.a**2 - (x - h)**2 / self.b**2 - 1) < 1e-9
        
    # focus-directrix property
    def focus_directrix_property(self, point: Point):
        distance_to_focus = self.distance_to_focus(point)
        
        if self.orientation == "horizontal":
            directrix = self.center.x - self.a / self.e
            distance_to_directrix = abs(point.x - directrix)
        else:
            directrix = self.center.y - self.a / self.e
            distance_to_directrix = abs(point.y - directrix)

        # returns True if point satisfies focus-directrix property
        return math.isclose(distance_to_focus, distance_to_directrix, rel_tol=1e-9)

    # Implementing abstract methods from Shape base class
    def area(self):
        # Hyperbola has infinite area, but we can return a symbolic representation
        return float('inf')
    
    def perimeter(self):
        # Hyperbola has infinite perimeter, but we can return a symbolic representation
        return float('inf')

    