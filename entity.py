"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from __future__ import annotations
from Helix.SakuyaEngine.tile import split_image

import pygame
import math
import json

from typing import List
from copy import copy

from .math import Vector
from .animation import Animation, load_anim_dict
from .physics import gravity
from .controllers import BaseController
from .particles import Particles

class Entity:
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: int = 1,
        max_health: float = 100,
        position: Vector = Vector(0, 0),
        controller: BaseController = None,
        fire_rate: int = 0,
        has_collision: bool = True,
        has_rigidbody: bool = False,
        obey_gravity: bool = True,
        speed: float = 0,
        custom_hitbox_size: Vector = Vector(0, 0),
        particle_systems: List[Particles] = [],
        bullet_spawners: List[BulletSpawner] = [],
    ):
        """Objects that goes with a scene
        """
        self.name = name
        self.tags = tags
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
        self.speed = speed
        self.acceleration = Vector(0, 0)
        self.obey_gravity = obey_gravity # bool
        # terminal velocity must be multipled
        # with delta time in comparision
        self.terminal_velocity = 10.0 # float
        self.enable_terminal_velocity = False

        self.has_collision = has_collision
        self.has_rigidbody = has_rigidbody
        self.custom_hitbox_size = custom_hitbox_size

        self.particle_systems = particle_systems
        self.bullet_spawners = bullet_spawners
        
        # destroy
        self._destroy_val = 0
        self._enable_destroy = False
        self._is_destroyed = False

        # shooting
        self.fire_rate = fire_rate
        self.can_shoot = True
        self.next_fire_ticks = pygame.time.get_ticks()

        self.current_health = max_health
        self.max_health = max_health

    @property
    def sprite(self) -> pygame.Surface:
        cur_anim = self.anim_get(self.current_anim)
        if cur_anim is not None:
            width, height = cur_anim.sprite.get_size()
            scaled_sprite = pygame.transform.scale(
                cur_anim.sprite, (
                    self.scale.x * width, 
                    self.scale.y * height
                )
            )
            return scaled_sprite
        if cur_anim is None:
            return None

    @property
    def rect(self) -> pygame.Rect:
        if self.sprite is not None:
            width, height = self.sprite.get_size()
            rect = pygame.Rect(
                self.position.x, 
                self.position.y, 
                width, height
            )
            return rect
        if self.sprite is None:
            return pygame.Rect(self.position.x, self.position.y, 1, 1)

    @property
    def custom_hitbox(self) -> pygame.Rect:
        return pygame.Rect(
            self.position.x + self.rect.width/2 - self.custom_hitbox_size.x,
            self.position.y + self.rect.height/2 - self.custom_hitbox_size.y,
            self.custom_hitbox_size.x*2,
            self.custom_hitbox_size.y*2
        )

    @property
    def center_position(self) -> Vector:
        return Vector(self.rect.width/2, self.rect.height/2)

    def destroy(self, time: int) -> None:
        """Set the destruction time.

        Parameters:
            time: milliseconds to destruction

        """
        self._enable_destroy = True
        self._destroy_val = time + pygame.time.get_ticks()

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
        speed: float
    ) -> Entity:
        """Shoot an entity.

        Parameters:
            offset: The position offset of where the projectile's initial position.
            projectile: The entity that will be spawned.
            angle: The angle (radian) of the projectile's velocity
            speed: Speed of the projectile.

        """
        if self.can_shoot and pygame.time.get_ticks() >= self.next_fire_ticks:
            self.next_fire_ticks = pygame.time.get_ticks() + self.fire_rate
            projectile = copy(projectile)
            projectile.owner = self
            projectile.velocity = Vector(speed * math.cos(angle), speed * math.sin(angle))
            projectile.position = self.position + offset - Vector(projectile.rect.width/2, projectile.rect.height/2)
            return projectile

    def anim_get(self, animation_name: str) -> Animation:
        if animation_name is not None:
            return self.animations[animation_name]
        if animation_name is None:
            return None

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
            If True, removing the animation was successful

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

    def update(self, delta_time: float) -> None:
        """Updates the position, animation, etc

        Parameters:
            delta_time: the game's delta time

        """
        # Destroy
        if self._enable_destroy and self._destroy_val <= pygame.time.get_ticks():
            self._is_destroyed = True

        # Update Particles
        for ps in self.particle_systems:
            ps.position = self.position
            ps.update(delta_time)

        # Update Animation
        if self.current_anim is not None:
            self.anim_get(self.current_anim).update(delta_time)

        # Apply terminal velocity
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

        # Controller movement
        if self.controller is not None:
            self.velocity = self.controller.movement * self.speed

        # Apply gravity?
        g = gravity
        if not self.obey_gravity:
            g = Vector(0, 0)

        # Apply velocity
        if self.has_rigidbody:
            self.velocity += self.acceleration + g
        
        velocity = self.velocity * delta_time
        self.move(velocity, [])

def load_entity_json(json_path: str) -> Entity:
    data = json.load(open(json_path))
    return_entity = Entity()

    # Position
    if "position" in data.keys():
        data["position"] = Vector(
            data["position"][0],
            data["position"][1]
        )

    # Custom Hitbox Size
    if "custom_hitbox_size" in data.keys():
        data["custom_hitbox_size"] = Vector(
            data["custom_hitbox_size"][0],
            data["custom_hitbox_size"][1]
        )

    # Animations
    if "animations" in data.keys():
        for a in data["animations"][:]:
            anim = load_anim_dict(a)
            return_entity.anim_add(anim)
        return_entity.anim_set(list(return_entity.animations.keys())[0])
        del data["animations"]

    # Particle Systems

    # Bullet Spawners

    for key in data:
        if hasattr(return_entity, key):
            setattr(return_entity, key, data[key])
    
    return return_entity