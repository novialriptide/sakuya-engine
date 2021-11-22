from .errors import *
from .math import *
from .entity import Entity

class World:
    def __init__(self):
        self.entities = []
        self.current_tick = 1
        self.ticks_elapsed = 0

    def test_collisions(self, object: Entity):
        entities = self.entities[:]
        try:
            entities.remove(object)
        except ValueError:
            raise ObjectNotInWorld

        collided = []
        for o in entities:
            if object.hitbox.collidecircle(o.hitbox):
                collided.append(o)

        return collided

    def find_entities_by_name(self, name):
        entities = []
        for o in self.entities:
            if o.name == name:
                entities.append(o)

        return entities

    def advance_frame(self, delta_time: float):
        """
        Updates the entities inside the world, such as 
        physics & animation
        
        Should be added to the end of the main loop
        """
        for object in self.entities[:]:
            object._gravity = self.gravity
            object.update(delta_time)

            if object._is_destroyed:
                self.entities.remove(object)