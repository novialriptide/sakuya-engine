from Sakuya.math import Vector
from Sakuya.physics import gravity
from typing import tuple

class Particle:
    def __init__(
        self,
        position: Vector,
        color: tuple(int, int, int)
    ):
        self.position = position
        self.color = color
        self.velocity = Vector(0, 0)

    def update(self, delta_time):
        self.velocity += gravity * delta_time
        self.position = self.velocity * delta_time

class Particles:
    def __init__(
        self,
        spread: int = 5
    ):
        self.particles = []
        self.spread = spread

    def update(self, delta_time):
        for p in self.particles:
            p.update(delta_time)