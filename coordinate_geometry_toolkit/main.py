# all classes test by ChatGPT
# This script tests all classes in the coordinate geometry toolkit.

# main.py
import math
import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import all classes
from point import Point
from vector import Vector
from line import Line
from circle import Circle
from polygon import Polygon
try:
    from rectangle import Rectangle
except ImportError:
    Rectangle = None
try:
    from square import Square
except ImportError:
    Square = None
try:
    from triangle import Triangle
except ImportError:
    Triangle = None
try:
    from ellipse import Ellipse
except ImportError:
    Ellipse = None
try:
    from hyperbola import Hyperbola
except ImportError:
    Hyperbola = None
try:
    from parabola import Parabola
except ImportError:
    Parabola = None


def test_point():
    print("\n=== Testing Point Class ===")
    print("1. Basic Point Creation and String Representation:")
    p1 = Point(3, 4)
    p2 = Point(0, 0)
    p3 = Point(-2, 5)
    print("p1:", p1)
    print("p2:", p2)
    print("p3:", p3)

    print("\n2. Getters and Setters:")
    print("p1 coordinates - x:", p1.x, "y:", p1.y)
    p1.x = 5
    p1.y = 6
    print("After moving p1 to (5,6):", p1)

    print("\n3. Distance Calculations:")
    print("Distance from origin (p1):", p1.distance_from_origin())
    print("Distance p1-p2:", p1.distance_bw_two_points(p2))
    
    print("\n4. Point Comparisons:")
    p4 = Point(0, 0)
    print("Are p2 and p4 equal?:", p2 == p4)
    print("Are p1 and p2 equal?:", p1 == p2)

    print("\n5. Midpoint Calculation:")
    mid = p1.midpoint(p2)
    print("Midpoint of p1 and p2:", mid)

    print("\n6. Reflections:")
    print("p1:", p1)
    print("Reflection about X-axis:", p1.reflection_of_point_about_X_Axis())
    print("Reflection about Y-axis:", p1.reflection_of_point_about_Y_Axis())
    print("Reflection about Origin:", p1.reflection_of_point_about_Origin())

    print("\n7. Translation:")
    print("Original point:", p1)
    print("After translation by (2,3):", p1.translate_point(2, 3))

    print("\n8. Quadrant Testing:")
    test_points = [
        Point(3, 4),    # I Quadrant
        Point(-3, 4),   # II Quadrant
        Point(-3, -4),  # III Quadrant
        Point(3, -4),   # IV Quadrant
        Point(0, 0),    # Origin
        Point(5, 0),    # On X-axis
        Point(0, 5)     # On Y-axis
    ]
    for p in test_points:
        print(f"Point {p} is in {p.quadrant_of_a_point()}")


def test_vector():
    print("\n=== Testing Vector Class ===")
    print("1. Vector Creation and Representation:")
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    p1, p2 = Point(0, 0), Point(3, 4)
    v3 = Vector.from_points(p1, p2)
    print("v1 (direct):", v1)
    print("v2 (direct):", v2)
    print("v3 (from points):", v3)
    print("v1 == v3:", v1 == v3)

    print("\n2. Basic Vector Operations:")
    print("Addition v1 + v2:", v1 + v2)
    print("Subtraction v1 - v2:", v1 - v2)
    print("v1 magnitude:", v1.magnitude())
    print("Unit vector of v1:", v1.unit_vector())

    print("\n3. Vector Products:")
    print("Dot product v1·v2:", v1.dot(v2))
    print("Cross product v1×v2:", v1.cross(v2))
    print("Angle between v1 and v2:", v1.angle_with(v2))
    print("Angle between (degrees):", v1.angle_between(v2))

    print("\n4. Vector Relationships:")
    # Test parallel vectors
    v4 = Vector(6, 8)  # Multiple of v1
    v5 = Vector(0, 0)  # Zero vector
    print("Are v1 and v4 parallel?", v1.is_parallel(v4))
    print("Is v5 a zero vector?", v5.is_zero_vector())
    
    # Test perpendicular vectors
    v6 = Vector(-4, 3)  # Perpendicular to v1
    print("Are v1 and v6 perpendicular?", v1.is_perpendicular(v6))

    print("\n5. Vector Projections:")
    proj = v1.projection_on(v2)
    print("Projection of v1 on v2:", proj)

    print("\n6. Vector Conversions:")
    p3 = v1.to_point()
    print("Vector v1 as point:", p3)


