import typing
from Sakuya.object import *
from Sakuya.vector import *

class world:
    def __init__(self):
        self.objects = []
        self.gravity = vector(0, -9.8)

    def advance_frame(self, delta_time: float):
        """
        Updates the entities inside the world, such as physics & animation
        Should be added to the end of the main loop
        """
        for object in self.objects:
            object.update(delta_time)