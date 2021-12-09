"""
SakuyaEngine // GameDen // GameDen Rewrite (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from .errors import NegativeSpeedError, LineSegmentLinesError
import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def ratio_xy(self):
        return self.x / self.y

    @property
    def ratio_yx(self):
        return self.y / self.x

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def to_list(self):
        return [self.x, self.y]
        
    def move_toward(self, target, speed: float):
        magnitude = get_magnitude(target, self)
        delta = target - self

        if (magnitude <= speed or magnitude == 0):
            return target
        
        return self + delta / magnitude * speed

def get_magnitude(point1: Vector, point2: Vector) -> float:
    return math.sqrt(
        math.pow((point1.x - point2.x), 2) 
        + math.pow((point1.y - point2.y), 2)
    )

def to_vector(point):
    return Vector(point[0], point[1])

def get_angle(origin: Vector, direction: Vector) -> float:
    """
    Returns an angle in radians of the object to look at from the origin point
    """
    distance = direction - origin
    return math.atan2(distance.y, distance.x)

def move_toward(origin: float, target: float, speed: float):
    if speed < 0:
        raise NegativeSpeedError

    if abs(target - origin) <= speed:
        return target

    if target - origin > speed:
        return origin + speed

    if target - origin < speed:
        return origin - speed

def eval_segment_intersection(
    point1: Vector, point2: Vector, 
    point3: Vector, point4: Vector
) -> Vector:
    """Evaluates if 2 line segments collide with each other.

    Parameters:
        point1: The starting Vector of line 1.
        point2: The ending Vector of line 1.
        point3: The starting Vector of line 2.
        point4: The ending Vector of line 2.
    
    Returns:
        Line 1's intersecting Vector on line 2.

    """
    # NOTE: This function is a variant 
    # from GameDen REWRITE for Novial's Gravity
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y
    x4, y4 = point4.x, point4.y

    dem = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if dem == 0:
        raise LineSegmentLinesError

    t1 = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
    t = t1/dem
    
    u1 = (x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)
    u = -(u1/dem)

    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        return Vector(
            x1 + t*(x2-x1),
            y1 + t*(y2-y1)
        )
    else:
        raise LineSegmentLinesError