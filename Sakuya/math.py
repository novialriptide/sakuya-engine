from Sakuya.vector import *
from Sakuya.config import *
import math
import typing

Pixel = typing.NewType("Pixel", int)
Unit = typing.NewType("Unit", float)

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