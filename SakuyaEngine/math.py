"""
SakuyaEngine // GameDen // GameDen Rewrite (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from __future__ import annotations
from typing import Tuple, List, Union

import math
import pygame

from .errors import NegativeSpeedError, LineSegmentLinesError

vector2 = Union[pygame.Vector2, Tuple[float, float]]


def vector2_ratio_xy(vector: vector2) -> float:
    return vector.x / vector.y


def vector2_ratio_yx(vector: vector2) -> float:
    return vector.y / vector.x


def vector2_move_toward(
    origin: vector2, target: vector2, distance: float
) -> vector2:
    """Moves towards the target Vector2 by the movement speed.

    Must be put in a loop until its reached its target.

    Parameters:
        origin: The original position
        target: The target position.
        distance: The movement distance.

    """
    delta = target - origin
    dist = delta.magnitude()

    if dist <= distance or dist == 0:
        return target

    return origin + delta / dist * distance


def get_angle(origin: vector2, target: vector2) -> float:
    """Returns an angle in radians of the object to look at from the origin point

    Parameters:
        origin: The original point.
        target: The target point.

    """
    distance = target - origin
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
    point1: vector2,
    point2: vector2,
    point3: vector2,
    point4: vector2,
) -> pygame.Vector2:
    """Evaluates if 2 line segments collide with each other.

    Parameters:
        point1: The starting point of line 1.
        point2: The ending point of line 1.
        point3: The starting point of line 2.
        point4: The ending point of line 2.

    Returns:
        Line 1's intersecting point on line 2.

    """
    # NOTE: This function is a variant
    # from GameDen REWRITE for Novial's Gravity
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    dem = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if dem == 0:
        raise LineSegmentLinesError

    t1 = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = t1 / dem

    u1 = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
    u = -(u1 / dem)

    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        return pygame.Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    else:
        raise LineSegmentLinesError

def eval_segment_intersection(point1: vector2, point2: vector2, rect: pygame.Rect):
    pass


def rect_to_lines(
    rect: pygame.Rect,
) -> List[
    vector2, vector2, vector2, vector2
]:
    return [
        (rect.bottomleft, rect.bottomright),
        (rect.bottomleft, rect.topleft),
        (rect.bottomright, rect.topright),
        (rect.topleft, rect.topright),
    ]
