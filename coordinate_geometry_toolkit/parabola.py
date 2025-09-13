import math
from coordinate_geometry_toolkit.point import Point   # added import for Point class
from coordinate_geometry_toolkit.base import Shape    # added import for Shape class

class Parabola(Shape):
    def __init__(self, vertex: Point, focus: Point):
        self.vertex = vertex
        self.focus = focus
        print("""
        Basic knowledge about the Parabola :

        1. x,y →  Coordinates of any point P(x, y) lying on the parabola.
        2. a →  Focal length parameter = distance from vertex to focus (also = distance from vertex to directrix).
        3. 4 a → Length of the latus rectum (a line segment through the    focus, perpendicular to the axis, whose endpoints lie on the parabola).
        4. Vertex → The fixed point where the parabola turns; here it’s at (0,0).
        5. Focus → Fixed point (0, a) inside the parabola.
        6. Directrix → Fixed line y = -a outside the parabola
        7. Axis → Vertical line x = 0 ( y-axis).
        8. Opening →
                    a> 0 → opens upward
                    a<0 → opens downward

        """)

        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        xf, yf = focus.x, focus.y            # changed get_x()/get_y() to x/y

        # calculate the focal length and the orientation (vertical or horizontal) of the parabola

        # If vertex.x == focus.x then vertical axis (focus is above or below vertex)
        if math.isclose(h, xf, abs_tol=1e-9):
            self.orientation = "vertical"
            self.a = yf - k
        
        # If vertex.y == focus.y then horizontal axis (focus is left or right of vertex)
        elif math.isclose(k, yf, abs_tol=1e-9):
            self.orientation = "horizontal"
            self.a = xf - h
        
        else:
            raise ValueError("Focus needs to line up with the vertex either horizontally or vertically.")

        # focal length
        if math.isclose(self.a, 0.0, abs_tol=1e-9):
            raise ValueError("Focus cannot be the same as vertex (a = 0).")

        # find the orientation of parabola about the axis
        if self.orientation == "vertical":
            if self.a > 0:
                print("Focus is ABOVE the vertex and Parabola opens UPWARD")
            else:
                print("Focus is BELOW the vertex and Parabola opens DOWNWARD")
        else: # horizontal
            if self.a > 0:
                print("Focus is RIGHT of the vertex and Parabola opens RIGHT")
            else:
                print("Focus is LEFT of the vertex and Parabola opens LEFT")

# find the eq. of the parabola
    def equation(self):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        # vertical (x^2 =4ay)
        if self.orientation == "vertical":
            return f"(x - {h})^2 = {4*self.a}(y - {k})"
        # horizontal (y^2 =4ax)
        else:
            return f"(y - {k})^2 = {4*self.a}(x - {h})"

    # find the focus point what we mention in the above code use method to call or use it directly
    def focus_point(self):
        return self.focus

# find the NIYTA (directrix) which is depend upon the orientaion of the parabola so we do here

# Vertical axis:    y = k −a

# Horizontal axis:  x = h − a

    def directrix(self):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        if self.orientation == "vertical":
            return f"y = {k - self.a}"
        else:
            return f"x = {h - self.a}"

    # latus rectum length =4|a|

    def latus_rectum_length(self):
        return abs(4*self.a)

    # axis of symmetry means x==h then symmetry about the vertical axis and y==k then about the horizontal axis

    def axis_of_symmetry(self):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        
        if self.orientation == "vertical":
            return f" symmetry about the vertical axis : x = {h}"
        else:
            return f" symmetry about the horizontal axis : y = {k}"

    # vertex form of parabola
    def vertex_form_of_parabola(self):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
    # coefficient
        A = 1/(4* self.a)
        if self.orientation == "vertical":
            return f"y = {A}(x - {h})^2 + {k}"
        else:
            return f"x = {A}(y - {k})^2 + {h}"

    # points of parabola
    def point_on_parabola(self, point: Point, tol=1e-9):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y
        if self.orientation == "vertical":
            return abs((x - h)**2 - 4*self.a*(y - k)) < tol
        else:
            return abs((y - k)**2 - 4*self.a*(x - h)) < tol

    # distance_to_focus
    def distance_to_focus(self, point: Point):
        xf, yf = self.focus.x, self.focus.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y
        return ((x - xf)**2 + (y - yf)**2)**0.5

    # distance_to_directrix
    def distance_to_directrix(self, point: Point):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y
        if self.orientation == "vertical":
            return abs(y - (k - self.a))
        else:
            return abs(x - (h - self.a))

    # check point inside the parabola
    def is_point_inside(self, point: Point):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y
        A = 1 / (4 * self.a)
        if self.orientation == "vertical":
            boundary_y = A * (x - h)**2 + k
            return y > boundary_y if self.a > 0 else y < boundary_y
        else:
            boundary_x = A * (y - k)**2 + h
            return x > boundary_x if self.a > 0 else x < boundary_x

    # generate points
    def generate_points(self, n=100, span=None):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        points = []
# span: distance from vertex in both directions (x-range if vertical, y-range if horizontal).
        if span is None:
            span = max(5.0, abs(self.a) * 5)
        if self.orientation == "vertical":
            start_x = h - span
            step = (2 * span) / (n - 1)
            for i in range(n):
                x = start_x + i * step
                y = ((x - h) ** 2) / (4 * self.a) + k
                points.append(Point(x, y))
        else:
            start_y = k - span
            step = (2 * span) / (n - 1)
            for i in range(n):
                y = start_y + i * step
                x = ((y - k) ** 2) / (4 * self.a) + h
                points.append(Point(x, y))
        
        return points

    # check if point is on the parabola
    def is_point_on_parabola(self, point: Point):
        h, k = self.vertex.x, self.vertex.y  # changed get_x()/get_y() to x/y
        x, y = point.x, point.y              # changed get_x()/get_y() to x/y
        if self.orientation == "vertical":
            return abs((x - h)**2 - 4*self.a*(y - k)) < 1e-9
        else:
            return abs((y - k)**2 - 4*self.a*(x - h)) < 1e-9
        
    # focus directrix property
    def focus_directrix_property(self, point: Point):
        distance_to_focus = self.distance_to_focus(point)
        distance_to_directrix = self.distance_to_directrix(point)
        return math.isclose(distance_to_focus, distance_to_directrix, rel_tol=1e-9)
        # This method is use for the "" checks if the point satisfies the focus-directrix property of the parabola".

