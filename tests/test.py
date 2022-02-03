import pygame

screen = pygame.display.set_mode((500, 500))


def eval_segment_intersection(
    point1,
    point2,
    point3,
    point4,
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
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    dem = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if dem == 0:
        return point2

    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / dem
    return pygame.Vector2(x3 + u * (x4 - x3), y3 + u * (y4 - y3))


point1 = pygame.Vector2(25, 25)
point2 = pygame.Vector2(150, 150)
point3 = pygame.Vector2(150, 25)
point4 = pygame.Vector2(25, 150)

while True:
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), point1, point2)
    pygame.draw.line(screen, (255, 255, 255), point3, point4)
    p = eval_segment_intersection(point1, point2, point3, point4)
    pygame.draw.circle(screen, (255, 0, 0), p, 25)
    pygame.display.update()
