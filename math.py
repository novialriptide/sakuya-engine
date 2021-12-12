"""
SakuyaEngine // GameDen // GameDen Rewrite (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from __future__ import annotations
from typing import Tuple
import math
import pygame

from .errors import NegativeSpeedError, LineSegmentLinesError

def vector2_ratio_xy(vector: pygame.math.Vector2) -> float:
    return vector.x / vector.y

def vector2_ratio_yx(vector: pygame.math.Vector2) -> float:
    return vector.y / vector.x
        
def vector2_move_toward(origin: pygame.math.Vector2, target: pygame.math.Vector2, speed: float) -> pygame.math.Vector2:
    """Moves towards the target pygame.math.Vector2 by the movement speed.

    Must be put in a loop until its reached its target.

    Parameters:
        target: The target pygame.math.Vector2.
        speed: The movement speed.
    
    """
    delta = target - origin

    if (target.magnitude() <= speed or target.magnitude() == 0):
        return target
    
    return origin + delta / target.magnitude() * speed

def get_magnitude(point1: pygame.math.Vector2, point2: pygame.math.Vector2) -> float:
    """Returns the magnitude of 2 points

    Parameters:
        point1: First point.
        point2: Second point.

    """
    return math.sqrt(
        math.pow((point1.x - point2.x), 2) 
        + math.pow((point1.y - point2.y), 2)
    )

def get_angle(origin: pygame.math.Vector2, direction: pygame.math.Vector2) -> float:
    """Returns an angle in radians of the object to look at from the origin point

    Parameters:
        origin: The original point.
        direction: The direction from origin point.

    """
    distance = direction - origin
    return math.atan2(distance.y, distance.x)

def move_toward(origin: float, target: float, speed: float) -> float:
    """Moves towards the origin to the target by speed.

    Must put in a loop until it's reach its goal.

    Parameters:
        origin: The first point.
        target: The target point.
        speed: The movement speed.

    """
    if speed < 0:
        raise NegativeSpeedError

    if abs(target - origin) <= speed:
        return target

    if target - origin > speed:
        return origin + speed

    if target - origin < speed:
        return origin - speed

def eval_segment_intersection(
    point1: pygame.math.Vector2, point2: pygame.math.Vector2, 
    point3: pygame.math.Vector2, point4: pygame.math.Vector2
) -> pygame.math.Vector2:
    """Evaluates if 2 line segments collide with each other.

    Parameters:
        point1: The starting pygame.math.Vector2 of line 1.
        point2: The ending pygame.math.Vector2 of line 1.
        point3: The starting pygame.math.Vector2 of line 2.
        point4: The ending pygame.math.Vector2 of line 2.
    
    Returns:
        Line 1's intersecting pygame.math.Vector2 on line 2.

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
        return pygame.math.Vector2(
            x1 + t*(x2-x1),
            y1 + t*(y2-y1)
        )
    else:
        raise LineSegmentLinesError