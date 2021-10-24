from Sakuya.object import *
from Sakuya.entity import *
from Sakuya.vector import *

class particle(entity):
    def __init__(self, position: vector):
        super().__init__(position, 0, has_rigidbody=True, has_box_collider=False)

class particles:
    def __init__(self):
        pass
