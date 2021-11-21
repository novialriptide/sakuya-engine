from Sakuya.object import *
from Sakuya.entity import *
from Sakuya.math import *

class Particle(Entity):
    def __init__(self, position: Vector):
        super().__init__(position, 0, has_rigidbody=True, has_box_collider=False)

class Particles:
    def __init__(self):
        pass
