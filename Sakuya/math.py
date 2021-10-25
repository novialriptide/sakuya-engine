from Sakuya.vector import *
from Sakuya.config import *
import math
import typing

pixel = typing.NewType("pixel", int)
unit = typing.NewType("unit", float)

def to_pixels(val: unit):
    return val * PIXELS_PER_UNIT

def to_units(val: pixel):
    return val / PIXELS_PER_UNIT

def get_angle(origin: vector, direction: vector) -> float:
    """
    Returns an angle in radians of the object to look at from the origin point
    """
    distance = direction - origin
    return math.atan2(distance.y, distance.x)