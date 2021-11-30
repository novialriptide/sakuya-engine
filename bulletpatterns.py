from typing import List

from .entity import Entity

def generate_bullet_pattern(
    projectile: Entity,
    starting_angle: float, # radians
    ending_angle: float = None, # radians
    bullet_count: int = 1,
    angle_spread_between_bullets: float = 0, # radians
    bullet_acceleration: float = 0,
    spin_rate: float = 0, # ms
    fire_rate: float = 0, # ms
    bullet_curve: float = 0
) -> List[Entity]:
    projectiles = []

    

    return projectiles