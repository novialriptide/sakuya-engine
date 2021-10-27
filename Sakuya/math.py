from Sakuya.config import *
from Sakuya.errorhandler import *
import math
import typing

Pixel = typing.NewType("Pixel", int)
Unit = typing.NewType("Unit", float)

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

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

def to_pixels(val: Unit):
    return val * PIXELS_PER_UNIT

def to_units(val: Pixel):
    return val / PIXELS_PER_UNIT

def get_angle(origin: Vector, direction: Vector) -> float:
    """
    Returns an angle in radians of the object to look at from the origin point
    """
    distance = direction - origin
    return math.atan2(distance.y, distance.x)

def move_toward(origin: float, target: float, speed: float):
    if speed < 0:
        raise NegativeSpeedError()

    if abs(target - origin) <= speed:
        return target

    if target - origin > speed:
        return origin + speed

    if target - origin < speed:
        return origin - speed