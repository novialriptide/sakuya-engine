from typing import Tuple

import pygame
import math

__all__ = ["draw_pie"]


def draw_pie(
    surface: pygame.Surface,
    color: Tuple[int, int, int],
    position: pygame.Vector2,
    radius: int,
    start_angle: int,
    end_angle: int,
):
    """Draws a pie on a pygame Surface.

    Warning: This will be outdated by the time pygame will
    release a native pygame.draw.pie() by Novial. Estimated
    version release is pygame version 2.2.0.

    Parameters:
        surface: Surface to draw on.
        color: Color in RGB format.
        position: Position to be drawn on surface.
        start_angle: Starting angle of the pie in degrees.
        end_angle: Ending angle of the pie in degrees.

    """
    if start_angle == -180 and end_angle == 180:
        pygame.draw.circle(surface, color, position, radius)
        return None

    points = [position]
    for angle in range(start_angle, end_angle):
        angle = math.radians(angle)
        point = pygame.Vector2(math.cos(angle), math.sin(angle)) * radius
        points.append(point + position)

    pygame.draw.polygon(surface, color, points)
