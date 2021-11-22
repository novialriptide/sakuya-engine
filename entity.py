import pygame
from typing import List
from Sakuya.math import Vector
from Sakuya.animation import Animation
from Sakuya.physics import gravity

class Entity:
    def __init__(self, has_collision: bool = True):
        self.animations = []
        self.current_anim = None
        self.current_anim_key = 0
        self.position = None
        self.velocity = Vector(0, 0)

    @property
    def name(self) -> str:
        return __name__

    @property
    def rect(self) -> pygame.Rect:
        cur_anim = self.anim_get(self.current_anim)
        return cur_anim[self.current_anim_key].get_rect()

    def get_collisions(self, rects: List[pygame.Rect]) -> List[pygame.Rect]:
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

        # TODO: add collision support
        test_rect = self.rect.copy()
        test_rect.x += movement.x
        test_rect.y += movement.y
        tested_collisions = self.get_collisions(collision_rects)


    def anim_get(self, animation_name: str) -> Animation:
        pass

    def anim_set(self, animation_name: str) -> bool:
        """
        Assign an animation to be played

        Parameters:
            animation_name: Animation to be played

        Returns:
            If true, playing the animation was successful

        """
        pass

    def anim_add(self, animation: Animation) -> None:
        """
        Adds an animation

        Parameters:
            animation: Animation to be added

        """
        self.animations.append(animation)

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
        if self.has_rigidbody:
            self.velocity += (
                self.acceleration
                + gravity
            ) * delta_time
            self.move(self.velocity * delta_time)