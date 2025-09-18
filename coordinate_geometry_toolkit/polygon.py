import math
from coordinate_geometry_toolkit.point import Point
from coordinate_geometry_toolkit.base import Shape

class Polygon(Shape):
    """
    General Polygon class
    - n-sided polygon defined by a list of vertices (Point objects)
    """
    def __init__(self, vertices: list[Point]):
        # Polygon vertices (points) ka list store kar rahe hain
        self._vertices = vertices  # Changed to protected attribute
        
    # Getter and setter for encapsulation
    @property
    def vertices(self):
        return self._vertices
        
    @vertices.setter
    def vertices(self, value):
        self._vertices = value

    def perimeter(self):
        # Formula: sum of all side lengths
        n = len(self._vertices)
        peri = 0
        for i in range(n):
            p1 = self._vertices[i]
            p2 = self._vertices[(i + 1) % n]  # last vertex se first tak join
            peri += p1.distance_bw_two_points(p2)
        return peri

    def area(self):
        # Formula (Shoelace theorem):
        # Area = 1/2 * |(x1*y2 + x2*y3 + ... + xn*y1) - (y1*x2 + y2*x3 + ... + yn*x1)|
        n = len(self._vertices)
        sum1, sum2 = 0, 0
        for i in range(n):
            x1, y1 = self._vertices[i].x, self._vertices[i].y  # Changed to use getters
            x2, y2 = self._vertices[(i + 1) % n].x, self._vertices[(i + 1) % n].y  # Changed to use getters
            sum1 += x1 * y2
            sum2 += y1 * x2
        return abs(sum1 - sum2) / 2

    def centroid(self):
        # Formula: (sum of x-coordinates / n, sum of y-coordinates / n)
        n = len(self.vertices)
        cx = sum(p._x for p in self.vertices) / n
        cy = sum(p._y for p in self.vertices) / n
        return Point(cx, cy)

    def is_point_inside(self, point: Point):
        # Ray Casting Algorithm:
        # Ek horizontal line draw karo point se → agar odd times intersect karti hai polygon ke sides ko → andar
        n = len(self.vertices)
        count = 0
        for i in range(n):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % n]

            # Check karo ki line y-cross karti hai ki nahi
            if ((p1._y > point._y) != (p2._y > point._y)):
                # Intersection point ka x calculate karo
                x_intersect = (p2._x - p1._x) * (point._y - p1._y) / (p2._y - p1._y) + p1._x
                if point._x < x_intersect:
                    count += 1
        return count % 2 == 1  # odd → inside, even → outside

    def __repr__(self):
        # Polygon ko readable form me print karne ke liye
        return f"Polygon({self.vertices})"

    def __str__(self):
        vertices_str = ", ".join(str(v) for v in self.vertices)
        return f"Polygon with vertices: {vertices_str}"

