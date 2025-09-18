# class Triangle

import math
from coordinate_geometry_toolkit.point import Point  # added import for Point class
from coordinate_geometry_toolkit.base import Shape    # added import for Shape class

class Triangle(Shape):

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.a = self.p1.distance_bw_two_points(self.p2)
        self.b = self.p2.distance_bw_two_points(self.p3)
        self.c = self.p3.distance_bw_two_points(self.p1)

    def __str__(self):
        return f"Triangle with vertices at {self.p1},{self.p2},{self.p3}"

    def __repr__(self):
        return self.__str__()

    def side_length(self):
        a = self.p1.distance_bw_two_points(self.p2)
        b = self.p2.distance_bw_two_points(self.p3)
        c = self.p3.distance_bw_two_points(self.p1)
        return a, b, c

# Area using Heron’s Formula
# s=(a+b+c)/2
# Area= sqrt(s(s−a)(s−b)(s−c))

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return round(math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c)), 2)

    def perimeter(self):
        return round(self.a + self.b + self.c, 2)

#Centroid of Triangle
    def centroid(self):           # p1:Point,p2:Point,p3:Point not use these parameteres  here bccz obj already have self.p1, self.p2, self.p3
        x_cod = (self.p1.x + self.p2.x + self.p3.x) / 3  # changed _x to x
        y_cod = (self.p1.y + self.p2.y + self.p3.y) / 3  # changed _y to y
        return Point(x_cod, y_cod)
    
    # Alias for web app compatibility
    def Centroid(self):
        return self.centroid()

# Type of Triangle (by sides)

    def type_of_triangle(self):
        if(self.a == self.b == self.c):
            return "Equilateral Triangle"
        elif (self.a == self.b or self.b == self.c or self.a == self.c):
            return "Isosceles Triangle"
        else:
            return "Scalene Triangle"

# right angle triangle
    def is_right_angle_triangle(self):
        if ((self.a**2 + self.b**2 == self.c**2) or (self.b**2 + self.c**2 == self.a**2) or (self.a**2 + self.c**2 == self.b**2)):
            return "Right Angle Triangle"
        else:
            return "Not Right Angle Triangle"

# collinear
    def is_collinear(self):
        # area using determinant method taaki chhoti rounding galti ignore ho jaaye.
        area = ((self.p1.x*(self.p2.y - self.p3.y) +
                 self.p2.x*(self.p3.y - self.p1.y) +
                 self.p3.x*(self.p1.y - self.p2.y)) / 2)  # changed _x/_y to x/y
        #  isclose use here bcz
        return math.isclose(area, 0.0, abs_tol=1e-9) # True if collinear o/w False

# valid triangle

    def is_Valid_Triangle(self):
        if (self.a + self.b > self.c and
            self.b + self.c > self.a and
            self.a + self.c > self.b):
            return "Valid Triangle"
        else:
            return "Not Valid Triangle"

# angle of triangle

    def angle_of_triangle(self):
        angle_A = round(math.degrees(math.acos((self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c))), 2)
        angle_B = round(math.degrees(math.acos((self.a**2 + self.c**2 - self.b**2) / (2 * self.a * self.c))), 2)
        angle_C = round(math.degrees(math.acos((self.a**2 + self.b**2 - self.c**2) / (2 * self.a * self.b))), 2)
        return {"angle_A =": angle_A,
                "angle_B =": angle_B,
                "angle_C =": angle_C
                }

# incenter of triangle
    def Incenter(self):
        x_cod = (self.a * self.p1.x + self.b * self.p2.x + self.c * self.p3.x) / (self.a + self.b + self.c)  # changed _x to x
        y_cod = (self.a * self.p1.y + self.b * self.p2.y + self.c * self.p3.y) / (self.a + self.b + self.c)  # changed _y to y
        return Point(x_cod, y_cod)

# circumcenter of triangle
    def circumcenter(self):
        if self.is_collinear():
            return "Collinear. Can't find circumcenter"

        D = (self.p1.x*(self.p2.y - self.p3.y) +  # changed _x/_y to x/y
             self.p2.x*(self.p3.y - self.p1.y) +
             self.p3.x*(self.p1.y - self.p2.y))
        if(D == 0):
            return "Collinear. Can't find circumcenter"

        x_cod = ((self.p1.x**2 + self.p1.y**2)*(self.p2.y - self.p3.y) +
                 (self.p2.x**2 + self.p2.y**2)*(self.p3.y - self.p1.y) +
                 (self.p3.x**2 + self.p3.y**2)*(self.p1.y - self.p2.y)) / (2*D)
        y_cod = ((self.p1.x**2 + self.p1.y**2)*(self.p3.x - self.p2.x) +
                 (self.p2.x**2 + self.p2.y**2)*(self.p1.x - self.p3.x) +
                 (self.p3.x**2 + self.p3.y**2)*(self.p2.x - self.p1.x)) / (2*D)

        return Point(round(x_cod, 2), round(y_cod, 2))

# orthocenter of triangle
    def orthocenter(self):
        if self.is_collinear():
            return "Collinear. Can't find orthocenter"

        # Using the formula for orthocenter
        x_cod = (self.p1.x + self.p2.x + self.p3.x) / 3  # changed _x to x
        y_cod = (self.p1.y + self.p2.y + self.p3.y) / 3  # changed _y to y

        return Point(round(x_cod, 2), round(y_cod, 2))

# circumradius of triangle
    def circumradius(self):
        if self.is_collinear():
            return "Collinear but  Can't find circumradius"

        # Using the formula for circumradius
        area = self.area()
        if area == 0:
            return "Collinear but Can't find circumradius"
        
        circumradius = (self.a * self.b * self.c) / (4 * area)
        return round(circumradius, 2)

# inradius of triangle
    def inradius(self):
        if self.is_collinear():
            return "Collinear but  Can't find inradius"

        area = self.area()
        if area == 0:
            return "Collinear but  Can't find inradius"
        
        s = (self.a + self.b + self.c) / 2
        inradius = area / s
        return round(inradius, 2)
    
# reflection of triangle about X-axis
    def reflection_of_triangle_about_X_axis(self):
        p1_reflected = self.p1.reflection_of_point_about_X_Axis()
        p2_reflected = self.p2.reflection_of_point_about_X_Axis()
        p3_reflected = self.p3.reflection_of_point_about_X_Axis()
       
       # here we are creating a new Triangle object with the reflected points about X-axis
        return Triangle(p1_reflected, p2_reflected, p3_reflected)
    
# reflection of triangle about Y-axis
    def reflection_of_triangle_about_Y_axis(self):
        p1_reflected = self.p1.reflection_of_point_about_Y_Axis()
        p2_reflected = self.p2.reflection_of_point_about_Y_Axis()
        p3_reflected = self.p3.reflection_of_point_about_Y_Axis()
        
        # here we are creating a new Triangle object with the reflected points about Y-axis
        return Triangle(p1_reflected, p2_reflected, p3_reflected)

# reflection of triangle about Origin
    def reflection_of_triangle_about_origin(self):
        p1_reflected = self.p1.reflection_of_point_about_Origin()
        p2_reflected = self.p2.reflection_of_point_about_Origin()
        p3_reflected = self.p3.reflection_of_point_about_Origin()
        
        # here we are creating a new Triangle object with the reflected points about Origin
        return Triangle(p1_reflected, p2_reflected, p3_reflected)
