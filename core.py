from typing import Tuple
import pygame

def rotate_by_center(image: pygame.Surface, angle: float) -> pygame.Surface:
    """Rotate an image while keeping its center.

    Warning: This only works with SQUARE SURFACES!

    Parameters:
        image: Image to rotate.
        angle: The angle you want the image to be. (degrees)

    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image