def test_line():
    print("\n=== Testing Line Class ===")
    print("1. Basic Line Creation and String Representation:")
    p1 = Point(0, 0)
    p2 = Point(4, 4)
    p3 = Point(2, 0)
    p4 = Point(2, 5)
    line1 = Line(p1, p2)  # Diagonal line
    line2 = Line(p3, p4)  # Vertical line
    line3 = Line(Point(0, 3), Point(4, 3))  # Horizontal line
    print("Diagonal line:", line1)
    print("Vertical line:", line2)
    print("Horizontal line:", line3)

    print("\n2. Line Properties:")
    print("Line1 slope:", line1.slope())
    print("Line2 slope:", line2.slope())
    print("Line3 slope:", line3.slope())
    print("Line1 length:", line1.length_of_the_line_segment())
    print("Line1 equation:", line1.equation())
    print("Line2 equation:", line2.equation())
    print("Line3 equation:", line3.equation())

    print("\n3. Line Type Checks:")
    print("Is line1 vertical?", line1.is_vertical())
    print("Is line2 vertical?", line2.is_vertical())
    print("Is line3 horizontal?", line3.is_horizontal())

    print("\n4. Line Comparisons:")
    line4 = Line(Point(0, 0), Point(4, 4))  # Same as line1
    print("Are line1 and line4 equal?", line1 == line4)

    print("\n5. Midpoint:")
    mid = line1.midpoint_line_segment()
    print("Midpoint of line1:", mid)

    print("\n6. Line Relationships:")
    # Parallel lines
    line5 = Line(Point(0, 1), Point(4, 5))  # Parallel to line1
    print("Are line1 and line5 parallel?", line1.is_Parallel(line5))
    
    # Perpendicular lines
    line6 = Line(Point(0, 0), Point(-4, 4))  # Perpendicular to line1
    print("Are line1 and line6 perpendicular?", line1.is_perpendicular(line6))
    print("Are vertical and horizontal lines perpendicular?", line2.is_perpendicular(line3))


def test_circle():
    print("\n=== Testing Circle Class ===")
    print("1. Basic Circle Creation and String Representation:")
    center = Point(0, 0)
    c1 = Circle(center, 5)
    print("Circle1:", c1)

    print("\n2. Circle Measurements:")
    print("Area:", c1.area())
    print("Perimeter:", c1.perimeter())
    print("Diameter:", c1.diameter())

    print("\n3. Point Position Testing:")
    p1 = Point(5, 0)    # Point on circle
    p2 = Point(2, 2)    # Point inside circle
    p3 = Point(10, 10)  # Point outside circle
    print("Point (5,0) is", c1.is_point_on_circle(p1))
    print("Point (2,2) is", c1.is_point_on_circle(p2))
    print("Point (10,10) is", c1.is_point_on_circle(p3))

    print("\n4. Circle Creation from Diameter:")
    diam1 = Point(-3, 0)
    diam2 = Point(3, 0)
    c2 = Circle.cir_from_diameter(diam1, diam2)
    print("Circle from diameter points (-3,0) and (3,0):", c2)
    print("New circle radius (should be 3):", c2.radius)

    print("\n5. Point Generation on Circle:")
    print("Generating 8 points on circle c1:")
    points = c1.generate_points(8)  # Generate 8 points for demonstration
    for i, p in enumerate(points[:8]):  # Show first 8 points
        print(f"Point {i+1}: {p} is {c1.is_point_on_circle(p)}")


def test_polygon():
    print("\n=== Testing Polygon Class ===")
    print("1. Rectangle as Polygon:")
    p1, p2, p3, p4 = Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)
    rectangle = Polygon([p1, p2, p3, p4])
    print("Rectangle vertices:", rectangle)
    print("Rectangle perimeter:", rectangle.perimeter())
    print("Rectangle area:", rectangle.area())

    print("\n2. Triangle as Polygon:")
    p1, p2, p3 = Point(0, 0), Point(3, 0), Point(0, 4)
    triangle = Polygon([p1, p2, p3])
    print("Triangle vertices:", triangle)
    print("Triangle perimeter:", triangle.perimeter())
    print("Triangle area:", triangle.area())

    print("\n3. Pentagon as Polygon:")
    pentagon_points = [
        Point(0, 0),
        Point(2, 0),
        Point(3, 2),
        Point(1, 3),
        Point(-1, 2)
    ]
    pentagon = Polygon(pentagon_points)
    print("Pentagon vertices:", pentagon)
    print("Pentagon perimeter:", pentagon.perimeter())
    print("Pentagon area:", pentagon.area())


