"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from typing import List

from .entity import Entity
from .events import WaitEvent
from .math import Vector

def generate_bullet_pattern(
    projectile: Entity, # entity
    starting_position: Vector, # Vector
    angle: float, # radians
    spread: float = 0, # radians
    bullet_count: int = 1, # int
    bullet_acceleration: Vector = 0, # Vector
    fire_rate: float = 0, # ms
) -> List[WaitEvent]:
    """Generates a bullet pattern.

    Parameters:
        projectile:
        starting_position: The bullet's initial position.
        angle: The middle angle of where bullets will spread. ;)
        spread: Angle spread between each bullets.
        bullet_count: The amount of bullets that will be spawned.
        bullet_acceleration: The bullet's acceleration.
        fire_rate: The fire rate of the bullets.

    Returns:
        A list of events that should be added to the scene.

    """
    # The reason why we're returning events in this case instead of
    # projectiles that will be added to teh scene is because we want
    # to take in account of the bullet fire rates.
    events = []

    

    return events