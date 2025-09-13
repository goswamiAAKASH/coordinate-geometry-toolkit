import math
from coordinate_geometry_toolkit.point import Point

class Vector:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @classmethod
    def from_points(cls, p1: Point, p2: Point):
        # Vector from point p1 to p2 → (x2-x1, y2-y1)
        return cls(p2._x - p1._x, p2._y - p1._y)

    def magnitude(self):
        # Formula: |v| = √(x² + y²)
        return math.sqrt(self._x ** 2 + self._y ** 2)

    def dot(self, other):
        # dot product---> v1 · v2 = x1*x2 + y1*y2
        return self._x * other._x + self._y * other._y

    def cross(self, other):
        # cross product---> (2D cross product → scalar): v1 × v2 = x1*y2 - y1*x2
        return self._x * other._y - self._y * other._x

    def angle_with(self, other):
        # angle find : cosθ = (v1·v2) / (|v1||v2|)
        dot = self.dot(other)
        mag = self.magnitude() * other.magnitude()
        if mag == 0:
            return None
        return math.degrees(math.acos(dot / mag))
    def __eq__(self, other):
        return isinstance(other, Vector) and self._x == other._x and self._y == other._y
    
    def __add__(self, other):
        return Vector(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        return Vector(self._x - other._x, self._y - other._y)

    def __str__(self):
        return f"<{self._x}, {self._y}>"

    def __repr__(self):
        return self.__str__()
    
    def __mul__(self, scalar):
        return Vector(self._x * scalar, self._y * scalar)
    
    def __true_div__(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self._x / scalar, self._y / scalar)
    
    
    def projection_on(self, other):
        """
        Projection of v1 on v2
        Formula: proj_v2(v1) = (v1·v2 / |v2|²) * v2
        """
        mag_sq = other.magnitude() ** 2
        if mag_sq == 0:
            return Vector(0, 0)
        scalar = self.dot(other) / mag_sq
        return Vector(other._x * scalar, other._y * scalar)

    def is_parallel(self, other):
        """
        Two vectors are parallel if cross product = 0
        """
        return self.cross(other) == 0

    def is_perpendicular(self, other):
        """
        Two vectors are perpendicular if dot product = 0
        """
        return self.dot(other) == 0
       
    def unit_vector(self):
        """
        Returns the unit vector in the direction of this vector
        Formula: u = v / |v|
        """
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return Vector(self._x / mag, self._y / mag)

    def angle_between(self, other):
        """
        Returns the angle between this vector and another vector in degrees
        Formula: θ = cos⁻¹( (v1·v2) / (|v1||v2|) )
        """
        mag_product = self.magnitude() * other.magnitude()
        if mag_product == 0:
            return None  # angle undefined with zero vector
        angle_rad = math.acos(self.dot(other) / mag_product)
        return math.degrees(angle_rad)

    def is_zero_vector(self):
        """
        Checks if the vector is a zero vector (both components are zero)
        """
        return self._x == 0 and self._y == 0

    def to_point(self):
        """
        Converts the vector to a Point object
        """
        return Point(self._x, self._y)

    @classmethod
    def from_point(cls, point: Point):
        """
        Converts a Point object to a Vector
        """
        return cls(point._x, point._y)

    def scale(self, scalar):
        """
        Scales the vector by a scalar value
        Formula: v' = scalar * v
        """
        return Vector(self._x * scalar, self._y * scalar)

    def is_collinear(self, other):
        """
        Checks if two vectors are collinear
        Two vectors are collinear if their cross product is zero
        """
        return self.cross(other) == 0

    def angle_with_x_axis(self):
        """
        Returns the angle between this vector and the positive x-axis in degrees
        Uses atan2(y, x) to cover all quadrants
        """
        if self.is_zero_vector():
            return None
        angle_rad = math.atan2(self._y, self._x)
        return math.degrees(angle_rad) % 360

    def angle_with_y_axis(self):
        """
        Returns the angle between this vector and the positive y-axis in degrees
        Uses atan2(x, y) to cover all quadrants
        """
        if self.is_zero_vector():
            return None
        angle_rad = math.atan2(self._x, self._y)
        return math.degrees(angle_rad) % 360

    def quadrant(self):
        """
        Returns the quadrant in which the vector lies
        1: Quadrant I, 2: Quadrant II, 3: Quadrant III, 4: Quadrant IV
        """
        if self._x > 0 and self._y > 0:
            return 1
        elif self._x < 0 and self._y > 0:
            return 2
        elif self._x < 0 and self._y < 0:
            return 3
        elif self._x > 0 and self._y < 0:
            return 4
        else:
            return None
        
    def reflect_x_axis(self):
        """
        Reflects the vector across the x-axis
        Formula: v' = (x, -y)
        """
        return Vector(self._x, -self._y)
    
    def reflect_y_axis(self):
        """
        Reflects the vector across the y-axis
        Formula: v' = (-x, y)
        """
        return Vector(-self._x, self._y)
    
    def reflect_origin(self):
        """
        Reflects the vector across the origin
        Formula: v' = (-x, -y)
        """
        return Vector(-self._x, -self._y)
    
    def translate(self, dx, dy):
        """
        Translates the vector by dx in x-direction and dy in y-direction
        Formula: v' = (x + dx, y + dy)
        """
        return Vector(self._x + dx, self._y + dy)
    
    def rotate(self, angle_degrees):
        """
        Rotates the vector by a given angle in degrees
        Formula: v' = (x*cos(θ) - y*sin(θ), x*sin(θ) + y*cos(θ))
        """
        angle_rad = math.radians(angle_degrees)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        new_x = self._x * cos_angle - self._y * sin_angle
        new_y = self._x * sin_angle + self._y * cos_angle
        return Vector(new_x, new_y)
    
    # rotate about a point
    def rotate_about_point(self, angle_degrees, point: Point):
        """
          Steps for rotating a vector about a point:
        1.Translate vector to origin (subtract point coordinates)
        2. Rotate using rotation matrix
        3.Translate back (add point coordinates)
        """
        # Step 1: Translate to origin
        translated_x = self._x -point._x
        translated_y =self._y -point._y

        # Step2:Rotate it 
        angle_rad=  math.radians(angle_degrees)
        cos_angle =math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        rotated_x = translated_x * cos_angle - translated_y * sin_angle
        rotated_y= translated_x * sin_angle + translated_y * cos_angle

        # Step 3:Translate back to the point
        final_x = rotated_x + point._x
        final_y = rotated_y + point._y

        return Vector(final_x, final_y)
        
    # convert to polar coordinates (r, θ)    
    def to_polar(self):
        r = self.magnitude()
        if r == 0:
            return (0.0, None)
        theta = math.degrees(math.atan2(self._y, self._x)) % 360
        return (r, theta)