def test_rectangle():
    print("\n--- Testing Rectangle Class ---")
    if Rectangle is None:
        print("Rectangle class is not implemented yet")
        return
    try:
        p1 = Point(0, 0)
        p2 = Point(4, 3)
        rect = Rectangle(p1, p2)
        print("Rectangle:", rect)
        if hasattr(rect, 'area'):
            print("Area:", rect.area())
        if hasattr(rect, 'perimeter'):
            print("Perimeter:", rect.perimeter())
        if hasattr(rect, 'diagonal'):
            print("Diagonal:", rect.diagonal())
    except Exception as e:
        print(f"Rectangle test failed: {e}")

def test_square():
    print("\n--- Testing Square Class ---")
    if Square is None:
        print("Square class is not implemented yet")
        return
    try:
        p1 = Point(0, 0)
        p2 = Point(4, 4)
        square = Square(p1, p2)
        print("Square:", square)
        if hasattr(square, 'area'):
            print("Area:", square.area())
        if hasattr(square, 'perimeter'):
            print("Perimeter:", square.perimeter())
        if hasattr(square, 'diagonal'):
            print("Diagonal:", square.diagonal())
    except Exception as e:
        print(f"Square test failed: {e}")

def test_triangle():
    print("\n--- Testing Triangle Class ---")
    if Triangle is None:
        print("Triangle class is not implemented yet")
        return
    try:
        p1 = Point(0, 0)
        p2 = Point(3, 0)
        p3 = Point(0, 4)
        triangle = Triangle(p1, p2, p3)
        print("Triangle:", triangle)
        if hasattr(triangle, 'area'):
            print("Area:", triangle.area())
        if hasattr(triangle, 'perimeter'):
            print("Perimeter:", triangle.perimeter())
        if hasattr(triangle, 'triangle_type'):
            print("Type:", triangle.triangle_type())
    except Exception as e:
        print(f"Triangle test failed: {e}")

def test_ellipse():
    print("\n--- Testing Ellipse Class ---")
    if Ellipse is None:
        print("Ellipse class is not implemented yet")
        return
    try:
        center = Point(0, 0)
        ellipse = Ellipse(center, 5, 3)
        print("Ellipse:", ellipse)
        if hasattr(ellipse, 'area'):
            print("Area:", ellipse.area())
        if hasattr(ellipse, 'perimeter'):
            print("Perimeter:", ellipse.perimeter())
    except Exception as e:
        print(f"Ellipse test failed: {e}")

def test_hyperbola():
    print("\n--- Testing Hyperbola Class ---")
    if Hyperbola is None:
        print("Hyperbola class is not implemented yet")
        return
    try:
        center = Point(0, 0)
        hyperbola = Hyperbola(center, 5, 3)
        print("Hyperbola:", hyperbola)
        if hasattr(hyperbola, 'eccentricity'):
            print("Eccentricity:", hyperbola.eccentricity())
    except Exception as e:
        print(f"Hyperbola test failed: {e}")

def test_parabola():
    print("\n--- Testing Parabola Class ---")
    if Parabola is None:
        print("Parabola class is not implemented yet")
        return
    try:
        vertex = Point(0, 0)
        focus = Point(0, 2)   # Focus 2 units above vertex for upward-opening parabola
        parabola = Parabola(vertex, focus)
        print("Parabola:", parabola)
        print("Vertex:", parabola.vertex)
        print("Focus:", parabola.focus)
    except Exception as e:
        print(f"Parabola test failed: {e}")

if __name__ == "__main__":
    print("=== Starting Comprehensive Geometry Toolkit Tests ===\n")
    test_point()
    test_vector()
    test_line()
    test_circle()
    test_polygon()
    test_rectangle()
    test_square()
    test_triangle()
    test_ellipse()
    test_hyperbola()
    test_parabola()
    print("\n=== All tests completed! ===")
