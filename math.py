from .errors import NegativeSpeedError
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

    def __and__(self, other):
        return self.x == other.x and self.y == other.y

    def to_list(self):
        return [self.x, self.y]
        
    def move_toward(self, target, speed: float):
        return Vector(
            move_toward(self.x, target.x, speed), move_toward(self.y, target.y, speed)
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
         NegativeSpeedError()

    if abs(target - origin) <= speed:
        return target

    if target - origin > speed:
        return origin + speed

    if target - origin < speed:
        return origin - speed