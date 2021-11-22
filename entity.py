import pygame
from typing import List
from .math import Vector
from .animation import Animation
from .physics import gravity
from .controllers import BaseController

class Entity:
    def __init__(
        self, 
        controller: BaseController,
        position: Vector,
        has_collision: bool = True,
        has_rigidbody: bool = False
    ):
        """
        Objects that goes with a scene

        Parameters:
            controller: type of controller (ai or player)
            has_collision
        """
        self.controller = controller()
        self.has_collision = has_collision
        self.animations = {}
        self.current_anim = None # str
        self.current_anim_key = 0
        self.position = position
        self.velocity = Vector(0, 0)

        self.has_collision = has_collision
        self.has_rigidbody = has_rigidbody

    @property
    def sprite(self) -> pygame.Surface:
        cur_anim = self.anim_get(self.current_anim)
        return cur_anim.sprites[self.current_anim_key]

    @property
    def rect(self) -> pygame.Rect:
        width, height = self.sprite.get_size()
        rect = pygame.Rect(
            self.position.x, 
            self.position.y, 
            width, height
        )
        return rect

    def get_collisions(
        self,
        rects: List[pygame.Rect]
    ) -> List[pygame.Rect]:
        """
        Get a list of rects that collide with the entity's rect

        Parameters:
            rects: list of pygame rects

        Returns:
            list of collided rects

        """
        return pygame.Rect.collidelistall(self.rect, rects)

    def move(
        self,
        movement: Vector, 
        collision_rects: List[pygame.Rect]
    ) -> bool:
        """
        Moves the position

        Parameters:
            movement: value to add to position

        Returns:
            If true, the position has been updated

        """
        
        self.position += movement

    def anim_get(self, animation_name: str) -> Animation:
        return self.animations[animation_name]

    def anim_set(self, animation_name: str) -> bool:
        """
        Assign an animation to be played

        Parameters:
            animation_name: Animation to be played

        Returns:
            If true, playing the animation was successful

        """
        self.current_anim = animation_name

    def anim_add(self, animation: Animation) -> None:
        """
        Adds an animation

        Parameters:
            animation: Animation to be added

        """
        self.animations[animation.name] = animation

    def anim_remove(self, animation_name: str) -> bool:
        """
        Removes an animation

        Parameters:
            animation_name: Animation to be removed

        Returns:
            If true, removing the animation was successful

        """
        pass

    def update(self, delta_time) -> None:
        """
        Updates the position, animation, etc

        Parameters:
            delta_time: the game's delta time

        """
        self.velocity += self.controller.movement * delta_time * self.controller.speed

        if self.has_rigidbody:
            self.velocity += (
                self.acceleration
                + gravity
            ) * delta_time
            
        self.move(self.velocity * delta_time, [])