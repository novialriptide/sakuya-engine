from __future__ import annotations

import pygame
import json
import math

from typing import List
from copy import copy

from .math import Vector
from .animation import Animation
from .physics import gravity
from .controllers import BaseController
from .particles import Particles

class Entity:
    def __init__(
        self, 
        controller: BaseController,
        position: Vector,
        has_collision: bool = True,
        has_rigidbody: bool = False,
        scale: int = 1,
        particle_systems: List[Particles] = [],
        obey_gravity: bool = True
    ):
        """Objects that goes with a scene

        Parameters:
            controller: type of controller (ai or player)
            has_collision
        """
        self.scale = Vector(1, 1) * scale
        
        if controller is not None:
            self.controller = controller()
        if controller is None:
            self.controller = None

        self.has_collision = has_collision
        self.animations = {}
        self.current_anim = None # str
        self.position = position # Vector
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.obey_gravity = obey_gravity # bool
        # terminal velocity must be multipled
        # with delta time in comparision
        self.terminal_velocity = 10.0 # float
        self.enable_terminal_velocity = False

        self.has_collision = has_collision
        self.has_rigidbody = has_rigidbody

        self.particle_systems = particle_systems

    @property
    def sprite(self) -> pygame.Surface:
        cur_anim = self.anim_get(self.current_anim)
        width, height = cur_anim.sprite.get_size()
        scaled_sprite = pygame.transform.scale(
            cur_anim.sprite, (
                self.scale.x * width, 
                self.scale.y * height
            )
        )
        return scaled_sprite

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
        """Get a list of rects that collide with the entity's rect.
        
        It's recommended to use scene.test_collisions() instead.

        Parameters:
            rects: List of pygame rects.

        """
        return pygame.Rect.collidelistall(self.rect, rects)

    def move(
        self,
        movement: Vector, 
        collision_rects: List[pygame.Rect]
    ) -> bool:
        """Moves the position

        Parameters:
            movement: value to add to position

        Returns:
            If true, the position has been updated

        """
        
        self.position += movement
    
    def shoot(
        self,
        offset: Vector,
        projectile,
        angle: float,
        speed: int
    ) -> Entity:
        """Shoot an entity.

        Parameters:
            offset: The position offset of where the projectile's initial position.
            projectile: The entity that will be spawned.
            angle: The angle (radian) of the projectile's velocity
            speed: Speed of the projectile.

        """
        projectile = copy(projectile)
        projectile.velocity = Vector(speed * math.cos(angle), speed * math.sin(angle))
        projectile.position = self.position + offset
        return projectile

    def anim_get(self, animation_name: str) -> Animation:
        return self.animations[animation_name]

    def anim_set(self, animation_name: str) -> bool:
        """Assign an animation to be played

        Parameters:
            animation_name: Animation to be played

        Returns:
            If true, playing the animation was successful

        """
        self.current_anim = animation_name

    def anim_add(self, animation: Animation) -> None:
        """Adds an animation

        Parameters:
            animation: Animation to be added

        """
        self.animations[animation.name] = copy(animation)

    def anim_remove(self, animation_name: str) -> bool:
        """Removes an animation

        Parameters:
            animation_name: Animation to be removed

        Returns:
            If true, removing the animation was successful

        """
        raise NotImplementedError

    def copy(self) -> Entity:
        """Returns a copy of the entity
        
        You should not use Python3's copy.copy() method since
        it will interfere with the same entities animations

        """
        e = copy(self)
        new_anims = {}
        for a in self.animations.keys():
            new_anims[a] = copy(self.anim_get(a))

        e.animations = new_anims

        return e

    def update(self, delta_time) -> None:
        """Updates the position, animation, etc

        Parameters:
            delta_time: the game's delta time

        """
        # particles
        for ps in self.particle_systems:
            ps.update(delta_time, self.position)

        # animations
        self.anim_get(self.current_anim).update(delta_time)

        # apply terminal velocity
        # TODO: find a cleaner way to implement this
        term_vec = self.terminal_velocity * delta_time
        if self.velocity.x < 0 and self.enable_terminal_velocity:
            self.velocity.x = max(self.velocity.x, term_vec)
        if self.velocity.x > 0 and self.enable_terminal_velocity:
            self.velocity.x = min(self.velocity.x, term_vec)
        if self.velocity.y < 0 and self.enable_terminal_velocity:
            self.velocity.y = max(self.velocity.y, term_vec)
        if self.velocity.y > 0 and self.enable_terminal_velocity:
            self.velocity.y = min(self.velocity.y, term_vec)

        if self.controller is not None:
            self.velocity += self.controller.movement * self.controller.speed

        g = gravity
        if not self.obey_gravity:
            g = Vector(0, 0)

        if self.has_rigidbody:
            self.velocity += (
                (self.acceleration
                + g)
            )
        
        self.move(self.velocity * math.pow(delta_time, 2), [])

def load_entity(json_path: str) -> Entity:
    raise NotImplementedError

def dump_entity(dump_path: str) -> None:
    raise NotImplementedError